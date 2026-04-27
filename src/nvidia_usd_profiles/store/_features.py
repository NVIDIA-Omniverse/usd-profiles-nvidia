# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import logging
from typing import Any

from nvidia_usd_profiles.model import Feature, IdVersion, Version

from ._keystore import PersistentVersionedRegistry

logger = logging.getLogger(__name__)


class FeatureStore(PersistentVersionedRegistry[Feature]):
    """
    A store of features.

    Args:
        directory: The directory to load features from.
    """

    def create_key(self, value: Any) -> IdVersion | None:
        if isinstance(value, Feature):
            return IdVersion(value.id, Version(value.version))
        return None

    def resolve_requirements(self, feature: Feature) -> list[IdVersion]:
        """
        Return all requirements in the inheritance chain.

        Args:
            feature: The feature to resolve the requirements for.

        Returns:
            A list of requirements.
        """
        base: list[IdVersion] = []
        if feature.extends:
            if parent := self.find(feature.extends):
                base.extend(self.resolve_requirements(parent))
        merged: dict[str, IdVersion] = {iv.id: iv for iv in base}
        for iv in feature.requirements:
            merged[iv.id] = iv
        return list(merged.values())
