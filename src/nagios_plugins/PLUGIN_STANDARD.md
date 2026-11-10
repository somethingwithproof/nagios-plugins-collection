<!--
SPDX-FileCopyrightText: 2025 Thomas Vincent
SPDX-License-Identifier: Apache-2.0
-->

# Nagios Plugin Standards

This document outlines the standard structure, dependencies, and patterns for all Nagios plugins in this collection. Following these standards ensures consistency, maintainability, and security across all plugins.

## Plugin Structure

All plugins should follow this common structure:

### 1. Base Structure

- Each plugin should be a class that inherits from `NagiosPlugin` base class or implements a similar interface
- The plugin class should have a clear purpose and responsibility (following Single Responsibility Principle)
- Standard exit codes (0 = OK, 1 = WARNING, 2 = CRITICAL, 3 = UNKNOWN) should be used via the `Status` enum

### 2. Common Methods

Every plugin class should include these standard methods:

- `__init__`: Initialize the plugin with necessary configuration
- `check`: Main method that performs the check and returns a `CheckResult`
- Standard command-line argument parsing using `argparse`
- Support for async operations when appropriate

### 3. Plugin Template

```python
#!/usr/bin/env python3
"""[Service] check: report [specific data points] against -w/-c ranges."""

from __future__ import annotations

import argparse

from nagios_plugins.base import (
    CheckResult,
    NagiosPlugin,
    PerfData,
    Status,
    threshold_check,
)


class CheckService(NagiosPlugin):
    """Check [service]."""

    def __init__(self) -> None:
        """Register plugin-specific arguments next to the shared ones."""
        super().__init__()
        self.parser.add_argument("--host", required=True, help="[Service] host")

    def check(self, args: argparse.Namespace) -> CheckResult:
        """Measure the value and classify it with the shared Nagios ranges."""
        value = ...  # absent data is UNKNOWN, never a default of 0
        if value is None:
            return CheckResult(Status.UNKNOWN, "[service] returned no data")
        status = threshold_check(value, args.warning, args.critical)
        perf = PerfData(value, warning=args.warning, critical=args.critical)
        return CheckResult(status, f"[service] value={value}", metrics={"value": perf})


def main() -> int:
    """Run the installed command and return its Nagios status code."""
    return CheckService().run()


if __name__ == "__main__":
    raise SystemExit(main())
```

`NagiosPlugin` supplies `-v`, `-t`, `-w`, `-c` and `--json`, a
`NagiosArgumentParser` named after the command whose usage errors exit UNKNOWN
(3), stderr logging configured after parsing, and conversion of unhandled
exceptions to UNKNOWN. Every installed command is a `NagiosPlugin` subclass;
do not build a separate parser or `main()` loop.

- A check that awaits I/O derives from `AsyncNagiosPlugin` and implements
  `async def check_async(self, args)`; the base class owns the event loop.
- Set `default_timeout` to change the `-t/--timeout` default. The base class
  ends the whole run UNKNOWN one second after `--timeout` (see
  `nagios_plugins.deadline`), so use `--timeout` for each request or command
  and `remaining_time()` to bound retries, and register child processes with
  `track_child()` so they are killed when the run is ended.
- Set `has_thresholds = False` when the check has no `-w`/`-c`, so they are
  rejected instead of silently ignored, or override `add_threshold_arguments`
  when established options take something other than Nagios ranges.

## Dependencies

### Core Dependencies

Limit dependencies to these essential libraries:

1. **Standard Library**:
   - `argparse`: For command-line argument parsing
   - `json`: For JSON handling
   - `logging`: For structured logging
   - `asyncio`: For asynchronous operations
   - `sys`: For system interactions
   - `typing`: For type annotations
   - `pathlib`: For file path handling (preferred over `os.path`)
   - `re`: For regular expressions
   - `tempfile`: For temporary file operations

2. **Essential External Libraries**:
   - `httpx`: For HTTP requests (preferred over `requests` for async support)

### Optional Dependencies

These should only be included when specifically needed by a plugin:

- `pymongo`: Only for MongoDB-specific plugins
- `paramiko`: Only for SSH-specific functionality
- `psutil`: Only for detailed system monitoring

## Security Standards

All plugins must follow these security practices:

1. **Input Validation**:
   - Validate all user inputs before use
   - Use appropriate type checking
   - Sanitize any inputs used in command execution

2. **Command Execution**:
   - Never use `shell=True` with subprocess
   - Use list arguments for command execution
   - Prefer the utilities in `utils.py` for command execution

3. **Network Requests**:
   - Always include timeouts for network operations
   - Validate URL schemes
   - Use proper exception handling for network errors
   - Verify SSL certificates by default

4. **Error Handling**:
   - Use specific exception handling (avoid broad except)
   - Log exceptions with appropriate context
   - Return clear, actionable error messages

## Logging Standards

All plugins should follow these logging practices:

1. **Log Levels**:
   - `DEBUG`: Detailed debugging information
   - `INFO`: Confirmation that things are working as expected
   - `WARNING`: Indication that something unexpected happened
   - `ERROR`: Error conditions preventing normal operation
   - `CRITICAL`: Critical errors requiring immediate attention

2. **Log Destination**:
   - Use `logging.getLogger(...)`; never call `logging.basicConfig` or add
     handlers at import time
   - `configure_logging` (called by `NagiosPlugin.parse_args`) sends
     records to stderr, so stdout carries only the plugin result
   - Include the log level and keep messages clear and actionable

## Output Format

All plugins must support these output formats:

1. **Standard Output**:
   - First line: STATUS - Message, on a single line
   - Performance data: `'label'=value[UOM];warn;crit;min;max`, rendered by
     `CheckResult` from numeric metrics or `PerfData` values

2. **JSON Output**:
   - Status code
   - Status name
   - Message
   - Metrics
   - Optional details

## Testing Requirements

Each plugin should include:

1. Unit tests covering core functionality
2. Sample command-line usage in documentation
3. Expected output examples
