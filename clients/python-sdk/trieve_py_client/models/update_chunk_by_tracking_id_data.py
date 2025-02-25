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
from typing import Optional, Set
from typing_extensions import Self

class UpdateChunkByTrackingIdData(BaseModel):
    """
    UpdateChunkByTrackingIdData
    """ # noqa: E501
    chunk_html: Optional[StrictStr] = Field(default=None, description="HTML content of the chunk you want to update. This can also be plaintext. The innerText of the HTML will be used to create the embedding vector. The point of using HTML is for convienience, as some users have applications where users submit HTML content. If no chunk_html is provided, the existing chunk_html will be used.")
    convert_html_to_text: Optional[StrictBool] = Field(default=None, description="Convert HTML to raw text before processing to avoid adding noise to the vector embeddings. By default this is true. If you are using HTML content that you want to be included in the vector embeddings, set this to false.")
    group_ids: Optional[List[StrictStr]] = Field(default=None, description="Group ids are the ids of the groups that the chunk should be placed into. This is useful for when you want to update a chunk and add it to a group or multiple groups in one request.")
    group_tracking_ids: Optional[List[StrictStr]] = Field(default=None, description="Group tracking_ids are the tracking_ids of the groups that the chunk should be placed into. This is useful for when you want to update a chunk and add it to a group or multiple groups in one request.")
    link: Optional[StrictStr] = Field(default=None, description="Link of the chunk you want to update. This can also be any string. Frequently, this is a link to the source of the chunk. The link value will not affect the embedding creation. If no link is provided, the existing link will be used.")
    metadata: Optional[Any] = Field(default=None, description="The metadata is a JSON object which can be used to filter chunks. This is useful for when you want to filter chunks by arbitrary metadata. Unlike with tag filtering, there is a performance hit for filtering on metadata. If no metadata is provided, the existing metadata will be used.")
    time_stamp: Optional[StrictStr] = Field(default=None, description="Time_stamp should be an ISO 8601 combined date and time without timezone. It is used for time window filtering and recency-biasing search results. If no time_stamp is provided, the existing time_stamp will be used.")
    tracking_id: StrictStr = Field(description="Tracking_id of the chunk you want to update. This is required to match an existing chunk.")
    weight: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Weight is a float which can be used to bias search results. This is useful for when you want to bias search results for a chunk. The magnitude only matters relative to other chunks in the chunk's dataset dataset. If no weight is provided, the existing weight will be used.")
    __properties: ClassVar[List[str]] = ["chunk_html", "convert_html_to_text", "group_ids", "group_tracking_ids", "link", "metadata", "time_stamp", "tracking_id", "weight"]

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
        """Create an instance of UpdateChunkByTrackingIdData from a JSON string"""
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
        # set to None if chunk_html (nullable) is None
        # and model_fields_set contains the field
        if self.chunk_html is None and "chunk_html" in self.model_fields_set:
            _dict['chunk_html'] = None

        # set to None if convert_html_to_text (nullable) is None
        # and model_fields_set contains the field
        if self.convert_html_to_text is None and "convert_html_to_text" in self.model_fields_set:
            _dict['convert_html_to_text'] = None

        # set to None if group_ids (nullable) is None
        # and model_fields_set contains the field
        if self.group_ids is None and "group_ids" in self.model_fields_set:
            _dict['group_ids'] = None

        # set to None if group_tracking_ids (nullable) is None
        # and model_fields_set contains the field
        if self.group_tracking_ids is None and "group_tracking_ids" in self.model_fields_set:
            _dict['group_tracking_ids'] = None

        # set to None if link (nullable) is None
        # and model_fields_set contains the field
        if self.link is None and "link" in self.model_fields_set:
            _dict['link'] = None

        # set to None if metadata (nullable) is None
        # and model_fields_set contains the field
        if self.metadata is None and "metadata" in self.model_fields_set:
            _dict['metadata'] = None

        # set to None if time_stamp (nullable) is None
        # and model_fields_set contains the field
        if self.time_stamp is None and "time_stamp" in self.model_fields_set:
            _dict['time_stamp'] = None

        # set to None if weight (nullable) is None
        # and model_fields_set contains the field
        if self.weight is None and "weight" in self.model_fields_set:
            _dict['weight'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UpdateChunkByTrackingIdData from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "chunk_html": obj.get("chunk_html"),
            "convert_html_to_text": obj.get("convert_html_to_text"),
            "group_ids": obj.get("group_ids"),
            "group_tracking_ids": obj.get("group_tracking_ids"),
            "link": obj.get("link"),
            "metadata": obj.get("metadata"),
            "time_stamp": obj.get("time_stamp"),
            "tracking_id": obj.get("tracking_id"),
            "weight": obj.get("weight")
        })
        return _obj


