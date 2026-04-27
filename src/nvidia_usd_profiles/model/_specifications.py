# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

from dataclasses import dataclass
from functools import cached_property

from ._capability import Capability
from ._feature import Feature
from ._profile import Profile
from ._requirement import Requirement


@dataclass(frozen=True)
class Specifications:
    """
    A collection of specifications.

    Args:
        capabilities: The capabilities of the specifications.
        features: The features of the specifications.
        profiles: The profiles of the specifications.
        reverse_domain: Reverse-domain prefix for spec identifiers (e.g. ``"com.nvidia.simready"``). Empty means legacy behavior.
    """

    capabilities: list[Capability]
    features: list[Feature]
    profiles: list[Profile]
    reverse_domain: str = ""

    @cached_property
    def requirements(self) -> list[Requirement]:
        """
        Get the requirements of the specifications.
        """
        return [requirement for capability in self.capabilities for requirement in capability.requirements]
