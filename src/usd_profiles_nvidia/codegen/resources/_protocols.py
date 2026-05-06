# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

from typing import Protocol, runtime_checkable

from ._examples import Example
from ._parameters import Parameter


@runtime_checkable
class RequirementProtocol(Protocol):
    """
    A protocol definition of requirement.

    Attributes:
        code: A unique identifier of the requirement
        display_name: The name of the requirement (optional)
        message: A basic description of the requirement (optional)
        path: Relative path in documentation (optional)
        tags: Tags of the requirement (optional)
        version: The version of the requirement
        parameters: The collection of parameters associated with the requirement (optional)
    """

    code: str
    version: str | None
    display_name: str | None
    message: str | None
    path: str | None
    compatibility: str | None
    tags: tuple[str, ...]
    parameters: tuple[Parameter, ...]
    examples: tuple[Example, ...]


@runtime_checkable
class CapabilityProtocol(Protocol):
    """
    A protocol definition of capability.

    Attributes:
        id: A unique identifier of the capability
        version: The version of the capability
        path: The path to the capability
        requirements: The requirements of the capability
    """

    id: str
    version: str
    path: str
    requirements: list[RequirementProtocol]


@runtime_checkable
class FeatureProtocol(Protocol):
    """
    A protocol definition of feature.

    Attributes:
        id: A unique identifier of the feature
        version: The version of the feature
        path: The path to the feature
        requirements: The requirements of the feature
    """

    id: str
    version: str
    path: str
    requirements: list[RequirementProtocol]


@runtime_checkable
class ProfileProtocol(Protocol):
    """
    A protocol definition of profile.

    Attributes:
        id: A unique identifier of the profile
        version: The version of the profile
        path: The path to the profile
        capabilities: The capabilities of the profile
    """

    id: str
    version: str
    path: str
    capabilities: list[CapabilityProtocol]
