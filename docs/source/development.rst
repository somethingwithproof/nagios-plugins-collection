.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

Development
===========

Select Python through ``mise`` and use the locked tooling described in
:doc:`installation`. Python 3.11, 3.12, 3.13 and 3.14 are the tested matrix.

.. code-block:: bash

   mise exec python@3.12 -- uv sync --locked --all-extras
   mise exec python@3.12 -- uv run pytest tests
   mise exec python@3.12 -- uv run ruff check .
   mise exec python@3.12 -- uv run ruff format --check src tests
   mise exec python@3.12 -- uv run mypy src
   mise exec python@3.12 -- uv run pytest --cov=nagios_plugins tests
   mise exec python@3.12 -- uv run bandit -r src/ -c pyproject.toml --severity-level medium
   mise exec python@3.12 -- uv run pip-audit --local
   mise exec python@3.12 -- uv run pre-commit run --all-files

Test another interpreter with ``uv run --python 3.13 pytest tests``.
``uv.lock`` is the single dependency lock. Development tools are the ``test``,
``lint``, ``type``, ``docs``, ``security`` and ``build`` dependency groups, which
the default ``dev`` group includes. uv verifies the locked hashes and installs
wheels only (``tool.uv.no-build``); it builds the first-party project with the
locked setuptools rather than an isolated, unlocked backend. Coverage measures the imported ``nagios_plugins``
package and must remain at least 80%; docstring coverage must remain at least
95%. Formatting and imports use Ruff; types use mypy. Bandit blocks medium/high
findings and pip-audit checks installed dependencies.

Plugin contract
---------------

Add modules under ``src/nagios_plugins/plugins`` and register their ``main``
functions in ``[project.scripts]``. Derive new synchronous CLI adapters from
``NagiosPlugin`` and return ``CheckResult`` with a ``Status`` and useful metrics.
Use ``asyncio.run`` at the synchronous boundary when the work is asynchronous.
Wrap async utility calls with ``asyncio.timeout``; propagate cancellation and
clean up owned resources. Keep certificate verification enabled. Avoid shell
command interpolation and redact credentials from diagnostics.

Add behavioral tests for status, thresholds, failure paths and CLI contracts.
Use isolated HTTP transports, verified local TLS servers or disposable services;
the Docker end-to-end mocks use static fake credentials and isolated networking.
Update the plugin page and migration guide when the public interface changes.

Build documentation with
``uv run sphinx-build -W -b html docs/source docs/build/html`` and check docstrings
with ``uv run docstr-coverage src --fail-under=95``. The Sphinx pages include all installed
plugin APIs; ``sphinx-build -W`` treats documentation warnings as failures.

Release changes
---------------

Update the project and Helm versions together. Run ``uv lock`` after changing
dependencies. Run the Linux package smoke
tests and full CI before publication; see :doc:`releasing`. Validate supported
platform dates against upstream sources before expanding the matrix.

Dependency updates must preserve the complete dependency graph. For example,
Pydantic requires an exact ``pydantic-core`` version, while aiohttp and Sphinx
bound the compatible multidict and docutils versions. Resolve the lock from the
project inputs rather than updating an indirect pin in isolation. CI installs
``uv.lock`` with ``uv sync --locked`` on every supported Python version; native
package builds export the runtime set from ``uv.lock`` and install it with
hashes for the target Linux platform. Both checks must pass before merging updates.
