<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: Apache-2.0
-->

# Nagios Plugins Collection

[![CI](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=somethingwithproof_nagios-plugins-collection&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=somethingwithproof_nagios-plugins-collection)
[![codecov](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection/branch/main/graph/badge.svg)](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection)
[![Release](https://img.shields.io/github/v/release/somethingwithproof/nagios-plugins-collection)](https://github.com/somethingwithproof/nagios-plugins-collection/releases)
[![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/somethingwithproof/nagios-plugins-collection/main/pyproject.toml)](../../../pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](../../../LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/nagios-plugins-collection/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/nagios-plugins-collection)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · **Nederlands** · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Een Python-verzameling van monitoringchecks met commando-ingangspunten voor webdiensten, databases, DNS, certificaten, infrastructuur en cloudresources. De implementatie van elke plugin bepaalt de eigen opties, resultaatsemantiek en optionele afhankelijkheden.

## Beschikbare ingangspunten

De volgende namen zijn gedeclareerd in [pyproject.toml](../../../pyproject.toml) en hebben bijbehorende bronbestanden:

| Commando | Implementatie |
| --- | --- |
| `check_website_status` | [check_website_status](../../../src/nagios_plugins/plugins/check_website_status.py) |
| `check_component_status` | [check_component_status](../../../src/nagios_plugins/plugins/check_component_status.py) |
| `check_mongodb_health` | [check_mongodb_health](../../../src/nagios_plugins/plugins/check_mongodb_health.py) |
| `check_ro_mounts` | [check_ro_mounts](../../../src/nagios_plugins/plugins/check_ro_mounts.py) |
| `check_tls_expiry` | [check_tls_expiry](../../../src/nagios_plugins/plugins/check_tls_expiry.py) |
| `check_prometheus_query` | [check_prometheus_query](../../../src/nagios_plugins/plugins/check_prometheus_query.py) |
| `check_http_sli` | [check_http_sli](../../../src/nagios_plugins/plugins/check_http_sli.py) |
| `check_dns_health` | [check_dns_health](../../../src/nagios_plugins/plugins/check_dns_health.py) |
| `check_k8s_node_status` | [check_k8s_node_status](../../../src/nagios_plugins/plugins/check_k8s_node_status.py) |
| `check_postgres_replication_lag` | [check_postgres_replication_lag](../../../src/nagios_plugins/plugins/check_postgres_replication_lag.py) |
| `check_queue_depth` | [check_queue_depth](../../../src/nagios_plugins/plugins/check_queue_depth.py) |
| `check_oauth2_token` | [check_oauth2_token](../../../src/nagios_plugins/plugins/check_oauth2_token.py) |
| `check_redis_saturation` | [check_redis_saturation](../../../src/nagios_plugins/plugins/check_redis_saturation.py) |
| `check_log_errors` | [check_log_errors](../../../src/nagios_plugins/plugins/check_log_errors.py) |
| `check_cloud_budget` | [check_cloud_budget](../../../src/nagios_plugins/plugins/check_cloud_budget.py) |
| `check_backup_freshness` | [check_backup_freshness](../../../src/nagios_plugins/plugins/check_backup_freshness.py) |
| `check_aws_cloudwatch` | [check_aws_cloudwatch](../../../src/nagios_plugins/plugins/check_aws_cloudwatch.py) |
| `check_monghealth` | [check_monghealth](../../../src/nagios_plugins/plugins/check_monghealth.py) |
| `check_hadoop` | [check_hadoop](../../../src/nagios_plugins/plugins/check_hadoop.py) |
| `check_dig` | [check_dig](../../../src/nagios_plugins/plugins/check_dig.py) |
| `check_jobs` | [check_jobs](../../../src/nagios_plugins/plugins/check_jobs.py) |

Lees `--help` en de implementatie van de afzonderlijke check voordat je drempelwaarden configureert. Ga er niet van uit dat JSON-, timeout-, performance-data- en authenticatiegedrag bij elke plugin identiek zijn.

## Installeren vanuit broncode

Het manifest vereist Python >=3.11,<3.15. [packaging/platform-support.json](../../../packaging/platform-support.json) legt de beoordeelde runtime- en packaging-doelen vast. Vanuit deze checkout:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` installeert de vergrendelde afhankelijkheden, de ontwikkeltools en het project in `.venv/`; gebruik bijvoorbeeld `uv sync --locked --no-dev --extra aws` voor een omgeving met alleen de runtime. De beschikbare extras zijn gedefinieerd in het manifest; installeer alleen de integraties die je nodig hebt. Installatie vanuit de broncode wordt getoond zonder publicatie in een pakketindex te claimen.

## Compatibiliteit en beheer

Om checks uit te voeren op Kubernetes of Nomad gebruik je de Helm-chart in [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) of de job in [deploy/nomad](../../../deploy/nomad); de [installatiehandleiding](../../../docs/source/installation.rst#containers-and-kubernetes) bevat volledige Helm- en Nomad-voorbeelden, inclusief secrets die worden aangeleverd vanuit een Kubernetes Secret of een Nomad Variable.

Gebruik [MIGRATION.md](../../../MIGRATION.md) voor historische migratie-opmerkingen, maar controleer commandonamen en opties altijd aan de hand van deze checkout. Een wijziging in Python-versie, type hints of CI-configuratie garandeert niet dat het gedrag van elke oudere check ongewijzigd is gebleven. Externe diensten en platformtools moeten beschikbaar zijn voor de check die wordt uitgevoerd.

## Lokalisatie

Gedeelde CLI-help en diagnostische berichten ondersteunen 45 locales (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) via meegeleverde catalogi die met stdlib worden geladen. De bepaling controleert `--lang`, daarna `LC_ALL`, `LC_MESSAGES` en `LANG`, met `en` als terugvaloptie. Nagios-statusvoorvoegsels (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), performance data en JSON-sleutels blijven in alle locales ongewijzigd.

## Ontwikkeling

Tests en toolconfiguratie staan in [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock) en [de CI-workflow](../../../.github/workflows/ci.yml); voer tests uit met `uv run pytest`. Er wordt hier geen vast dekkingspercentage, universele slagingsgarantie voor strikte typecontrole of supply-chain-certificering geclaimd.

## Beveiliging en licentie

Zie [SECURITY.md](../../../SECURITY.md). De broncode gebruikt de [Apache-2.0-licentie](../../../LICENSE). [packaging/license-policy.json](../../../packaging/license-policy.json) legt het licentiebeleid voor afhankelijkheden vast.
