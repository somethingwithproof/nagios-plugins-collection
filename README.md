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

- Modern Python: Requires Python 3.11+ with type hints and strict linting/typing (ruff, mypy)
- Async support where it matters (httpx, asyncio) for high fan‑out checks
- JSON output across plugins for easy ingestion
- Consistent CLI interface with common flags: `--timeout`, `--warning`, `--critical`, `--json`, `--verbose`
- Performance data (Nagios perfdata) standard across checks
- CI/CD with tests, coverage, SBOM generation, Trivy scanning, and cosign signing
- Kubernetes Helm chart and Nomad job provided for scheduled runs
- Security scanning with bandit/safety and dependency pinning

## Available Plugins (modern set)

Note on legacy components: legacy standalone scripts were removed. Prefer the modern, typed plugins under `src/nagios_plugins/plugins/`. Install extras with `pip install "nagios-plugins-collection[all]"` or a subset (e.g., `[aws]`, `[k8s]`, `[pg]`, `[redis]`, `[prom]`, `[dns]`, `[es]`).

Core plugins:
- check_tls_expiry: Verify TLS certificate expiry and chain health
- check_dns_health: DNS resolution/NS health (dnspython optional)
- check_prometheus_query: Evaluate PromQL expressions and threshold results
- check_http_sli: Measure latency percentiles and error rate for an endpoint
- check_log_errors: Count error patterns via Elastic/OpenSearch HTTP
- check_k8s_node_status: Summarize Kubernetes node health (client optional)
- check_postgres_replication_lag: Lag in seconds via SQL (psycopg optional)
- check_queue_depth: AWS SQS queue depth/inflight (boto3 optional)
- check_redis_saturation: Redis memory/evictions/hitrates (redis-py)
- check_backup_freshness: Age of latest S3 object by prefix (boto3)
- check_cloud_budget: AWS Cost Explorer monthly spend (boto3)
- check_oauth2_token: Validate token endpoint and scopes

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

General install:
```bash
helm upgrade --install npc charts/nagios-plugins-collection \
  --set image.repository=ghcr.io/thomasvincent/nagios-plugins-collection \
  --set image.tag=latest \
  --set-json 'command=["check_http_sli","--url=https://example.com","--samples","5","--warning","0.2","--critical","0.5"]'
```

Examples per plugin (values overrides):

TLS expiry
```bash
helm upgrade --install tls charts/nagios-plugins-collection \
  --set-json 'command=["check_tls_expiry","--host","example.com","--port","443","--warning","14","--critical","7"]'
```

Prometheus query
```bash
helm upgrade --install prom charts/nagios-plugins-collection \
  --set-json 'command=["check_prometheus_query","--server","http://prometheus:9090","--query","sum(rate(http_requests_total[5m]))","--warning","100","--critical","200"]'
```

Kubernetes nodes
```bash
helm upgrade --install k8s charts/nagios-plugins-collection \
  --set-json 'command=["check_k8s_node_status","--label","node-role.kubernetes.io/worker=true"]'
```

AWS S3 backup freshness
```bash
helm upgrade --install backup charts/nagios-plugins-collection \
  --set-json 'command=["check_backup_freshness","--bucket","my-bucket","--prefix","backups/","--warning","3600","--critical","7200"]' \
  --set env[0].name=AWS_REGION --set env[0].value=us-east-1
```

## Nomad

General job file ships at `deploy/nomad/nagios-plugins-collection.nomad.hcl`. Override args per plugin. Examples:

HTTP SLI
```hcl
args = ["check_http_sli","--url=https://example.com","--samples","5","--warning","0.2","--critical","0.5"]
```

TLS Expiry
```hcl
args = ["check_tls_expiry","--host","example.com","--port","443","--warning","14","--critical","7"]
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
