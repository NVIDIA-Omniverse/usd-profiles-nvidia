# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import unittest

from usd_profiles_nvidia.model import Requirement, Version


class TestRequirement(unittest.TestCase):
    def test_enum_name(self):
        requirement = Requirement(code="VG.001", version=Version(1, 0, 0))

        self.assertEqual(requirement.enum_id, "VG_001")
        self.assertEqual(requirement.enum_id_version, "VG_001_V1_0_0")

    def test_namespace_set_after_construction(self):
        """Setting namespace leaves id raw but namespaced_id returns qualified form."""
        req = Requirement(code="materials.MAT.001", version=Version(1, 0, 0))
        req.namespace = "com.nvidia.simready"
        # Raw id stays as-is — no mutation
        self.assertEqual(req.id, "materials.MAT.001")
        self.assertEqual(req.code, "materials.MAT.001")
        # Computed property returns qualified form
        self.assertEqual(req.namespaced_id, "com.nvidia.simready.materials.MAT.001")
        # enum names strip the namespace
        self.assertEqual(req.enum_id, "MATERIALS_MAT_001")
        self.assertEqual(req.enum_id_version, "MATERIALS_MAT_001_V1_0_0")

    def test_namespace_in_constructor(self):
        """Namespace at construction time leaves id raw; namespaced_id computes."""
        req = Requirement(code="materials.MAT.001", namespace="com.nvidia.simready")
        self.assertEqual(req.id, "materials.MAT.001")
        self.assertEqual(req.namespaced_id, "com.nvidia.simready.materials.MAT.001")

    def test_namespace_already_qualified(self):
        """Already-qualified id is not double-prefixed by namespaced_id."""
        req = Requirement(code="com.nvidia.simready.materials.MAT.001")
        req.namespace = "com.nvidia.simready"
        self.assertEqual(req.id, "com.nvidia.simready.materials.MAT.001")
        self.assertEqual(req.namespaced_id, "com.nvidia.simready.materials.MAT.001")

    def test_no_namespace_unchanged(self):
        """Without namespace, id/code stay as-is."""
        req = Requirement(code="VG.001")
        self.assertEqual(req.id, "VG.001")
        self.assertEqual(req.code, "VG.001")
