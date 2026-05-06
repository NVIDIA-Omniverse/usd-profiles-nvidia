# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import json
import re
from dataclasses import dataclass
from functools import singledispatchmethod

from usd_profiles_nvidia.model import (
    Capability,
    Compatibility,
    Example,
    ExampleSnippet,
    Feature,
    IdVersion,
    Metadata,
    Parameter,
    Profile,
    Requirement,
    Tag,
    Version,
)

__all__ = ["JsonSerialize"]


@dataclass
class _InlineDirective:
    value: str


class JsonSerialize(json.JSONEncoder):
    @singledispatchmethod
    def default(self, o):
        return super().default(o)

    @default.register
    def _(self, o: Requirement):
        return {
            "code": o.code,
            "version": o.version,
            "name": o.name,
            "compatibility": o.compatibility,
            "tags": o.tags,
            "validator": _InlineDirective(o.validator) if o.validator else None,
            "parameters": o.parameters if o.parameters else [],
            "metadata": o.metadata,
            "message": o.description,
            "examples": o.examples if o.examples else [],
        }

    @default.register
    def _(self, o: Parameter):
        return {
            "display_name": o.display_name,
            "type": o.type.value,
            "assigned_value": o.assigned_value,
            "enum_values": o.enum_values,
        }

    @default.register
    def _(self, o: ExampleSnippet):
        return {
            "language": o.language.value,
            "content": o.content,
        }

    @default.register
    def _(self, o: Example):
        return {
            "snippet": o.snippet,
            "name": o.name,
            "result": o.result.value,
        }

    @default.register
    def _(self, o: Capability):
        return {
            "capability": {
                "id": o.id,
                "version": o.version,
                "name": o.name,
                "description": o.description,
                "requirements": o.requirements,
                "metadata": o.metadata,
            }
        }

    @default.register
    def _(self, o: Profile):
        return {
            "profile": {
                "id": o.id,
                "version": o.version,
                "name": o.name,
                "description": o.description,
                "requirements": [],
                "capabilities": [],
                "features": o.features,
                "metadata": o.metadata,
            }
        }

    @default.register
    def _(self, o: Feature):
        return {
            "feature": {
                "id": o.id,
                "version": o.version,
                "name": o.name,
                "description": o.description,
                "requirements": o.requirements,
                "extends": o.extends,
                "metadata": o.metadata,
            }
        }

    @default.register
    def _(self, o: Metadata):
        return {
            "path": o.html_path,
            "internal_path": o.md_path,
        }

    @default.register
    def _(self, o: _InlineDirective):
        if value := re.search(r"{.*}`(.*?)`", o.value):
            return value.group(1)
        return o.value

    @default.register
    def _(self, o: Version):
        return str(o)

    @default.register
    def _(self, o: IdVersion):
        if o.version is None:
            return o.id
        else:
            return f"{o.id}@{o.version}"

    @default.register
    def _(self, o: Compatibility):
        return o.display_name

    @default.register
    def _(self, o: Tag):
        return o.display_name
