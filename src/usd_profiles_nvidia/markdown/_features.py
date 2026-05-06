# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import json
import logging
import os
from dataclasses import dataclass, replace
from typing import Any

from usd_profiles_nvidia.model import Feature, IdVersion, Metadata, Requirement, Version
from usd_profiles_nvidia.serialization import JsonDeserialize

from ._model import Section, Sections
from ._parser import walk_md
from ._references import ReferencesParser

logger = logging.getLogger(__name__)


class _FeatureParser(ReferencesParser):

    @property
    def default_name(self) -> str:
        return super().default_name.removeprefix("feature-")

    def _parse_attributes(self, document) -> dict[str, Any]:
        """
        Parse attributes from the document's first table.

        Returns:
            A dictionary of attribute key-value pairs.
        """
        data: dict[str, str] = self.main_table.to_dict()
        if "version" not in data:
            raise ValueError(f"Feature {self.relpath} has no version.")
        if "dependency" not in data:
            raise ValueError(f"Feature {self.relpath} has no dependency.")
        data["version"] = Version(data["version"])
        if "extends" in data:
            data["extends"] = IdVersion.parse(data["extends"])
        return data

    @property
    def requirements_json(self) -> str:
        """
        Returns the requirements JSON.
        """
        return os.path.join(os.path.dirname(self.source_file), f"requirements-{self.default_id}.json")

    @property
    def feature_json(self) -> list[IdVersion]:
        """
        Returns the requirements from the feature JSON.
        """
        if not os.path.exists(self.requirements_json):
            return []
        with open(self.requirements_json, encoding="utf-8") as f:
            feature: Feature = json.load(f, cls=JsonDeserialize)
            return feature.requirements

    def parse(self) -> Feature | None:
        """
        Parse the feature from the source file.
        Returns None if the feature has no requirements.
        """
        requirements: list[IdVersion] = []
        if requirements_list := self.requirements_list:
            requirements.extend(IdVersion(requirement.code, requirement.version) for requirement in requirements_list)
        elif requirements_table := self.requirements_table:
            requirements.extend(IdVersion(requirement.code, requirement.version) for requirement in requirements_table)
        elif features_table := self.features_table:
            requirements.extend(features_table)
        elif feature_json := self.feature_json:
            requirements.extend(feature_json)
        else:
            return None
        document = self.document
        attrs: dict[str, Any] = self._parse_attributes(document)
        return Feature(
            id=self.default_id,
            version=attrs["version"],
            name=self.title,
            description=self.description_content,
            requirements=requirements,
            metadata=Metadata(path=self.relpath),
            dependency=attrs["dependency"],
            extends=attrs.get("extends"),
        )


@dataclass
class FeatureParser:
    """
    Parser for a single feature.

    Args:
        root_dir: Sphinx srcdir.
        source_file: The file to parse features from.
    """

    root_dir: str
    source_file: str

    def parse(self) -> Feature | None:
        """
        Parse the feature from the source file.
        """
        return _FeatureParser(self.root_dir, self.source_file).parse()


@dataclass
class MultiFeatureParser(ReferencesParser):
    """
    Parser for a single feature with multiple versions.

    Args:
        root_dir: Sphinx srcdir.
        path: The path to the features directory.
    """

    @property
    def internal_id(self) -> str:
        try:
            attrs = self.main_table.to_dict()
        except ValueError:
            attrs = {}
        internal_id: str = attrs.get("internal id") or attrs.get("id") or self.default_id
        if internal_id.startswith("`") and internal_id.endswith("`"):
            internal_id = internal_id[1:-1]
        return internal_id

    def is_version_section(self, section: Section) -> bool:
        tokens: list[str] = section.title.split(" ", 1)
        if len(tokens) < 2 or tokens[0] != "Version":
            return False
        requirements_section: Section | None = section.sections.get("requirements")
        if requirements_section is None:
            return False
        if not requirements_section.bullets:
            return False
        return True

    @property
    def versions_section(self) -> Section | None:
        for section in self.main_section.walk_sections():
            subsections: Sections = section.sections
            if any(map(self.is_version_section, subsections)):
                return section
        return None

    def parse(self) -> list[Feature]:
        """
        Parse the feature from the source file.
        """
        versions_section: Section | None = self.versions_section
        if versions_section is None:
            return []
        feature: Feature = Feature(
            id=self.internal_id,
            name=self.title,
            description=self.description_content,
            metadata=Metadata(path=self.relpath),
        )
        features: list[Feature] = []
        for section in filter(self.is_version_section, versions_section.sections):
            version: Version = Version(section.title.split(" ")[1])
            requirements_section: Section | None = section.sections.get("requirements")
            if requirements_section is None:
                continue
            requirements: list[Requirement] = self.get_requirements_list(requirements_section) or []
            id_versions: list[IdVersion] = [
                IdVersion(requirement.code, requirement.version) for requirement in requirements
            ]
            features.append(replace(feature, version=version, requirements=id_versions))
        return features


@dataclass
class FeaturesParser:
    """
    Parser for features.

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
        features: list[Feature] = []
        for source_path in walk_md(self.path):
            if feature := FeatureParser(self.root_dir, source_path).parse():
                features.append(feature)
            elif multi_feature := MultiFeatureParser(self.root_dir, source_path).parse():
                features.extend(multi_feature)
        return features
