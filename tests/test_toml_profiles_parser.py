# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import tempfile
import unittest
from pathlib import Path

from nvidia_usd_profiles.markdown import ProfilesParser
from nvidia_usd_profiles.model import IdVersion, Version
from nvidia_usd_profiles.toml import TomlProfilesParser


class TestTomlProfilesParser(unittest.TestCase):

    def setUp(self):
        self.toml_path = str(Path(__file__).parent / "resources" / "toml-profiles" / "profiles.toml")
        self.profiles = TomlProfilesParser(toml_path=self.toml_path).parse()

    def test_parse_profiles(self):
        profile_ids = [(p.id, str(p.version)) for p in self.profiles]
        self.assertIn(("Prop-Robotics-Neutral", "1.0.0"), profile_ids)
        self.assertIn(("Prop-Robotics-Neutral", "2.0.0"), profile_ids)
        self.assertIn(("Robot-Body-Isaac", "1.0.0"), profile_ids)
        self.assertEqual(len(self.profiles), 3)

    def test_parse_profile_features(self):
        neutral_v1 = next(p for p in self.profiles if p.id == "Prop-Robotics-Neutral" and str(p.version) == "1.0.0")
        self.assertEqual(len(neutral_v1.features), 2)
        self.assertEqual(neutral_v1.features[0], IdVersion("FET001_BASE_NEUTRAL", Version("0.1.0")))
        self.assertEqual(neutral_v1.features[1], IdVersion("FET003_BASE_NEUTRAL", Version("0.1.0")))

    def test_parse_multi_version_profile(self):
        neutral_v1 = next(p for p in self.profiles if p.id == "Prop-Robotics-Neutral" and str(p.version) == "1.0.0")
        neutral_v2 = next(p for p in self.profiles if p.id == "Prop-Robotics-Neutral" and str(p.version) == "2.0.0")
        self.assertEqual(neutral_v1.features[0], IdVersion("FET001_BASE_NEUTRAL", Version("0.1.0")))
        self.assertEqual(neutral_v2.features[0], IdVersion("FET001_BASE_NEUTRAL", Version("1.0.0")))

    def test_parse_robot_body_isaac(self):
        isaac = next(p for p in self.profiles if p.id == "Robot-Body-Isaac")
        self.assertEqual(isaac.version, Version("1.0.0"))
        self.assertEqual(len(isaac.features), 3)
        self.assertEqual(isaac.features[1], IdVersion("FET004_ROBOT_PHYSX", Version("0.2.0")))

    def test_parse_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            TomlProfilesParser(toml_path="/nonexistent/profiles.toml").parse()

    def test_profile_name_preserved(self):
        isaac = next(p for p in self.profiles if p.id == "Robot-Body-Isaac")
        self.assertEqual(isaac.name, "Robot-Body-Isaac")

    def test_malformed_version_not_a_table(self):
        # Version entry is a plain string instead of a TOML inline table — hits
        # the per-version isinstance(version_data, dict) check.
        with tempfile.TemporaryDirectory() as tmpdir:
            toml_path = str(Path(tmpdir) / "profiles.toml")
            Path(toml_path).write_text('[Bad]\n"1.0.0" = "just a string"\n')
            with self.assertRaises(ValueError) as ctx:
                TomlProfilesParser(toml_path=toml_path).parse()
            self.assertIn("must be a table", str(ctx.exception))

    def test_malformed_missing_features_key(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            toml_path = str(Path(tmpdir) / "profiles.toml")
            Path(toml_path).write_text('[Bad]\n"1.0.0" = {other = "data"}\n')
            with self.assertRaises(ValueError) as ctx:
                TomlProfilesParser(toml_path=toml_path).parse()
            self.assertIn("missing required 'features' key", str(ctx.exception))

    def test_malformed_feature_multi_key(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            toml_path = str(Path(tmpdir) / "profiles.toml")
            Path(toml_path).write_text(
                '[Bad]\n"1.0.0" = {features = [{A = {version = "1.0.0"}, B = {version = "2.0.0"}}]}\n'
            )
            with self.assertRaises(ValueError) as ctx:
                TomlProfilesParser(toml_path=toml_path).parse()
            self.assertIn("single-key", str(ctx.exception))

    def test_malformed_feature_missing_version(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            toml_path = str(Path(tmpdir) / "profiles.toml")
            Path(toml_path).write_text('[Bad]\n"1.0.0" = {features = [{FET001 = {}}]}\n')
            with self.assertRaises(KeyError):
                TomlProfilesParser(toml_path=toml_path).parse()

    def test_malformed_bad_version_string(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            toml_path = str(Path(tmpdir) / "profiles.toml")
            Path(toml_path).write_text('[Bad]\n"not.a.ver.sion" = {features = []}\n')
            with self.assertRaises(ValueError):
                TomlProfilesParser(toml_path=toml_path).parse()

    def test_empty_features_list(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            toml_path = str(Path(tmpdir) / "profiles.toml")
            Path(toml_path).write_text('[EmptyProfile]\n"1.0.0" = {features = []}\n')
            profiles = TomlProfilesParser(toml_path=toml_path).parse()
            self.assertEqual(len(profiles), 1)
            self.assertEqual(profiles[0].id, "EmptyProfile")
            self.assertEqual(profiles[0].features, [])


class TestProfilesParserTomlFallback(unittest.TestCase):
    """ProfilesParser should prefer TOML when profiles.toml exists."""

    def test_profiles_parser_finds_toml(self):
        root_dir = str(Path(__file__).parent / "resources" / "toml-profiles")
        parser = ProfilesParser(root_dir=root_dir, path=root_dir)
        profiles = parser.parse()

        self.assertEqual(len(profiles), 3)
        profile_ids = {p.id for p in profiles}
        self.assertIn("Prop-Robotics-Neutral", profile_ids)
        self.assertIn("Robot-Body-Isaac", profile_ids)

    def test_profiles_parser_falls_back_to_markdown(self):
        root_dir = str(Path(__file__).parent / "resources" / "simple-profile")
        parser = ProfilesParser(root_dir=root_dir, path=root_dir)
        profiles = parser.parse()

        self.assertGreaterEqual(len(profiles), 1)
        self.assertEqual(profiles[0].id, "name")
