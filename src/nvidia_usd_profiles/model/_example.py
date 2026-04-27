# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import hashlib
from dataclasses import dataclass
from enum import Enum

from ._naming import Naming


class ExampleResult(str, Enum):
    """Expected result of an example."""

    SUCCESS = "success"
    FAILURE = "failure"


class ExampleSnippetLanguage(str, Enum):
    """Language of an example snippet."""

    PYTHON = "python"
    USD = "usd"


@dataclass(frozen=True, slots=True)
class ExampleSnippet:
    """A snippet of code in a specific language."""

    language: ExampleSnippetLanguage
    content: str

    @property
    def filename(self) -> str:
        md5 = hashlib.md5(self.content.encode("utf-8")).hexdigest()[:12]
        return f"{md5}.{self.language.value}"


@dataclass(frozen=True, slots=True)
class Example:
    """An example of a requirement."""

    snippet: ExampleSnippet
    name: str
    result: ExampleResult

    @property
    def enum_name(self) -> str:
        suffix: str = "_OK" if self.result is ExampleResult.SUCCESS else "_NOK"
        return Naming.enum_name(self.name) + suffix
