import {
  Show,
  createEffect,
  createSignal,
  For,
  onMount,
  onCleanup,
  Switch,
  Match,
  createMemo,
  useContext,
} from "solid-js";
import {
  type ChunkGroupDTO,
  type ChunkGroupBookmarkDTO,
  ScoreChunkDTO,
  ChunkGroupSearchDTO,
  isScoreChunkDTO,
  isChunkGroupPageDTO,
  ChunkMetadata,
  ChunkBookmarksDTO,
} from "../../utils/apiTypes";
import { FullScreenModal } from "./Atoms/FullScreenModal";
import { FiEdit, FiTrash } from "solid-icons/fi";
import { ConfirmModal } from "./Atoms/ConfirmModal";
import { PaginationController } from "./Atoms/PaginationController";
import { ScoreChunkArray } from "./ScoreChunkArray";
import SearchForm from "./SearchForm";
import ChunkMetadataDisplay from "./ChunkMetadataDisplay";
import { Portal } from "solid-js/web";
import ChatPopup from "./ChatPopup";
import { AiOutlineRobot } from "solid-icons/ai";
import { IoDocumentOutline, IoDocumentsOutline } from "solid-icons/io";
import { useLocation, useNavigate } from "@solidjs/router";
import { DatasetAndUserContext } from "./Contexts/DatasetAndUserContext";

export interface GroupPageProps {
  groupID: string;
}

