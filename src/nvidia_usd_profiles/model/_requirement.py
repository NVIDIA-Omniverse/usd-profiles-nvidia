# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

from dataclasses import dataclass, field

from ._compatibility import Compatibility
from ._example import Example
from ._model import Model
from ._parameter import Parameter
from ._tag import Tag


@dataclass(slots=True)
class Requirement(Model):
    """
    Represents a single requirement.

    Args:
        code: Unique identifier for this requirement (e.g. ``"com.nvidia.simready.materials.MAT.001"``).
        compatibility (Compatibility): Compatibility of the requirement
        validator (str): Validator of the requirement
        tags (Tag): Tags of the requirement
        parameters (list[Parameter]): Parameters of the requirement
        examples (list[Example]): Examples of the requirement
    """

    code: str = ""
    compatibility: Compatibility | None = None
    validator: str | None = None
    tags: Tag | None = None
    parameters: list[Parameter] = field(default_factory=list)
    examples: list[Example] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.code:
            self.id = self.code

    @property
    def priority(self) -> int:
        return self.tags.priority if self.tags else 0
