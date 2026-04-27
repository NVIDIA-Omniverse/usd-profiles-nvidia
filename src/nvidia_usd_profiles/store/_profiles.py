# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import logging
from typing import Any

from nvidia_usd_profiles.model import IdVersion, Profile

from ._keystore import PersistentVersionedRegistry

logger = logging.getLogger(__name__)


class ProfileStore(PersistentVersionedRegistry[Profile]):
    """
    A store of profiles.

    Args:
        directory: The directory to load profiles from.
    """

    def __init__(self, directory: str) -> None:
        super().__init__(directory)

    def create_key(self, value: Any) -> IdVersion | None:
        if isinstance(value, Profile):
            return IdVersion(value.id, value.version)
        return None
