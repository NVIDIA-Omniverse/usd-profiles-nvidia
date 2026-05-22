# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

from dataclasses import dataclass

from usd_profiles_nvidia.markdown import MdFeaturesParser
from usd_profiles_nvidia.model import Feature


@dataclass
class FeaturesParser:
    """
    Format-agnostic parser for all features in the root directory.

    Args:
        root_dir: Sphinx srcdir.
        path: The path to the features directory.
    """

    root_dir: str
    path: str

    def parse(self) -> list[Feature]:
        """
        Parse all features from the root directory.
        """
        return MdFeaturesParser(root_dir=self.root_dir, path=self.path).parse()
