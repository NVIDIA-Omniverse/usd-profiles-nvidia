# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import logging
import os
from dataclasses import dataclass

from usd_profiles_nvidia.model import (
    Compatibility,
    Example,
    Metadata,
    Requirement,
    Tag,
    Version,
)

from ._examples import ExamplesParser
from ._parameters import ParameterParser
from ._parser import FileParser, walk_md

logger = logging.getLogger(__name__)


class _RequirementParser(FileParser):

    def _parse_parameters(self, document) -> list:
        """
        Parse parameters from the document.

        Args:
            document: The parsed document.

        Returns:
            A list of Parameter objects.
        """
        # Check if there's a Parameters section
        parameters_section = document.sections[0].sections.get("parameters")
        if not parameters_section:
            return []

        # Delegate to ParameterParser
        parser = ParameterParser(parameters_section)
        return parser.parse()

    def _parse_examples(self, document) -> list[Example]:
        """
        Parse examples from the document.
        """
        examples_section = document.sections[0].sections.get("examples")
        if not examples_section:
            return []
        parser = ExamplesParser(examples_section)
        return parser.parse()

    def _parse_attributes(self, document) -> dict[str, str]:
        """
        Parse attributes from the document's first table.

        Returns:
            A dictionary of attribute key-value pairs.
        """
        data: dict[str, str] = self.main_table.to_dict()
        if "tags" in data:
            data["tags"] = Tag.from_role(data["tags"].strip())
        if "compatibility" in data:
            data["compatibility"] = Compatibility.from_role(data["compatibility"].strip())
        if "code" not in data:
            raise ValueError(f"Requirement {self.relpath} has no code.")
        return data

    def run(self) -> Requirement:
        """
        Parse the requirements from the source file.
        """

        document = self.document
        data = self._parse_attributes(document)
        parameters = self._parse_parameters(document)
        examples = self._parse_examples(document)

        return Requirement(
            code=data["code"],
            version=Version(data.get("version")) if data.get("version") else None,
            name=self.default_name,
            description=self.summary_content,
            compatibility=data.get("compatibility"),
            validator=data.get("validator"),
            tags=data.get("tags"),
            parameters=parameters,
            examples=examples,
            metadata=Metadata(path=self.relpath),
        )


@dataclass
class RequirementParser:
    """
    Parser for a single requirement.

    Args:
        root_dir: Sphinx srcdir.
        source_file: The file to parse requirements from.
    """

    root_dir: str
    source_file: str

    def parse(self) -> Requirement:
        """
        Parse the requirement from the source file. Raises an exception if the
        source file is not a valid requirement file.
        """
        logger.info(f"Parsing requirement from: {self.source_file}")
        return _RequirementParser(self.root_dir, self.source_file).run()


@dataclass
class RequirementsParser:
    """
    Parser for requirements.

    Args:
        root_dir: Sphinx srcdir.
        paths: The paths to parse requirements from.
    """

    root_dir: str
    paths: list[str]

    def parse(self) -> list[Requirement]:
        """
        Parse all requirements from the given paths.
        """
        for path in self.paths:
            if not os.path.exists(path):
                raise ValueError(f"Requirement path {path} does not exist.")

        requirements: list[Requirement] = []
        for source_path in walk_md(self.paths):
            try:
                if requirement := RequirementParser(self.root_dir, source_path).parse():
                    requirements.append(requirement)
            except ValueError as e:
                logger.warning(f"Failed to parse requirement from {source_path}: {e}")
                continue
        return requirements
