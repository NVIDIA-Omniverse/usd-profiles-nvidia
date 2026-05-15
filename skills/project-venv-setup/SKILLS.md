---
# SPDX-FileCopyrightText: Copyright (c) 2024-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
name: project-venv-setup
description: Creating a local Python venv for usd-profiles-nvidia, installing the package from source or a built wheel, building the project wheel, running unit tests, or smoke testing usd_profiles_nvidia.codegen from that environment.
---

# Project Virtual Environment Setup

## Overview

`usd-profiles-nvidia` can be built, installed, and tested from a plain Python virtual environment. Use this skill when a
task needs local package installation, wheel verification, test execution from an installed package, or a quick
`usd_profiles_nvidia.codegen` smoke test.

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
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip build
python -m pip install -e .
```

On Windows:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip build
python -m pip install -e .
```

Install the optional Sphinx dependencies only when working on documentation rendering, directives, roles, or Sphinx
compatibility:

```bash
python -m pip install -e ".[sphinx]"
```

On Windows:

```powershell
python -m pip install -e ".[sphinx]"
```

## Build from Source

Build the wheel into `dist/`:

```bash
python -m build --wheel --outdir dist
```

The package uses a `src/` layout and includes both the current `usd_profiles_nvidia` package and the compatibility
`omni.usd_profiles` import package.

## Run

Run the unit tests from the activated virtual environment:

```bash
python -m unittest discover -s tests
```

To test the built wheel instead of the editable source install, install the newest wheel from `dist/` and rerun tests:

```bash
wheel=$(ls -t dist/usd_profiles_nvidia-*.whl | head -n 1)
python -m pip install --force-reinstall "$wheel"
python -m unittest discover -s tests
```

On Windows:

```powershell
$wheel = (
  Get-ChildItem .\dist\usd_profiles_nvidia-*.whl |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1
).FullName
python -m pip install --force-reinstall $wheel
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

## Key Types / Functions

- `python -m venv .venv`: creates the local virtual environment.
- `python -m pip install -e .`: installs the source tree for iterative development.
- `python -m build --wheel --outdir dist`: builds a wheel from the source tree.
- `python -m unittest discover -s tests`: runs the repository test suite.
- `python -m usd_profiles_nvidia.codegen`: generates Python enums and dataclasses from profile specs.
- `python -m omni.usd_profiles.codegen`: compatibility import path for legacy downstream consumers.

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `build` | PEP 517 wheel build frontend for source builds inside the venv |
| `jinja2` | Templates generated Python package files |
| `markdown-it-py` | Parses Markdown profile specs |
| `tomli` | Reads TOML profile files on Python versions earlier than 3.11 |
| `usd-profiles-nvidia[sphinx]` | Optional Sphinx integration for documentation directives and roles |

## Common Pitfalls

- Use Python 3.10 or later; the examples above prefer Python 3.11.
- Activate the virtual environment before installing build tools, the package, or test dependencies.
- Use `--package-name` for new codegen examples; `--namespace` remains available for compatibility but is deprecated.
- Keep `profiles.toml.example` as documentation-only unless TOML profiles should replace Markdown profile parsing.
- Reinstall the wheel after rebuilding, otherwise smoke tests may still exercise a previous local build.
- Leave generated `_build/`, `.venv/`, and `dist/` contents out of commits.
