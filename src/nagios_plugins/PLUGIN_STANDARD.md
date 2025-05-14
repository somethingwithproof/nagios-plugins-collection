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
"""
[Service] Check Plugin for Nagios.

This plugin checks [specific metric/service] and reports [specific data points].
It supports [features like thresholds, remote execution].

Usage:
    check_[service].py [--host HOST] [--timeout SECONDS] [--warning THRESHOLD]
                     [--critical THRESHOLD] [--json] [--verbose]

Returns:
    0 (OK): [condition for OK]
    1 (WARNING): [condition for WARNING]
    2 (CRITICAL): [condition for CRITICAL]
    3 (UNKNOWN): An unexpected error occurred during the check
"""

import argparse
import json
import logging
import sys
from typing import Dict, Optional, List

from nagios_plugins.base import Status, CheckResult, NagiosPlugin
from nagios_plugins.utils import [only necessary utilities]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
)
logger = logging.getLogger("check_[service]")


class ServiceChecker:
    """[Service] checker class."""

    def __init__(
        self,
        [required parameters],
        [optional parameters with defaults],
    ):
        """Initialize the [service] checker.

        Args:
            [document all parameters]
        """
        [initialize instance variables]

    async def check(self) -> CheckResult:
        """Perform the service check.

        Returns:
            CheckResult with status and metrics
        """
        try:
            [perform check logic]
            
            # Create metrics dictionary
            metrics = {
                "key": value,
            }
            
            # Evaluate results against thresholds
            if [critical condition]:
                return CheckResult(
                    Status.CRITICAL,
                    "[critical message]",
                    metrics=metrics,
                )
            elif [warning condition]:
                return CheckResult(
                    Status.WARNING,
                    "[warning message]",
                    metrics=metrics,
                )
            else:
                return CheckResult(
                    Status.OK,
                    "[ok message]",
                    metrics=metrics,
                )
                
        except Exception as e:
            logger.exception("Error checking [service]")
            return CheckResult(
                Status.UNKNOWN,
                f"Error checking [service]: {str(e)}",
                details=str(e),
            )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Check [service]",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # Common arguments
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout in seconds",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )
    parser.add_argument(
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times)",
    )
    
    # Plugin-specific arguments
    [add plugin-specific arguments]
    
    return parser.parse_args()


def main() -> int:
    """Main function.

    Returns:
        Exit code
    """
    args = parse_args()

    # Set logging level based on verbosity
    if args.verbose == 1:
        logger.setLevel(logging.INFO)
    elif args.verbose >= 2:
        logger.setLevel(logging.DEBUG)

    # Create checker and run check
    checker = ServiceChecker(
        [initialize with args],
    )

    # Run the check
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    result = loop.run_until_complete(checker.check())

    # Output the result
    if args.json:
        print(result.to_json())
    else:
        print(result)

    return result.status.value


if __name__ == "__main__":
    sys.exit(main())
```

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
   - `rich`: For improved console output and logging

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

2. **Log Format**:
   - Include timestamps
   - Include log level
   - Keep messages clear and actionable

## Output Format

All plugins must support these output formats:

1. **Standard Output**:
   - First line: STATUS - Message
   - Performance data: 'metric=value;warning;critical;min;max'

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