<!--
SPDX-FileCopyrightText: 2025 Thomas Vincent
SPDX-License-Identifier: Apache-2.0
-->

# Nagios Plugins Collection

[![CI](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=somethingwithproof_nagios-plugins-collection&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=somethingwithproof_nagios-plugins-collection)
[![codecov](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection/branch/main/graph/badge.svg)](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection)
[![Release](https://img.shields.io/github/v/release/somethingwithproof/nagios-plugins-collection)](https://github.com/somethingwithproof/nagios-plugins-collection/releases)
[![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/somethingwithproof/nagios-plugins-collection/main/pyproject.toml)](./pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/nagios-plugins-collection/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/nagios-plugins-collection)

**Languages:** **English** · [Deutsch](docs/i18n/de/README.md) · [Español](docs/i18n/es/README.md) · [Français](docs/i18n/fr/README.md) · [Italiano](docs/i18n/it/README.md) · [Português (BR)](docs/i18n/pt-BR/README.md) · [Nederlands](docs/i18n/nl/README.md) · [Русский](docs/i18n/ru/README.md) · [Українська](docs/i18n/uk/README.md) · [日本語](docs/i18n/ja/README.md) · [한국어](docs/i18n/ko/README.md) · [简体中文](docs/i18n/zh-CN/README.md) · [繁體中文](docs/i18n/zh-TW/README.md) · [العربية](docs/i18n/ar/README.md) · [हिन्दी](docs/i18n/hi/README.md) · [Polski](docs/i18n/pl/README.md) · [Türkçe](docs/i18n/tr/README.md) · [Svenska](docs/i18n/sv/README.md) · [Tiếng Việt](docs/i18n/vi/README.md) · [Bahasa Indonesia](docs/i18n/id/README.md)

<details><summary>More languages (28 locales)</summary>

[Afrikaans](docs/i18n/af-ZA/README.md) · [አማርኛ](docs/i18n/am-ET/README.md) · [العربية (مصر)](docs/i18n/ar-EG/README.md) · [العربية (المغرب)](docs/i18n/ar-MA/README.md) · [বাংলা](docs/i18n/bn/README.md) · [Bosanski](docs/i18n/bs/README.md) · [فارسی](docs/i18n/fa/README.md) · [Filipino](docs/i18n/fil/README.md) · [Français (Maroc)](docs/i18n/fr-MA/README.md) · [Français (Sénégal)](docs/i18n/fr-SN/README.md) · [Hausa](docs/i18n/ha-NG/README.md) · [עברית](docs/i18n/he/README.md) · [Hrvatski](docs/i18n/hr/README.md) · [Igbo](docs/i18n/ig-NG/README.md) · [Malagasy](docs/i18n/mg-MG/README.md) · [मराठी](docs/i18n/mr/README.md) · [Bahasa Melayu](docs/i18n/ms/README.md) · [Kinyarwanda](docs/i18n/rw-RW/README.md) · [Soomaali](docs/i18n/so-SO/README.md) · [Српски](docs/i18n/sr/README.md) · [Kiswahili](docs/i18n/sw-KE/README.md) · [தமிழ்](docs/i18n/ta/README.md) · [తెలుగు](docs/i18n/te/README.md) · [ไทย](docs/i18n/th/README.md) · [اردو](docs/i18n/ur/README.md) · [isiXhosa](docs/i18n/xh-ZA/README.md) · [Yorùbá](docs/i18n/yo-NG/README.md) · [isiZulu](docs/i18n/zu-ZA/README.md)

</details>

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
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` installs the locked dependencies, the development tools and the project into `.venv/`; use `uv sync --locked --no-dev --extra aws` (for example) for a runtime-only environment. The available extras are defined in the manifest; install only the integrations you need. Source installation is shown without asserting package-index publication.

## Compatibility and operations

To run checks on Kubernetes or Nomad, use the Helm chart in [charts/nagios-plugins-collection](charts/nagios-plugins-collection) or the job in [deploy/nomad](deploy/nomad); the [installation guide](docs/source/installation.rst#containers-and-kubernetes) has complete Helm and Nomad examples, including secrets supplied from a Kubernetes Secret or a Nomad Variable.

Use [MIGRATION.md](MIGRATION.md) for historical migration notes, but verify command names and options against this checkout. A Python-version change, type hints, or CI configuration do not establish unchanged behavior for every legacy check. External services and platform tools must be available for the check being run.

## Localization

Shared CLI help and diagnostic messages support 48 locales (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`, `bs`, `hr`, `sr`) using bundled stdlib-loaded catalogs. Resolution checks `--lang`, then `LC_ALL`, `LC_MESSAGES`, and `LANG`, falling back to `en`. Nagios status prefixes (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), performance data, and JSON keys remain unchanged across all locales.

## Development

Tests and tool configuration live in [pyproject.toml](pyproject.toml), [uv.lock](uv.lock), and [the CI workflow](.github/workflows/ci.yml); run tests with `uv run pytest`. No fixed coverage percentage, universal strict-type-checking success, or supply-chain certification is claimed here.

## Security and license

See [SECURITY.md](SECURITY.md). The source uses the [Apache-2.0 license](LICENSE). [packaging/license-policy.json](packaging/license-policy.json) records the dependency-license policy.
