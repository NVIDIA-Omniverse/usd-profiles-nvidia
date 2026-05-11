---
# SPDX-FileCopyrightText: Copyright (c) 2024-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
---

# usd-profiles-nvidia Skills Directory

This directory contains structured skill files for AI coding agents working on the usd-profiles-nvidia codebase. Each
skill is a self-contained reference for a specific usd-profiles-nvidia task and points to runnable examples when
possible.

## Structure

Each subdirectory contains a single `SKILLS.md` file with YAML frontmatter:

    skills/
      project-setup-python/SKILLS.md

## SKILLS.md Format

    ---
    name: skill-name
    description: What this skill covers. Use when user asks to [trigger phrases].
    ---

    # Skill Title

    ## Overview
    Brief explanation of when/why you'd use this.

    ## Project Structure
    Minimal file layout for the workflow.

    ## Setup
    Environment setup with uv and pip.

    ## Minimal Example
    References to live example files instead of long inline blocks.

    ## Run
    Commands that exercise the workflow.

    ## Key Dependencies
    Quick reference of the packages involved.

    ## Common Pitfalls
    Gotchas and things to watch out for.

## Example References

Skills reference files in `examples/` instead of duplicating longer snippets inline. This keeps examples accurate as
the API evolves.

### Reference format in SKILLS.md

    > Source: `examples/python/minimal/specs/features/feature-example.md`

Agents should read the referenced file directly when they need the current example content.

## Adding a New Skill

1. Create a new directory under `skills/` named after the skill using kebab-case.
2. Add a `SKILLS.md` file inside it following the format above.
3. Prefer runnable examples under `examples/` and reference them from the skill.
4. Keep each skill focused on one workflow.

## Updating Skills

When you change codegen behavior, example specs, or command-line options that affect an existing skill, update the
corresponding `SKILLS.md` to keep it accurate.
