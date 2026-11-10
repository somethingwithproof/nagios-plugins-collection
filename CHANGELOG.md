<!--
SPDX-FileCopyrightText: 2025 Thomas Vincent
SPDX-License-Identifier: Apache-2.0
-->

# Changelog

## Unreleased

- Thresholds follow the Nagios Plugin Guidelines range format in one shared
  parser: `@a:b` now alerts when `a <= value <= b` (endpoints were excluded),
  `~:10` is accepted, a bare `10` means `0:10` so negative values alert, and a
  value inside a critical `@` range is CRITICAL even when the warning range is
  narrower. Malformed ranges, including a start above its end, return UNKNOWN.
  `check_prometheus_query` now uses these ranges instead of a plain upper bound
  that silently ignored malformed thresholds.
- Performance data uses one formatter: `'label'=value[UOM];warn;crit;min;max`.
  Labels with spaces, `=` or `'` are quoted, and non-numeric or non-finite
  values (for example CloudWatch `unit=Percent`, component `status=ok`, Hadoop
  memory text, `p95_ms=inf`) are no longer emitted as perfdata. CloudWatch
  values carry their unit as a UOM (for example `value=45.5%;70;90`) and Hadoop
  memory is `mem=<n>KB`. The status message is always one line, with `|`
  replaced by `/`. JSON output keeps plain metric values and writes `null`
  instead of the invalid `Infinity`.
- `check_monghealth` uses the shared result type, so its JSON output now
  includes `timestamp` and `details` like the other plugins.
- Make `uv.lock` the single dependency lock. Development tools moved from the
  `dev` and `security` extras to PEP 735 dependency groups; install them with
  `uv sync`. The runtime extras, including `prom` and `es`, are unchanged.
- Replace tox and the `packaging/*-requirements` files with `uv sync --locked`
  and `uv run`. The container image and native packages export hashed
  requirements from `uv.lock` at build time.

## 2.0.1 — 2026-10-06

- Align package metadata and SPDX headers with the existing Apache-2.0 LICENSE.
- Add file-level SPDX identifiers and REUSE mappings for non-commentable files.
- Parse shipping license expressions without regex backtracking.
- Supersede the unpublished 2.0.0 candidate after the license consistency audit.

## 2.0.0 — 2026-10-06 (unpublished candidate)

Verified TLS defaults, async cancellation ownership, maintained-platform policy and wheel/Helm/DEB/RPM releases.

Documentation includes migration, installation, release checks, SVG project branding and operational diagrams.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2025-12-27

### Changed
- Python 3 modernization across the repo; removed legacy standalone scripts and vendored third-party code.
- Security: disallow shell=True in execute_command.
- Adopted Ruff + pre-commit; tightened lint/type gates and standardized formatting.
- CI cleanup and stability improvements.

### Fixed
- Multiple lint issues (flake8/ruff) and minor type issues in runtime code.

## [1.1.0] - 2025-04-11

### Added
- JSON output format support for all plugins
- Asynchronous execution support for improved performance
- Rich terminal output with progress indicators
- New `ThresholdRange` class for better threshold handling
- Added `get_directory_size` utility function
- Added `get_system_info` utility function
- Added security scanning with Bandit and pip-audit
- Added CommandResult dataclass for better command execution results
- Added timestamp to CheckResult for better tracking
- Added to_json method to CheckResult for JSON serialization

### Changed
- Modernized codebase to use maintained Python 3.11–3.14 features
- Updated all dependencies to latest versions
- Improved error handling with better error messages
- Refactored base plugin class for better extensibility
- Enhanced HTTP endpoint checking with more options
- Improved process checking across different operating systems
- Updated GitHub Actions workflow with modern actions
- Switched to modern Python packaging with pyproject.toml
- Improved documentation with more examples
- Enhanced test coverage and test organization

### Removed
- Support for Python 3.7 (now requires maintained Python 3.11–3.14)
- Deprecated utility functions replaced with modern alternatives

## [1.0.0] - 2024-01-01

### Added
- Initial release of nagios-plugins-collection
- Base plugin framework
- Core utility functions
- Initial set of monitoring plugins
- Documentation and examples
- Test suite
