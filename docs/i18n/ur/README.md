<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: Apache-2.0
-->

# Nagios پلگ انز کلیکشن

[![CI](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=somethingwithproof_nagios-plugins-collection&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=somethingwithproof_nagios-plugins-collection)
[![codecov](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection/branch/main/graph/badge.svg)](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection)
[![Release](https://img.shields.io/github/v/release/somethingwithproof/nagios-plugins-collection)](https://github.com/somethingwithproof/nagios-plugins-collection/releases)
[![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/somethingwithproof/nagios-plugins-collection/main/pyproject.toml)](./pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/nagios-plugins-collection/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/nagios-plugins-collection)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · **اردو** · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

ویب سروسز، ڈیٹا بیسز، DNS، سرٹیفکیٹس، انفراسٹرکچر، اور کلاؤڈ وسائل کے لیے کمانڈ اینٹری پوائنٹس کے ساتھ مانیٹرنگ چیکس کا ایک Python مجموعہ۔ ہر پلگ ان کا نفاذ اس کے اختیارات، نتائج کے معانی، اور اختیاری انحصار کی وضاحت کرتا ہے۔

## دستیاب اینٹری پوائنٹس

درج ذیل نام [pyproject.toml](../../../pyproject.toml) میں بیان کیے گئے ہیں اور ان کی متعلقہ سورس فائلیں موجود ہیں:

| کمانڈ | نفاذ |
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

تھریش ہولڈز کنفیگر کرنے سے پہلے متعلقہ چیک کا `--help` اور نفاذ پڑھیں۔ ہر پلگ ان میں JSON، ٹائم آؤٹ، کارکردگی کے ڈیٹا (performance-data)، اور توثیق کے رویے کو یکساں فرض نہیں کیا جانا چاہیے۔

## سورس کوڈ سے تنصیب

مینی فیسٹ کے لیے Python >=3.11,<3.15 درکار ہے۔ [packaging/platform-support.json](../../../packaging/platform-support.json) میں جائزہ لیے گئے رن ٹائم اور پیکیجنگ اہداف درج ہیں۔ اس چیک آؤٹ سے:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` لاک کردہ انحصار، ڈویلپمنٹ ٹولز اور پروجیکٹ کو `.venv/` میں انسٹال کرتا ہے؛ صرف رن ٹائم ماحول کے لیے (مثال کے طور پر) `uv sync --locked --no-dev --extra aws` استعمال کریں۔ دستیاب اضافی اجزاء (extras) مینی فیسٹ میں بیان کیے گئے ہیں؛ صرف وہی انٹیگریشنز انسٹال کریں جن کی آپ کو ضرورت ہے۔ سورس انسٹالیشن پیکیج انڈیکس کی اشاعت کا دعویٰ کیے بغیر دکھائی گئی ہے۔

## مطابقت اور آپریشنز

Kubernetes یا Nomad پر چیکس چلانے کے لیے [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) میں موجود Helm چارٹ یا [deploy/nomad](../../../deploy/nomad) میں موجود جاب استعمال کریں؛ [تنصیب کے رہنما](../../../docs/source/installation.rst#containers-and-kubernetes) میں مکمل Helm اور Nomad مثالیں موجود ہیں، جن میں Kubernetes Secret یا Nomad Variable سے فراہم کردہ سیکرٹس بھی شامل ہیں۔

تاریخی منتقلی کے نوٹس کے لیے [MIGRATION.md](../../../MIGRATION.md) استعمال کریں، لیکن اس چیک آؤٹ کے مطابق کمانڈ کے ناموں اور اختیارات کی تصدیق کر لیں۔ Python ورژن میں تبدیلی، ٹائپ ہنٹس، یا CI کنفیگریشن ہر پرانے چیک کے غیر متبدل رویے کو ثابت نہیں کرتے۔ چلائے جانے والے چیک کے لیے بیرونی سروسز اور پلیٹ فارم ٹولز دستیاب ہونے چاہئیں۔

## لوکلائزیشن

مشترکہ CLI مدد اور تشخیصی پیغامات بنڈل شدہ stdlib سے لوڈ ہونے والے کیٹلاگز کا استعمال کرتے ہوئے 45 لوکیلز (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) کی معاونت کرتے ہیں۔ لوکیل کی شناخت پہلے `--lang`، پھر `LC_ALL`، `LC_MESSAGES`، اور `LANG` کو چیک کرتی ہے، اور آخر میں `en` پر واپس آتی ہے۔ Nagios اسٹیٹس کے سابقے (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`)، کارکردگی کا ڈیٹا، اور JSON کیز تمام لوکیلز میں غیر متبدل رہتی ہیں۔

## ترقی

ٹیسٹس اور ٹول کنفیگریشن [pyproject.toml](../../../pyproject.toml)، [uv.lock](../../../uv.lock)، اور [CI ورک فلو](../../../.github/workflows/ci.yml) میں موجود ہیں؛ `uv run pytest` کے ساتھ ٹیسٹس چلائیں۔ یہاں کوریج کے کسی مقررہ فیصد، عالمگیر اسٹرکٹ ٹائپ چیکنگ کی کامیابی، یا سپلائی چین سرٹیفیکیشن کا کوئی دعویٰ نہیں کیا گیا ہے۔

## سیکیورٹی اور لائسنس

[SECURITY.md](../../../SECURITY.md) دیکھیں۔ سورس کوڈ [Apache-2.0 لائسنس](../../../LICENSE) استعمال کرتا ہے۔ [packaging/license-policy.json](../../../packaging/license-policy.json) میں انحصار کے لائسنس کی پالیسی درج ہے۔