export const GroupPage = (props: GroupPageProps) => {
  const apiHost: string = import.meta.env.VITE_API_HOST as string;
  const datasetAndUserContext = useContext(DatasetAndUserContext);

  const $dataset = datasetAndUserContext.currentDataset;
  const location = useLocation();
  const navigate = useNavigate();

  const searchChunkMetadatasWithVotes: ScoreChunkDTO[] = [];

  const [query, setQuery] = createSignal<string>("");
  const [page, setPage] = createSignal<number>(1);
  const [searchType, setSearchType] = createSignal<string>("hybrid");
  const [slimChunks, setSlimChunks] = createSignal(false);
  const [getTotalPages, setGetTotalPages] = createSignal(false);
  const [highlightResults, setHighlightResults] = createSignal(true);
  const [highlightDelimiters, setHighlightDelimiters] = createSignal<string[]>([
    "?",
    ",",
    ".",
    "!",
  ]);
  const [searchLoading, setSearchLoading] = createSignal(false);
  const [chunkMetadatas, setChunkMetadatas] = createSignal<ChunkMetadata[]>([]);
  const [searchMetadatasWithVotes, setSearchMetadatasWithVotes] = createSignal<
    ScoreChunkDTO[]
  >(searchChunkMetadatasWithVotes);
  const [clientSideRequestFinished, setClientSideRequestFinished] =
    createSignal(false);
  const [groupInfo, setGroupInfo] = createSignal<ChunkGroupDTO | null>(null);
  const [chunkGroups, setChunkGroups] = createSignal<ChunkGroupDTO[]>([]);
  const [bookmarks, setBookmarks] = createSignal<ChunkBookmarksDTO[]>([]);
  const [error, setError] = createSignal("");
  const [fetchingGroups, setFetchingGroups] = createSignal(false);
  const [deleting, setDeleting] = createSignal(false);
  const [editing, setEditing] = createSignal(false);
  const $currentUser = datasetAndUserContext.user;
  const [totalPages, setTotalPages] = createSignal(0);
  const [loadingRecommendations, setLoadingRecommendations] =
    createSignal(false);
  const [recommendedChunks, setRecommendedChunks] = createSignal<
    ChunkMetadata[]
  >([]);
  const [showConfirmDeleteModal, setShowConfirmDeleteModal] =
    createSignal(false);
  const [showConfirmGroupDeleteModal, setShowConfirmGroupmDeleteModal] =
    createSignal(false);
  const [totalGroupPages, setTotalGroupPages] = createSignal(1);
  // eslint-disable-next-line @typescript-eslint/no-empty-function
  const [onDelete, setOnDelete] = createSignal(() => {});
  // eslint-disable-next-line @typescript-eslint/no-empty-function
  const [onGroupDelete, setOnGroupDelete] = createSignal(() => {});
  const [openChat, setOpenChat] = createSignal(false);
  const [selectedIds, setSelectedIds] = createSignal<string[]>([]);

  onMount(() => {
    fetchBookmarks();
  });

  createEffect(() => {
    const resultsLength = chunkMetadatas().length;
    if (!openChat()) {
      setSelectedIds((prev) => (prev.length < resultsLength ? prev : []));
    }
  });

  createEffect(() => {
    setQuery(location.query.q ?? "");
    setPage(Number(location.query.page) || 1);
    setSearchType(location.query.searchType ?? "hybrid");
    setSlimChunks(location.query.slimChunks === "true");
    setGetTotalPages(location.query.getTotalPages === "true");
    setHighlightResults(location.query.highlightResults === "true");
    setHighlightDelimiters(
      location.query.highlightDelimiters?.split(",") ?? ["?", ".", "!"],
    );
  });

  createEffect(() => {
    const abortController = new AbortController();
    let group_id: string | null = null;
    const currentDataset = $dataset?.();
    if (!currentDataset) return;

    if (query() === "") {
      void fetch(`${apiHost}/chunk_group/${props.groupID}/${page()}`, {
        method: "GET",
        credentials: "include",
        signal: abortController.signal,
        headers: {
          "TR-Dataset": currentDataset.dataset.id,
        },
      }).then((response) => {
        if (response.ok) {
          void response.json().then((data) => {
            const groupBookmarks = data as ChunkGroupBookmarkDTO;
            group_id = groupBookmarks.group.id;
            setGroupInfo(groupBookmarks.group);
            setTotalPages(groupBookmarks.total_pages);
            setChunkMetadatas(groupBookmarks.chunks);
            setError("");
          });
        }
        if (response.status == 403) {
          setError("You are not authorized to view this group");
        }
        if (response.status == 404) {
          setError("Group not found, it never existed or was deleted");
        }
        setClientSideRequestFinished(true);
      });
    } else {
      setSearchLoading(true);

      void fetch(`${apiHost}/chunk_group/search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "TR-Dataset": currentDataset.dataset.id,
        },
        signal: abortController.signal,
        credentials: "include",
        body: JSON.stringify({
          query: query(),
          page: page(),
          group_id: props.groupID,
          search_type: searchType(),
          slim_chunks: slimChunks(),
          get_total_pages: getTotalPages(),
          highlight_results: highlightResults(),
          highlight_delimiters: highlightDelimiters(),
        }),
      }).then((response) => {
        if (response.ok) {
          void response.json().then((data) => {
            const groupBookmarks = data as ChunkGroupSearchDTO;
            group_id = groupBookmarks.group.id;
            setGroupInfo(groupBookmarks.group);
            setTotalPages(groupBookmarks.total_pages);
            setSearchMetadatasWithVotes(groupBookmarks.bookmarks);
            setError("");
          });
        }
        if (response.status == 403) {
          setError("You are not authorized to view this group");
        }
        setClientSideRequestFinished(true);
        setSearchLoading(false);
      });

      onCleanup(() => {
        abortController.abort();
      });
    }

    fetchChunkGroups();

    setOnGroupDelete(() => {
      return () => {
        setDeleting(true);
        if (group_id === null) return;

        void fetch(`${apiHost}/chunk_group/${group_id}`, {
          method: "DELETE",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            "TR-Dataset": currentDataset.dataset.id,
          },
          signal: abortController.signal,
        }).then((response) => {
          setDeleting(false);
          if (response.ok) {
            navigate(`/`);
          }
          if (response.status == 403) {
            setDeleting(false);
          }
        });
      };
    });
  });

  createEffect(() => {
    resizeTextarea(
      document.getElementById(
        "group-query-textarea",
      ) as HTMLTextAreaElement | null,
    );
  });

  // Fetch the chunk groups for the auth'ed user
  const fetchChunkGroups = () => {
    const currentDataset = $dataset?.();
    if (!currentDataset) return;
    if (!$currentUser?.()) return;

    void fetch(`${apiHost}/dataset/groups/${currentDataset.dataset.id}/1`, {
      method: "GET",
      credentials: "include",
      headers: {
        "TR-Dataset": currentDataset.dataset.id,
      },
    }).then((response) => {
      if (response.ok) {
        void response.json().then((data) => {
          if (isChunkGroupPageDTO(data)) {
            setChunkGroups(data.groups);
            setTotalGroupPages(data.total_pages);
          }
        });
      }
    });
  };

  const fetchBookmarks = () => {
    const currentDataset = $dataset?.();
    if (!currentDataset) return;

    void fetch(`${apiHost}/chunk_group/chunks`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "TR-Dataset": currentDataset.dataset.id,
      },
      body: JSON.stringify({
        chunk_ids: chunkMetadatas().flatMap((m) => {
          return m.id;
        }),
      }),
    }).then((response) => {
      if (response.ok) {
        void response.json().then((data: ChunkBookmarksDTO[]) => {
          setBookmarks(data);
        });
      }
    });
  };

  const updateGroup = () => {
    const currentDataset = $dataset?.();
    if (!currentDataset) return;

    setFetchingGroups(true);
    const body = {
      group_id: groupInfo()?.id,
      name: groupInfo()?.name,
      description: groupInfo()?.description,
    };
    void fetch(`${apiHost}/chunk_group`, {
      method: "PUT",
      credentials: "include",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
        "TR-Dataset": currentDataset.dataset.id,
      },
    }).then((response) => {
      setFetchingGroups(false);
      if (response.ok) {
        setEditing(false);
      }
    });
  };

  const fetchRecommendations = (
    ids: string[],
    prev_recommendations: ChunkMetadata[],
  ) => {
    const currentDataset = $dataset?.();
    if (!currentDataset) return;

    setLoadingRecommendations(true);
    void fetch(`${apiHost}/chunk/recommend`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "TR-Dataset": currentDataset.dataset.id,
      },
      body: JSON.stringify({
        positive_chunk_ids: ids,
        limit: prev_recommendations.length + 10,
      }),
    }).then((response) => {
      if (response.ok) {
        void response.json().then((data) => {
          const typed_data = data as ChunkMetadata[];
          const deduped_data = typed_data.filter((d) => {
            return !prev_recommendations.some((c) => c.id == d.id);
          });
          const new_recommendations = [
            ...prev_recommendations,
            ...deduped_data,
          ];
          setRecommendedChunks(new_recommendations);
        });
      } else {
        const newEvent = new CustomEvent("show-toast", {
          detail: {
            type: "error",
            message: "Failed to fetch recommendations",
          },
        });
        window.dispatchEvent(newEvent);
      }

      setLoadingRecommendations(false);
    });
  };

  const resizeTextarea = (textarea: HTMLTextAreaElement | null) => {
    if (!textarea) return;

    textarea.style.height = `${textarea.scrollHeight}px`;
  };

  const chatPopupChunks = createMemo(() => {
    const curSearchMetadatasWithVotes = searchMetadatasWithVotes();
    if (curSearchMetadatasWithVotes.length > 0) {
      return curSearchMetadatasWithVotes;
    }
    const curMetadatasWithVotes = chunkMetadatas();
    return curMetadatasWithVotes.map((m) => {
      return {
        metadata: [m],
        author: null,
        score: 0,
      } as unknown as ScoreChunkDTO;
    });
  });

  return (
    <>
      <Show when={openChat()}>
        <Portal>
          <FullScreenModal isOpen={openChat} setIsOpen={setOpenChat}>
            <div class="max-h-[75vh] min-h-[75vh] min-w-[75vw] max-w-[75vw] overflow-y-auto rounded-md scrollbar-thin">
              <ChatPopup
                chunks={chatPopupChunks}
                selectedIds={selectedIds}
                setOpenChat={setOpenChat}
              />
            </div>
          </FullScreenModal>
        </Portal>
      </Show>
      <div class="flex w-full flex-col items-center space-y-2">
        <Show when={error().length == 0}>
          <div class="flex w-full max-w-7xl items-center justify-end space-x-2 px-4 sm:px-8 md:px-20">
            <Show
              when={chunkGroups().some((group) => group.id == groupInfo()?.id)}
            >
              <button
                classList={{
                  "h-fit text-red-700 dark:text-red-400": true,
                  "animate-pulse": deleting(),
                }}
                onClick={() => setShowConfirmGroupmDeleteModal(true)}
              >
                <FiTrash class="h-5 w-5" />
              </button>
              <button onClick={() => setEditing((prev) => !prev)}>
                <FiEdit class="h-5 w-5" />
              </button>
            </Show>
          </div>
          <Show when={!editing()}>
            <div class="flex w-full items-center justify-center">
              <h1 class="max-w-7xl break-all text-center text-lg min-[320px]:text-xl sm:text-3xl">
                {groupInfo()?.name}
              </h1>
            </div>
            <Show
              when={groupInfo()?.description.length ?? (0 > 0 && !editing())}
            >
              <div class="mx-auto flex max-w-7xl justify-items-center gap-x-2 text-center">
                {groupInfo()?.description}
              </div>
            </Show>
          </Show>

          <Show when={editing()}>
            <div class="vertical-align-left mt-8 grid w-full max-w-7xl auto-rows-max grid-cols-[1fr,3fr] gap-y-2 px-4 sm:px-8 md:px-20">
              <h1 class="text-md min-[320px]:text-md sm:text-md mt-10 text-left font-bold">
                Name:
              </h1>
              <input
                type="text"
                class="mt-10 max-h-fit w-full rounded-md bg-neutral-200 px-2 py-1 dark:bg-neutral-700"
                value={groupInfo()?.name}
                onInput={(e) => {
                  const curGroupInfo = groupInfo();
                  if (curGroupInfo) {
                    setGroupInfo({
                      ...curGroupInfo,
                      name: e.target.value,
                    });
                  }
                }}
              />
              <textarea
                class="max-md w-full justify-start rounded-md bg-neutral-200 px-2 py-1 dark:bg-neutral-700"
                value={groupInfo()?.description}
                onInput={(e) => {
                  const curGroupInfo = groupInfo();
                  if (curGroupInfo) {
                    setGroupInfo({
                      ...curGroupInfo,
                      description: e.target.value,
                    });
                  }
                }}
              />
            </div>
            <div class="mt-4 flex w-full max-w-7xl justify-end px-4 sm:px-8 md:px-20">
              <button
                classList={{
                  "!pointer-events-auto relative max-h-10 mt-2 mr-2 items-end justify-end rounded-md p-2 text-center bg-red-500":
                    true,
                  "animate-pulse": fetchingGroups(),
                }}
                onClick={() => setEditing(false)}
              >
                Cancel
              </button>
              <button
                classList={{
                  "!pointer-events-auto relative max-h-10 mt-2 mr-2 items-end justify-end rounded-md p-2 text-center bg-green-500":
                    true,
                  "animate-pulse": fetchingGroups(),
                }}
                onClick={() => updateGroup()}
              >
                Save
              </button>
            </div>
          </Show>
        </Show>
        <div class="flex w-full max-w-7xl flex-col space-y-4 border-t border-neutral-500 px-4 sm:px-8 md:px-20">
          <Show when={query() != ""}>
            <button
              class="relative mx-auto ml-8 mt-8 h-fit max-h-[240px] rounded-md bg-neutral-100 p-2 dark:bg-neutral-700"
              onClick={() => navigate(`/group/${props.groupID}`)}
            >
              ← Back
            </button>
          </Show>
          <Show when={chunkMetadatas().length > 0}>
            <div class="mx-auto w-full max-w-7xl">
              <div
                classList={{
                  "mx-auto w-full max-w-[calc(100%-32px)] min-[360px]:max-w-[calc(100%-64px)]":
                    true,
                  "mt-8": query() == "",
                }}
              >
                <Show when={query()}>
                  <SearchForm
                    query={query()}
                    searchType={searchType()}
                    getTotalPages={getTotalPages()}
                    groupID={props.groupID}
                    slimChunks={slimChunks()}
                  />
                </Show>
              </div>
            </div>
          </Show>
          <Show when={query() != ""}>
            <div class="flex w-full flex-col items-center rounded-md px-8 py-2">
              <div class="text-xl font-semibold">
                Search results for "{query()}"
              </div>
            </div>
          </Show>
          <Switch>
            <Match when={searchLoading()}>
              <div class="flex w-full justify-center">
                <div
                  class="text-primary inline-block h-12 w-12 animate-spin rounded-full border-4 border-solid border-current border-magenta border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
                  role="status"
                >
                  <span class="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">
                    Loading...
                  </span>
                </div>
              </div>
            </Match>
            <Match when={!searchLoading()}>
              <For
                each={
                  query() == "" ? chunkMetadatas() : searchMetadatasWithVotes()
                }
              >
                {(chunk) => (
                  <div class="mt-4">
                    <ScoreChunkArray
                      totalGroupPages={totalGroupPages()}
                      chunks={
                        !isScoreChunkDTO(chunk) ? [chunk] : chunk.metadata
                      }
                      score={isScoreChunkDTO(chunk) ? chunk.score : 0}
                      group={true}
                      chunkGroups={chunkGroups()}
                      bookmarks={bookmarks()}
                      setOnDelete={setOnDelete}
                      setShowConfirmModal={setShowConfirmDeleteModal}
                      showExpand={clientSideRequestFinished()}
                      defaultShowMetadata={slimChunks()}
                      setChunkGroups={setChunkGroups}
                      setSelectedIds={setSelectedIds}
                      selectedIds={selectedIds}
                    />
                  </div>
                )}
              </For>
            </Match>
          </Switch>
          <div class="mx-auto my-12 flex items-center justify-center space-x-2">
            <PaginationController page={page()} totalPages={totalPages()} />
          </div>
          <Show when={recommendedChunks().length > 0}>
            <div class="mx-auto mt-8 w-full max-w-[calc(100%-32px)] min-[360px]:max-w-[calc(100%-64px)]">
              <div class="flex w-full flex-col items-center rounded-md p-2">
                <div class="text-xl font-semibold">Related Chunks</div>
              </div>
              <For each={recommendedChunks()}>
                {(chunk) => (
                  <>
                    <div class="mt-4">
                      <ChunkMetadataDisplay
                        totalGroupPages={totalGroupPages()}
                        chunk={chunk}
                        chunkGroups={chunkGroups()}
                        bookmarks={[]}
                        setShowConfirmModal={setShowConfirmDeleteModal}
                        fetchChunkGroups={fetchChunkGroups}
                        setChunkGroups={setChunkGroups}
                        setOnDelete={setOnDelete}
                        showExpand={true}
                      />
                    </div>
                  </>
                )}
              </For>
            </div>
          </Show>
          <Show when={chunkMetadatas().length > 0}>
            <div class="mx-auto mt-8 w-full max-w-[calc(100%-32px)] min-[360px]:max-w-[calc(100%-64px)]">
              <button
                classList={{
                  "w-full rounded  bg-neutral-100 p-2 text-center hover:bg-neutral-100 dark:bg-neutral-700 dark:hover:bg-neutral-800":
                    true,
                  "animate-pulse": loadingRecommendations(),
                }}
                onClick={() =>
                  fetchRecommendations(
                    chunkMetadatas().map((m) => m.id),
                    recommendedChunks(),
                  )
                }
              >
                {recommendedChunks().length == 0 ? "Get" : "Get More"} Related
                Chunks
              </button>
            </div>
          </Show>
          <Show when={error().length > 0}>
            <div class="flex w-full flex-col items-center rounded-md p-2">
              <div class="text-xl font-semibold text-red-500">{error()}</div>
            </div>
          </Show>
          <Show
            when={
              chunkMetadatas().length == 0 &&
              searchMetadatasWithVotes().length == 0 &&
              clientSideRequestFinished()
            }
          >
            <div class="flex w-full flex-col items-center rounded-md p-2">
              <div class="text-xl font-semibold">
                This group is currently empty
              </div>
            </div>
          </Show>
        </div>
      </div>
      <div>
        <div
          data-dial-init
          class="group fixed bottom-6 right-6"
          onMouseEnter={() => {
            document
              .getElementById("speed-dial-menu-text-outside-button")
              ?.classList.remove("hidden");
            document
              .getElementById("speed-dial-menu-text-outside-button")
              ?.classList.add("flex");
          }}
          onMouseLeave={() => {
            document
              .getElementById("speed-dial-menu-text-outside-button")
              ?.classList.add("hidden");
            document
              .getElementById("speed-dial-menu-text-outside-button")
              ?.classList.remove("flex");
          }}
        >
          <div
            id="speed-dial-menu-text-outside-button"
            class="mb-4 hidden flex-col items-center space-y-2"
          >
            <button
              type="button"
              class="relative h-[52px] w-[52px] items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-500 shadow-sm hover:bg-gray-50 hover:text-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-400 dark:hover:bg-gray-600 dark:hover:text-white dark:focus:ring-gray-400"
              onClick={() => {
                const searchResults = searchMetadatasWithVotes();
                if (searchResults.length > 0) {
                  setSelectedIds(
                    searchResults
                      .flatMap((c) => {
                        return c.metadata[0].id;
                      })
                      .slice(0, 10),
                  );
                  setOpenChat(true);
                } else {
                  setSelectedIds(
                    chunkMetadatas()
                      .flatMap((c) => {
                        return c.id ?? "";
                      })
                      .slice(0, 10),
                  );
                }
                setOpenChat(true);
              }}
            >
              <IoDocumentsOutline class="mx-auto h-7 w-7" />
              <span class="font-sm absolute -left-[8.5rem] top-1/2 mb-px block -translate-y-1/2 break-words bg-white/30 text-sm backdrop-blur-xl dark:bg-black/30">
                Chat with all results
              </span>
            </button>
            <button
              type="button"
              class="relative h-[52px] w-[52px] items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-500 shadow-sm hover:bg-gray-50 hover:text-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-400 dark:hover:bg-gray-600 dark:hover:text-white dark:focus:ring-gray-400"
              onClick={() => {
                setOpenChat(true);
              }}
            >
              <IoDocumentOutline class="mx-auto h-7 w-7" />
              <span class="font-sm absolute -left-[10.85rem] top-1/2 mb-px block -translate-y-1/2 bg-white/30 text-sm backdrop-blur-xl dark:bg-black/30">
                Chat with selected results
              </span>
            </button>
          </div>
          <button
            type="button"
            class="flex h-14 w-14 items-center justify-center rounded-lg bg-magenta-500 text-white hover:bg-magenta-400 focus:outline-none focus:ring-4 focus:ring-magenta-300 dark:bg-magenta-500 dark:hover:bg-magenta-400 dark:focus:ring-magenta-600"
          >
            <AiOutlineRobot class="h-7 w-7" />
            <span class="sr-only">Open actions menu</span>
          </button>
        </div>
      </div>
      <ConfirmModal
        showConfirmModal={showConfirmDeleteModal}
        setShowConfirmModal={setShowConfirmDeleteModal}
        onConfirm={onDelete}
        message="Are you sure you want to delete this chunk?"
      />
      <ConfirmModal
        showConfirmModal={showConfirmGroupDeleteModal}
        setShowConfirmModal={setShowConfirmGroupmDeleteModal}
        onConfirm={onGroupDelete}
        message="Are you sure you want to delete this group?"
      />
    </>
  );
};
