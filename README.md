<!--
SPDX-FileCopyrightText: 2025 Thomas Vincent
SPDX-License-Identifier: Apache-2.0
-->

# Nagios Plugins Collection

[![CI](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache-2.0-blue)](./LICENSE)
[![Python requirement](https://img.shields.io/badge/Python_requirement-%3E%3D3.11%2C%3C3.15-blue)](./pyproject.toml)

A Python collection of monitoring checks with command entry points for web services, databases, DNS, certificates, infrastructure, and cloud resources. Each plugin's implementation defines its options, result semantics, and optional dependencies.

## Available entry points

The following names are declared in [pyproject.toml](pyproject.toml) and have corresponding source files:

| Command | Implementation |
| --- | --- |
| `check_website_status` | [check_website_status](src/nagios_plugins/plugins/check_website_status.py) |
| `check_component_status` | [check_component_status](src/nagios_plugins/plugins/check_component_status.py) |
| `check_mongodb_health` | [check_mongodb_health](src/nagios_plugins/plugins/check_mongodb_health.py) |
| `check_ro_mounts` | [check_ro_mounts](src/nagios_plugins/plugins/check_ro_mounts.py) |
| `check_tls_expiry` | [check_tls_expiry](src/nagios_plugins/plugins/check_tls_expiry.py) |
| `check_prometheus_query` | [check_prometheus_query](src/nagios_plugins/plugins/check_prometheus_query.py) |
| `check_http_sli` | [check_http_sli](src/nagios_plugins/plugins/check_http_sli.py) |
| `check_dns_health` | [check_dns_health](src/nagios_plugins/plugins/check_dns_health.py) |
| `check_k8s_node_status` | [check_k8s_node_status](src/nagios_plugins/plugins/check_k8s_node_status.py) |
| `check_postgres_replication_lag` | [check_postgres_replication_lag](src/nagios_plugins/plugins/check_postgres_replication_lag.py) |
| `check_queue_depth` | [check_queue_depth](src/nagios_plugins/plugins/check_queue_depth.py) |
| `check_oauth2_token` | [check_oauth2_token](src/nagios_plugins/plugins/check_oauth2_token.py) |
| `check_redis_saturation` | [check_redis_saturation](src/nagios_plugins/plugins/check_redis_saturation.py) |
| `check_log_errors` | [check_log_errors](src/nagios_plugins/plugins/check_log_errors.py) |
| `check_cloud_budget` | [check_cloud_budget](src/nagios_plugins/plugins/check_cloud_budget.py) |
| `check_backup_freshness` | [check_backup_freshness](src/nagios_plugins/plugins/check_backup_freshness.py) |
| `check_aws_cloudwatch` | [check_aws_cloudwatch](src/nagios_plugins/plugins/check_aws_cloudwatch.py) |
| `check_monghealth` | [check_monghealth](src/nagios_plugins/plugins/check_monghealth.py) |
| `check_hadoop` | [check_hadoop](src/nagios_plugins/plugins/check_hadoop.py) |
| `check_dig` | [check_dig](src/nagios_plugins/plugins/check_dig.py) |
| `check_jobs` | [check_jobs](src/nagios_plugins/plugins/check_jobs.py) |

Read the individual check's `--help` and implementation before configuring thresholds. JSON, timeout, performance-data, and authentication behavior should not be assumed identical across every plugin.

## Install from source

The manifest requires Python >=3.11,<3.15. [packaging/platform-support.json](packaging/platform-support.json) records the reviewed runtime and packaging targets. From this checkout:

```bash
uv venv
uv pip install -e ".[all]"
check_tls_expiry --help
```

Run the command in the created virtual environment or use its `.venv/bin/` path. The available extras are defined in the manifest; install only the integrations you need. Source installation is shown without asserting package-index publication.

## Compatibility and operations

Use [MIGRATION.md](MIGRATION.md) for historical migration notes, but verify command names and options against this checkout. A Python-version change, type hints, or CI configuration do not establish unchanged behavior for every legacy check. External services and platform tools must be available for the check being run.

## Development

Tests and tool configuration live in [pyproject.toml](pyproject.toml), [tox.ini](tox.ini), and [the CI workflow](.github/workflows/ci.yml). No fixed coverage percentage, universal strict-type-checking success, or supply-chain certification is claimed here.

## Security and license

See [SECURITY.md](SECURITY.md). The source uses the [Apache-2.0 license](LICENSE). [packaging/license-policy.json](packaging/license-policy.json) records the dependency-license policy.
