# Nagios Plugins Collection

[![GitHub Actions](https://github.com/thomasvincent/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg)](https://github.com/thomasvincent/nagios-plugins-collection/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/nagios-plugins-collection.svg)](https://badge.fury.io/py/nagios-plugins-collection)
[![Python Versions](https://img.shields.io/pypi/pyversions/nagios-plugins-collection.svg)](https://pypi.org/project/nagios-plugins-collection/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/nagios-plugins-collection/badge/?version=latest)](https://nagios-plugins-collection.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

A modern, enterprise-grade collection of Nagios plugins for monitoring various systems.

## Features

- **Modern Python**: Fully compatible with Python 3.8+ with type hints and modern language features
- **Async Support**: Asynchronous execution for improved performance in high-load environments
- **Rich Output**: Beautiful terminal output with progress indicators and formatted results
- **JSON Support**: All plugins support JSON output format for easier integration with other tools
- **Consistent Interface**: All plugins follow the same command-line interface pattern
- **Comprehensive Documentation**: Each plugin is thoroughly documented with examples
- **Extensive Test Coverage**: All plugins have unit and integration tests
- **Multi-Version Support**: Compatible with multiple Nagios versions (4.4.6+)
- **Performance Data**: All plugins provide performance data for trending and analysis
- **Threshold Handling**: Consistent threshold handling across all plugins
- **Error Handling**: Robust error handling with detailed error messages
- **Security Scanning**: Regular security audits with bandit and safety

## Available Plugins

Note on legacy components: some older, standalone scripts (e.g., under `check_procs/` or `check_dig/`) previously vendored third‑party libraries. These vendored copies have been removed; if you still rely on those legacy scripts, install the appropriate extras (e.g., `pip install "nagios-plugins-collection[legacy]"`) or migrate to the modern plugins under `src/nagios_plugins/plugins/`.

The collection includes plugins for monitoring:

- **check_component_status**: Generic component/status checks with thresholds
- **check_dig**: DNS resolution checks
- **check_hadoop**: Hadoop/YARN/HDFS health checks
- **check_jobs**: Job execution monitoring
- **check_monghealth**: Legacy MongoDB health checks (modern alternative: check_mongodb_health)
- **check_mongodb_health**: MongoDB health and performance
- **check_ro_mounts**: Detect read-only mounts on a system
- **check_website_status**: Simple website status and content checks

## Installation

```bash
# Basic installation
pip install nagios-plugins-collection

# With development dependencies
pip install "nagios-plugins-collection[dev]"

# With security tools
pip install "nagios-plugins-collection[security]"

# With all extras
pip install "nagios-plugins-collection[all]"
```

## Quick Start

Example usage:

```bash
# Check Hadoop cluster
check_hadoop command --url=http://hadoop-master:8088/ws/v1/cluster/info

# Check MongoDB health
check_monghealth --host=mongodb.example.com --port=27017 --warning=80 --critical=90

# Check component status (example)
check_component_status --warning=75 --critical=90

# Check read-only mounts
check_ro_mounts --exclude=/proc,/sys,/dev

# Check website status
check_website_status --url=https://example.com --pattern="Welcome" --timeout=10

# Get JSON output
check_website_status --url=https://example.com --pattern="Welcome" --timeout=10 --json
```

## Documentation

For full documentation, visit [nagios-plugins-collection.readthedocs.io](https://nagios-plugins-collection.readthedocs.io/).

## Install from GitHub Packages

If you prefer installing from GitHub Packages instead of PyPI:

- Create a fine-grained personal access token with the write:packages (for publishing) or read:packages (for install) scope. Do not paste the token into shell history.
- For installation, set an environment variable and use an extra index URL. Example:

```bash
export PIP_EXTRA_INDEX_URL="https://__token__:${GITHUB_PACKAGES_TOKEN}@pypi.pkg.github.com/thomasvincent/simple"
pip install --upgrade nagios-plugins-collection
```

Alternatively, configure `~/.pip/pip.conf`:

```
[global]
extra-index-url = https://pypi.pkg.github.com/thomasvincent/simple
```

Then authenticate using a credential helper (e.g., `~/.netrc`) or environment variables when invoking pip.

## Docker (end-to-end)

Build and run tests inside Docker:

```bash
docker build -f docker/Dockerfile -t nagios-plugins-collection:dev .
docker run --rm -it nagios-plugins-collection:dev pytest -q
```

Or with compose:

```bash
docker compose -f docker/docker-compose.yml up --build --abort-on-container-exit
```

Run a plugin inside the container:

```bash
docker run --rm nagios-plugins-collection:dev check_website_status --url=https://example.com --pattern=Example
```

## Helm (Kubernetes)

```bash
helm upgrade --install npc charts/nagios-plugins-collection \
  --set image.repository=ghcr.io/thomasvincent/nagios-plugins-collection \
  --set image.tag=latest \
  --set command="{check_website_status, --url=https://example.com, --pattern=Example}"
```

## Nomad

```bash
nomad job run deploy/nomad/nagios-plugins-collection.nomad.hcl
```

## Publishing

You can publish releases via GitHub Actions (recommended) or locally with Twine. Never paste tokens in plaintext; use environment variables/secrets.

### GitHub Actions (one-click)

- Publish to GitHub Packages: run the workflow "Publish to GitHub Packages" (on release or manual).
- Publish to PyPI: run "Publish to PyPI (manual)" and ensure the repo secret `PYPI_API_TOKEN` exists.
- Multi-destination: run "Publish Release (multi-destination)" and choose one of: `pypi`, `testpypi`, or `github-packages`. You can also set `dry-run=true` to only build and run `twine check`.

Required secrets
- For PyPI: `PYPI_API_TOKEN` (scoped to the package, from https://pypi.org/manage/account/token/)
- For TestPyPI: `TESTPYPI_API_TOKEN` (from https://test.pypi.org)
- GitHub Packages uses the built-in `GITHUB_TOKEN` (no extra setup).

### Local publish (manual)

Build and verify:

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
```

Upload to GitHub Packages (GPR):

```bash
export TWINE_USERNAME="${GITHUB_USER}"
export TWINE_PASSWORD="${GITHUB_TOKEN_WITH_write:packages}"
python -m twine upload --repository-url "https://pypi.pkg.github.com/thomasvincent" dist/*
```

Upload to TestPyPI:

```bash
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="{{TESTPYPI_API_TOKEN}}"
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Upload to PyPI:

```bash
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="{{PYPI_API_TOKEN}}"
python -m twine upload dist/*
```

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/thomasvincent/nagios-plugins-collection.git
cd nagios-plugins-collection

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev,security]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run linting
tox -e lint

# Run type checking
tox -e type

# Run security checks
tox -e security
```

See the [Development Guide](https://nagios-plugins-collection.readthedocs.io/en/latest/development.html) for more information.

## Contributing

Contributions are welcome! See the [Contributing Guide](https://nagios-plugins-collection.readthedocs.io/en/latest/contributing.html) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
