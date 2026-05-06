# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import logging
from collections.abc import Iterator

from usd_profiles_nvidia.model import Parameter

logger = logging.getLogger(__name__)


class ParameterStore:
    """
    A store of unique parameters extracted from requirements.

    This store validates parameter consistency: parameters with the same name
    must have identical type, assigned value, and enum values.

    Args:
        requirements: An iterable of requirements to extract parameters from.

    Raises:
        ValueError: If parameters with the same name have conflicting definitions.
    """

    def __init__(self, requirements) -> None:
        self._parameters: list[Parameter] = []
        self._param_by_name: dict[str, Parameter] = {}

        # Extract and validate parameters from all requirements
        for requirement in requirements:
            for param in requirement.parameters:
                if param.display_name in self._param_by_name:
                    existing = self._param_by_name[param.display_name]
                    # Check if all properties match
                    if (
                        existing.type != param.type
                        or existing.assigned_value != param.assigned_value
                        or existing.enum_values != param.enum_values
                    ):
                        raise ValueError(
                            f"Parameter '{param.display_name}' has conflicting definitions:\n"
                            f"  First definition: type={existing.type.name}, assigned={existing.assigned_value}, "
                            f"enum_values={existing.enum_values}\n"
                            f"  Conflicting definition: type={param.type.name}, assigned={param.assigned_value}, "
                            f"enum_values={param.enum_values}\n"
                            f"Parameters with the same name must have identical type, assigned value, and enum values."
                        )
                else:
                    # New unique parameter
                    self._param_by_name[param.display_name] = param
                    self._parameters.append(param)

    def __iter__(self) -> Iterator[Parameter]:
        """Iterate over all unique parameters in sorted order (by name)."""
        return iter(sorted(self._parameters, key=lambda p: p.display_name))

    def __len__(self) -> int:
        """Return the number of unique parameters."""
        return len(self._parameters)

    def __contains__(self, name: str) -> bool:
        """Check if a parameter with the given name exists."""
        return name in self._param_by_name

    def get(self, name: str) -> Parameter | None:
        """Get a parameter by name, or None if not found."""
        return self._param_by_name.get(name)
