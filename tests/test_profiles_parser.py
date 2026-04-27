# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import unittest
from pathlib import Path

from nvidia_usd_profiles.markdown import ProfilesParser
from nvidia_usd_profiles.model import IdVersion, Version


class TestProfilesParser(unittest.TestCase):

    def test_parse_ok(self):
        root_dir = Path(__file__).parent / "resources" / "simple-profile"
        parser = ProfilesParser(root_dir=str(root_dir), path=str(root_dir))
        profiles = parser.parse()

        self.assertGreaterEqual(len(profiles), 1)
        self.assertEqual(profiles[0].id, "name")
        self.assertEqual(profiles[0].version, Version(1, 0, 0))
        self.assertEqual(profiles[0].name, "Name")
        self.assertEqual(profiles[0].description, "Description")
        self.assertEqual(len(profiles[0].features), 2)
        self.assertEqual(profiles[0].features[0], IdVersion("simple", Version(1, 0, 0)))
        self.assertEqual(profiles[0].features[1], IdVersion("complex", Version(1, 0, 0)))
