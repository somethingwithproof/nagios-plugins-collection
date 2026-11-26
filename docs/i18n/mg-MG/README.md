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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · **Malagasy** · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Angona Python mirakitra fitsirihana fanaraha-maso miaraka amin'ny teboka fidirana baiko ho an'ny tolotra tranonkala, angon-drakitra, DNS, taratasy fanamarinana, fotodrafitrasa, ary loharanon-karena cloud. Ny fampiharana ny plugin tsirairay no mamaritra ny safidiny, ny hevitry ny valiny, ary ny fiankinan-doha azo safidiana.

## Teboka fidirana misy

Ireto anarana manaraka ireto dia voalaza ao amin'ny [pyproject.toml](../../../pyproject.toml) ary manana rakitra loharano mifanaraka aminy:

| Baiko | Fampiharana |
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

Vakio ny `--help` sy ny fampiharana ny fitsirihana tsirairay alohan'ny hametrahana ny fetra. Tsy tokony hoheverina ho mitovy amin'ny plugin rehetra ny fitondran-tenan'ny JSON, ny fe-potoana, ny angona momba ny fahombiazana, ary ny fanamarinana maha-izy azy.

## Fametrahana avy amin'ny kaody loharano

Mitaky Python >=3.11,<3.15 ny manifest. Ny [packaging/platform-support.json](../../../packaging/platform-support.json) no mirakitra ireo tanjona fampandehanana sy famonosana voamarina. Avy amin'ity dika mitovy ity:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

Ny `uv sync` dia mametraka ireo fiankinan-doha voahidy, ireo fitaovana fampandrosoana ary ny tetikasa ao amin'ny `.venv/`; ampiasao ny `uv sync --locked --no-dev --extra aws` (ohatra) ho an'ny tontolo fampandehanana ihany. Voafaritra ao amin'ny manifest ireo fanampiny (extras) misy; apetraho ihany ny fampidirana ilainao. Aseho ny fametrahana avy amin'ny kaody loharano nefa tsy milaza fisian'ny famoahana amin'ny tondron'ny fonosana (package index).

## Fifanarahana sy fampandehanana

Raha te hampandeha fitsirihana ao amin'ny Kubernetes na Nomad, ampiasao ny Helm chart ao amin'ny [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) na ny job ao amin'ny [deploy/nomad](../../../deploy/nomad); misy ohatra feno momba ny Helm sy Nomad ao amin'ny [torolàlana fametrahana](../../../docs/source/installation.rst#containers-and-kubernetes), anisan'izany ny tsiambaratelo omena avy amin'ny Kubernetes Secret na Nomad Variable.

Ampiasao ny [MIGRATION.md](../../../MIGRATION.md) ho an'ny naoty fifindra-monina ara-tantara, saingy hamarino amin'ity dika mitovy ity ny anaran'ny baiko sy ny safidy. Ny fiovan'ny dikan-tenin'ny Python, ny toro-karazana (type hints), na ny fanefena CI dia tsy manaporofo fitondran-tena tsy niova ho an'ny fitsirihana taloha rehetra. Tsy maintsy misy ny tolotra ivelany sy ny fitaovan'ny sehatra ilain'ny fitsirihana tanterahina.

## Fiteny sy faritra

Ny fanampiana CLI iombonana sy ny hafatra fitiliana dia manohana fiteny sy faritra 45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) amin'ny alalan'ny katalogy tafiditra ao anatiny izay alaina amin'ny stdlib. Ny famaritana ny fiteny dia manamarina ny `--lang`, avy eo `LC_ALL`, `LC_MESSAGES`, ary `LANG`, ary miverina amin'ny `en`. Ny tovona satan'ny Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), ny angona momba ny fahombiazana, ary ny fanalahidy JSON dia tsy miova amin'ny fiteny rehetra.

## Fampandrosoana

Ao amin'ny [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock), ary [ny workflow CI](../../../.github/workflows/ci.yml) ny fitsapana sy ny fanefena fitaovana; tanteraho amin'ny `uv run pytest` ny fitsapana. Tsy misy isan-jaton'ny fandrakofana raikitra, fahombiazana feno amin'ny fanamarinana karazana henjana, na fanamarinana rojo famatsiana ambara eto.

## Fiarovana sy lisansa

Jereo ny [SECURITY.md](../../../SECURITY.md). Mampiasa ny [lisansa Apache-2.0](../../../LICENSE) ny kaody loharano. Ny [packaging/license-policy.json](../../../packaging/license-policy.json) no mirakitra ny politikan'ny lisansa ho an'ny fiankinan-doha.
