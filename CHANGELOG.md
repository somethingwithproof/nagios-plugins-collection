# Changelog

## 2.0.0 — 2026-10-06

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
