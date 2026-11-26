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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · **Igbo** · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Nchịkọta Python nke nnyocha nlekọta nwere ebe nbanye iwu maka ọrụ weebụ, nchekwa data, DNS, asambodo, akụrụngwa, na akụrụngwa igwe ojii (cloud). Mmejupụta ngwa mgbakwụnye ọ bụla na-akọwa nhọrọ ya, nkọwa nsonaazụ ya, na ihe ndabere nhọrọ ya.

## Ebe nbanye dịnụ

E kwupụtara aha ndị a na [pyproject.toml](../../../pyproject.toml) ma ha nwere faịlụ koodu isi kwekọrọ na ha:

| Iwu | Mmejupụta |
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

Gụọ `--help` na mmejupụta nke nnyocha ọ bụla tupu ị hazie oke. E kwesịghị iche na omume JSON, nkwụsị oge, data arụmọrụ, na nkwenye njirimara bụ otu n'ofe ngwa mgbakwụnye ọ bụla.

## Nwụnye site na koodu isi

Faịlụ manifest ahụ chọrọ Python >=3.11,<3.15. [packaging/platform-support.json](../../../packaging/platform-support.json) na-edekọ ebumnuche oge ọrụ na nkwakọba e nyochara. Site na mbudata koodu a:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` na-awụnye ihe ndabere a kpọchiri akpọchi, ngwaọrụ mmepe na ọrụ ahụ n'ime `.venv/`; jiri `uv sync --locked --no-dev --extra aws` (dị ka ọmụmaatụ) maka gburugburu naanị oge ọrụ. A kọwara mgbakwụnye (extras) dịnụ na manifest ahụ; wụnye naanị njikọta ndị dị gị mkpa. E gosipụtara nwụnye site na koodu isi na-ekwughị na e bipụtara ya na ndepụta ngwugwu (package index).

## Ndakọrịta na arụmọrụ

Iji gbaa nnyocha na Kubernetes ma ọ bụ Nomad, jiri chaatị Helm dị na [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) ma ọ bụ ọrụ dị na [deploy/nomad](../../../deploy/nomad); [ntuziaka nwụnye](../../../docs/source/installation.rst#containers-and-kubernetes) nwere ọmụmaatụ Helm na Nomad zuru ezu, gụnyere ihe nzuzo e nyere site na Kubernetes Secret ma ọ bụ Nomad Variable.

Jiri [MIGRATION.md](../../../MIGRATION.md) maka ndetu mbufe akụkọ ihe mere eme, mana nyochaa aha iwu na nhọrọ megide mbudata koodu a. Mgbanwe ụdị Python, ntụnye ụdị data (type hints), ma ọ bụ nhazi CI anaghị egosi omume na-agbanweghị maka nnyocha ochie ọ bụla. Ọrụ mpụga na ngwaọrụ ikpo okwu ga-adịrịrị maka nnyocha a na-agba.

## Nhazi asụsụ mpaghara

Enyemaka CLI na ozi nnyocha nkekọrịta na-akwado asụsụ mpaghara 45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) site n'iji katalọgụ jikọtara nke stdlib na-ebunye. Mkpebi asụsụ na-enyocha `--lang`, wee `LC_ALL`, `LC_MESSAGES`, na `LANG`, wee laghachi na `en`. Okwu mbido ọkwa Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), data arụmọrụ, na igodo JSON anaghị agbanwe n'asụsụ mpaghara niile.

## Mmepe

Nnwale na nhazi ngwaọrụ dị na [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock), na [usoro ọrụ CI](../../../.github/workflows/ci.yml); gbaa nnwale site na `uv run pytest`. Ọ dịghị pasentị mkpuchi a kara aka, ihe ịga nke ọma nnyocha ụdị siri ike zuru ụwa ọnụ, ma ọ bụ asambodo usoro nnyefe (supply-chain) e kwuru ebe a.

## Nchekwa na ikikere

Lee [SECURITY.md](../../../SECURITY.md). Koodu isi ahụ na-eji [ikikere Apache-2.0](../../../LICENSE). [packaging/license-policy.json](../../../packaging/license-policy.json) na-edekọ ụkpụrụ ikikere ihe ndabere.
