# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import unittest

from nvidia_usd_profiles.model import Feature, Metadata, Version


class TestFeature(unittest.TestCase):

    def test_enum_name(self):
        feature = Feature(id="semantic_labels", version=Version(1, 0, 0))

        self.assertEqual(feature.enum_id, "SEMANTIC_LABELS")
        self.assertEqual(feature.enum_id_version, "SEMANTIC_LABELS_V1_0_0")

    def test_source_file_name(self):
        feature = Feature(id="semantic_labels", metadata=Metadata(path="docs/features/semantic_labels.md"))

        self.assertEqual(feature.source_file_name, "semantic_labels")
