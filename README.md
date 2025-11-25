# Nagios Plugins Collection

[![CI](https://github.com/thomasvincent/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg)](https://github.com/thomasvincent/nagios-plugins-collection/actions/workflows/ci.yml)
[![Python](https://img.shields.io/pypi/pyversions/nagios-plugins-collection.svg)](https://pypi.org/project/nagios-plugins-collection/)
[![License](https://img.shields.io/github/license/thomasvincent/nagios-plugins-collection.svg)](https://github.com/thomasvincent/nagios-plugins-collection/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A collection of production-ready Nagios monitoring plugins for various services and infrastructure components.

## Features

- **Modern Python** - Requires Python 3.9+, fully typed with type hints
- **Security First** - No shell injection vulnerabilities, credentials via environment variables
- **Comprehensive Metrics** - Rich performance data output for graphing
- **Flexible Thresholds** - Full Nagios range syntax support
- **Well Tested** - High test coverage with unit and integration tests
- **Easy Installation** - Available via pip with optional dependencies

## Plugins Included

| Plugin | Description |
|--------|-------------|
| `check_procs` | Monitor remote processes via SSH |
| `check_ro_mounts` | Detect read-only filesystem mounts |
| `check_dig` | DNS resolution monitoring |
| `check_hadoop` | Hadoop cluster health monitoring |
| `check_monghealth` | MongoDB health and replication monitoring |
| `check_jobs` | Job execution monitoring via JSON API |
| `check_website_status` | Website availability and content monitoring |
| `check_membase` | Membase/Couchbase statistics monitoring |

## Installation

### Basic Installation

```bash
pip install nagios-plugins-collection
```

### With Optional Dependencies

```bash
# For SSH-based plugins (check_procs, check_ro_mounts)
pip install nagios-plugins-collection[ssh]

# For MongoDB plugin
pip install nagios-plugins-collection[mongodb]

# All optional dependencies
pip install nagios-plugins-collection[all]

# Development dependencies
pip install nagios-plugins-collection[dev]
```

### From Source

```bash
git clone https://github.com/thomasvincent/nagios-plugins-collection.git
cd nagios-plugins-collection
pip install -e ".[dev]"
```

## Quick Start

### Check Website Status

```bash
# Basic check
check_website_status -U https://example.com

# Check for specific content
check_website_status -U https://example.com -s "Welcome"

# With timing thresholds
check_website_status -U https://example.com -w 2 -c 5
```

### Check Remote Processes

```bash
# Check httpd processes
check_procs -H webserver.example.com -C httpd -w 5:50 -c 1:100

# Filter by status flags (zombie processes)
check_procs -H server.example.com -s Z -c 0:0
```

### Check MongoDB Health

```bash
# Basic status
check_monghealth -H mongodb.example.com

# Check replication lag
check_monghealth -H mongodb.example.com -m replication -w 10 -c 60

# Check connection usage
check_monghealth -H mongodb.example.com -m connections -w 80 -c 90
```

### Check DNS Resolution

```bash
# Basic DNS check
check_dig -l example.com

# Check specific DNS server
check_dig -H 8.8.8.8 -l example.com

# Verify expected result
check_dig -l example.com -a 93.184.216.34
```

## Threshold Syntax

All plugins support standard Nagios threshold ranges:

| Format | Meaning |
|--------|---------|
| `10` | Alert if value is outside 0-10 range |
| `10:` | Alert if value is less than 10 |
| `~:10` | Alert if value is greater than 10 |
| `10:20` | Alert if value is outside 10-20 range |
| `@10:20` | Alert if value is inside 10-20 range |

## Environment Variables

For security, credentials should be passed via environment variables:

| Variable | Description |
|----------|-------------|
| `NAGIOS_SSH_USER` | Default SSH username for remote checks |
| `NAGIOS_SSH_PASS` | SSH password (prefer key-based auth) |
| `NAGIOS_SSH_KEY` | Path to SSH private key |
| `MONGO_PASSWORD` | MongoDB authentication password |
| `MEMBASE_PASSWORD` | Membase/Couchbase password |

## Nagios Configuration Example

```cfg
define command {
    command_name    check_remote_procs
    command_line    $USER1$/check_procs -H $HOSTADDRESS$ -C $ARG1$ -w $ARG2$ -c $ARG3$
}

define service {
    use                     generic-service
    host_name               webserver
    service_description     HTTP Processes
    check_command           check_remote_procs!httpd!5:50!1:100
}
```

## Docker

```bash
# Build image
docker build -t nagios-plugins .

# Run a check
docker run --rm nagios-plugins check_website_status -U https://example.com
```

## Development

### Setup

```bash
git clone https://github.com/thomasvincent/nagios-plugins-collection.git
cd nagios-plugins-collection
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/unit/test_check_procs.py -v
```

### Code Quality

```bash
# Format code
black src tests
isort src tests

# Lint
ruff check src tests

# Type check
mypy src

# Security scan
bandit -r src
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass and code is formatted
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Security

Please report security vulnerabilities privately. See [SECURITY.md](SECURITY.md) for our security policy and responsible disclosure process.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

Thomas Vincent - [thomas@thomasvincent.io](mailto:thomas@thomasvincent.io)

## Acknowledgments

- Nagios Plugins Development Team for the plugin guidelines
- Contributors to the monitoring community
