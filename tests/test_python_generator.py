# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import importlib
import os
import sys
import unittest
from tempfile import TemporaryDirectory


class TestPythonGenerator(unittest.TestCase):
    def assert_files(self, output_dir: str) -> None:
        self.assertTrue(os.path.exists(output_dir))
        self.assertTrue(os.path.exists(os.path.join(output_dir, "__init__.py")))
        self.assertTrue(os.path.exists(os.path.join(output_dir, "_protocols.py")))
        self.assertTrue(os.path.exists(os.path.join(output_dir, "_requirements.py")))
        self.assertTrue(os.path.exists(os.path.join(output_dir, "_capabilities.py")))
        self.assertTrue(os.path.exists(os.path.join(output_dir, "_profiles.py")))
        self.assertTrue(os.path.exists(os.path.join(output_dir, "_features.py")))

    def assert_protocols(self, module) -> None:
        self.assertTrue(hasattr(module, "RequirementProtocol"))
        self.assertTrue(hasattr(module, "CapabilityProtocol"))
        self.assertTrue(hasattr(module, "FeatureProtocol"))
        self.assertTrue(hasattr(module, "ProfileProtocol"))
        self.assertTrue(hasattr(module, "Requirements"))
        self.assertTrue(hasattr(module, "Capabilities"))
        self.assertTrue(hasattr(module, "Features"))
        self.assertTrue(hasattr(module, "Profiles"))
        for requirement in module.Requirements:
            self.assertIsInstance(requirement, module.RequirementProtocol)
        for capability in module.Capabilities:
            self.assertIsInstance(capability, module.CapabilityProtocol)
        for feature in module.Features:
            self.assertIsInstance(feature, module.FeatureProtocol)
        for profile in module.Profiles:
            self.assertIsInstance(profile, module.ProfileProtocol)

    def test_codegen_py(self):
        """Test basic code generation (legacy, no reverse_domain)."""
        from usd_profiles_nvidia.codegen import PythonGenerator

        docs_root = os.path.join(os.path.dirname(__file__), "resources", "simple-spec")
        with TemporaryDirectory() as tmpdirname:
            generator = PythonGenerator(
                docs_root=docs_root,
                destination_dir=os.path.join(tmpdirname, "python"),
                package_name="omni.profiles",
            )
            generator.generate()

            output_dir = os.path.join(tmpdirname, "python", "omni", "profiles")
            self.assert_files(output_dir)

            sys.path.insert(0, os.path.join(tmpdirname, "python"))
            try:
                profiles = importlib.import_module("omni.profiles")

                self.assert_protocols(profiles)
                self.assertTrue(hasattr(profiles.Capabilities, "GEOMETRY"))
                self.assertEqual(profiles.Capabilities.GEOMETRY.id, "geometry")

                self.assertTrue(hasattr(profiles.Requirements, "VG_RTX_002_V1_0_0"))
                self.assertEqual(profiles.Requirements.VG_RTX_002_V1_0_0.code, "VG.RTX.002")
                self.assertEqual(profiles.Requirements.VG_RTX_002_V1_0_0.version, "1.0.0")
            finally:
                sys.path.pop(0)

    def test_codegen_with_parameters(self):
        """Test code generation with parameters (legacy, no reverse_domain)."""
        from usd_profiles_nvidia.codegen import PythonGenerator

        docs_root = os.path.join(os.path.dirname(__file__), "resources", "param-test-spec")
        with TemporaryDirectory() as tmpdirname:
            generator = PythonGenerator(
                docs_root=docs_root,
                destination_dir=os.path.join(tmpdirname, "python"),
                package_name="omni.test_params",
            )
            generator.generate()

            output_dir = os.path.join(tmpdirname, "python", "omni", "test_params")
            self.assert_files(output_dir)

            sys.path.insert(0, os.path.join(tmpdirname, "python"))
            try:
                test_params = importlib.import_module("omni.test_params")

                self.assert_protocols(test_params)
                self.assertTrue(hasattr(test_params.Capabilities, "TEST"))
                self.assertEqual(test_params.Capabilities.TEST.id, "test")

                self.assertTrue(hasattr(test_params.Requirements, "VG_RTX_003_V1_0_0"))
                self.assertEqual(test_params.Requirements.VG_RTX_003_V1_0_0.code, "VG.RTX.003")
                self.assertTrue(hasattr(test_params.Parameters, "UP_AXIS"))
                self.assertTrue(hasattr(test_params.Parameters, "NESTING_LEVEL"))
                self.assertTrue(hasattr(test_params.Parameters, "ENABLED"))

                self.assertTrue(hasattr(test_params.Requirements, "VG_RTX_004_V1_0_0"))
                self.assertEqual(test_params.Requirements.VG_RTX_004_V1_0_0.code, "VG.RTX.004")
                self.assertTrue(hasattr(test_params.Parameters, "MODE"))
            finally:
                sys.path.pop(0)

    def test_codegen_with_reverse_domain(self):
        """reverse_domain auto-qualifies short names; enum members have the prefix stripped."""
        from usd_profiles_nvidia.codegen import PythonGenerator

        docs_root = os.path.join(os.path.dirname(__file__), "resources", "namespace-spec")
        with TemporaryDirectory() as tmpdirname:
            generator = PythonGenerator(
                docs_root=docs_root,
                destination_dir=os.path.join(tmpdirname, "python"),
                package_name="simready.foundations.core",
                reverse_domain="com.nvidia.simready",
            )
            generator.generate()

            output_dir = os.path.join(tmpdirname, "python", "simready", "foundations", "core")
            self.assert_files(output_dir)

            sys.path.insert(0, os.path.join(tmpdirname, "python"))
            try:
                core = importlib.import_module("simready.foundations.core")

                self.assertTrue(hasattr(core.Requirements, "MATERIALS_MAT_001_V1_0_0"))
                self.assertEqual(
                    core.Requirements.MATERIALS_MAT_001_V1_0_0.code,
                    "com.nvidia.simready.materials.MAT.001",
                )

                self.assertTrue(hasattr(core.Features, "RIGID_BODY_PHYSICS_V1_0_0"))
                self.assertEqual(
                    core.Features.RIGID_BODY_PHYSICS_V1_0_0.id,
                    "com.nvidia.simready.rigid_body_physics",
                )

                self.assertTrue(hasattr(core.Profiles, "PROP_ROBOTICS_NEUTRAL"))
                self.assertEqual(
                    core.Profiles.PROP_ROBOTICS_NEUTRAL.id,
                    "com.nvidia.simready.prop_robotics_neutral",
                )

                self.assertTrue(hasattr(core.Capabilities, "MATERIALS"))
                self.assertEqual(
                    core.Capabilities.MATERIALS.id,
                    "com.nvidia.simready.materials",
                )
            finally:
                sys.path.pop(0)
                for mod_name in list(sys.modules):
                    if mod_name.startswith("simready.foundations.core"):
                        del sys.modules[mod_name]
