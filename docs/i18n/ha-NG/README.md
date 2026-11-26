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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · **Hausa** · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Tarin binciken sa-ido na Python mai wuraren shigar umarni don ayyukan yanar gizo, rumbunan bayanai, DNS, takaddun shaida, kayayyakin more rayuwa na sadarwa, da albarkatun girgije. Aiwatarwar kowane plugin ce ke bayyana zaɓuɓɓukansa, ma'anar sakamako, da ƙarin abubuwan dogaro na zaɓi.

## Wuraren shigar umarni da ke akwai

An ayyana sunayen da ke ƙasa a cikin [pyproject.toml](../../../pyproject.toml) kuma suna da fayilolin lambar asali masu dacewa:

| Umarni | Aiwatarwa |
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

Karanta `--help` da aiwatarwar kowane bincike kafin saita iyakoki. Kada a ɗauka cewa halayyar JSON, ƙarewar lokaci, bayanan aiki (performance-data), da tantancewa iri ɗaya ce a kowane plugin.

## Shigarwa daga lambar asali

Fayil ɗin bayanin kunshin yana buƙatar Python >=3.11,<3.15. [packaging/platform-support.json](../../../packaging/platform-support.json) yana ɗauke da bayanan muhallin gudanarwa da maƙasudin tattara kunshi da aka duba. Daga wannan kwafin ma'ajiyar:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` yana shigar da abubuwan dogaro da aka kulle, kayan aikin haɓakawa, da aikin cikin `.venv/`; yi amfani da `uv sync --locked --no-dev --extra aws` (misali) don muhallin gudanarwa kaɗai. An ayyana ƙarin abubuwan da ke akwai a cikin fayil ɗin kunshin; shigar da haɗe-haɗen da kake buƙata kaɗai. An nuna shigarwa daga lambar asali ba tare da tabbatar da wallafawa a ma'ajiyar kunshi ba.

## Dacewa da gudanar da ayyuka

Don gudanar da bincike a kan Kubernetes ko Nomad, yi amfani da jadawalin Helm a cikin [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) ko aikin da ke cikin [deploy/nomad](../../../deploy/nomad); [jagorar shigarwa](../../../docs/source/installation.rst#containers-and-kubernetes) tana da cikakkun misalan Helm da Nomad, gami da bayanan sirri da aka bayar daga Kubernetes Secret ko Nomad Variable.

Yi amfani da [MIGRATION.md](../../../MIGRATION.md) don bayanan ƙaura na tarihi, amma ka tabbatar da sunayen umarni da zaɓuɓɓuka bisa wannan kwafin ma'ajiyar. Sauyin sigar Python, alamun nau'in bayanai, ko saitin CI ba su tabbatar da cewa halayyar kowane tsohon bincike ba ta canza ba. Dole ne ayyukan waje da kayan aikin dandali su kasance akwai don binciken da ake gudanarwa.

## Daidaita harshe

Taimakon CLI na gama-gari da saƙonnin binciken matsaloli suna goyan bayan harsuna 45 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) ta hanyar amfani da kundin harsuna da aka haɗa masu lodawa da stdlib. Zaɓin harshe yana duba `--lang`, sannan `LC_ALL`, `LC_MESSAGES`, da `LANG`, yana komawa zuwa `en` a ƙarshe. Alamomin matsayin Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), bayanan aiki, da maɓallan JSON ba su canzawa a duk harsunan.

## Haɓakawa

Gwaje-gwaje da saitin kayan aiki suna cikin [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock), da [tsarin aikin CI](../../../.github/workflows/ci.yml); gudanar da gwaje-gwaje tare da `uv run pytest`. Ba a yi da'awar wani takamaiman adadin kashi na gwaji, nasarar duba nau'in bayanai mai tsauri a ko'ina, ko takardar shaidar sarkar samar da kayayyaki a nan ba.

## Tsaro da lasisi

Duba [SECURITY.md](../../../SECURITY.md). Lambar asalin tana amfani da [lasisin Apache-2.0](../../../LICENSE). [packaging/license-policy.json](../../../packaging/license-policy.json) yana ɗauke da manufar lasisin abubuwan dogaro.
