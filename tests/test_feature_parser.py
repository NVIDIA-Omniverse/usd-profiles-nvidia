# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import unittest
from pathlib import Path

from nvidia_usd_profiles.markdown import FeaturesParser
from nvidia_usd_profiles.model import IdVersion, Version


class TestFeaturesParser(unittest.TestCase):
    def test_parse_ok(self):
        root_dir = Path(__file__).parent / "resources" / "simple-feature"
        parser = FeaturesParser(root_dir=str(root_dir), path=str(root_dir))
        features = parser.parse()

        self.assertEqual(len(features), 1)
        self.assertEqual(features[0].id, "example")
        self.assertEqual(features[0].version, Version(1, 0, 0))
        self.assertEqual(features[0].name, "Example")
        self.assertEqual(features[0].description, "This is an example feature")
        self.assertEqual(features[0].requirements, [IdVersion("HI.001")])

    def test_parse_with_options_ok(self):
        root_dir = Path(__file__).parent / "resources" / "simple-feature-options"
        parser = FeaturesParser(root_dir=str(root_dir), path=str(root_dir))
        features = parser.parse()

        self.assertEqual(len(features), 1)
        self.assertEqual(features[0].id, "example")
        self.assertEqual(features[0].version, Version(1, 0, 0))
        self.assertEqual(features[0].name, "Example")
        self.assertEqual(features[0].description, "This is an example feature")
        self.assertEqual(features[0].requirements, [IdVersion("HI.001"), IdVersion("HI.002")])

    def test_parse_with_extends_ok(self):
        root_dir = Path(__file__).parent / "resources" / "simple-feature-extends"
        parser = FeaturesParser(root_dir=str(root_dir), path=str(root_dir))
        features = parser.parse()

        self.assertEqual(len(features), 2)
        base, extended = sorted(features, key=lambda f: f.version or Version(0, 0, 0))
        self.assertEqual(base.id, "base")
        self.assertEqual(base.version, Version(1, 0, 0))
        self.assertEqual(
            base.requirements,
            [IdVersion("A", Version(1, 0, 0)), IdVersion("B", Version(1, 0, 0))],
        )
        self.assertEqual(extended.id, "extended")
        self.assertEqual(extended.version, Version(1, 1, 0))
        self.assertEqual(extended.extends, IdVersion("base", Version(1, 0, 0)))

    def test_parse_with_requirements_sublist_ok(self):
        root_dir = Path(__file__).parent / "resources" / "simple-feature-links"
        parser = FeaturesParser(root_dir=str(root_dir), path=str(root_dir))
        features = parser.parse()

        self.assertEqual(len(features), 1)
        self.assertEqual(features[0].id, "example")
        self.assertEqual(features[0].version, Version(1, 0, 0))
        self.assertEqual(features[0].name, "Naming Paths Feature")
        self.assertEqual(
            features[0].requirements,
            [IdVersion("NP.001", Version(0, 1, 0))],
        )

    def test_parse_with_multi_version_ok(self):
        root_dir = Path(__file__).parent / "resources" / "simple-feature-multi-version"
        parser = FeaturesParser(root_dir=str(root_dir), path=str(root_dir / "example.md"))
        features = parser.parse()

        self.assertEqual(len(features), 2)
        by_version = sorted(features, key=lambda f: f.version)
        v01, v10 = by_version[0], by_version[1]
        self.assertEqual(v01.id, "FET_001")
        self.assertEqual(v01.version, Version(0, 1, 0))
        self.assertEqual(v01.name, "Naming Paths Feature")
        self.assertEqual(v01.requirements, [IdVersion("NP.001", Version(0, 1, 0))])
        self.assertEqual(v10.id, "FET_001")
        self.assertEqual(v10.version, Version(1, 0, 0))
        self.assertEqual(v10.name, "Naming Paths Feature")
        self.assertEqual(v10.requirements, [IdVersion("NP.001", Version(0, 1, 0))])
