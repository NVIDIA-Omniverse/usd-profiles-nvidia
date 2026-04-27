# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import logging

from nvidia_usd_profiles.markdown import SpecificationsParser
from nvidia_usd_profiles.model import Specifications
from nvidia_usd_profiles.store import RequirementStore

logger = logging.getLogger(__name__)


def parse_specifications(app) -> None:
    """
    Parse the requirements from the specifications and store them in the environment.
    """
    specifications: Specifications = SpecificationsParser(root_dir=app.srcdir).parse()
    app.env.specifications = specifications

    requirement_store: RequirementStore = RequirementStore(specifications.requirements)
    app.env.requirement_store = requirement_store


def setup(app) -> dict[str, bool]:
    """
    Setup the Sphinx extension to build specifications.
    """
    app.connect("builder-inited", parse_specifications)
    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
