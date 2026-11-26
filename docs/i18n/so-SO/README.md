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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · **Soomaali** · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Ururin Python ah oo ka kooban hubinno la-socod (monitoring checks) oo leh baro gelitaan amareed oo loogu talagalay adeegyada webka, kaydadka xogta (databases), DNS, shahaadooyinka, kaabayaasha, iyo kheyraadka daruuraha (cloud resources). Hirgelinta plugin kasta ayaa qeexda xulashooyinkiisa, macnaha natiijooyinkiisa, iyo ku-tiirsanaantiisa ikhtiyaariga ah.

## Baraha gelitaanka ee la heli karo

Magacyada soo socda waxaa lagu caddeeyay [pyproject.toml](../../../pyproject.toml) waxayna leeyihiin faylasha koodka isha ee u dhigma:

| Amarka | Hirgelinta |
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

Akhri `--help` iyo hirgelinta hubin kasta ka hor inta aadan habayn xuduudaha (thresholds). Dhaqanka JSON, wakhtiga dhicitaanka (timeout), xogta waxqabadka (performance-data), iyo aqoonsiga lama malayn karo inay isku mid yihiin dhammaan plugin-yada.

## Ka rakib koodka isha

Liiska xirmadu (manifest) wuxuu u baahan yahay Python >=3.11,<3.15. [packaging/platform-support.json](../../../packaging/platform-support.json) wuxuu diiwaangeliyaa bartilmaameedyada socodsiinta iyo baakadaynta ee dib loo eegay. Laga bilaabo nuqulkan kaydka:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` wuxuu ku rakibaa ku-tiirsanaanta la xiray, qalabka horumarinta, iyo mashruuca gudaha `.venv/`; adeegso `uv sync --locked --no-dev --extra aws` (tusaale ahaan) deegaan socodsiin oo keliya ah. Waxyaabaha dheeraadka ah (extras) ee la heli karo waxaa lagu qeexay liiska xirmada; rakib oo keliya is-dhexgallada aad u baahan tahay. Rakibidda koodka isha waxaa loo muujiyay iyadoon la sheeganayn daabacaadda tusmada xirmooyinka (package-index).

## Is-waafajinta iyo hawlgallada

Si aad ugu socodsiiso hubinnada Kubernetes ama Nomad, adeegso jaantuska Helm ee ku jira [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) ama shaqada ku jirta [deploy/nomad](../../../deploy/nomad); [hagaha rakibidda](../../../docs/source/installation.rst#containers-and-kubernetes) wuxuu leeyahay tusaalooyin dhammaystiran oo Helm iyo Nomad ah, oo ay ku jiraan siraha laga keeno Kubernetes Secret ama Nomad Variable.

U adeegso [MIGRATION.md](../../../MIGRATION.md) qoraallada taariikhiga ah ee guurista, laakiin ku hubi magacyada amarrada iyo xulashooyinka nuqulkan kaydka. Isbeddelka nooca Python, tilmaamaha nooca (type hints), ama habaynta CI ma xaqiijinayaan dhaqan aan isbeddelin hubin kasta oo hore. Adeegyada dibadda iyo qalabka nidaamku waa inay diyaar u ahaadaan hubinta la socodsiinayo.

## Luqadeynta

Caawimaadda CLI ee la wadaago iyo farriimaha baaritaanku waxay taageeraan 45 luqadood (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) iyadoo la adeegsanayo buugaag-yar (catalogs) ku jira oo lagu soo raro stdlib. Xallintu waxay hubisaa `--lang`, ka dib `LC_ALL`, `LC_MESSAGES`, iyo `LANG`, iyadoo ku noqonaysa `en`. Horgalayaasha xaaladda Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), xogta waxqabadka, iyo furayaasha JSON lama beddelo dhammaan luqadaha.

## Horumarinta

Tijaabooyinka iyo habaynta qalabku waxay ku jiraan [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock), iyo [socodka shaqada CI](../../../.github/workflows/ci.yml); ku socodsii tijaabooyinka `uv run pytest`. Halkan laguma sheeganayo boqolley daboolid go'an, guul caalami ah oo hubinta nooca adag ah, ama shahaado silsiladda sahayda ah.

## Amniga iyo shatiga

Eeg [SECURITY.md](../../../SECURITY.md). Koodka isha wuxuu adeegsadaa [shatiga Apache-2.0](../../../LICENSE). [packaging/license-policy.json](../../../packaging/license-policy.json) wuxuu diiwaangeliyaa siyaasadda shatiga ku-tiirsanaanta.
