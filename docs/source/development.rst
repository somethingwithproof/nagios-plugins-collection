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

       pip install -e ".[dev]"

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
    ├── pyproject.toml          # Project configuration
    ├── setup.py                # Setup script (for backward compatibility)
    ├── tox.ini                 # Tox configuration
    └── README.md               # Project README

Creating a New Plugin
-------------------

To create a new plugin:

1. Create a new module in the ``src/nagios_plugins/`` directory:

   .. code-block:: python

       # src/nagios_plugins/check_example.py
       #!/usr/bin/env python3
       """Example Nagios plugin for demonstration purposes."""

       import argparse
       from nagios_plugins.base import NagiosPlugin, CheckResult, Status

       class ExamplePlugin(NagiosPlugin):
           """Example plugin that checks something."""

           def __init__(self):
               """Initialize the plugin."""
               super().__init__()
               self.parser.add_argument(
                   "--example-option",
                   help="An example option",
               )

           def check(self, args):
               """Perform the check."""
               # Implement your check logic here
               return CheckResult(Status.OK, "Everything is fine")

       def main():
           """Run the plugin."""
           plugin = ExamplePlugin()
           return plugin.run()

       if __name__ == "__main__":
           import sys
           sys.exit(main())

2. Add the plugin to the entry points in ``setup.py``:

   .. code-block:: python

       entry_points={
           "console_scripts": [
               # ...
               "check_example=nagios_plugins.check_example:main",
           ],
       }

3. Create tests for the plugin:

   .. code-block:: python

       # tests/unit/test_check_example.py
       """Tests for the check_example module."""

       from unittest.mock import patch
       import pytest
       from nagios_plugins.check_example import ExamplePlugin
       from nagios_plugins.base import Status

       class TestExamplePlugin:
           """Tests for the ExamplePlugin class."""

           @pytest.fixture
           def plugin(self):
               """Create a test plugin."""
               return ExamplePlugin()

           def test_check(self, plugin):
               """Test the check method."""
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

    tox -e py311-nagios4410  # Run tests with Python 3.11 and Nagios 4.4.10
    tox -e lint              # Run linting
    tox -e type              # Run type checking
    tox -e docs              # Build documentation

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

To format your code:

.. code-block:: bash

    black src tests
    isort src tests

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
- Test coverage
- Package building

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
