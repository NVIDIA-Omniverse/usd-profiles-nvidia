# Changelog

## [1.15.0] - 11/05/2026
### Added
- AI-agent guidance and a project setup skill for Python code generation workflows.
- Minimal runnable Python code generation example covering requirements, capabilities, features, and profiles.

### Changed
- Documented core package requirements and optional Sphinx integration dependencies.

## [1.14.1] - 06/05/2026
### Fixed
- Update project name.

## [1.14.0] - 05/05/2026
### Added
- `omni.usd_profiles` compatibility shims for the renamed `usd_profiles_nvidia` Python namespace.

## [1.13.1] - 28/04/2026
### Removed
- `setup_repo_tool` / `run_repo_tool` from `codegen` — repo-tool infrastructure not applicable to this pip package.

## [1.13.0] - 23/04/2026
### Added
- Support for `com.nvidia.*` reverse-domain naming convention in codegen (`--reverse-domain`).

## [1.12.0] - 22/04/2026
### Added
- TOML-based profile parser (`omni.usd_profiles.toml`) for multi-version profiles.

## [1.11.2] - 03/03/2026
### Added
- `MultiFeatureParser` for feature documents with multi-version segments.
- `FeaturesParser` tries `MultiFeatureParser` when `FeatureParser` raises.
### Changed
- `RequirementsParser` logs a warning instead of raising on parse failure.
- Feature `internal_id` property simplified.

## [1.11.1] - 27/02/2026
### Changed
- `Capabilities` Add default version.

## [1.11.0] - 17/02/2026
### Added
- `Feature` supports inheritance via extends field.
- `FeatureParser` uses ReferenceParser for requirement references.
- `Model` base class for capability, feature, profile, requirement.
### Changed
- Improved Jinja2 environment reuse.
- Improved parsing phases during Sphinx documentation build.
- Requirement unused attributes removed.
- Improved documentation.
### Fixed
- Inconsistent root dir handling.

## [1.10.22] - 09/02/2026
### Changed
- Enable public releases

## [1.10.21] - 02/02/2026
### Fixed
- Fix release

## [1.10.20] - 02/02/2026
### Fixed
- Improved PythonGenerator performance

## [1.10.19] - 30/01/2026
### Fixed
- Fixed PythonGenerator dependency

## [1.10.18] - 30/01/2026
### Fixed
- Rename internal function get_sphinx_path to validate_repo_dependencies

## [1.10.17] - 30/01/2026
### Fixed
- Fixed repeated enum element

## [1.10.16] - 29/01/2026
### Added
- Add PythonGenerator to omni.usd_profiles.codegen

## [1.10.15] - 27/01/2026
### Changed
- Updated README.md

## [1.10.14] - 26/01/2026
### Changed
- Updated documentation about licenses

## [1.10.13] - 26/01/2026
### Changed
- Create reference parser, to handle references to requirements.

## [1.10.12] - 22/01/2026
### Fixed
- Relax conditions for overview.

## [1.10.11] - 22/01/2026
### Added
- Added protocols for requirements, capabilities, features and profiles.

## [1.10.10] - 20/01/2026
### Changed
- Fix version

## [1.10.9] - 20/01/2026
### Changed
- Fix CI/CD

## [1.10.8] - 20/01/2026
### Changed
- Add CI/CD to publish internally.

## [1.10.7] - 20/01/2026
### Changed
- requirements-table now registers requirements as included documents

## [1.10.6] - 16/01/2026
### Changed
- Add a common single file parser
### Fixed
- requirements-table did not work if included from a different document

## [1.10.5] - 16/01/2026
### Added
- requirements-table directive accepts configuration files.

## [1.10.4] - 15/01/2026
### Fixed
- features-table do not depends on JSON files.

## [1.10.3] - 15/01/2026
### Fixed
- Fix features-table and requirements-table sphinx directives.

## [1.10.2] - 14/01/2026
### Added
- Introduce Compatibility enumeration for better parsing.

## [1.10.1] - 14/01/2026
### Added
- Introduce Tag enumeration for better parsing.

## [1.10.0] - 14/01/2026
### Added
- Added `validator-link` and `validator-latest-link` roles.

## [1.9.3] - 08/01/2026
### Removed
- Removed unused Sphinx runner.

## [1.9.2] - 08/01/2026
### Changed
- `PersistentVersionedRegistry` and `SpecificationsStore` now accept either a directory path or objects directly.
- Refactored `_build_jsons.py` to use `SpecificationsParser`.

## [1.9.1] - 06/01/2026
### Changed
- Code generation partitions examples into subdirectories for improved scalability.

## [1.9.0] - 05/01/2026
### Added
- Python generator: Added support for multiple versions, backward support for no versions.

