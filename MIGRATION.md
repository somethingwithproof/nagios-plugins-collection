# Migration Guide: Python 3.12 and Type Hints

This document provides guidance for migrating to version 1.2.1+ of nagios-plugins-collection, which requires Python 3.12+ and includes full type hint coverage.

## Overview of Changes

### Python Version Requirement

- **Previous**: Python 3.11+
- **Current**: Python 3.12+

The project now requires Python 3.12 or newer to take advantage of modern type system features and performance improvements.

### Type Hints

All modules now include comprehensive type hints following PEP 484, PEP 585, and PEP 604 standards:

- All functions and methods have type-annotated parameters and return values
- All class attributes are properly typed
- Modern Python 3.12 syntax using built-in types (`list`, `dict`, `tuple`) instead of `typing.List`, `typing.Dict`, `typing.Tuple`
- Modern union syntax (`X | Y`) instead of `typing.Union[X, Y]` or `typing.Optional[X]`

### mypy Strict Mode

The codebase now passes mypy type checking in strict mode with the following flags enabled:

- `strict = true`
- `warn_return_any = true`
- `warn_unused_configs = true`
- `disallow_untyped_defs = true`
- `disallow_incomplete_defs = true`
- `disallow_any_unimported = true`
- `warn_redundant_casts = true`
- `warn_unused_ignores = true`
- `warn_unreachable = true`
- `no_implicit_optional = true`
- `strict_equality = true`

## Breaking Changes

### Python Version

If you're using Python 3.11 or earlier, you must upgrade to Python 3.12 or later.

```bash
# Check your Python version
python --version

# If using pyenv
pyenv install 3.12.3
pyenv global 3.12.3

# If using system package manager (Ubuntu/Debian)
sudo apt update
sudo apt install python3.12
```

### Type System Changes

If you're extending the plugin classes or importing types, note these changes:

#### Before (Python 3.11 with old typing)

```python
from typing import Dict, List, Optional, Tuple


def check_components(
    components: List[str], config: Optional[Dict[str, str]] = None
) -> Tuple[bool, str]:
    pass
```

#### After (Python 3.12 with modern typing)

```python
from __future__ import annotations


def check_components(
    components: list[str], config: dict[str, str] | None = None
) -> tuple[bool, str]:
    pass
```

### Import Changes

No breaking changes to public APIs. All plugin entry points and core classes remain unchanged:

```python
# These imports still work the same
from nagios_plugins.base import NagiosPlugin, CheckResult, Status
from nagios_plugins.utils import check_http_endpoint, execute_command
```

## Migration Steps

### Step 1: Update Python Version

Ensure you're running Python 3.12 or later:

```bash
python --version  # Should show 3.12.0 or higher
```

### Step 2: Update Package

Update to the latest version:

```bash
pip install --upgrade nagios-plugins-collection
```

Or if using extras:

```bash
pip install --upgrade "nagios-plugins-collection[all]"
```

### Step 3: Run Tests

Verify your plugins still work:

```bash
# Test individual plugins
check_website_status --url https://example.com

# Run your test suite
pytest tests/
```

### Step 4: Update Custom Plugins (If Any)

If you've created custom plugins that extend `NagiosPlugin`, update them to use modern type hints:

```python
from __future__ import annotations

import argparse
from nagios_plugins.base import CheckResult, NagiosPlugin, Status


class MyCustomPlugin(NagiosPlugin):
    """My custom monitoring plugin."""

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Perform the check."""
        # Your implementation here
        return CheckResult(Status.OK, "Check passed")


def main() -> int:
    """Main entry point."""
    plugin = MyCustomPlugin()
    return plugin.run()


if __name__ == "__main__":
    raise SystemExit(main())
```

### Step 5: Enable Type Checking (Optional)

If you want to benefit from type checking in your own code:

```bash
# Install mypy
pip install mypy

# Run type checking
mypy your_plugin.py
```

## Backwards Compatibility

### Runtime Behavior

All runtime behavior remains unchanged. Plugins work exactly the same way as before. Type hints are purely for static analysis and don't affect runtime execution.

### Plugin Scripts

