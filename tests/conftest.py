# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

from nvidia_usd_profiles import validate_repo_dependencies


def pytest_configure(config):
    """
    Configure pytest.
    """
    validate_repo_dependencies()
