Contributing
============

Thank you for your interest in contributing to the Nagios Plugins Collection! This document provides guidelines for contributing to the project.

Code of Conduct
-------------

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

Ways to Contribute
----------------

There are many ways to contribute to the project:

1. **Reporting Bugs**: If you find a bug, please report it by opening an issue on GitHub.
2. **Suggesting Enhancements**: Have an idea for a new feature or improvement? Open an issue to suggest it.
3. **Writing Documentation**: Help improve the documentation by fixing errors or adding examples.
4. **Contributing Code**: Implement new features or fix bugs by submitting pull requests.
5. **Reviewing Pull Requests**: Help review pull requests from other contributors.

Reporting Bugs
------------

When reporting a bug, please include:

- A clear and descriptive title
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Screenshots or error messages (if applicable)
- Environment information (OS, Python version, Nagios version, etc.)

Suggesting Enhancements
---------------------

When suggesting an enhancement, please include:

- A clear and descriptive title
- A detailed description of the proposed enhancement
- Any relevant examples or use cases
- If applicable, information about similar features in other projects

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

Development Workflow
-----------------

See the :doc:`development` guide for detailed information on setting up a development environment, running tests, and building documentation.

Commit Message Guidelines
----------------------

We follow the Conventional Commits specification for commit messages:

.. code-block:: text

    <type>[optional scope]: <description>

    [optional body]

    [optional footer(s)]

Types:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc.)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries

Examples:

.. code-block:: text

    feat(check_hadoop): add support for Hadoop 3.x

    fix(check_procs): handle processes with spaces in names

    docs: update installation instructions

    test(check_monghealth): add tests for replica set checks

Release Process
------------

1. Update version number in:
   - ``pyproject.toml``
   - ``setup.py``
   - ``src/nagios_plugins/__init__.py``
   - ``docs/source/conf.py``

2. Update the changelog

3. Create a new release on GitHub with release notes

4. The CI pipeline will automatically build and publish the package to PyPI

License
------

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.

Contact
------

If you have any questions or need help, please open an issue on GitHub or contact the maintainers directly.
