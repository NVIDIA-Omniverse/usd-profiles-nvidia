# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

from dataclasses import dataclass, field

from ._model import Model
from ._version import IdVersion


@dataclass(slots=True)
class Profile(Model):
    """
    Represents a profile.

    Args:
        features (list[IdVersion]): The features of the profile.
    """

    features: list[IdVersion] = field(default_factory=list)
