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

[Afrikaans](../af-ZA/README.md) · **አማርኛ** · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

ለድር አገልግሎቶች፣ የውሂብ ጎታዎች፣ DNS፣ የምስክር ወረቀቶች፣ መሠረተ ልማት እና የደመና ሀብቶች የትእዛዝ መግቢያ ነጥቦች ያሉት የPython የክትትል ፍተሻዎች ስብስብ። የእያንዳንዱ ፕለጊን አተገባበር አማራጮቹን፣ የውጤት ትርጉሞቹን እና አማራጭ ጥገኝነቶቹን ይወስናል።

## የሚገኙ መግቢያ ነጥቦች

የሚከተሉት ስሞች በ[pyproject.toml](../../../pyproject.toml) ውስጥ የታወጁ እና ተጓዳኝ የምንጭ ፋይሎች ያላቸው ናቸው:

| ትእዛዝ | አተገባበር |
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

ገደቦችን ከማዋቀርዎ በፊት የእያንዳንዱን ፍተሻ `--help` እና አተገባበር ያንብቡ። የJSON፣ የጊዜ ማብቂያ፣ የአፈጻጸም ውሂብ እና የማንነት ማረጋገጫ ባህሪ በእያንዳንዱ ፕለጊን ላይ አንድ ዓይነት ነው ተብሎ መገመት የለበትም።

## ከምንጭ ኮድ መጫን

መግለጫው Python >=3.11,<3.15 ይፈልጋል። [packaging/platform-support.json](../../../packaging/platform-support.json) የተገመገሙትን የአፈጻጸም ጊዜ እና የማሸጊያ ዒላማዎችን ይመዘግባል። ከዚህ ቅጂ ውስጥ:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` የተቆለፉትን ጥገኝነቶች፣ የልማት መሣሪያዎቹን እና ፕሮጀክቱን ወደ `.venv/` ይጭናል፤ ለአፈጻጸም ጊዜ ብቻ የሚሆን አካባቢ (ለምሳሌ) `uv sync --locked --no-dev --extra aws`ን ይጠቀሙ። የሚገኙት ተጨማሪዎች በመግለጫው ውስጥ ተገልጸዋል፤ የሚፈልጓቸውን ውህደቶች ብቻ ይጫኑ። የምንጭ ጭነት የጥቅል-ማውጫ ህትመትን ሳያረጋግጥ ቀርቧል።

## ተኳሃኝነት እና አሠራር

ፍተሻዎችን በKubernetes ወይም በNomad ላይ ለማስኬድ በ[charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) ውስጥ ያለውን የHelm chart ወይም በ[deploy/nomad](../../../deploy/nomad) ውስጥ ያለውን ሥራ ይጠቀሙ፤ [የመጫኛ መመሪያው](../../../docs/source/installation.rst#containers-and-kubernetes) ከKubernetes Secret ወይም ከNomad Variable የሚቀርቡ ምስጢሮችን ጨምሮ የተሟሉ የHelm እና Nomad ምሳሌዎችን ይዟል።

ለታሪካዊ የሽግግር ማስታወሻዎች [MIGRATION.md](../../../MIGRATION.md)ን ይጠቀሙ፣ ነገር ግን የትእዛዝ ስሞችን እና አማራጮችን ከዚህ ቅጂ ጋር ያረጋግጡ። የPython ስሪት ለውጥ፣ የዓይነት ፍንጮች ወይም የCI ውቅር ለእያንዳንዱ ነባር ፍተሻ ያልተለወጠ ባህሪን አያረጋግጡም። ለሚካሄደው ፍተሻ ውጫዊ አገልግሎቶች እና የመድረክ መሣሪያዎች መገኘት አለባቸው።

## የቋንቋ አካባቢያዊነት

የጋራ CLI እገዛ እና የምርመራ መልእክቶች በstdlib የሚጫኑ የተካተቱ ካታሎጎችን በመጠቀም 45 ቋንቋዎችን (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) ይደግፋሉ። የቋንቋ አመራረጥ መጀመሪያ `--lang`ን፣ ከዚያ `LC_ALL`፣ `LC_MESSAGES` እና `LANG`ን ይፈትሻል፣ ወደ `en` በመመለስ። የNagios ሁኔታ ቅድመ-ቅጥያዎች (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`)፣ የአፈጻጸም ውሂብ እና የJSON ቁልፎች በሁሉም ቋንቋዎች ውስጥ ሳይለወጡ ይቆያሉ።

## ልማት

ሙከራዎች እና የመሣሪያ ውቅር በ[pyproject.toml](../../../pyproject.toml)፣ [uv.lock](../../../uv.lock) እና [የCI የሥራ ፍሰት](../../../.github/workflows/ci.yml) ውስጥ ይገኛሉ፤ ሙከራዎችን በ`uv run pytest` ያስኪዱ። እዚህ ምንም የተወሰነ የሽፋን መቶኛ፣ ሁለንተናዊ ጥብቅ የዓይነት ፍተሻ ስኬት ወይም የአቅርቦት ሰንሰለት የምስክር ወረቀት አይቀርብም።

## ደህንነት እና ፈቃድ

[SECURITY.md](../../../SECURITY.md)ን ይመልከቱ። ምንጭ ኮዱ [የApache-2.0 ፈቃድ](../../../LICENSE)ን ይጠቀማል። [packaging/license-policy.json](../../../packaging/license-policy.json) የጥገኝነት-ፈቃድ ፖሊሲውን ይመዘግባል።
