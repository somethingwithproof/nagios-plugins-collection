# Nagios Plugins Collection

[![GitHub Actions](https://github.com/thomasvincent/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg)](https://github.com/thomasvincent/nagios-plugins-collection/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/nagios-plugins-collection.svg)](https://badge.fury.io/py/nagios-plugins-collection)
[![Python Versions](https://img.shields.io/pypi/pyversions/nagios-plugins-collection.svg)](https://pypi.org/project/nagios-plugins-collection/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/nagios-plugins-collection/badge/?version=latest)](https://nagios-plugins-collection.readthedocs.io/en/latest/?badge=latest)

A collection of enterprise-grade Nagios plugins for monitoring various systems.

## Features

- **Consistent Interface**: All plugins follow the same command-line interface pattern, making them easy to use and integrate.
- **Comprehensive Documentation**: Each plugin is thoroughly documented, with examples and usage information.
- **Extensive Test Coverage**: All plugins have unit and integration tests to ensure they work correctly.
- **Multi-Version Support**: The plugins support multiple Python versions (3.7+) and Nagios versions (4.4.6+).
- **Performance Data**: All plugins provide performance data that can be used for trending and analysis.
- **Threshold Handling**: Consistent threshold handling across all plugins, following Nagios plugin development guidelines.
- **Error Handling**: Robust error handling to ensure plugins fail gracefully and provide useful error messages.

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
pip install nagios-plugins-collection
```

For development:

```bash
pip install -e ".[dev]"
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
```

## Documentation

For full documentation, visit [nagios-plugins-collection.readthedocs.io](https://nagios-plugins-collection.readthedocs.io/).

## Development

See the [Development Guide](https://nagios-plugins-collection.readthedocs.io/en/latest/development.html) for information on setting up a development environment, running tests, and building documentation.

## Contributing

Contributions are welcome! See the [Contributing Guide](https://nagios-plugins-collection.readthedocs.io/en/latest/contributing.html) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
