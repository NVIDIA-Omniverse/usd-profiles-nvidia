# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import unittest

from nvidia_usd_profiles import __version__


class TestVersion(unittest.TestCase):
    """Tests for the package version attribute."""

    def test_version_is_set(self):
        """__version__ should be a non-empty string."""
        self.assertTrue(__version__)
