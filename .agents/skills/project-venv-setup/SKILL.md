---
name: project-venv-setup
version: "1.15.0"
license: Apache-2.0
description: "Set up a local Python venv for usd-profiles-nvidia: build/install the wheel, run tests, or smoke test usd_profiles_nvidia.codegen. Do NOT use for profile spec authoring."
metadata:
  author: NVIDIA
  tags:
    - usd-profiles-nvidia
    - venv
    - build
    - codegen
compatibility: "Requires Python 3.10-3.12, pip and venv, network access to Python package indexes, and Linux/macOS shell or Windows PowerShell command syntax."
---

<!-- SPDX-FileCopyrightText: Copyright (c) 2024-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Project Virtual Environment Setup

## Purpose

`usd-profiles-nvidia` can be built, installed, and tested from a plain Python virtual environment. Use this skill when a
task needs clean virtual environment setup, wheel build/install verification, test execution from an installed package,
or a quick `usd_profiles_nvidia.codegen` smoke test.

## Prerequisites

- Python 3.10-3.12.
- `pip`, `venv`, and package-index access.

## Project Structure

```text
usd-profiles-nvidia/
  .venv/
  dist/
  examples/python/minimal/
  src/
  tests/
```

Run these commands from the repository root. Do not commit `.venv/`, `dist/`, `_build/`, or other generated package
artifacts.

## Setup with venv

```bash
python3.11 -m venv .venv  # use python3.10 or python3.12 if 3.11 is not installed
source .venv/bin/activate
python -m pip install --upgrade pip build
python -m pip install "sphinx>=7.2.6" "myst-parser>=4.0.0"
```

On Windows:

```powershell
py -3.11 -m venv .venv  # use -3.10 or -3.12 if 3.11 is not installed
./.venv/Scripts/Activate.ps1
python -m pip install --upgrade pip build
python -m pip install "sphinx>=7.2.6" "myst-parser>=4.0.0"
```

This installs only build tooling and optional Sphinx test dependencies. Keep the package itself out of the virtual
environment until the built wheel is installed.

## Build from Source

Build the wheel into `dist/`:

```bash
python -m build --wheel --outdir dist
```

The package uses a `src/` layout and includes both the current `usd_profiles_nvidia` package and the compatibility
`omni.usd_profiles` import package.

## Install Built Wheel

Install the newest built wheel into the activated virtual environment:

```bash
wheel=$(ls -t dist/usd_profiles_nvidia-*.whl | head -n 1)
python -m pip install --force-reinstall "$wheel"
```

On Windows:

```powershell
$wheel = (
  Get-ChildItem ./dist/usd_profiles_nvidia-*.whl |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1
).FullName
python -m pip install --force-reinstall $wheel
```

## Run

After installing the built wheel, run the unit tests from the activated virtual environment:

```bash
python -m unittest discover -s tests
```

On Windows:

```powershell
python -m unittest discover -s tests
```

Smoke test code generation with the minimal example:

```bash
python -m usd_profiles_nvidia.codegen \
  --docs-root examples/python/minimal/specs \
  --destination-dir _build/minimal \
  --package-name example_profiles
```

On Windows:

```powershell
python -m usd_profiles_nvidia.codegen `
  --docs-root examples/python/minimal/specs `
  --destination-dir _build/minimal `
  --package-name example_profiles
```

Generated files should appear under `_build/minimal/example_profiles`.

For fast iterative source-tree development instead of wheel verification, install the source tree in editable mode:

```bash
python -m pip install -e .
```

Install optional Sphinx dependencies only when working on documentation rendering, directives, roles, or Sphinx
compatibility:

```bash
python -m pip install -e ".[sphinx]"
```

## Key Types / Functions

- `python -m venv .venv`: creates the local virtual environment.
- `python -m build --wheel --outdir dist`: builds a wheel from the source tree.
- `python -m pip install --force-reinstall "$wheel"`: installs the built wheel into the virtual environment.
- `python -m unittest discover -s tests`: runs the repository test suite.
- `python -m usd_profiles_nvidia.codegen`: generates Python enums and dataclasses from profile specs.
- `python -m omni.usd_profiles.codegen`: compatibility import path for legacy downstream consumers.
- `python -m pip install -e .`: optional editable source-tree install for iterative development.

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `build` | PEP 517 wheel build frontend for source builds inside the venv |
| `jinja2` | Templates for generated Python package files |
| `markdown-it-py` | Parses Markdown profile specs |
| `tomli` | Reads TOML profile files on Python versions earlier than 3.11 |
| `sphinx` | Optional Sphinx runtime used by directive tests |
| `myst-parser` | Optional MyST Markdown parser used by Sphinx tests |

## Limitations

- Covers local venv and wheel verification only; use `project-setup-python` for profile spec authoring.
- Does not publish packages or configure external CI.

## Common Pitfalls

- Use Python 3.10 or later; the examples above prefer Python 3.11.
- Activate the virtual environment before installing build tools, the built wheel, or test dependencies.
- Install optional Sphinx dependencies during venv setup before running the full test suite.
- Install the built wheel before running package smoke tests in a clean venv.
- Use `--package-name` for new codegen examples; `--namespace` remains available for compatibility but is deprecated.
- Keep `profiles.toml.example` as documentation-only unless TOML profiles should replace Markdown profile parsing.
- Reinstall the wheel after rebuilding, otherwise smoke tests may still exercise a previous local build.
- Leave generated `_build/`, `.venv/`, and `dist/` contents out of commits.

## Troubleshooting

- If `python -m build` is missing, install or upgrade the `build` package in the active virtual environment.
- If build, test, or codegen validation errors still show old behavior after rebuilding, reinstall the newest wheel from
  `dist/`.
