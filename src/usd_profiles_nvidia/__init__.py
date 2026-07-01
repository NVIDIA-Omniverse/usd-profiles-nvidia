# SPDX-FileCopyrightText: Copyright (c) 2024-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from importlib.metadata import version

from usd_profiles_nvidia.graph import CapabilityGraph

__version__ = version("usd-profiles-nvidia")

__all__ = ["CapabilityGraph", "__version__"]
