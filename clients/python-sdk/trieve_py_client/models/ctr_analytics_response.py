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
import json
import pprint
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Any, List, Optional
from trieve_py_client.models.ctr_recommendations_with_clicks_response import CTRRecommendationsWithClicksResponse
from trieve_py_client.models.ctr_recommendations_without_clicks_response import CTRRecommendationsWithoutClicksResponse
from trieve_py_client.models.ctr_search_query_with_clicks_response import CTRSearchQueryWithClicksResponse
from trieve_py_client.models.ctr_search_query_without_clicks_response import CTRSearchQueryWithoutClicksResponse
from trieve_py_client.models.recommendation_ctr_metrics import RecommendationCTRMetrics
from trieve_py_client.models.search_ctr_metrics import SearchCTRMetrics
from pydantic import StrictStr, Field
from typing import Union, List, Optional, Dict
from typing_extensions import Literal, Self

CTRANALYTICSRESPONSE_ONE_OF_SCHEMAS = ["CTRRecommendationsWithClicksResponse", "CTRRecommendationsWithoutClicksResponse", "CTRSearchQueryWithClicksResponse", "CTRSearchQueryWithoutClicksResponse", "RecommendationCTRMetrics", "SearchCTRMetrics"]

class CTRAnalyticsResponse(BaseModel):
    """
    CTRAnalyticsResponse
    """
    # data type: SearchCTRMetrics
    oneof_schema_1_validator: Optional[SearchCTRMetrics] = None
    # data type: CTRSearchQueryWithoutClicksResponse
    oneof_schema_2_validator: Optional[CTRSearchQueryWithoutClicksResponse] = None
    # data type: CTRSearchQueryWithClicksResponse
    oneof_schema_3_validator: Optional[CTRSearchQueryWithClicksResponse] = None
    # data type: RecommendationCTRMetrics
    oneof_schema_4_validator: Optional[RecommendationCTRMetrics] = None
    # data type: CTRRecommendationsWithoutClicksResponse
    oneof_schema_5_validator: Optional[CTRRecommendationsWithoutClicksResponse] = None
    # data type: CTRRecommendationsWithClicksResponse
    oneof_schema_6_validator: Optional[CTRRecommendationsWithClicksResponse] = None
    actual_instance: Optional[Union[CTRRecommendationsWithClicksResponse, CTRRecommendationsWithoutClicksResponse, CTRSearchQueryWithClicksResponse, CTRSearchQueryWithoutClicksResponse, RecommendationCTRMetrics, SearchCTRMetrics]] = None
    one_of_schemas: List[str] = Field(default=Literal["CTRRecommendationsWithClicksResponse", "CTRRecommendationsWithoutClicksResponse", "CTRSearchQueryWithClicksResponse", "CTRSearchQueryWithoutClicksResponse", "RecommendationCTRMetrics", "SearchCTRMetrics"])

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )


    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator('actual_instance')
    def actual_instance_must_validate_oneof(cls, v):
        instance = CTRAnalyticsResponse.model_construct()
        error_messages = []
        match = 0
        # validate data type: SearchCTRMetrics
        if not isinstance(v, SearchCTRMetrics):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SearchCTRMetrics`")
        else:
            match += 1
        # validate data type: CTRSearchQueryWithoutClicksResponse
        if not isinstance(v, CTRSearchQueryWithoutClicksResponse):
            error_messages.append(f"Error! Input type `{type(v)}` is not `CTRSearchQueryWithoutClicksResponse`")
        else:
            match += 1
        # validate data type: CTRSearchQueryWithClicksResponse
        if not isinstance(v, CTRSearchQueryWithClicksResponse):
            error_messages.append(f"Error! Input type `{type(v)}` is not `CTRSearchQueryWithClicksResponse`")
        else:
            match += 1
        # validate data type: RecommendationCTRMetrics
        if not isinstance(v, RecommendationCTRMetrics):
            error_messages.append(f"Error! Input type `{type(v)}` is not `RecommendationCTRMetrics`")
        else:
            match += 1
        # validate data type: CTRRecommendationsWithoutClicksResponse
        if not isinstance(v, CTRRecommendationsWithoutClicksResponse):
            error_messages.append(f"Error! Input type `{type(v)}` is not `CTRRecommendationsWithoutClicksResponse`")
        else:
            match += 1
        # validate data type: CTRRecommendationsWithClicksResponse
        if not isinstance(v, CTRRecommendationsWithClicksResponse):
            error_messages.append(f"Error! Input type `{type(v)}` is not `CTRRecommendationsWithClicksResponse`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in CTRAnalyticsResponse with oneOf schemas: CTRRecommendationsWithClicksResponse, CTRRecommendationsWithoutClicksResponse, CTRSearchQueryWithClicksResponse, CTRSearchQueryWithoutClicksResponse, RecommendationCTRMetrics, SearchCTRMetrics. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in CTRAnalyticsResponse with oneOf schemas: CTRRecommendationsWithClicksResponse, CTRRecommendationsWithoutClicksResponse, CTRSearchQueryWithClicksResponse, CTRSearchQueryWithoutClicksResponse, RecommendationCTRMetrics, SearchCTRMetrics. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Union[str, Dict[str, Any]]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        match = 0

        # deserialize data into SearchCTRMetrics
        try:
            instance.actual_instance = SearchCTRMetrics.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into CTRSearchQueryWithoutClicksResponse
        try:
            instance.actual_instance = CTRSearchQueryWithoutClicksResponse.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into CTRSearchQueryWithClicksResponse
        try:
            instance.actual_instance = CTRSearchQueryWithClicksResponse.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into RecommendationCTRMetrics
        try:
            instance.actual_instance = RecommendationCTRMetrics.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into CTRRecommendationsWithoutClicksResponse
        try:
            instance.actual_instance = CTRRecommendationsWithoutClicksResponse.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into CTRRecommendationsWithClicksResponse
        try:
            instance.actual_instance = CTRRecommendationsWithClicksResponse.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into CTRAnalyticsResponse with oneOf schemas: CTRRecommendationsWithClicksResponse, CTRRecommendationsWithoutClicksResponse, CTRSearchQueryWithClicksResponse, CTRSearchQueryWithoutClicksResponse, RecommendationCTRMetrics, SearchCTRMetrics. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into CTRAnalyticsResponse with oneOf schemas: CTRRecommendationsWithClicksResponse, CTRRecommendationsWithoutClicksResponse, CTRSearchQueryWithClicksResponse, CTRSearchQueryWithoutClicksResponse, RecommendationCTRMetrics, SearchCTRMetrics. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Optional[Union[Dict[str, Any], CTRRecommendationsWithClicksResponse, CTRRecommendationsWithoutClicksResponse, CTRSearchQueryWithClicksResponse, CTRSearchQueryWithoutClicksResponse, RecommendationCTRMetrics, SearchCTRMetrics]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


