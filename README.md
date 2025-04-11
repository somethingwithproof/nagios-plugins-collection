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

The collection includes plugins for monitoring:

- **check_hadoop**: Monitor Hadoop clusters and HDFS
- **check_monghealth**: Monitor MongoDB health and performance
- **check_procs**: Check processes on remote systems via SSH
- **check_mounts**: Check for read-only mounts on a system
- **check_counters_db**: Monitor Vertica database counters
- **check_dig**: Check DNS resolution
- **check_etl**: Monitor ETL processes
- **check_http500**: Check for HTTP 500 errors
- **check_jobs**: Monitor job execution
- **check_scribe**: Monitor Scribe log aggregation
- **check_statusthroughweb**: Check status through a web interface
- **check_website_status**: Check website status
- **check_advanced_website_status**: Advanced website status checking
- **membase_stats**: Monitor Membase/Couchbase statistics
- **url_monitor**: Monitor URLs for availability and content
- **xml_url_checker**: Check XML content from URLs

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

# Check processes
check_procs --host=server.example.com --process=nginx --min=1 --max=10

# Check read-only mounts
check_mounts --exclude=/proc,/sys,/dev

# Check website status
check_website_status --url=https://example.com --pattern="Welcome" --timeout=10

# Get JSON output
check_website_status --url=https://example.com --pattern="Welcome" --timeout=10 --json
```

## Documentation

For full documentation, visit [nagios-plugins-collection.readthedocs.io](https://nagios-plugins-collection.readthedocs.io/).

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
