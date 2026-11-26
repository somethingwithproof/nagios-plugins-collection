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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · **Kinyarwanda** · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Itsinda ry'ibisuzuma byo gukurikirana sisitemu byanditse muri Python bifite amategeko yo gutangiza ku serivisi za urubuga, ububiko bw'amakuru (databases), DNS, ibyemezo by'umutekano (certificates), ibikorwa remezo, n'ibikoresho bya cloud. Ishyirwa mu bikorwa rya buri plugin rigennye amahitamo yayo, ubusobanuro bw'ibisubizo byayo, n'imishinga y'inyongera ishobora gusabwa.

## Amategeko yo gutangiza aboneka

Amazina akurikira yanditswe muri [pyproject.toml](../../../pyproject.toml) kandi afite dosiye za kode zihura na yo:

| Itegeko | Ishyirwa mu bikorwa |
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

Soma `--help` n'ishyirwa mu bikorwa rya buri gisuzuma mbere yo gushyiraho imipaka y'uburinzi (thresholds). Ntibikwiye gufatwa ko imikorere ya JSON, igihe ntarengwa (timeout), amakuru y'imikorere (performance-data), n'iyemeza ry'umwirondoro ihuje kuri buri plugin yose.

## Gushyiramo uhereye kuri kode

Dosiye y'imiterere isaba Python >=3.11,<3.15. [packaging/platform-support.json](../../../packaging/platform-support.json) ibika intego z'imikorere n'ipakira zasuzumwe. Uhereye kuri ubu bubiko:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` ishyira mu `.venv/` imishinga ikenewe ifunze, ibikoresho by'iterambere, n'uyu mushinga ubwawo; koresha `uv sync --locked --no-dev --extra aws` (nk'urugero) kugira ngo ubone ahantu ho gukorera gusa (runtime-only). Inyongera (extras) ziboneka zisobanurwa muri dosiye y'imiterere; shyiramo gusa ibyo ukeneye guhuza na byo. Gushyiramo uhereye kuri kode birerekanwa hatemejwe ko byashyizwe ku rubuga rw'amapaki.

## Ihuzwa n'imikorere

Kugira ngo ukoreshe ibisuzuma kuri Kubernetes cyangwa Nomad, koresha Helm chart iri muri [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) cyangwa job iri muri [deploy/nomad](../../../deploy/nomad); [inyoborabikorwa yo gushyiramo](../../../docs/source/installation.rst#containers-and-kubernetes) irimo ingero zuzuye za Helm na Nomad, harimo n'amabanga atangwa avuye muri Kubernetes Secret cyangwa Nomad Variable.

Koresha [MIGRATION.md](../../../MIGRATION.md) ku nyandiko z'amateka yo kwimuka, ariko ugenzure amazina y'amategeko n'amahitamo ugereranyije n'ubu bubiko. Impinduka ya verisiyo ya Python, type hints, cyangwa igenamiterere rya CI ntibihamya ko imikorere ya buri gisuzuma cya kera itahindutse. Serivisi zo hanze n'ibikoresho bya sisitemu bigomba kuba bihari kugira ngo igisuzuma kiri gukorwa kibashe gukora.

## Gushyira mu ndimi

Ubufasha buhuriweho ku murongo w'amabwiriza n'ubutumwa bw'isuzuma bishyigikira indimi 45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) hakoreshejwe urutonde rw'indimi rwashyizwemo rutwarwa na stdlib. Ihitamo ry'ururimi risuzuma `--lang`, hagakurikiraho `LC_ALL`, `LC_MESSAGES`, na `LANG`, hanyuma rigasubira kuri `en`. Ibirango bibanza by'imiterere ya Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), amakuru y'imikorere, n'imfunguzo za JSON biguma uko biri mu ndimi zose.

## Iterambere

Amasuzuma n'igenamiterere ry'ibikoresho biri muri [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock), no muri [workflow ya CI](../../../.github/workflows/ci.yml); kora amasuzuma ukoresheje `uv run pytest`. Nta kigero ntarengwa cy'isuzuma (coverage), intsinzi rusange ya strict-type-checking, cyangwa icyemezo cy'uruhererekane rw'ibikoresho (supply-chain) byemezwa hano.

## Umutekano n'uruhushya

Reba [SECURITY.md](../../../SECURITY.md). Kode ikoresha [uruhushya rwa Apache-2.0](../../../LICENSE). [packaging/license-policy.json](../../../packaging/license-policy.json) ibika politiki y'uruhushya rw'imishinga ikenewe.
