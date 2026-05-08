# AGENTS.md - AI Agent Guide for usd-profiles-nvidia

This file gives AI coding agents the minimum context needed to work effectively in this repository. Use it as a starting map, then go to `skills/` for task-level implementation guidance.

## What This Repo Is

`usd-profiles-nvidia` is a Python package for defining OpenUSD profile specifications and generating Python code from them. It provides:

  * Markdown parsers for requirements, capabilities, features, and profiles (`src/usd_profiles_nvidia/markdown/`)
  * TOML profile parsing support (`src/usd_profiles_nvidia/toml/`)
  * Python enum/dataclass code generation (`src/usd_profiles_nvidia/codegen/`)
  * Optional Sphinx extensions for rendering profile documentation (`src/usd_profiles_nvidia/sphinx/`)

Primary use case: author structured profile specs, then generate importable Python enums for downstream tools.

## Start Here

  * Read `README.md` for package context, installation, and top-level examples.
  * Read `skills/README.md` to understand the skill format and maintenance expectations.
  * Use `skills/profile-codegen/SKILLS.md` for profile spec authoring and Python enum generation.
  * Use `examples/python/profile-codegen/` as the runnable minimal codegen reference.

## Repo Layout (High-Level)

  * `src/usd_profiles_nvidia/` - Current Python package source
  * `src/omni/usd_profiles/` - Compatibility import package
  * `tests/` - Unit tests and parser/codegen fixtures
  * `tests/resources/` - Minimal and edge-case spec fixtures
  * `examples/python/profile-codegen/` - Minimal runnable codegen example
  * `skills/` - Task-oriented AI agent skills (`*/SKILLS.md`)
  * `docs/` - Documentation support files

## Common Workflows

### Code Generation (uv)

  * Generate the minimal example:
    * `uv run --no-project --with . python -m usd_profiles_nvidia.codegen --docs-root examples/python/profile-codegen/specs --destination-dir _build/profile-codegen --package-name example_profiles`
  * Generated files appear under `_build/profile-codegen/example_profiles`.

### Tests

  * Tests live under `tests/`.
  * If working on parser or codegen behavior, run targeted tests first, then broader suites as needed.

## Use Skills for Task-Specific Work

When a request maps to a known usd-profiles-nvidia workflow, go directly to the relevant skill in `skills/`:

  * Profile spec authoring and Python enum codegen -> `skills/profile-codegen/SKILLS.md`

If you add a repeated workflow, add a matching skill under `skills/` and reference a runnable example where practical.

## Agent Expectations

  * Prefer small, targeted edits over broad refactors unless requested.
  * Keep examples, skills, and CLI option names in sync with code behavior.
  * Keep runnable examples under `examples/` and have skills point to those files.
  * Use `--package-name` for codegen examples; the older namespace option is deprecated.
  * Mention `usd-profiles-nvidia[sphinx]` only for optional Sphinx documentation integration, not as a codegen requirement.
  * Preserve licensing headers and proprietary notices where present.
  * Do not commit generated `_build/`, local virtual environments, or package caches.
  * Keep profile codegen guidance focused on usd-profiles-nvidia. Runtime validation integration belongs in downstream documentation.

## Notes

  * `profiles.toml` is authoritative when present in a profiles directory; use `profiles.toml.example` for documentation-only examples that should not affect Markdown profile parsing.
  * The package includes compatibility imports under `omni.usd_profiles`; prefer `usd_profiles_nvidia` for new examples.
  * Sphinx support is optional and separate from the core codegen flow.
