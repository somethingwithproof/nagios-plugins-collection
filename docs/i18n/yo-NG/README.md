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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · **Yorùbá** · [isiZulu](../zu-ZA/README.md)

</details>

Àkójọ Python kan ti àwọn àyẹ̀wò àbójútó pẹ̀lú àwọn ojú-ìbẹ̀rẹ̀ àṣẹ fún àwọn iṣẹ́-ìsìn wẹ́ẹ̀bù, àwọn ibi-ìpamọ́ dátà, DNS, àwọn ìwé-ẹ̀rí, àwọn ohun-èlò ìpìlẹ̀, àti àwọn ohun-èlò ìkùukùu. Ìmúṣẹ àfikún kọ̀ọ̀kan ni ó ń ṣàlàyé àwọn àṣàyàn rẹ̀, ìtumọ̀ èsì rẹ̀, àti àwọn ìgbẹ́kẹ̀lé àṣàyàn rẹ̀.

## Àwọn ojú-ìbẹ̀rẹ̀ tó wà

A ṣàlàyé àwọn orúkọ wọ̀nyí nínú [pyproject.toml](../../../pyproject.toml) wọ́n sì ní àwọn fáìlì orísun tí ó bá wọn mu:

| Àṣẹ | Ìmúṣẹ |
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

Ka `--help` àti ìmúṣẹ àyẹ̀wò kọ̀ọ̀kan ṣáájú kí o tó ṣètò àwọn ààlà. A kò gbọ́dọ̀ gbà pé ìwà JSON, ìparí àkókò, dátà iṣẹ́-ṣíṣe, àti ìdánimọ̀ jọra lórí gbogbo àfikún.

## Ìfisórí láti orísun

Àkọsílẹ̀ ètò náà nílò Python >=3.11,<3.15. [packaging/platform-support.json](../../../packaging/platform-support.json) ṣe àkọsílẹ̀ àwọn àfojúsùn àkókò-ìṣiṣẹ́ àti ìdìpọ̀ tí a ti ṣàyẹ̀wò. Láti inú ẹ̀dà ibi-ìpamọ́ yìí:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` ń fi àwọn ìgbẹ́kẹ̀lé tí a tì pa, àwọn irinṣẹ́ ìdàgbàsókè àti iṣẹ́-àkànṣe náà sínú `.venv/`; lo `uv sync --locked --no-dev --extra aws` (fún àpẹẹrẹ) fún àyíká àkókò-ìṣiṣẹ́ nìkan. A ṣàlàyé àwọn àfikún tó wà nínú àkọsílẹ̀ ètò náà; fi àwọn ìṣọ̀kan tí o nílò nìkan sórí ẹ̀rọ. A fi ìfisórí orísun hàn láìsọ pé a ti tẹ̀ ẹ́ jáde lórí àkójọ àpò.

## Ìbáramu àti àwọn iṣẹ́-ìṣe

Láti ṣe àwọn àyẹ̀wò lórí Kubernetes tàbí Nomad, lo àtẹ Helm nínú [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) tàbí iṣẹ́ náà nínú [deploy/nomad](../../../deploy/nomad); [ìtọ́sọ́nà ìfisórí](../../../docs/source/installation.rst#containers-and-kubernetes) ní àwọn àpẹẹrẹ Helm àti Nomad pípé, títí kan àwọn àṣírí tí a pèsè láti inú Kubernetes Secret tàbí Nomad Variable.

Lo [MIGRATION.md](../../../MIGRATION.md) fún àwọn àkọsílẹ̀ ìṣípòpadà ti ìtàn, ṣùgbọ́n ṣàyẹ̀wò àwọn orúkọ àṣẹ àti àwọn àṣàyàn pẹ̀lú ẹ̀dà ibi-ìpamọ́ yìí. Àyípadà ẹ̀dà Python, àwọn àmì irú dátà, tàbí ìṣètò CI kò fìdí ìwà àìyípadà múlẹ̀ fún gbogbo àyẹ̀wò àtijọ́. Àwọn iṣẹ́-ìsìn òde àti àwọn irinṣẹ́ pẹpẹ gbọ́dọ̀ wà fún àyẹ̀wò tí a ń ṣe.

## Ìsọdèdè

Ìrànlọ́wọ́ ìlà-àṣẹ àjọpín àti àwọn ìfiránṣẹ́ ìwádìí ṣe àtìlẹ́yìn fún èdè agbègbè 45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) nípa lílo àwọn àkójọ tí a dì pọ̀ tí stdlib ń gbé jáde. Ìyànjú ń ṣàyẹ̀wò `--lang`, lẹ́yìn náà `LC_ALL`, `LC_MESSAGES`, àti `LANG`, ó sì ń padà sí `en`. Àwọn ìṣáájú ipò Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), dátà iṣẹ́-ṣíṣe, àti àwọn kọ́kọ́rọ́ JSON kò ní yípadà ní gbogbo èdè agbègbè.

## Ìdàgbàsókè

Àwọn àyẹ̀wò àti ìṣètò irinṣẹ́ wà nínú [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock), àti [ìṣàn-iṣẹ́ CI](../../../.github/workflows/ci.yml); ṣe àwọn àyẹ̀wò pẹ̀lú `uv run pytest`. A kò sọ pé a ní ìpín ìbòjútó pàtó kan, àṣeyọrí àyẹ̀wò irú dátà tó le níbi gbogbo, tàbí ìwé-ẹ̀rí ẹ̀wọ̀n ìpèsè níbí.

## Ààbò àti ìwé-àṣẹ

Wo [SECURITY.md](../../../SECURITY.md). Orísun náà ń lo [ìwé-àṣẹ Apache-2.0](../../../LICENSE). [packaging/license-policy.json](../../../packaging/license-policy.json) ṣe àkọsílẹ̀ ìlànà ìwé-àṣẹ ìgbẹ́kẹ̀lé.
