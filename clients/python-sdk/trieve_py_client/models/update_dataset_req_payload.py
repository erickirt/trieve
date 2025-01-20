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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from trieve_py_client.models.crawl_options import CrawlOptions
from trieve_py_client.models.dataset_configuration_dto import DatasetConfigurationDTO
from typing import Optional, Set
from typing_extensions import Self

class UpdateDatasetReqPayload(BaseModel):
    """
    UpdateDatasetReqPayload
    """ # noqa: E501
    crawl_options: Optional[CrawlOptions] = None
    dataset_id: Optional[StrictStr] = Field(default=None, description="The id of the dataset you want to update.")
    dataset_name: Optional[StrictStr] = Field(default=None, description="The new name of the dataset. Must be unique within the organization. If not provided, the name will not be updated.")
    new_tracking_id: Optional[StrictStr] = Field(default=None, description="Optional new tracking ID for the dataset. Can be used to track the dataset in external systems. Must be unique within the organization. If not provided, the tracking ID will not be updated. Strongly recommended to not use a valid uuid value as that will not work with the TR-Dataset header.")
    server_configuration: Optional[DatasetConfigurationDTO] = None
    tracking_id: Optional[StrictStr] = Field(default=None, description="The tracking ID of the dataset you want to update.")
    __properties: ClassVar[List[str]] = ["crawl_options", "dataset_id", "dataset_name", "new_tracking_id", "server_configuration", "tracking_id"]

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
        """Create an instance of UpdateDatasetReqPayload from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of crawl_options
        if self.crawl_options:
            _dict['crawl_options'] = self.crawl_options.to_dict()
        # override the default output from pydantic by calling `to_dict()` of server_configuration
        if self.server_configuration:
            _dict['server_configuration'] = self.server_configuration.to_dict()
        # set to None if crawl_options (nullable) is None
        # and model_fields_set contains the field
        if self.crawl_options is None and "crawl_options" in self.model_fields_set:
            _dict['crawl_options'] = None

        # set to None if dataset_id (nullable) is None
        # and model_fields_set contains the field
        if self.dataset_id is None and "dataset_id" in self.model_fields_set:
            _dict['dataset_id'] = None

        # set to None if dataset_name (nullable) is None
        # and model_fields_set contains the field
        if self.dataset_name is None and "dataset_name" in self.model_fields_set:
            _dict['dataset_name'] = None

        # set to None if new_tracking_id (nullable) is None
        # and model_fields_set contains the field
        if self.new_tracking_id is None and "new_tracking_id" in self.model_fields_set:
            _dict['new_tracking_id'] = None

        # set to None if server_configuration (nullable) is None
        # and model_fields_set contains the field
        if self.server_configuration is None and "server_configuration" in self.model_fields_set:
            _dict['server_configuration'] = None

        # set to None if tracking_id (nullable) is None
        # and model_fields_set contains the field
        if self.tracking_id is None and "tracking_id" in self.model_fields_set:
            _dict['tracking_id'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UpdateDatasetReqPayload from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "crawl_options": CrawlOptions.from_dict(obj["crawl_options"]) if obj.get("crawl_options") is not None else None,
            "dataset_id": obj.get("dataset_id"),
            "dataset_name": obj.get("dataset_name"),
            "new_tracking_id": obj.get("new_tracking_id"),
            "server_configuration": DatasetConfigurationDTO.from_dict(obj["server_configuration"]) if obj.get("server_configuration") is not None else None,
            "tracking_id": obj.get("tracking_id")
        })
        return _obj


