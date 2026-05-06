# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import logging
import os
from dataclasses import dataclass

from usd_profiles_nvidia.model import IdVersion, Metadata, Naming, Profile
from usd_profiles_nvidia.toml import PROFILES_TOML, TomlProfilesParser

from ._features import FeatureParser
from ._parser import FileParser, walk_md

logger = logging.getLogger(__name__)


class _ProfileTreeProcessor(FileParser):

    def _parse_id(self, document) -> str:
        """
        Parse the id from the document.
        """
        return Naming.identifier(self.title)

    def _parse_features(self, document) -> list[str]:
        """
        Parse the features from the document.
        """
        if len(document.sections) != 1:
            raise ValueError(f"Profile {self.relpath} has more than one section.")
        if document.sections[0].sections.get("features") is None:
            raise ValueError(f"Profile {self.relpath} has no features section.")
        features: list[str] = []
        for bullet_list in document.sections[0].sections.get("features").bullets:
            for bullet in bullet_list:
                for link in bullet.links:
                    feature_path: str = os.path.normpath(os.path.join(os.path.dirname(self.source_file), link.href))
                    if not feature_path.startswith(os.path.normpath(self.root_dir)):
                        raise ValueError(
                            f"Profile {self.relpath} references feature {link.href} which is outside documentation."
                        )
                    if not os.path.exists(feature_path):
                        raise ValueError(f"Profile {self.relpath} references feature {link.href} which does not exist.")
                    if feature := FeatureParser(self.root_dir, feature_path).parse():
                        features.append(IdVersion(feature.id, feature.version))
        return features

    def run(self) -> Profile:
        document = self.document
        return Profile(
            id=self._parse_id(document),
            version=self.default_version,
            name=self.title,
            description=self.description,
            features=self._parse_features(document),
            metadata=Metadata(path=self.relpath),
        )


@dataclass
class ProfilesParser:
    """
    Parser for all profiles in the root directory.

    Tries ``profiles.toml`` first (multi-version TOML format), then falls
    back to individual ``profile-*.md`` files (markdown with linked features).

    Args:
        root_dir: Sphinx srcdir.
        path: The path to the profiles directory.
    """

    root_dir: str
    path: str

    def _parse_md(self, source_path: str) -> Profile:
        logger.info(f"Parsing profile from: {source_path}")
        return _ProfileTreeProcessor(self.root_dir, source_path).run()

    def _parse_toml(self) -> list[Profile]:
        toml_path = os.path.join(self.path, PROFILES_TOML)
        if not os.path.exists(toml_path):
            return []
        logger.info(f"Parsing profiles from TOML: {toml_path}")
        return TomlProfilesParser(toml_path).parse()

    def _parse_markdown(self) -> list[Profile]:
        profiles: list[Profile] = []
        for full_path in walk_md(self.path):
            source_file = os.path.basename(full_path)
            if source_file.endswith("profiles.md"):
                continue
            if not source_file.startswith("profile-"):
                continue
            if profile := self._parse_md(full_path):
                profiles.append(profile)
        return profiles

    def parse(self) -> list[Profile]:
        # TOML is the authoritative source when present; if the file
        # exists we use it exclusively (even if empty) and never fall
        # through to markdown parsing.
        toml_path = os.path.join(self.path, PROFILES_TOML)
        if os.path.exists(toml_path):
            return self._parse_toml()
        return self._parse_markdown()
