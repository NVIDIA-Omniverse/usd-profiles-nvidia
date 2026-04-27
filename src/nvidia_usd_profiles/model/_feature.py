# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

from dataclasses import dataclass, field

from ._model import Model
from ._version import IdVersion


@dataclass(slots=True)
class Feature(Model):
    """
    Represents a feature of a capability.

    Args:
        requirements (list[IdVersion]): The requirements of the feature.
        dependency (str): The dependency of the feature.
        extends (IdVersion | None): The feature this feature extends, if any.
    """

    requirements: list[IdVersion] = field(default_factory=list)
    dependency: str | None = None
    extends: IdVersion | None = None
