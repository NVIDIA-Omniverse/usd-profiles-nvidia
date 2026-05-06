# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import unittest

from usd_profiles_nvidia.model import Capability, Version


class TestCapability(unittest.TestCase):

    def test_enum_name(self):
        capability = Capability(id="semantic_labels", version=Version(1, 0, 0))

        self.assertEqual(capability.enum_id, "SEMANTIC_LABELS")
        self.assertEqual(capability.enum_id_version, "SEMANTIC_LABELS_V1_0_0")

    def test_class_name(self):
        capability = Capability(id="semantic_labels")

        self.assertEqual(capability.class_name, "SemanticLabels")
