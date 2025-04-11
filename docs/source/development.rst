Development
===========

This guide provides information for developers who want to contribute to the Nagios Plugins Collection.

Development Environment Setup
---------------------------

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/thomasvincent/nagios-plugins-collection.git
       cd nagios-plugins-collection

2. Create a virtual environment:

   .. code-block:: bash

       python -m venv venv
       source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install development dependencies:

   .. code-block:: bash

       pip install -e ".[dev,security]"

Project Structure
---------------

The project is organized as follows:

.. code-block:: text

    nagios-plugins-collection/
    ├── .github/                # GitHub workflows and configuration
    ├── docs/                   # Documentation
    ├── src/                    # Source code
    │   └── nagios_plugins/     # Main package
    │       ├── __init__.py     # Package initialization
    │       ├── base.py         # Base classes and utilities
    │       ├── utils.py        # Common utility functions
    │       └── ...             # Plugin modules
    ├── tests/                  # Tests
    │   ├── unit/               # Unit tests
    │   └── integration/        # Integration tests
    ├── pyproject.toml          # Project configuration (main configuration)
    ├── setup.py                # Setup script (for backward compatibility)
    ├── tox.ini                 # Tox configuration
    ├── README.md               # Project README
    └── CHANGELOG.md            # Project changelog

Creating a New Plugin
-------------------

To create a new plugin:

1. Create a new module in the ``src/nagios_plugins/`` directory:

   .. code-block:: python

       # src/nagios_plugins/check_example.py
       #!/usr/bin/env python3
       """Example Nagios plugin for demonstration purposes."""

       from typing import Dict, Any, Optional
       import argparse
       import asyncio

       from rich.console import Console

       from nagios_plugins.base import NagiosPlugin, CheckResult, Status
       from nagios_plugins.utils import check_http_endpoint

       class ExamplePlugin(NagiosPlugin):
           """Example plugin that checks something."""

           def __init__(self) -> None:
               """Initialize the plugin."""
               super().__init__()
               self.parser.add_argument(
                   "--example-option",
                   help="An example option",
               )
               self.parser.add_argument(
                   "--url",
                   help="URL to check",
               )
               self.console = Console()

           async def async_check(self, args: argparse.Namespace) -> CheckResult:
               """Perform the check asynchronously."""
               self.console.print("[bold blue]Checking example...[/bold blue]")
               
               if args.url:
                   # Use the utility function for HTTP checks
                   return check_http_endpoint(
                       url=args.url,
                       timeout=args.timeout,
                   )
               
               # Implement your check logic here
               metrics: Dict[str, Any] = {
                   "example_metric": 100,
                   "response_time": 42.5,
               }
               
               return CheckResult(
                   status=Status.OK,
                   message="Everything is fine",
                   metrics=metrics,
                   details="Detailed information about the check result."
               )

           def check(self, args: argparse.Namespace) -> CheckResult:
               """Perform the check."""
               # Run the async check in the event loop
               try:
                   loop = asyncio.get_event_loop()
               except RuntimeError:
                   loop = asyncio.new_event_loop()
                   asyncio.set_event_loop(loop)
               
               return loop.run_until_complete(self.async_check(args))

       def main() -> int:
           """Run the plugin."""
           plugin = ExamplePlugin()
           return plugin.run()

       if __name__ == "__main__":
           import sys
           sys.exit(main())

2. Add the plugin to the entry points in ``pyproject.toml``:

   .. code-block:: toml

       [project.scripts]
       check_example = "nagios_plugins.check_example:main"

3. Create tests for the plugin:

   .. code-block:: python

       # tests/unit/test_check_example.py
       """Tests for the check_example module."""

       from unittest.mock import patch, AsyncMock
       import pytest
       import asyncio

       from nagios_plugins.check_example import ExamplePlugin
       from nagios_plugins.base import Status, CheckResult

       class TestExamplePlugin:
           """Tests for the ExamplePlugin class."""

           @pytest.fixture
           def plugin(self):
               """Create a test plugin."""
               return ExamplePlugin()

           @pytest.mark.asyncio
           async def test_async_check(self, plugin):
               """Test the async_check method."""
               args = plugin.parse_args([])
               result = await plugin.async_check(args)
               assert result.status == Status.OK
               assert "Everything is fine" in result.message
               assert "example_metric" in result.metrics
               assert result.metrics["example_metric"] == 100

           def test_check(self, plugin):
               """Test the check method."""
               with patch.object(
                   plugin, 'async_check', 
                   return_value=CheckResult(Status.OK, "Everything is fine")
               ):
                   result = plugin.check(plugin.parse_args([]))
                   assert result.status == Status.OK
                   assert "Everything is fine" in result.message

4. Add documentation for the plugin:

   .. code-block:: rst

       .. _check_example:

       check_example
       ============

       Description
       -----------

       This plugin checks something for demonstration purposes.

       Usage
       -----

       .. code-block:: bash

           check_example [options]

       Options
       -------

       --example-option
           An example option

       Examples
       --------

       .. code-block:: bash

           check_example --example-option=value

       Output
       ------

       .. code-block:: text

           OK - Everything is fine

Testing
------

Run the tests with tox:

.. code-block:: bash

    tox

This will run the tests with multiple Python versions and Nagios versions.

To run specific tests:

.. code-block:: bash

    tox -e py312-nagios4410  # Run tests with Python 3.12 and Nagios 4.4.10
    tox -e lint              # Run linting
    tox -e type              # Run type checking
    tox -e docs              # Build documentation
    tox -e security          # Run security checks

Code Style
---------

This project follows these code style guidelines:

- PEP 8 for Python code style
- Google style for docstrings
- 100 character line length
- Black for code formatting
- isort for import sorting
- pylint for linting
- mypy for type checking
- bandit for security scanning

To format your code:

.. code-block:: bash

    black src tests
    isort src tests

To check for security issues:

.. code-block:: bash

    bandit -r src/
    safety check

Documentation
------------

Documentation is built with Sphinx. To build the documentation:

.. code-block:: bash

    tox -e docs

The documentation will be available in ``docs/build/html/``.

Continuous Integration
--------------------

This project uses GitHub Actions for continuous integration. The CI pipeline runs:

- Tests with multiple Python and Nagios versions
- Linting
- Type checking
- Documentation building
- Security scanning
- Test coverage
- Package building and verification

Pull Request Process
-----------------

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the tests
5. Submit a pull request

Your pull request should:

- Include tests for new functionality
- Update documentation as needed
- Follow the code style guidelines
- Pass all CI checks
