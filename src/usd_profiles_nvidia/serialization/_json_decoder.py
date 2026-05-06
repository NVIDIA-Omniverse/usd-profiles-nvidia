# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import json

from usd_profiles_nvidia.model import (
    Capability,
    Compatibility,
    Example,
    ExampleResult,
    ExampleSnippet,
    ExampleSnippetLanguage,
    Feature,
    IdVersion,
    Metadata,
    Parameter,
    ParameterType,
    Profile,
    Requirement,
    Tag,
    Version,
)

__all__ = ["JsonDeserialize"]


class JsonDeserialize(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    @classmethod
    def object_hook(cls, dct):
        if "capability" in dct:
            return cls.decode_capability(dct["capability"])
        elif "profile" in dct:
            return cls.decode_profile(dct["profile"])
        elif "feature" in dct:
            return cls.decode_feature(dct["feature"])
        elif "code" in dct and "tags" in dct:
            return cls.decode_requirement(dct)
        elif "type" in dct and "display_name" in dct and "assigned_value" in dct:
            return cls.decode_parameter(dct)
        elif "path" in dct:
            return cls.decode_metadata(dct)
        elif "snippet" in dct and "name" in dct and "result" in dct:
            return cls.decode_example(dct)
        elif "language" in dct and "content" in dct:
            return cls.decode_example_snippet(dct)
        else:
            return dct

    @classmethod
    def decode_capability(cls, dct):
        return Capability(
            id=dct["id"],
            version=cls.decode_version(dct.get("version")),
            name=dct.get("name"),
            description=dct.get("description"),
            requirements=dct.get("requirements", []),
            metadata=dct.get("metadata", Metadata()),
        )

    @classmethod
    def decode_profile(cls, dct):
        return Profile(
            id=dct["id"],
            version=cls.decode_version(dct.get("version")),
            name=dct.get("name"),
            description=dct.get("description"),
            features=cls.decode_id_versions(dct.get("features")),
            metadata=dct.get("metadata", Metadata()),
        )

    @classmethod
    def decode_feature(cls, dct):
        return Feature(
            id=dct["id"],
            version=cls.decode_version(dct.get("version")),
            name=dct.get("name"),
            description=dct.get("description"),
            requirements=cls.decode_id_versions(dct.get("requirements")),
            extends=cls.decode_id_version(dct.get("extends")),
            metadata=dct.get("metadata", Metadata()),
        )

    @classmethod
    def decode_requirement(cls, dct):
        return Requirement(
            code=dct["code"],
            version=cls.decode_version(dct.get("version")),
            name=dct.get("name"),
            compatibility=Compatibility.from_name(dct.get("compatibility")),
            tags=Tag.from_name(dct.get("tags")),
            validator=dct.get("validator"),
            parameters=dct.get("parameters", []),
            metadata=dct.get("metadata", Metadata()),
            description=dct.get("message"),
            examples=dct.get("examples", []),
        )

    @classmethod
    def decode_parameter(cls, dct):
        return Parameter(
            display_name=dct["display_name"],
            type=ParameterType(dct["type"]),
            assigned_value=dct.get("assigned_value"),
            enum_values=dct.get("enum_values"),
        )

    @classmethod
    def decode_example(cls, dct):
        return Example(
            snippet=dct["snippet"],
            name=dct["name"],
            result=ExampleResult(dct["result"]),
        )

    @classmethod
    def decode_example_snippet(cls, dct):
        return ExampleSnippet(
            language=ExampleSnippetLanguage(dct["language"]),
            content=dct["content"],
        )

    @classmethod
    def decode_metadata(cls, dct):
        return Metadata(
            path=dct.get("path"),
        )

    @classmethod
    def decode_version(cls, version: str | None):
        if version is not None:
            return Version(version)
        else:
            return None

    @classmethod
    def decode_id_versions(cls, id_versions: list[str] | None) -> list[IdVersion]:
        if id_versions is not None:
            return [IdVersion.parse(id_version) for id_version in id_versions]
        else:
            return []

    @classmethod
    def decode_id_version(cls, id_version: str | None) -> IdVersion | None:
        if id_version is not None:
            return IdVersion.parse(id_version)
        else:
            return None
