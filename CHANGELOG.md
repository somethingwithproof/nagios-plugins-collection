# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-04-11

### Added
- JSON output format support for all plugins
- Asynchronous execution support for improved performance
- Rich terminal output with progress indicators
- New `ThresholdRange` class for better threshold handling
- Added `get_directory_size` utility function
- Added `get_system_info` utility function
- Added security scanning with bandit and safety
- Added CommandResult dataclass for better command execution results
- Added timestamp to CheckResult for better tracking
- Added to_json method to CheckResult for JSON serialization

### Changed
- Modernized codebase to use Python 3.8+ features
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
- Support for Python 3.7 (now requires Python 3.8+)
- Deprecated utility functions replaced with modern alternatives

## [1.0.0] - 2024-01-01

### Added
- Initial release of nagios-plugins-collection
- Base plugin framework
- Core utility functions
- Initial set of monitoring plugins
- Documentation and examples
- Test suite
