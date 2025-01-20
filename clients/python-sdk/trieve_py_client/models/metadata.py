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
from typing_extensions import Annotated
from trieve_py_client.models.sitemap import Sitemap
from typing import Optional, Set
from typing_extensions import Self

class Metadata(BaseModel):
    """
    Metadata
    """ # noqa: E501
    article_section: Optional[StrictStr] = Field(default=None, alias="articleSection")
    article_tag: Optional[StrictStr] = Field(default=None, alias="articleTag")
    dc_date: Optional[StrictStr] = Field(default=None, alias="dcDate")
    dc_date_created: Optional[StrictStr] = Field(default=None, alias="dcDateCreated")
    dc_description: Optional[StrictStr] = Field(default=None, alias="dcDescription")
    dc_subject: Optional[StrictStr] = Field(default=None, alias="dcSubject")
    dc_terms_audience: Optional[StrictStr] = Field(default=None, alias="dcTermsAudience")
    dc_terms_created: Optional[StrictStr] = Field(default=None, alias="dcTermsCreated")
    dc_terms_keywords: Optional[StrictStr] = Field(default=None, alias="dcTermsKeywords")
    dc_terms_subject: Optional[StrictStr] = Field(default=None, alias="dcTermsSubject")
    dc_terms_type: Optional[StrictStr] = Field(default=None, alias="dcTermsType")
    dc_type: Optional[StrictStr] = Field(default=None, alias="dcType")
    description: Optional[StrictStr] = None
    error: Optional[StrictStr] = None
    keywords: Optional[StrictStr] = None
    language: Optional[StrictStr] = None
    modified_time: Optional[StrictStr] = Field(default=None, alias="modifiedTime")
    og_audio: Optional[StrictStr] = Field(default=None, alias="ogAudio")
    og_description: Optional[StrictStr] = Field(default=None, alias="ogDescription")
    og_determiner: Optional[StrictStr] = Field(default=None, alias="ogDeterminer")
    og_image: Optional[StrictStr] = Field(default=None, alias="ogImage")
    og_locale: Optional[StrictStr] = Field(default=None, alias="ogLocale")
    og_locale_alternate: Optional[List[StrictStr]] = Field(default=None, alias="ogLocaleAlternate")
    og_site_name: Optional[StrictStr] = Field(default=None, alias="ogSiteName")
    og_title: Optional[StrictStr] = Field(default=None, alias="ogTitle")
    og_url: Optional[StrictStr] = Field(default=None, alias="ogUrl")
    og_video: Optional[StrictStr] = Field(default=None, alias="ogVideo")
    published_time: Optional[StrictStr] = Field(default=None, alias="publishedTime")
    robots: Optional[StrictStr] = None
    site_map: Optional[Sitemap] = None
    source_url: Optional[StrictStr] = Field(default=None, alias="sourceURL")
    status_code: Optional[Annotated[int, Field(strict=True, ge=0)]] = Field(default=None, alias="statusCode")
    title: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["articleSection", "articleTag", "dcDate", "dcDateCreated", "dcDescription", "dcSubject", "dcTermsAudience", "dcTermsCreated", "dcTermsKeywords", "dcTermsSubject", "dcTermsType", "dcType", "description", "error", "keywords", "language", "modifiedTime", "ogAudio", "ogDescription", "ogDeterminer", "ogImage", "ogLocale", "ogLocaleAlternate", "ogSiteName", "ogTitle", "ogUrl", "ogVideo", "publishedTime", "robots", "site_map", "sourceURL", "statusCode", "title"]

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
        """Create an instance of Metadata from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of site_map
        if self.site_map:
            _dict['site_map'] = self.site_map.to_dict()
        # set to None if article_section (nullable) is None
        # and model_fields_set contains the field
        if self.article_section is None and "article_section" in self.model_fields_set:
            _dict['articleSection'] = None

        # set to None if article_tag (nullable) is None
        # and model_fields_set contains the field
        if self.article_tag is None and "article_tag" in self.model_fields_set:
            _dict['articleTag'] = None

        # set to None if dc_date (nullable) is None
        # and model_fields_set contains the field
        if self.dc_date is None and "dc_date" in self.model_fields_set:
            _dict['dcDate'] = None

        # set to None if dc_date_created (nullable) is None
        # and model_fields_set contains the field
        if self.dc_date_created is None and "dc_date_created" in self.model_fields_set:
            _dict['dcDateCreated'] = None

        # set to None if dc_description (nullable) is None
        # and model_fields_set contains the field
        if self.dc_description is None and "dc_description" in self.model_fields_set:
            _dict['dcDescription'] = None

        # set to None if dc_subject (nullable) is None
        # and model_fields_set contains the field
        if self.dc_subject is None and "dc_subject" in self.model_fields_set:
            _dict['dcSubject'] = None

        # set to None if dc_terms_audience (nullable) is None
        # and model_fields_set contains the field
        if self.dc_terms_audience is None and "dc_terms_audience" in self.model_fields_set:
            _dict['dcTermsAudience'] = None

        # set to None if dc_terms_created (nullable) is None
        # and model_fields_set contains the field
        if self.dc_terms_created is None and "dc_terms_created" in self.model_fields_set:
            _dict['dcTermsCreated'] = None

        # set to None if dc_terms_keywords (nullable) is None
        # and model_fields_set contains the field
        if self.dc_terms_keywords is None and "dc_terms_keywords" in self.model_fields_set:
            _dict['dcTermsKeywords'] = None

        # set to None if dc_terms_subject (nullable) is None
        # and model_fields_set contains the field
        if self.dc_terms_subject is None and "dc_terms_subject" in self.model_fields_set:
            _dict['dcTermsSubject'] = None

        # set to None if dc_terms_type (nullable) is None
        # and model_fields_set contains the field
        if self.dc_terms_type is None and "dc_terms_type" in self.model_fields_set:
            _dict['dcTermsType'] = None

        # set to None if dc_type (nullable) is None
        # and model_fields_set contains the field
        if self.dc_type is None and "dc_type" in self.model_fields_set:
            _dict['dcType'] = None

        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        # set to None if error (nullable) is None
        # and model_fields_set contains the field
        if self.error is None and "error" in self.model_fields_set:
            _dict['error'] = None

        # set to None if keywords (nullable) is None
        # and model_fields_set contains the field
        if self.keywords is None and "keywords" in self.model_fields_set:
            _dict['keywords'] = None

        # set to None if language (nullable) is None
        # and model_fields_set contains the field
        if self.language is None and "language" in self.model_fields_set:
            _dict['language'] = None

        # set to None if modified_time (nullable) is None
        # and model_fields_set contains the field
        if self.modified_time is None and "modified_time" in self.model_fields_set:
            _dict['modifiedTime'] = None

        # set to None if og_audio (nullable) is None
        # and model_fields_set contains the field
        if self.og_audio is None and "og_audio" in self.model_fields_set:
            _dict['ogAudio'] = None

        # set to None if og_description (nullable) is None
        # and model_fields_set contains the field
        if self.og_description is None and "og_description" in self.model_fields_set:
            _dict['ogDescription'] = None

        # set to None if og_determiner (nullable) is None
        # and model_fields_set contains the field
        if self.og_determiner is None and "og_determiner" in self.model_fields_set:
            _dict['ogDeterminer'] = None

        # set to None if og_image (nullable) is None
        # and model_fields_set contains the field
        if self.og_image is None and "og_image" in self.model_fields_set:
            _dict['ogImage'] = None

        # set to None if og_locale (nullable) is None
        # and model_fields_set contains the field
        if self.og_locale is None and "og_locale" in self.model_fields_set:
            _dict['ogLocale'] = None

        # set to None if og_locale_alternate (nullable) is None
        # and model_fields_set contains the field
        if self.og_locale_alternate is None and "og_locale_alternate" in self.model_fields_set:
            _dict['ogLocaleAlternate'] = None

        # set to None if og_site_name (nullable) is None
        # and model_fields_set contains the field
        if self.og_site_name is None and "og_site_name" in self.model_fields_set:
            _dict['ogSiteName'] = None

        # set to None if og_title (nullable) is None
        # and model_fields_set contains the field
        if self.og_title is None and "og_title" in self.model_fields_set:
            _dict['ogTitle'] = None

        # set to None if og_url (nullable) is None
        # and model_fields_set contains the field
        if self.og_url is None and "og_url" in self.model_fields_set:
            _dict['ogUrl'] = None

        # set to None if og_video (nullable) is None
        # and model_fields_set contains the field
        if self.og_video is None and "og_video" in self.model_fields_set:
            _dict['ogVideo'] = None

        # set to None if published_time (nullable) is None
        # and model_fields_set contains the field
        if self.published_time is None and "published_time" in self.model_fields_set:
            _dict['publishedTime'] = None

        # set to None if robots (nullable) is None
        # and model_fields_set contains the field
        if self.robots is None and "robots" in self.model_fields_set:
            _dict['robots'] = None

        # set to None if site_map (nullable) is None
        # and model_fields_set contains the field
        if self.site_map is None and "site_map" in self.model_fields_set:
            _dict['site_map'] = None

        # set to None if source_url (nullable) is None
        # and model_fields_set contains the field
        if self.source_url is None and "source_url" in self.model_fields_set:
            _dict['sourceURL'] = None

        # set to None if status_code (nullable) is None
        # and model_fields_set contains the field
        if self.status_code is None and "status_code" in self.model_fields_set:
            _dict['statusCode'] = None

        # set to None if title (nullable) is None
        # and model_fields_set contains the field
        if self.title is None and "title" in self.model_fields_set:
            _dict['title'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Metadata from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "articleSection": obj.get("articleSection"),
            "articleTag": obj.get("articleTag"),
            "dcDate": obj.get("dcDate"),
            "dcDateCreated": obj.get("dcDateCreated"),
            "dcDescription": obj.get("dcDescription"),
            "dcSubject": obj.get("dcSubject"),
            "dcTermsAudience": obj.get("dcTermsAudience"),
            "dcTermsCreated": obj.get("dcTermsCreated"),
            "dcTermsKeywords": obj.get("dcTermsKeywords"),
            "dcTermsSubject": obj.get("dcTermsSubject"),
            "dcTermsType": obj.get("dcTermsType"),
            "dcType": obj.get("dcType"),
            "description": obj.get("description"),
            "error": obj.get("error"),
            "keywords": obj.get("keywords"),
            "language": obj.get("language"),
            "modifiedTime": obj.get("modifiedTime"),
            "ogAudio": obj.get("ogAudio"),
            "ogDescription": obj.get("ogDescription"),
            "ogDeterminer": obj.get("ogDeterminer"),
            "ogImage": obj.get("ogImage"),
            "ogLocale": obj.get("ogLocale"),
            "ogLocaleAlternate": obj.get("ogLocaleAlternate"),
            "ogSiteName": obj.get("ogSiteName"),
            "ogTitle": obj.get("ogTitle"),
            "ogUrl": obj.get("ogUrl"),
            "ogVideo": obj.get("ogVideo"),
            "publishedTime": obj.get("publishedTime"),
            "robots": obj.get("robots"),
            "site_map": Sitemap.from_dict(obj["site_map"]) if obj.get("site_map") is not None else None,
            "sourceURL": obj.get("sourceURL"),
            "statusCode": obj.get("statusCode"),
            "title": obj.get("title")
        })
        return _obj


