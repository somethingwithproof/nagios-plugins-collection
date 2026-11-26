<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · **Filipino** · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Isang Python na koleksyon ng mga monitoring check na may mga command entry point para sa mga web service, database, DNS, mga sertipiko, imprastraktura, at mga cloud resource. Tinutukoy ng implementasyon ng bawat plugin ang mga opsyon, semantika ng resulta, at mga opsyonal na dependency nito.

## Mga available na entry point

Ang mga sumusunod na pangalan ay nakadeklara sa [pyproject.toml](../../../pyproject.toml) at may mga kaukulang source file:

| Command | Implementasyon |
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

Basahin ang `--help` at implementasyon ng bawat check bago mag-configure ng mga threshold. Hindi dapat ipalagay na pare-pareho ang gawi ng JSON, timeout, performance-data, at authentication sa bawat plugin.

## Pag-install mula sa source

Kinakailangan ng manifest ang Python >=3.11,<3.15. Itinatala ng [packaging/platform-support.json](../../../packaging/platform-support.json) ang mga sinuring runtime at packaging target. Mula sa checkout na ito:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

Ini-install ng `uv sync` ang mga naka-lock na dependency, mga tool sa pag-develop, at ang proyekto sa `.venv/`; gamitin ang `uv sync --locked --no-dev --extra aws` (halimbawa) para sa isang runtime-only environment. Nakasaad sa manifest ang mga available na extra; i-install lamang ang mga integrasyong kailangan mo. Ipinapakita ang source installation nang hindi iginigiit ang paglalathala sa package-index.

## Compatibility at mga operasyon

Upang patakbuhin ang mga check sa Kubernetes o Nomad, gamitin ang Helm chart sa [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) o ang job sa [deploy/nomad](../../../deploy/nomad); ang [gabay sa pag-install](../../../docs/source/installation.rst#containers-and-kubernetes) ay may kumpletong mga halimbawa para sa Helm at Nomad, kabilang ang mga secret na ibinibigay mula sa isang Kubernetes Secret o isang Nomad Variable.

Gamitin ang [MIGRATION.md](../../../MIGRATION.md) para sa mga nakaraang tala sa paglipat, ngunit i-verify ang mga pangalan ng command at opsyon laban sa checkout na ito. Ang pagbabago sa bersyon ng Python, mga type hint, o configuration ng CI ay hindi nagpapatunay ng hindi nagbagong gawi para sa bawat legacy check. Dapat na available ang mga panlabas na serbisyo at platform tool para sa check na pinapatakbo.

## Localization

Sinusuportahan ng nakabahaging tulong sa CLI at mga mensahe ng diagnostic ang 45 locale (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) gamit ang mga naka-bundle na catalog na ni-load ng stdlib. Sinusuri ng pagresolba ang `--lang`, pagkatapos ay `LC_ALL`, `LC_MESSAGES`, at `LANG`, at bumabalik sa `en`. Nananatiling hindi nagbabago sa lahat ng locale ang mga Nagios status prefix (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), performance data, at mga JSON key.

## Pag-develop

Nasa [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock), at [sa CI workflow](../../../.github/workflows/ci.yml) ang mga test at configuration ng tool; patakbuhin ang mga test gamit ang `uv run pytest`. Walang nakatakdang porsyento ng coverage, pangkalahatang tagumpay ng strict-type-checking, o sertipikasyon ng supply-chain na inaangkin dito.

## Seguridad at lisensya

Tingnan ang [SECURITY.md](../../../SECURITY.md). Gumagamit ang source ng [Apache-2.0 license](../../../LICENSE). Itinatala ng [packaging/license-policy.json](../../../packaging/license-policy.json) ang patakaran sa dependency-license.
