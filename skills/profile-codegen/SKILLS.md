---
name: profile-codegen
description: Authoring usd-profiles-nvidia requirement, capability, feature, and profile specifications and generating Python enums. Use when user asks to create profile specs, generate Python enums with usd_profiles_nvidia.codegen, or scaffold a minimal profile codegen example.
---

# Profile Codegen

## Overview

usd-profiles-nvidia reads structured Markdown and TOML profile specs and generates a Python package with requirement, capability, feature, and profile enums. Use this skill for usd-profiles-nvidia code generation only; downstream integration belongs in a separate project.

## Project Structure

    examples/python/profile-codegen/
      pyproject.toml
      specs/
        capabilities/
          capability-example.md
          requirements/
            single-root.md
        features/
          feature-example.md
        profiles/
          profile-example.md
          profiles.toml.example

## Setup with uv (Recommended)

Use uv to run codegen without creating a local virtual environment:

    uv run \
      --no-project \
      --with . \
      python -m usd_profiles_nvidia.codegen --help

Note: `--with .` uses the local repo; remove it to use the public package.

The example project file lists the package dependency:

> Source: `examples/python/profile-codegen/pyproject.toml`

## Setup with pip

Install the codegen package into an environment you control:

    python -m pip install usd-profiles-nvidia

Then run `python -m usd_profiles_nvidia.codegen` with the same arguments shown below.

## Minimal specs / Minimal example

The example contains one requirement, one capability, one feature, and one profile.

> Source: `examples/python/profile-codegen/specs/capabilities/requirements/single-root.md`
>
> Source: `examples/python/profile-codegen/specs/capabilities/capability-example.md`
>
> Source: `examples/python/profile-codegen/specs/features/feature-example.md`
>
> Source: `examples/python/profile-codegen/specs/profiles/profile-example.md`
>
> Optional TOML profile format: `examples/python/profile-codegen/specs/profiles/profiles.toml.example`

## Run

From the repository root:

    uv run \
      --no-project \
      --with . \
      python -m usd_profiles_nvidia.codegen \
        --docs-root examples/python/profile-codegen/specs \
        --destination-dir _build/profile-codegen \
        --package-name example_profiles

Note: `--with .` uses the local repo; remove it to use the public package.

Generated files appear under `_build/profile-codegen/example_profiles`.

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `usd-profiles-nvidia` | Parses specs and generates Python enums |
| `uv` | Runs the package without a checked-in virtual environment |
| `usd-profiles-nvidia[sphinx]` | Optional Sphinx documentation integration; not required for codegen |

## Common Pitfalls

* Use `--package-name`; the older namespace option is deprecated.
* Keep `capabilities/`, `features/`, and `profiles/` under the docs root passed to codegen.
* Leave `profiles.toml.example` with the `.example` suffix unless you want TOML profiles to replace `profile-*.md` parsing.
* Match `features-table` entries to requirement codes and versions, such as `EX.001@1.0.0`.
* Keep this workflow focused on profile code generation.