## [1.8.1] - 19/12/2025
### Fixed
- Add back missing capabilities field.

## [1.8.0] - 19/12/2025
### Added
- Support for Profile parsing, serialization and generation.

## [1.7.2] - 17/12/2025
### Changed
- Support id version for feature requirements.

## [1.7.1] - 17/12/2025
### Changed
- Support version object internally.

## [1.7.0] - 16/12/2025
### Changed
- Add SphinxDirectiveBlock in markdown parsers
- Features can now read requirements from requirements options

## [1.6.19] - 16/12/2025
### Fixed
- Fix feature-table directive bug.

## [1.6.18] - 15/12/2025
### Changed
- It is possible to have exactly two examples.
- Add efficient and inefficeint for example parsing.

## [1.6.17] - 05/12/2025
### Changed
- Relax conditions for examples
- Relax conditions for capabilities
- Missing utf-8 encoding when opening files

## [1.6.16] - 14/11/2025
### Changed
- Add comprehensive documentation and examples

## [1.6.15] - 11/11/2025
### Fixed
- Add frozen=True to examples

## [1.6.14] - 07/11/2025
### Changed
- Content filename name is shorter.

## [1.6.13] - 07/11/2025
### Changed
- ExampleSnippet.content is now lazy loaded.

## [1.6.12] - 06/11/2025
### Added
- Add `destination_dir` option for code generation.

## [1.6.11] - 17/10/2025
### Fixed
- Example change name to display_name to avoid confusion with enums.

## [1.6.10] - 17/10/2025
### Fixed
- Added enum_name to Parameter and changed templates to ensure proper Python naming

## [1.6.9] - 16/10/2025
### Changed
- Added parameters to the _capabilities.py codegen template.
- Renamed Parameter.name to Parameter.display_name
- Renamed Parameter.default_value to Parameter.assigned_value.
- Added Enum as a parent class to Parameters to match Requirements.

## [1.6.8] - 15/10/2025
### Changed
- Generation of examples uses more patterns to match
- Asserts no example names have been duplicated.

## [1.6.7] - 15/10/2025
### Added
- Generation of examples

## [1.6.6] - 14/10/2025
### Changed
- Improve feature parsing.

## [1.6.5] - 09/10/2025
### Added
- Float parameter type support

## [1.6.4] - 08/10/2025
### Added
- Parameters enum class in generated Python code
  - Generated code now includes a `Parameters` enum with all unique parameter definitions
  - Requirements reference parameters via `Parameters.PARAMETER_NAME` instead of inlining
  - Automatic parameter deduplication for parameters with identical definitions
  - Added comprehensive unit tests for parameter generation and reuse
  - Updated documentation with usage examples and code generation details

## [1.6.3] - 08/10/2025
### Changed
- Enum syntax now requires quoted string values: `enum("X", "Y", "Z")` instead of `enum(X, Y, Z)`
  - Allows for future support of integer enumerations
  - Flexible whitespace handling around parentheses

## [1.6.2] - 07/10/2025
### Added
- Parameter support for requirements
  - Support for int, bool, and enum parameter types with validation
  - Parameters table parsing from markdown specifications
  - JSON serialization/deserialization support
  - Code generation with proper single-element tuple handling
  - Default value validation (enum values, int numeric strings, bool true/false)
  - Comprehensive documentation in docs/PARAMETERS.md

## [1.6.1] - 01/10/2025
### Changed
- Fixed a bug where version was ignored

## [1.6.0] - 30/09/2025
### Added
- Added version to requirements

## [1.5.2] - 18/09/2025
### Changed
- Use single ext in templates/repo.toml

## [1.5.1] - 18/09/2025
### Added
- Use single ext in conf.py

## [1.5.0] - 18/09/2025
### Added
- Added `static` Sphinx extension.

## [1.4.0] - 17/09/2025
### Added
- Added `features-table` directive

## [1.3.0] - 17/09/2025
### Added
- Added `requirements-table` directive

## [1.2.1] - 12/09/2025
### Fixed
- Update code for repo_profiles_codegen

## [1.2.0] - 10/09/2025
### Added
- First prototype for Sphinx parser

## [1.1.1] - 10/09/2025
### Fixed
- Hide import within function

## [1.1.0] - 10/09/2025
### Added
- Added pyproject and requirements
- Added repo_profiles_codegen

## [1.0.1] - 10/09/2025
### Added
- Templates to use in external projects.

## [1.0.0] - 10/09/2025
### Added
- Initial project structure for Omniverse OpenUSD Profiles.
- KeyStore class for managing key-value pairs loaded from JSON files.
- Basic repo configuration, formatting, linting, testing, packaging, and documentation setup.

### Changed
- None.

### Fixed
- None.
