# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import json
import os
from dataclasses import dataclass, replace

from usd_profiles_nvidia.api import Feature, FeatureRef, RequirementRef
from usd_profiles_nvidia.model import IdVersion, Metadata, Version


class _FeatureDeserialize(json.JSONDecoder):
    """
    JSON decoder for feature files.

    Unlike JsonDeserialize, this assumes top-level JSON objects with id, version,
    and requirements keys are feature definitions.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    @classmethod
    def object_hook(cls, dct):
        if "id" in dct and "version" in dct and "requirements" in dct:
            return Feature(
                id=dct["id"],
                version=dct["version"],
                requirements=cls.decode_requirement_refs(dct.get("requirements")),
                dependencies=cls.decode_feature_refs(dct.get("dependencies")),
                path=Metadata(path=path_val).path if (path_val := dct.get("path")) else "",
            )
        return dct

    @classmethod
    def decode_id_versions(cls, id_versions):
        if id_versions is None:
            return []
        return [cls.decode_id_version(id_version) for id_version in id_versions]

    @classmethod
    def decode_requirement_refs(cls, id_versions):
        return [
            RequirementRef(id_version.id, str(id_version.version) if id_version.version is not None else None)
            for id_version in cls.decode_id_versions(id_versions)
        ]

    @classmethod
    def decode_feature_refs(cls, id_versions):
        return [
            FeatureRef(id_version.id, str(id_version.version) if id_version.version is not None else None)
            for id_version in cls.decode_id_versions(id_versions)
        ]

    @classmethod
    def decode_id_version(cls, id_version):
        if id_version is None:
            return None
        elif isinstance(id_version, str):
            return IdVersion.parse(id_version)
        elif isinstance(id_version, dict):
            if len(id_version) != 1:
                raise ValueError(f"Expected exactly one id per versioned reference, got: {list(id_version.keys())}")
            identifier, attrs = next(iter(id_version.items()))
            version = attrs.get("version") if isinstance(attrs, dict) else None
            return IdVersion(identifier, Version(version) if version is not None else None)
        else:
            raise ValueError(f"Expected a string or single-key dict versioned reference, got: {id_version!r}")


@dataclass
class JsonFeaturesParser:
    """
    JSON parser for all features in the root directory.

    Args:
        root_dir: Sphinx srcdir.
        path: The path to the features directory.
    """

    root_dir: str
    path: str

    def parse(self) -> list[Feature]:
        """
        Parse all feature JSON files from the root directory.
        """
        features: list[Feature] = []
        for filename in sorted(os.listdir(self.path)):
            if not filename.endswith(".json"):
                continue
            filepath = os.path.join(self.path, filename)
            with open(filepath, encoding="utf-8") as f:
                feature = json.load(f, cls=_FeatureDeserialize)
            if isinstance(feature, Feature):
                if not feature.path:
                    feature = replace(feature, path=Metadata(path=os.path.relpath(filepath, self.root_dir)).path)
                features.append(feature)
        return features