All plugin entry points remain unchanged:

- `check_website_status`
- `check_tls_expiry`
- `check_prometheus_query`
- `check_http_sli`
- `check_dns_health`
- `check_k8s_node_status`
- `check_postgres_replication_lag`
- `check_queue_depth`
- `check_oauth2_token`
- `check_redis_saturation`
- `check_log_errors`
- `check_cloud_budget`
- `check_backup_freshness`
- And all legacy plugins

### Configuration Files

No changes required to Nagios configuration files, command definitions, or service definitions.

## Benefits of Python 3.12 and Type Hints

### For Users

1. **Better Error Detection**: Type hints help catch errors before runtime
2. **Improved IDE Support**: Better autocomplete and inline documentation
3. **Enhanced Documentation**: Types serve as inline documentation
4. **Performance**: Python 3.12 includes performance improvements (up to 10-60% faster)

### For Developers

1. **Code Quality**: Catch type errors during development
2. **Refactoring Confidence**: Types make refactoring safer
3. **Better Tooling**: IDEs can provide better suggestions
4. **Documentation**: Types reduce need for verbose docstrings

## Troubleshooting

### "Module not found" errors

If you get import errors after upgrading:

```bash
# Reinstall the package
pip uninstall nagios-plugins-collection
pip install nagios-plugins-collection
```

### Python version conflicts

If you have multiple Python versions:

```bash
# Use python3.12 explicitly
python3.12 -m pip install nagios-plugins-collection
python3.12 /path/to/plugin
```

### Type checking errors in your code

If mypy reports errors in your custom plugins:

1. Add `from __future__ import annotations` at the top of your file
2. Update old-style types (`List` → `list`, `Dict` → `dict`, `Optional[X]` → `X | None`)
3. Ensure all functions have return type annotations

## Getting Help

If you encounter issues during migration:

1. Check the [GitHub Issues](https://github.com/thomasvincent/nagios-plugins-collection/issues)
2. Review the [Documentation](https://nagios-plugins-collection.readthedocs.io/)
3. Open a new issue with:
   - Python version (`python --version`)
   - Package version (`pip show nagios-plugins-collection`)
   - Error message and traceback
   - Steps to reproduce

## Example: Complete Migration

Here's a complete example of migrating a custom plugin:

### Before (Python 3.11)

```python
#!/usr/bin/env python3
"""Custom HTTP checker."""

import argparse
from typing import Optional
from nagios_plugins.base import CheckResult, NagiosPlugin, Status


class HTTPChecker(NagiosPlugin):
    def check(self, args: argparse.Namespace) -> CheckResult:
        result = self._perform_check(args.url, args.timeout)
        return result

    def _perform_check(self, url: str, timeout: Optional[int] = None) -> CheckResult:
        # Implementation
        return CheckResult(Status.OK, f"OK: {url}")


def main() -> int:
    return HTTPChecker().run()


if __name__ == "__main__":
    exit(main())
```

### After (Python 3.12)

```python
#!/usr/bin/env python3
"""Custom HTTP checker."""

from __future__ import annotations

import argparse

from nagios_plugins.base import CheckResult, NagiosPlugin, Status


class HTTPChecker(NagiosPlugin):
    """Custom HTTP status checker."""

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Perform the HTTP check."""
        result = self._perform_check(args.url, args.timeout)
        return result

    def _perform_check(self, url: str, timeout: int | None = None) -> CheckResult:
        """Perform the actual HTTP request and return result."""
        # Implementation
        return CheckResult(Status.OK, f"OK: {url}")


def main() -> int:
    """Main entry point."""
    return HTTPChecker().run()


if __name__ == "__main__":
    raise SystemExit(main())
```

### Key Changes

1. Added `from __future__ import annotations` at the top
2. Changed `Optional[int]` to `int | None`
3. Added docstrings to all methods
4. Changed `exit(main())` to `raise SystemExit(main())` (modern best practice)

## Conclusion

The migration to Python 3.12 with type hints improves code quality and developer experience without breaking existing functionality. All plugins continue to work as before, with the added benefit of better type safety and IDE support.
