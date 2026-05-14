# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from functools import cache

from usd_profiles_nvidia.markdown import SpecificationsParser
from usd_profiles_nvidia.model import Specifications
from usd_profiles_nvidia.store import SpecificationsStore


@cache
def get_environment():
    """Load the Jinja2 environment.

    Jinja2 is imported lazily because this module is loaded by the repo tool
    runner whose Python environment may not have jinja2 installed.
    """
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    resources_dir: str = os.path.join(os.path.dirname(__file__), "resources")
    loader: FileSystemLoader = FileSystemLoader(resources_dir)
    return Environment(loader=loader, autoescape=select_autoescape(["html", "xml"]))


@dataclass(kw_only=True)
class PythonGenerator:
    """
    Python code generator for USD Profiles.

    Args:
        docs_root: Root directory containing capabilities/, profiles/, and features/ subdirectories.
                   If provided, capabilities_root, profiles_root, and features_root are derived from it.
        capabilities_root: Directory containing capability files.
        profiles_root: Directory containing profile files.
        features_root: Directory containing feature files.
        destination_dir: Output directory for generated Python code.
        package_name: Python package path for generated modules (e.g. ``"omni.profiles"`` → ``omni/profiles/``).
        reverse_domain: Reverse-domain prefix for spec identifiers (e.g. ``"com.nvidia.simready"``). Empty means legacy behavior.
    """

    docs_root: str | None = None
    capabilities_root: str | None = None
    profiles_root: str | None = None
    features_root: str | None = None
    destination_dir: str
    package_name: str
    reverse_domain: str = ""

    def __post_init__(self) -> None:
        os.makedirs(self.python_output_dir, exist_ok=True)

    @property
    def python_output_dir(self) -> str:
        return os.path.join(self.destination_dir, self.package_name.replace(".", os.path.sep))

    @classmethod
    def _render_template(cls, template_name: str, **kwargs) -> str:
        """
        Render a template with the given arguments.

        Args:
            template_name: Name of the template file (without .jinja2 extension)
            **kwargs: Template variables to pass to the template

        Returns:
            The rendered template content as a string
        """
        template = get_environment().get_template(f"{template_name}.jinja2")
        return template.render(**kwargs)

    def _generate_module(
        self,
        name: str,
        store: SpecificationsStore,
    ) -> None:
        destination_file: str = os.path.join(self.python_output_dir, f"{name}.py")
        content = self._render_template(
            f"{name}.py",
            name=name,
            capabilities=store.capabilities,
            profiles=store.profiles,
            requirements=store.requirements,
            features=store.features,
            parameters=store.parameters,
            examples=store.examples,
        )
        with open(destination_file, "w", encoding="utf-8") as destination_fptr:
            destination_fptr.write(content)

    def _generate_protocols(self) -> None:
        source_file: str = os.path.join(os.path.dirname(__file__), "resources", "_protocols.py")
        with open(source_file, encoding="utf-8") as source_fptr:
            content = source_fptr.read()

        destination_file: str = os.path.join(self.python_output_dir, "_protocols.py")
        with open(destination_file, "w", encoding="utf-8") as destination_fptr:
            destination_fptr.write(content)

    def _generate_example_files(self, store: SpecificationsStore) -> None:
        examples_dir: str = os.path.join(self.python_output_dir, "resources", "examples")
        shutil.rmtree(examples_dir, ignore_errors=True)
        os.makedirs(examples_dir, exist_ok=True)

        for partition, example in store.examples.partition():
            filename: str = example.snippet.filename
            filepath: str = os.path.join(examples_dir, partition, filename)
            os.makedirs(os.path.join(examples_dir, partition), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(example.snippet.content)

    def generate(self) -> None:
        specifications: Specifications = SpecificationsParser(
            root_dir=self.docs_root,
            capabilities_root=self.capabilities_root,
            profiles_root=self.profiles_root,
            features_root=self.features_root,
            reverse_domain=self.reverse_domain,
        ).parse()
        store: SpecificationsStore = SpecificationsStore(specifications)

        self._generate_module("__init__", store)
        self._generate_module("_parameters", store)
        self._generate_module("_requirements", store)
        self._generate_module("_capabilities", store)
        self._generate_module("_profiles", store)
        self._generate_module("_features", store)
        self._generate_module("_examples", store)
        self._generate_protocols()
        self._generate_example_files(store)
