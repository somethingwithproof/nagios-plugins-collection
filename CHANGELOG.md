# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2024-01-15

### Added
- Modern Python package structure with `pyproject.toml`
- Full type hints throughout the codebase
- Comprehensive test suite with pytest
- Pre-commit hooks for code quality
- Docker support with multi-stage builds
- CI/CD with GitHub Actions
- Security policy (SECURITY.md)
- Contributing guidelines (CONTRIBUTING.md)
- Environment variable support for credentials
- Nagios range threshold syntax support
- Performance data output for all plugins
- New plugin: `check_jobs` for JSON API status checking
- New plugin: `check_website_status` with regex and timing support

### Changed
- **BREAKING**: Minimum Python version is now 3.9
- **BREAKING**: Plugin command-line arguments have been standardized
- Rewrote all plugins using the new `NagiosPlugin` base class
- `check_procs` now uses paramiko library instead of subprocess with shell=True
- `check_monghealth` now supports multiple check modes (status, replication, connections, memory)
- `check_hadoop` now supports both CLI and HTTP API modes
- Credentials are now read from environment variables by default

### Fixed
- **SECURITY**: Fixed shell injection vulnerability in `check_procs`
- **SECURITY**: Fixed shell injection risk in SSH command execution
- Proper error handling and exit codes
- Timeout handling for all network operations

### Removed
- Bundled `pexpect` library (now an optional dependency)
- Bundled `pynag` library (replaced with custom implementation)
- Legacy Python 2 compatibility code
- Deprecated `check_procs_simple.py` (functionality merged into `check_procs`)

### Security
- All subprocess calls now use list arguments instead of shell=True
- Input sanitization for command filter parameters
- Credentials no longer visible in process listings
- Added security scanning with Bandit and Safety

## [1.0.0] - 2023-01-01

### Added
- Initial collection of Nagios plugins
- check_counters_db: Vertica database monitoring
- check_dig: DNS resolution checking
- check_monghealth: MongoDB health monitoring
- check_procs: Remote process monitoring via SSH
- check_ro_mounts: Read-only mount detection
- check_scribe: Scribe log aggregation monitoring
- membase_stats: Membase/Couchbase statistics

[Unreleased]: https://github.com/thomasvincent/nagios-plugins-collection/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/thomasvincent/nagios-plugins-collection/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/thomasvincent/nagios-plugins-collection/releases/tag/v1.0.0
