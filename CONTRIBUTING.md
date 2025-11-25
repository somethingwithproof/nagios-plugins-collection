# Contributing to Nagios Plugins Collection

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We're all here to make better monitoring tools.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- A GitHub account

### Development Setup

1. Fork the repository on GitHub

2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/nagios-plugins-collection.git
   cd nagios-plugins-collection
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev,all]"
   ```

5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-mysql-plugin` - New features
- `fix/ssh-timeout-handling` - Bug fixes
- `docs/update-readme` - Documentation
- `refactor/cleanup-base-module` - Refactoring

### Commit Messages

Follow conventional commits format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(check_mysql): add MySQL plugin for query monitoring

fix(check_procs): handle empty process list gracefully

docs(readme): add MongoDB plugin examples
```

### Code Style

- Follow PEP 8 and the Google Python Style Guide
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use `black` for formatting and `isort` for import sorting

The pre-commit hooks will check these automatically.

### Testing

Write tests for all new functionality:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific tests
pytest tests/unit/test_check_procs.py -v
```

Aim for >80% code coverage on new code.

### Documentation

- Update README.md if adding new plugins or features
- Add docstrings to all public functions and classes
- Include usage examples in plugin epilog text

## Adding a New Plugin

1. Create the plugin file in `src/nagios_plugins/`:
   ```python
   """
   check_myservice - MyService Monitoring Plugin for Nagios

   Description of what this plugin does.
   """

   from .base import CheckResult, NagiosPlugin, Status

   class CheckMyService(NagiosPlugin):
       name = "check_myservice"
       version = "2.0.0"
       description = "Check MyService health"

       def _add_arguments(self) -> None:
           # Add plugin-specific arguments
           pass

       def check(self, args) -> CheckResult:
           # Implement the check logic
           return CheckResult(Status.OK, "All good")

   def main() -> None:
       plugin = CheckMyService()
       plugin.run()
   ```

2. Add entry point in `pyproject.toml`:
   ```toml
   [project.scripts]
   check_myservice = "nagios_plugins.check_myservice:main"
   ```

3. Add tests in `tests/unit/test_check_myservice.py`

4. Update documentation

## Pull Request Process

1. Ensure all tests pass and code is formatted
2. Update documentation as needed
3. Create a pull request with a clear description
4. Link any related issues
5. Wait for review and address feedback

### PR Checklist

- [ ] Tests added/updated and passing
- [ ] Code formatted with `black` and `isort`
- [ ] Type hints added
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced
- [ ] Commit messages follow conventional format

## Reporting Issues

### Bug Reports

Include:
- Plugin name and version
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages and stack traces

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative solutions considered

## Security Issues

**Do not open public issues for security vulnerabilities.**

Please report security issues privately to: thomas@thomasvincent.io

See [SECURITY.md](SECURITY.md) for our security policy.

## Questions?

- Check existing issues and discussions
- Open a new issue with the "question" label

Thank you for contributing!
