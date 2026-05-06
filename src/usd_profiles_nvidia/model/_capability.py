# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import os
from dataclasses import dataclass, field

from ._model import Model
from ._requirement import Requirement


def get_capability_name(capability_file: str) -> str:
    """
    Extract the capability name from a file path.
    Assumes the file is in the format: /CAPABILITY_NAME/capability-CAPABILITY_NAME.md
    """
    base_name = os.path.basename(os.path.dirname(capability_file))

    return base_name


@dataclass(slots=True)
class Capability(Model):
    """
    Represents a capability.

    Args:
        requirements (list[Requirement]): The requirements of the capability.
    """

    requirements: list[Requirement] = field(default_factory=list)

    @property
    def source_file_name(self) -> str:
        return get_capability_name(self.metadata.path)
