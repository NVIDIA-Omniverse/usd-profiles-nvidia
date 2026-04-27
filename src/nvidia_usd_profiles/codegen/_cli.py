# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import annotations

from argparse import ArgumentParser
from collections.abc import Callable
from typing import Any


def add_arguments(parser: ArgumentParser, required: bool = True) -> None:
    """Add codegen arguments to an argument parser."""
    parser.add_argument(
        "-f",
        "--docs-root",
        dest="docs_root",
        required=required,
        help="Where to find profiles markdown files, i.e. docs/.",
    )
    parser.add_argument(
        "-d",
        "--destination-dir",
        dest="destination_dir",
        required=required,
        help="Destination dir for the generated code, i.e. python/.",
    )
    parser.add_argument(
        "-p",
        "--package-name",
        dest="package_name",
        required=False,
        help="Python package path for generated modules, e.g. omni.profiles.",
    )
    parser.add_argument(
        "-r",
        "--reverse-domain",
        dest="reverse_domain",
        required=False,
        default="",
        help=("Reverse-domain prefix for spec identifiers, e.g. com.nvidia.simready. Empty means legacy behavior."),
    )
    # Deprecated: use --package-name and --reverse-domain instead.
    parser.add_argument(
        "-n",
        "--namespace",
        dest="namespace",
        required=False,
        help="Deprecated: use --package-name and --reverse-domain instead.",
    )


def generate(docs_root: str, destination_dir: str, package_name: str, reverse_domain: str = "") -> None:
    """Generate Python code from Profiles Markdown files."""
    from nvidia_usd_profiles.codegen._py_generate import PythonGenerator

    generator = PythonGenerator(
        docs_root=docs_root,
        destination_dir=destination_dir,
        package_name=package_name,
        reverse_domain=reverse_domain,
    )
    generator.generate()


def run_repo_tool(options: Any, config: dict[str, Any]) -> None:
    """
    Run repo tool.

    Args:
        options: Options.
        config: Config.
    """
    python_config: dict[str, Any] = config.get("repo_profiles_codegen", {}).get("python", {})
    docs_root: str = options.docs_root or python_config.get("docs_root", "")
    destination_dir: str = options.destination_dir or python_config.get("destination_dir", "")

    # Resolve package_name and reverse_domain, with --namespace as deprecated fallback.
    namespace: str = getattr(options, "namespace", None) or python_config.get("namespace", "")
    package_name: str = getattr(options, "package_name", None) or python_config.get("package_name", "") or namespace
    reverse_domain: str = getattr(options, "reverse_domain", None) or python_config.get("reverse_domain", "")

    from nvidia_usd_profiles import validate_repo_dependencies

    validate_repo_dependencies()
    generate(docs_root, destination_dir, package_name, reverse_domain)


def setup_repo_tool(parser: ArgumentParser, config: dict[str, Any]) -> Callable[[Any, dict[str, Any]], None] | None:
    """
    Setup repo tool.
    """
    parser.description = "Generate Python from Profiles Markdown files."
    add_arguments(parser, required=False)

    tool_config = config.get("repo_profiles_codegen", {})
    if not tool_config.get("enabled", True):
        return None

    return run_repo_tool
