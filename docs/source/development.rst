.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

Development
===========

Select Python through ``mise`` and use the hash-locked tooling described in
:doc:`installation`. Python 3.11, 3.12, 3.13 and 3.14 are the tested matrix.

.. code-block:: bash

   mise exec python@3.12 -- tox -e py312,lint,type,docs,coverage,security
   mise exec python@3.12 -- pre-commit run --all-files

Tox installs dependencies from ``packaging/ci-requirements.txt`` with hashes and
wheel-only third-party installs. It builds the first-party project using the
installed locked backend. Coverage measures the imported ``nagios_plugins``
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

Build documentation with ``tox -e docs``. The Sphinx pages include all installed
plugin APIs; ``sphinx-build -W`` treats documentation warnings as failures.

Release changes
---------------

Update the project and Helm versions together. Refresh the relevant hashed
locks and ``uv.lock`` after changing dependencies. Run the Linux package smoke
tests and full CI before publication; see :doc:`releasing`. Validate supported
platform dates against upstream sources before expanding the matrix.
