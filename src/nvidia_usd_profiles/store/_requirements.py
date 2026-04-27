# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import logging
from typing import Any

from nvidia_usd_profiles.model import Capability, IdVersion, Requirement

from ._keystore import PersistentVersionedRegistry

logger = logging.getLogger(__name__)


class RequirementStore(PersistentVersionedRegistry[Requirement]):
    """
    A store of requirements.

    Args:
        directory: The directory to load requirements from.
    """

    def create_values(self, result: Any) -> list[Requirement]:
        if isinstance(result, Capability):
            return result.requirements
        return []

    def create_key(self, value: Any) -> IdVersion | None:
        if isinstance(value, Requirement):
            return IdVersion(value.code, value.version)
        return None
