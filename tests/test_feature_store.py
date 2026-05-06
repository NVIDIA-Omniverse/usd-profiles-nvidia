# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import unittest

from usd_profiles_nvidia.model import Feature, IdVersion, Version
from usd_profiles_nvidia.store import FeatureStore


class TestFeatureStore(unittest.TestCase):
    def test_merges_extended_and_self(self):
        # Base feature @ 1.0.0: requirements A@1.0.0, B@1.0.0
        base = Feature(
            id="feature-id",
            version=Version(1, 0, 0),
            requirements=[
                IdVersion("A", Version(1, 0, 0)),
                IdVersion("B", Version(1, 0, 0)),
            ],
        )
        # Current feature @ 1.1.0 extends 1.0.0, requirements B@1.1.0 only
        current = Feature(
            id="feature-id",
            version=Version(1, 1, 0),
            extends=IdVersion("feature-id", Version(1, 0, 0)),
            requirements=[IdVersion("B", Version(1, 1, 0))],
        )
        store = FeatureStore([base, current])

        resolved = sorted(store.resolve_requirements(current))
        self.assertEqual(
            resolved,
            [
                IdVersion("A", Version(1, 0, 0)),
                IdVersion("B", Version(1, 1, 0)),
            ],
        )

    def test_no_extends_returns_self_requirements(self):
        feature = Feature(
            id="feature-id",
            version=Version(1, 0, 0),
            requirements=[IdVersion("A", Version(1, 0, 0))],
        )
        store = FeatureStore([feature])

        resolved = store.resolve_requirements(feature)
        self.assertEqual(resolved, feature.requirements)
