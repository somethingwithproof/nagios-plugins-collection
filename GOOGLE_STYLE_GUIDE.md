# Google Style Guide Implementation

This document outlines how the Google Python Style Guide has been implemented in the modernized Nagios plugins. The Google Style Guide provides a consistent, readable, and maintainable approach to Python code.

## Key Google Style Guide Principles Applied

### 1. Imports

- Imports are grouped in the following order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application/library specific imports
- Each group is separated by a blank line
- Imports are alphabetized within each group
- Avoid wildcard imports (`from module import *`)

Example from `check_etl/etl_modernized.py`:

```python
import argparse
import asyncio
import json
import logging
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union, Any

import httpx
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
```

### 2. Indentation and Line Length

- Use 4 spaces for indentation (not tabs)
- Maximum line length is 100 characters
- For line continuations, indent by 4 spaces
- Hanging indents should add 4 spaces

Example from `check_etl/etl_modernized.py`:

```python
def __init__(
    self,
    host: str,
    port: int = 80,
    timeout: int = 10,
    use_ssl: bool = False,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> None:
    """
    Initialize the ComponentStatusChecker.
    
    Args:
        host: Hostname of the ETL API server
        port: Port number of the ETL API server
        timeout: Timeout in seconds for API requests
        use_ssl: Whether to use HTTPS instead of HTTP
        username: Optional username for authentication
        password: Optional password for authentication
    """
```

### 3. Docstrings

- Use Google-style docstrings
- Include a one-line summary followed by a blank line
- For functions and methods, document:
  - Args: for each parameter
  - Returns: what the function returns
  - Raises: exceptions that may be raised
- For classes, document the class's behavior and attributes

Example from `check_monghealth/check_monghealth_modernized.py`:

```python
async def check_components(
    self, required_components: List[Tuple[str, bool]]
) -> CheckResult:
    """Check the status of MongoDB components.
    
    Args:
        required_components: List of (component_name, expected_value) tuples
        
    Returns:
        CheckResult with the check result
    """
```

### 4. Naming Conventions

- `module_name`, `package_name`, `function_name`, `method_name`, `instance_var_name`, `function_parameter_name`, `local_var_name`: Use lowercase with underscores
- `ClassName`, `ExceptionName`: Use CapWords convention
- `GLOBAL_CONSTANT_NAME`: Use all uppercase with underscores
- Protected instance attributes: Use single leading underscore (`_protected_attribute`)
- Private instance attributes: Use double leading underscore (`__private_attribute`)

Example from `check_etl/etl_modernized.py`:

```python
class ComponentStatusChecker:
    """
    A class for checking the status of ETL components by querying a JSON API.
    """

    def __init__(self, host: str, port: int = 80):
        self.host = host
        self.port = port
        self._auth = None  # Protected attribute
```

### 5. Comments and Annotations

- Use type annotations for function declarations
- Comments should be complete sentences
- Use inline comments sparingly
- Use TODO comments for code that is temporary or a short-term solution

Example from `check_monghealth/check_monghealth_modernized.py`:

```python
def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.
    
    Returns:
        Parsed arguments
    """
```

### 6. Classes

- Use `dataclasses` for data containers
- Use explicit `__init__` methods for complex initialization
- Follow the single responsibility principle
- Use properties instead of getter/setter methods

Example from `check_etl/etl_modernized.py`:

```python
@dataclass
class CheckResult:
    """Data class to store check results."""
    status: Status
    message: str
    metrics: Dict[str, Any] = field(default_factory=dict)
    details: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
```

### 7. Functions and Methods

- Functions should do one thing
- Keep functions small and focused
- Use default parameter values instead of overloading methods
- Avoid mutable objects as default values

Example from `check_monghealth/check_monghealth_modernized.py`:

```python
async def check_engine_status(self) -> Tuple[bool, Dict[str, Any]]:
    """Check the MongoDB engine status.
    
    Returns:
        A tuple of (is_alive, status_data)
    """
```

### 8. Error Handling

- Use specific exception types
- Handle exceptions at the appropriate level
- Use context managers for resource cleanup
- Provide informative error messages

Example from `check_etl/etl_modernized.py`:

```python
try:
    async with httpx.AsyncClient(
        timeout=self.timeout, auth=self.auth
    ) as client:
        response = await client.get(url)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        status = data.get("status", "").lower()
        
        # Parse the updated timestamp
        updated = None
        if "updated" in data:
            try:
                updated = datetime.fromisoformat(data["updated"])
            except (ValueError, TypeError):
                logger.warning(
                    "Invalid timestamp format: %s", data["updated"]
                )
        
        return status, updated
        
except httpx.HTTPStatusError as e:
    logger.error("HTTP error: %s", e)
    return "error", None
```

### 9. String Formatting

- Use f-strings for string formatting
- Use r-strings for regular expressions
- Use triple quotes for multi-line strings

Example from `check_etl/etl_modernized.py`:

```python
def __str__(self) -> str:
    """Return the string representation of the check result."""
    output = f"{self.status} - {self.message}"
    if self.metrics:
        metrics_str = " ".join(
            f"{key}={value}" for key, value in self.metrics.items()
        )
        output += f" | {metrics_str}"
    if self.details:
        output += f"\n{self.details}"
    return output
```

### 10. Main Function

- Use a `main()` function as the entry point
- Use `if __name__ == "__main__":` to call the main function
- Return an exit code from the main function

Example from `check_monghealth/check_monghealth_modernized.py`:

```python
def main() -> int:
    """Main function.
    
    Returns:
        Exit code
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(main_async())


if __name__ == "__main__":
    sys.exit(main())
```

## Tools for Google Style Guide Compliance

The following tools are configured in each plugin's `pyproject.toml` to ensure compliance with the Google Style Guide:

1. **Black**: Code formatter with a line length of 100 characters
2. **isort**: Import sorter configured to be compatible with Black
3. **pylint**: Linter with Google Style Guide rules
4. **mypy**: Static type checker

Example configuration from `check_etl/pyproject.toml`:

```toml
[tool.black]
line-length = 100
target-version = ["py38", "py39", "py310", "py311", "py312"]

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true

[tool.pylint]
max-line-length = 100
disable = [
    "C0111",  # missing-docstring
    "C0103",  # invalid-name
    "C0330",  # bad-continuation
    "C0326",  # bad-whitespace
    "W0511",  # fixme
]
```

## Conclusion

By following the Google Style Guide, the modernized Nagios plugins are more readable, maintainable, and consistent. This approach will be applied to all plugins in the collection, ensuring a high-quality, enterprise-grade codebase.
