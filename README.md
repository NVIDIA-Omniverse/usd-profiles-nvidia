# NVIDIA USD Profiles

A framework for defining and managing [OpenUSD](https://openusd.org) asset profiles, capabilities, and requirements.
This library provides tools for parsing profile specifications from Markdown, generating Python code,
and integrating with Sphinx documentation.

## Features

- **Profile definitions** — Define capabilities, features, and requirements in structured Markdown
- **Code generation** — Generate Python enums and dataclasses from profile specifications
- **Sphinx integration** — Custom directives and roles for rendering profile documentation
- **Validation support** — Generate validation rules from requirement specifications
- **Extensible** — Modular architecture for custom profile components

## Installation

Install from PyPI:

```bash
pip install nvidia-usd-profiles
```

For Sphinx integration (directives and roles for profile documentation), install the optional dependency:

```bash
pip install nvidia-usd-profiles[sphinx]
```

## Basic Usage

### Code Generation

Generate Python code from profile specifications. Create a folder (e.g. `specs/`) with this structure and the following files:

```
specs/
├── capabilities/
│   ├── capability-example.md
│   └── requirements/
│       └── single-root.md
├── features/
│   └── feature-example.md
└── profiles/
    └── profile-example.md
```

**specs/capabilities/requirements/single-root.md**

```markdown
# single-root

| Code          | REQ.001                   |
|---------------|---------------------------|
| Version       | 1.0.0                     |
| Compatibility | {compatibility}`OpenUSD`   |
| Validator     |                           |
| Tags          | {tag}`essential`          |

## Summary

USD stage must have a single root prim.

## Description

Every USD asset must contain one root prim from which all other prims descend.
```

**specs/capabilities/capability-example.md**

~~~markdown
# Example

## Overview

Minimal capability with one requirement.

## Requirements

```{requirements-table}
```
~~~

**specs/features/feature-example.md**

~~~markdown
# Example

| Property   | Value   |
|------------|---------|
| Version    | 1.0.0   |
| Dependency | OpenUSD |

## Description

Minimal feature with one requirement.

## Requirements

```{features-table}
REQ.001@1.0.0
```
~~~

**specs/profiles/profile-example.md**

```markdown
# Example

Minimal profile with one feature.

## Features

- [Example](../features/feature-example.md)
```

Then run:

```bash
python -m nvidia_usd_profiles.codegen --docs-root specs --destination-dir output --namespace mypackage.profiles
```

Generated code will be under `output/mypackage/profiles/`.

### NVIDIA USD Validation integration

Use the generated requirements and features with [NVIDIA USD Validation](https://pypi.org/project/nvidia-usd-validation/) to implement rule checkers and run validation.

**Implement a rule** — Register requirements and implement checks (e.g. for the minimal example's single-root requirement):

```python
import mypackage.profiles as cap
from nvidia_usd_validation import BaseRuleChecker, register_requirements

@register_requirements(cap.Requirements.REQ_001_V1_0_0)
class SingleRootChecker(BaseRuleChecker):
    """USD stage must have a single root prim."""

    def CheckStage(self, usdStage):
        roots = [p for p in usdStage.GetPseudoRoot().GetChildren() if p.IsValid()]
        if len(roots) != 1:
            self._AddFailedCheck(
                "Stage must have exactly one root prim.",
                requirement=cap.Requirements.REQ_001_V1_0_0,
            )
```

**Validate with the generated feature** — Enable the feature you generated and run the engine:

```python
import nvidia_usd_validation
import mypackage.profiles

engine = nvidia_usd_validation.ValidationEngine(init_rules=False)
engine.enable_feature(mypackage.profiles.Features.EXAMPLE)
results = engine.validate("path/to/asset.usd")
```

### Sphinx Integration

Add to your Sphinx `conf.py`:

```python
extensions = [
    "nvidia_usd_profiles.sphinx.ext",
]
```

Use directives in your documentation:

````markdown
```{requirements-table}
geometry/mesh-valid
geometry/mesh-normals
```

```{features-table}
geometry/feature-mesh
```
````

Use roles for inline tags and compatibility badges:

```markdown
{tag}`performance` - Display a tag badge
{compatibility}`omniverse` - Display a compatibility badge
```

## Documentation

- [Full Documentation](https://docs.omniverse.nvidia.com/kit/docs/asset-requirements)

## Requirements

- Python 3.10 or later
- Jinja2 3.1.5 or later
- Sphinx 7.2.6 or later

## License

Apache-2.0
