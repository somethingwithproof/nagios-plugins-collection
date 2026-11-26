<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: Apache-2.0
-->

# Mkusanyiko wa Programu-jalizi za Nagios

[![CI](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=somethingwithproof_nagios-plugins-collection&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=somethingwithproof_nagios-plugins-collection)
[![codecov](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection/branch/main/graph/badge.svg)](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection)
[![Release](https://img.shields.io/github/v/release/somethingwithproof/nagios-plugins-collection)](https://github.com/somethingwithproof/nagios-plugins-collection/releases)
[![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/somethingwithproof/nagios-plugins-collection/main/pyproject.toml)](../../../pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](../../../LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/nagios-plugins-collection/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/nagios-plugins-collection)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · **Kiswahili** · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Mkusanyiko wa Python wa ukaguzi wa ufuatiliaji wenye sehemu za kuingilia za amri kwa huduma za wavuti, hifadhidata, DNS, vyeti, miundombinu, na rasilimali za wingu. Utekelezaji wa kila programu-jalizi hufafanua chaguo zake, maana ya matokeo, na vitegemezi vya hiari.

## Sehemu za kuingilia zinazopatikana

Majina yafuatayo yametangazwa katika [pyproject.toml](../../../pyproject.toml) na yana faili chanzo zinazolingana:

| Amri | Utekelezaji |
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

Soma `--help` na utekelezaji wa ukaguzi husika kabla ya kusanidi viwango vya tahadhari. Tabia za JSON, muda wa kuisha, data ya utendakazi, na uthibitishaji hazipaswi kuchukuliwa kuwa zinafanana kwa kila programu-jalizi.

## Sakinisha kutoka kwa msimbo chanzo

Faili ya maelezo inahitaji Python >=3.11,<3.15. [packaging/platform-support.json](../../../packaging/platform-support.json) inarekodi mazingira ya uendeshaji na malengo ya ufungashaji yaliyokaguliwa. Kutoka kwenye nakala hii ya hazina:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` husakinisha vitegemezi vilivyofungwa, zana za uendelezaji na mradi ndani ya `.venv/`; tumia `uv sync --locked --no-dev --extra aws` (kwa mfano) kwa mazingira ya uendeshaji pekee. Nyenzo za ziada zinazopatikana zimefafanuliwa kwenye faili ya maelezo; sakinisha viunganishi unavyohitaji pekee. Usakinishaji wa msimbo chanzo umeonyeshwa bila kudai uchapishaji kwenye faharasa ya vifurushi.

## Utangamano na uendeshaji

Ili kuendesha ukaguzi kwenye Kubernetes au Nomad, tumia chati ya Helm katika [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) au kazi katika [deploy/nomad](../../../deploy/nomad); [mwongozo wa usakinishaji](../../../docs/source/installation.rst#containers-and-kubernetes) una mifano kamili ya Helm na Nomad, ikijumuisha siri zinazotolewa kutoka kwa Kubernetes Secret au Nomad Variable.

Tumia [MIGRATION.md](../../../MIGRATION.md) kwa maelezo ya kihistoria ya uhamishaji, lakini thibitisha majina ya amri na chaguo dhidi ya nakala hii ya hazina. Mabadiliko ya toleo la Python, vidokezo vya aina, au usanidi wa CI havithibitishi tabia isiyobadilika kwa kila ukaguzi wa zamani. Huduma za nje na zana za jukwaa lazima zipatikane kwa ukaguzi unaoendeshwa.

## Ujanibishaji

Usaidizi wa pamoja wa CLI na ujumbe wa uchunguzi unasaidia lugha 45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) kwa kutumia katalogi zilizopakiwa kutoka stdlib. Utatuzi hukagua `--lang`, kisha `LC_ALL`, `LC_MESSAGES`, na `LANG`, na kurudi kwenye `en`. Viambishi awali vya hali ya Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), data ya utendakazi, na funguo za JSON hubaki bila kubadilika katika lugha zote.

## Uendelezaji

Majaribio na usanidi wa zana viko katika [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock), na [mtiririko wa kazi wa CI](../../../.github/workflows/ci.yml); endesha majaribio kwa `uv run pytest`. Hakuna asilimia maalum ya majaribio, mafanikio ya ukaguzi mkali wa aina kwa wote, au uthibitishaji wa mnyororo wa ugavi unaodaiwa hapa.

## Usalama na leseni

Tazama [SECURITY.md](../../../SECURITY.md). Msimbo chanzo unatumia [leseni ya Apache-2.0](../../../LICENSE). [packaging/license-policy.json](../../../packaging/license-policy.json) inarekodi sera ya leseni za vitegemezi.
