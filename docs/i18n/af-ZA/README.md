<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: Apache-2.0
-->

# Nagios-inpropversameling

[![CI](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=somethingwithproof_nagios-plugins-collection&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=somethingwithproof_nagios-plugins-collection)
[![codecov](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection/branch/main/graph/badge.svg)](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection)
[![Release](https://img.shields.io/github/v/release/somethingwithproof/nagios-plugins-collection)](https://github.com/somethingwithproof/nagios-plugins-collection/releases)
[![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/somethingwithproof/nagios-plugins-collection/main/pyproject.toml)](./pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/nagios-plugins-collection/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/nagios-plugins-collection)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

**Afrikaans** · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

'n Python-versameling van moniteringskontroles met opdragingangspunte vir webdienste, databasisse, DNS, sertifikate, infrastruktuur en wolkhulpbronne. Elke inprop se implementering definieer sy opsies, resultaatsemantiek en opsionele afhanklikhede.

## Beskikbare ingangspunte

Die volgende name word in [pyproject.toml](../../../pyproject.toml) verklaar en het ooreenstemmende bronlêers:

| Opdrag | Implementering |
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

Lees die individuele kontrole se `--help` en implementering voordat jy drempels konfigureer. Daar moet nie aangeneem word dat JSON-, tydlimiet-, werkverrigtingsdata- en verifikasiegedrag identies oor elke inprop heen is nie.

## Installeer vanuit bronkode

Die manifes vereis Python >=3.11,<3.15. [packaging/platform-support.json](../../../packaging/platform-support.json) teken die hersiende looptyd- en verpakkingsteikens aan. Vanuit hierdie werkkopie:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` installeer die geslote afhanklikhede, die ontwikkelingsnutsgoed en die projek in `.venv/`; gebruik `uv sync --locked --no-dev --extra aws` (byvoorbeeld) vir 'n slegs-looptyd-omgewing. Die beskikbare ekstras word in die manifes gedefinieer; installeer slegs die integrasies wat jy nodig het. Broninstallasie word getoon sonder om pakketindeks-publikasie te beweer.

## Versoenbaarheid en bedrywighede

Om kontroles op Kubernetes of Nomad te laat loop, gebruik die Helm-kaart in [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) of die taak in [deploy/nomad](../../../deploy/nomad); die [installasiegids](../../../docs/source/installation.rst#containers-and-kubernetes) het volledige Helm- en Nomad-voorbeelde, insluitend geheime wat vanaf 'n Kubernetes Secret of 'n Nomad Variable verskaf word.

Gebruik [MIGRATION.md](../../../MIGRATION.md) vir historiese migrasie-aantekeninge, maar verifieer opdragname en opsies teen hierdie werkkopie. 'n Python-weergaweverandering, tipewenke of CI-konfigurasie vestig nie onveranderde gedrag vir elke ouer kontrole nie. Eksterne dienste en platformnutsgoed moet beskikbaar wees vir die kontrole wat uitgevoer word.

## Lokalisering

Gedeelde CLI-hulp en diagnostiese boodskappe ondersteun 45 lokale (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) deur gebundelde katalogusse te gebruik wat met stdlib gelaai word. Oplossing kontroleer `--lang`, dan `LC_ALL`, `LC_MESSAGES`, en `LANG`, en val terug na `en`. Nagios-statusvoorvoegsels (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), werkverrigtingsdata en JSON-sleutels bly onveranderd oor alle lokale heen.

## Ontwikkeling

Toetse en nutsmiddelkonfigurasie lê in [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock), en [die CI-werkvloei](../../../.github/workflows/ci.yml); voer toetse uit met `uv run pytest`. Geen vaste dekkingspersentasie, universele streng-tipekontrolesukses of voorsieningskettingsertifisering word hier beweer nie.

## Sekuriteit en lisensie

Sien [SECURITY.md](../../../SECURITY.md). Die bronkode gebruik die [Apache-2.0-lisensie](../../../LICENSE). [packaging/license-policy.json](../../../packaging/license-policy.json) teken die afhanklikheidslisensiebeleid aan.
