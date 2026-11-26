<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: Apache-2.0
-->

# Iqoqo lama-Plugin e-Nagios

[![CI](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=somethingwithproof_nagios-plugins-collection&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=somethingwithproof_nagios-plugins-collection)
[![codecov](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection/branch/main/graph/badge.svg)](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection)
[![Release](https://img.shields.io/github/v/release/somethingwithproof/nagios-plugins-collection)](https://github.com/somethingwithproof/nagios-plugins-collection/releases)
[![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/somethingwithproof/nagios-plugins-collection/main/pyproject.toml)](./pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/nagios-plugins-collection/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/nagios-plugins-collection)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · **isiZulu**

</details>

Iqoqo le-Python lezivivinyo zokuqapha elinezindawo zokungena zemiyalo yezinsiza zewebhu, imininingwane egciniwe (databases), i-DNS, izitifiketi, ingqalasizinda, nezinsiza zamafu (cloud). Ukusetshenziswa kwe-plugin ngayinye kuchaza izinketho zayo, incazelo yemiphumela, kanye nokunye okuncikene nakho okungakhethwa.

## Izindawo zokungena ezitholakalayo

Amagama alandelayo amenyezelwe ku-[pyproject.toml](../../../pyproject.toml) futhi anamafayela ekhodi yomthombo ahambisanayo:

| Umyalo | Ukusetshenziswa kwekhodi |
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

Funda i-`--help` nokusetshenziswa kwekhodi kokuhlola ngakunye ngaphambi kokucusha imikhawulo (thresholds). Ukuziphatha kwe-JSON, ukuphela kwesikhathi (timeout), idatha yokusebenza, kanye nokuqinisekiswa kobunikazi akufanele kucatshangwe ukuthi kuyafana kuwo wonke ama-plugin.

## Faka kusukela kukhodi yomthombo

I-manifest idinga i-Python >=3.11,<3.15. I-[packaging/platform-support.json](../../../packaging/platform-support.json) irekhoda izinhloso zesikhathi sokusebenza nezokupakisha ezibuyekeziwe. Kusukela kule khophi ekhishiwe:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

I-`uv sync` ifaka okuncikene nakho okukhiyiwe, amathuluzi okuthuthukisa kanye nephrojekthi ku-`.venv/`; sebenzisa i-`uv sync --locked --no-dev --extra aws` (ngokwesibonelo) ukuze uthole indawo yesikhathi sokusebenza kuphela. Okungeziwe (extras) okutholakalayo kuchazwe ku-manifest; faka kuphela ukuhlanganiswa okudingayo. Ukufakwa kusukela kukhodi yomthombo kuboniswa ngaphandle kokugomela ukuthi kushicilelwe kunkomba yamaphakheji.

## Ukuhambisana nokusebenza

Ukuze usebenzise izivivinyo ku-Kubernetes noma ku-Nomad, sebenzisa i-Helm chart ku-[charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) noma umsebenzi ku-[deploy/nomad](../../../deploy/nomad); [umhlahlandlela wokufaka](../../../docs/source/installation.rst#containers-and-kubernetes) unezibonelo eziphelele ze-Helm ne-Nomad, okuhlanganisa izimfihlo ezihlinzekwa nge-Kubernetes Secret noma i-Nomad Variable.

Sebenzisa i-[MIGRATION.md](../../../MIGRATION.md) ukuze uthole amanothi omlando wokuthutha, kodwa qinisekisa amagama emiyalo nezinketho ngokuqhathanisa nale khophi ekhishiwe. Ukushintsha kwenguqulo ye-Python, amacebiso ezinhlobo zedatha (type hints), noma ukucushwa kwe-CI akuqinisekisi ukuthi ukuziphatha akushintshile kuzo zonke izivivinyo zakudala. Izinsiza zangaphandle namathuluzi epulatifomu kufanele kutholakale ngesivivinyo esisetshenziswayo.

## Ukuhunyushelwa ezilimini zendawo

Usizo lwe-CLI olwabiwe nemilayezo yokuxilonga kusekela izilimi zendawo ezingu-45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) kusetshenziswa amakhathalogi ahlanganiswe nalolu hlelo alayishwa nge-stdlib. Ukukhethwa kolimi kuhlolwa ku-`--lang`, kulandele i-`LC_ALL`, i-`LC_MESSAGES`, ne-`LANG`, kubuyele ku-`en`. Iziqalo zesimo ze-Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), idatha yokusebenza, nokhiye be-JSON bahlala bengashintshile kuzo zonke izilimi zendawo.

## Ukuthuthukiswa

Izivivinyo nokucushwa kwamathuluzi kutholakala ku-[pyproject.toml](../../../pyproject.toml), ku-[uv.lock](../../../uv.lock), kanye [naku-workflow ye-CI](../../../.github/workflows/ci.yml); sebenzisa izivivinyo nge-`uv run pytest`. Akukho phesenti elinqunyiwe lokumbozwa kwezivivinyo, impumelelo eqinile yokuhlola izinhlobo zedatha yonke indawo, noma isitifiketi se-supply-chain esishiwo lapha.

## Ezokuphepha nelayisensi

Bona i-[SECURITY.md](../../../SECURITY.md). Ikhodi yomthombo isebenzisa [ilayisensi ye-Apache-2.0](../../../LICENSE). I-[packaging/license-policy.json](../../../packaging/license-policy.json) irekhoda inqubomgomo yelayisensi yezinto ezincikene nayo.
