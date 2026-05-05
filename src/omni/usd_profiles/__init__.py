# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

from pkgutil import extend_path

import nvidia_usd_profiles
from nvidia_usd_profiles import __version__

__path__ = extend_path(__path__, __name__)

__all__ = ["__version__"]
