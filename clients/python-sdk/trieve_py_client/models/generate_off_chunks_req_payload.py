# coding: utf-8

"""
    Trieve API

    Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API.

    The version of the OpenAPI document: 0.13.0
    Contact: developers@trieve.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from trieve_py_client.models.chat_message_proxy import ChatMessageProxy
from trieve_py_client.models.context_options import ContextOptions
from trieve_py_client.models.image_config import ImageConfig
from typing import Optional, Set
from typing_extensions import Self

class GenerateOffChunksReqPayload(BaseModel):
    """
    GenerateOffChunksReqPayload
    """ # noqa: E501
    audio_input: Optional[StrictStr] = Field(default=None, description="Audio input to be used in the chat. This will be used to generate the audio tokens for the model. The default is None.")
    chunk_ids: List[StrictStr] = Field(description="The ids of the chunks to be retrieved and injected into the context window for RAG.")
    context_options: Optional[ContextOptions] = None
    frequency_penalty: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Frequency penalty is a number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim. Default is 0.7.")
    highlight_results: Optional[StrictBool] = Field(default=None, description="Set highlight_results to false for a slight latency improvement (1-10ms). If not specified, this defaults to true. This will add `<mark><b>` tags to the chunk_html of the chunks to highlight matching splits.")
    image_config: Optional[ImageConfig] = None
    image_urls: Optional[List[StrictStr]] = Field(default=None, description="Image URLs to be used in the chat. These will be used to generate the image tokens for the model. The default is None.")
    max_tokens: Optional[Annotated[int, Field(strict=True, ge=0)]] = Field(default=None, description="The maximum number of tokens to generate in the chat completion. Default is None.")
    presence_penalty: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Presence penalty is a number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics. Default is 0.7.")
    prev_messages: List[ChatMessageProxy] = Field(description="The previous messages to be placed into the chat history. There must be at least one previous message.")
    prompt: Optional[StrictStr] = Field(default=None, description="Prompt will be used to tell the model what to generate in the next message in the chat. The default is 'Respond to the previous instruction and include the doc numbers that you used in square brackets at the end of the sentences that you used the docs for:'. You can also specify an empty string to leave the final message alone such that your user's final message can be used as the prompt. See docs.trieve.ai or contact us for more information.")
    stop_tokens: Optional[List[StrictStr]] = Field(default=None, description="Stop tokens are up to 4 sequences where the API will stop generating further tokens. Default is None.")
    stream_response: Optional[StrictBool] = Field(default=None, description="Whether or not to stream the response. If this is set to true or not included, the response will be a stream. If this is set to false, the response will be a normal JSON response. Default is true.")
    temperature: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. Default is 0.5.")
    user_id: Optional[StrictStr] = Field(default=None, description="User ID is the id of the user who is making the request. This is used to track user interactions with the RAG results.")
    __properties: ClassVar[List[str]] = ["audio_input", "chunk_ids", "context_options", "frequency_penalty", "highlight_results", "image_config", "image_urls", "max_tokens", "presence_penalty", "prev_messages", "prompt", "stop_tokens", "stream_response", "temperature", "user_id"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of GenerateOffChunksReqPayload from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of context_options
        if self.context_options:
            _dict['context_options'] = self.context_options.to_dict()
        # override the default output from pydantic by calling `to_dict()` of image_config
        if self.image_config:
            _dict['image_config'] = self.image_config.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in prev_messages (list)
        _items = []
        if self.prev_messages:
            for _item in self.prev_messages:
                if _item:
                    _items.append(_item.to_dict())
            _dict['prev_messages'] = _items
        # set to None if audio_input (nullable) is None
        # and model_fields_set contains the field
        if self.audio_input is None and "audio_input" in self.model_fields_set:
            _dict['audio_input'] = None

        # set to None if context_options (nullable) is None
        # and model_fields_set contains the field
        if self.context_options is None and "context_options" in self.model_fields_set:
            _dict['context_options'] = None

        # set to None if frequency_penalty (nullable) is None
        # and model_fields_set contains the field
        if self.frequency_penalty is None and "frequency_penalty" in self.model_fields_set:
            _dict['frequency_penalty'] = None

        # set to None if highlight_results (nullable) is None
        # and model_fields_set contains the field
        if self.highlight_results is None and "highlight_results" in self.model_fields_set:
            _dict['highlight_results'] = None

        # set to None if image_config (nullable) is None
        # and model_fields_set contains the field
        if self.image_config is None and "image_config" in self.model_fields_set:
            _dict['image_config'] = None

        # set to None if image_urls (nullable) is None
        # and model_fields_set contains the field
        if self.image_urls is None and "image_urls" in self.model_fields_set:
            _dict['image_urls'] = None

        # set to None if max_tokens (nullable) is None
        # and model_fields_set contains the field
        if self.max_tokens is None and "max_tokens" in self.model_fields_set:
            _dict['max_tokens'] = None

        # set to None if presence_penalty (nullable) is None
        # and model_fields_set contains the field
        if self.presence_penalty is None and "presence_penalty" in self.model_fields_set:
            _dict['presence_penalty'] = None

        # set to None if prompt (nullable) is None
        # and model_fields_set contains the field
        if self.prompt is None and "prompt" in self.model_fields_set:
            _dict['prompt'] = None

        # set to None if stop_tokens (nullable) is None
        # and model_fields_set contains the field
        if self.stop_tokens is None and "stop_tokens" in self.model_fields_set:
            _dict['stop_tokens'] = None

        # set to None if stream_response (nullable) is None
        # and model_fields_set contains the field
        if self.stream_response is None and "stream_response" in self.model_fields_set:
            _dict['stream_response'] = None

        # set to None if temperature (nullable) is None
        # and model_fields_set contains the field
        if self.temperature is None and "temperature" in self.model_fields_set:
            _dict['temperature'] = None

        # set to None if user_id (nullable) is None
        # and model_fields_set contains the field
        if self.user_id is None and "user_id" in self.model_fields_set:
            _dict['user_id'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GenerateOffChunksReqPayload from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "audio_input": obj.get("audio_input"),
            "chunk_ids": obj.get("chunk_ids"),
            "context_options": ContextOptions.from_dict(obj["context_options"]) if obj.get("context_options") is not None else None,
            "frequency_penalty": obj.get("frequency_penalty"),
            "highlight_results": obj.get("highlight_results"),
            "image_config": ImageConfig.from_dict(obj["image_config"]) if obj.get("image_config") is not None else None,
            "image_urls": obj.get("image_urls"),
            "max_tokens": obj.get("max_tokens"),
            "presence_penalty": obj.get("presence_penalty"),
            "prev_messages": [ChatMessageProxy.from_dict(_item) for _item in obj["prev_messages"]] if obj.get("prev_messages") is not None else None,
            "prompt": obj.get("prompt"),
            "stop_tokens": obj.get("stop_tokens"),
            "stream_response": obj.get("stream_response"),
            "temperature": obj.get("temperature"),
            "user_id": obj.get("user_id")
        })
        return _obj


