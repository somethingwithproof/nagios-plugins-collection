.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

Contributing
============

Thank you for your interest in contributing to the Nagios Plugins Collection! This document provides guidelines for contributing to the project.

Code of Conduct
---------------

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

Ways to Contribute
------------------

There are many ways to contribute to the project:

1. **Reporting Bugs**: If you find a bug, please report it by opening an issue on GitHub.
2. **Suggesting Enhancements**: Have an idea for a new feature or improvement? Open an issue to suggest it.
3. **Writing Documentation**: Help improve the documentation by fixing errors or adding examples.
4. **Contributing Code**: Implement new features or fix bugs by submitting pull requests.
5. **Reviewing Pull Requests**: Help review pull requests from other contributors.

Reporting Bugs
--------------

When reporting a bug, please include:

- A clear and descriptive title
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Screenshots or error messages (if applicable)
- Environment information (OS, Python version, Nagios version, etc.)

Suggesting Enhancements
-----------------------

When suggesting an enhancement, please include:

- A clear and descriptive title
- A detailed description of the proposed enhancement
- Any relevant examples or use cases
- If applicable, information about similar features in other projects

Pull Request Process
--------------------

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

Development Workflow
--------------------

See the :doc:`development` guide for detailed information on setting up a development environment, running tests, and building documentation.

Pre-commit Hooks
----------------

This project uses `pre-commit <https://pre-commit.com>`_ to run linters and
formatters before each commit.  After ``uv sync`` installs the development
dependencies, enable the hooks with:

.. code-block:: bash

   uv run pre-commit install

You can then run the hooks against all files or specific paths:

.. code-block:: bash

   uv run pre-commit run --all-files
   uv run pre-commit run --files path/to/file.py docs/source/file.rst

Commit Message Guidelines
-------------------------

Pull requests are squash-merged, so the pull request title becomes the commit
subject on main, and Release Please derives the next version and the changelog
from those subjects. Titles must follow `Conventional Commits
<https://www.conventionalcommits.org/en/v1.0.0/>`_; the ``Semantic PR title``
check enforces this and re-runs when the title is edited:

.. code-block:: text

    <type>[optional scope][!]: <description>

    [optional body]

    [optional footer(s)]

Types, and where they appear in the changelog:

- **feat**: a new command, option or capability (Features; a minor release)
- **fix**: a bug fix (Bug Fixes; a patch release)
- **perf**: a performance improvement (Performance)
- **revert**: reverts an earlier change (Reverts)
- **build**: packaging, dependencies or the container image (Build and Packaging)
- **docs**: documentation only (Documentation)
- **refactor**, **test**, **ci**, **style**, **chore**: no user-visible change
  (not listed)

Mark a breaking change with ``!`` after the type or scope, for example
``feat(check_http_sli)!: split latency and error-rate thresholds``, and explain
the upgrade step in a ``BREAKING CHANGE:`` paragraph at the end of the pull
request description (it becomes the squash commit body). Add the details to
``MIGRATION.md`` under the next major version.

Examples:

.. code-block:: text

    feat(check_hadoop): add support for Hadoop 3.x

    fix(check_website_status): reject invalid response patterns

    docs: update installation instructions

    refactor!: run every command on the NagiosPlugin base

Versioning and deprecation policy
---------------------------------

Releases follow `Semantic Versioning 2.0.0 <https://semver.org/spec/v2.0.0.html>`_.
The public interface is what monitoring configurations and integrations depend
on:

- console script names and the plugin directory layout of the native packages;
- option names, short flags, defaults, accepted values and the environment
  variables that supply secrets;
- exit codes and the status each condition reports (OK, WARNING, CRITICAL,
  UNKNOWN), including how thresholds are interpreted;
- the status line and performance data format: labels, units, the
  ``warn;crit;min;max`` fields and their meaning;
- ``--json`` field names, types and values;
- Helm chart values and the Nomad job variables;
- the documented Python API (``nagios_plugins.base``, ``nagios_plugins.deadline``
  and ``nagios_plugins.services.http``).

A **major** release removes or renames any of these, changes what an existing,
valid command definition reports (a different status, exit code, perfdata
label or JSON field for the same input), or turns previously accepted input into
a usage error. A **minor** release adds commands, options, perfdata labels or
JSON fields without changing existing ones, or deprecates something. A
**patch** release fixes behavior that contradicted the documentation without
changing the result for configurations that worked as documented.

Deprecated options keep working, and warn on stderr (never on stdout, which
Nagios parses), for at least one minor release before a major release removes
them. A deprecation is announced in the changelog with its replacement, and the
removal is listed in ``MIGRATION.md``. Compatibility aliases that change
nothing, such as ``--verify-ssl``, may stay hidden from ``--help`` indefinitely.

Release Process
---------------

1. Merge Conventional Commit pull requests into main. Release Please keeps a
   ``chore: release X.Y.Z`` pull request open that bumps the version in
   ``pyproject.toml``, ``uv.lock``, the Helm chart, the Nomad job, the chart
   test and the installation guide, and adds the changelog section.
2. A maintainer reviews that pull request (including the computed version) and
   merges it when the release is due. Release Please then tags ``vX.Y.Z``,
   creates the GitHub release with its notes and calls the Release workflow,
   which verifies CI, native packages, container signatures and GitHub
   artifacts before publishing them.
3. PyPI and TestPyPI publication is a separate manual workflow using the
   already-published, checksum-verified and provenance-verified Python assets.

See :doc:`releasing` for the complete release contract.

License
-------

Contributions use the project's Apache-2.0 license, matching the LICENSE file.

Contact
-------

If you have any questions or need help, please open an issue on GitHub or contact the maintainers directly.
