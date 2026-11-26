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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · **فارسی** · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

مجموعه‌ای پایتونی از بررسی‌های پایش (monitoring checks) با نقاط ورود دستوری برای سرویس‌های وب، پایگاه‌های داده، DNS، گواهی‌ها، زیرساخت و منابع ابری. پیاده‌سازی هر افزونه گزینه‌ها، معنای نتایج و وابستگی‌های اختیاری آن را مشخص می‌کند.

## نقاط ورود در دسترس

نام‌های زیر در [pyproject.toml](../../../pyproject.toml) تعریف شده‌اند و فایل‌های سورس متناظر دارند:

| دستور | پیاده‌سازی |
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

پیش از پیکربندی آستانه‌ها، `--help` و پیاده‌سازی هر بررسی را مطالعه کنید. نباید فرض کرد که رفتار JSON، زمان انقضا (timeout)، داده‌های عملکرد و احراز هویت در همه افزونه‌ها یکسان است.

## نصب از سورس

فایل مانیفست به Python >=3.11,<3.15 نیاز دارد. [packaging/platform-support.json](../../../packaging/platform-support.json) زمان‌های اجرا و هدف‌های بسته‌بندی بررسی‌شده را ثبت کرده است. از درون این نسخه کلون‌شده:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

دستور `uv sync` وابستگی‌های قفل‌شده، ابزارهای توسعه و پروژه را در `.venv/` نصب می‌کند؛ برای محیط فقط زمان اجرا از `uv sync --locked --no-dev --extra aws` (برای مثال) استفاده کنید. قابلیت‌های اضافه (extras) موجود در مانیفست تعریف شده‌اند؛ فقط یکپارچه‌سازی‌هایی را که نیاز دارید نصب کنید. نصب از سورس بدون ادعای انتشار در مخزن بسته (package-index) نمایش داده شده است.

## سازگاری و عملیات

برای اجرای بررسی‌ها روی Kubernetes یا Nomad، از چارت Helm در [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) یا جاب موجود در [deploy/nomad](../../../deploy/nomad) استفاده کنید؛ [راهنمای نصب](../../../docs/source/installation.rst#containers-and-kubernetes) دارای نمونه‌های کامل Helm و Nomad از جمله تامین محرمانه‌ها از Kubernetes Secret یا Nomad Variable است.

برای یادداشت‌های تاریخی مهاجرت از [MIGRATION.md](../../../MIGRATION.md) استفاده کنید، اما نام دستورها و گزینه‌ها را با همین نسخه مخزن بررسی کنید. تغییر نسخه پایتون، type hintها یا پیکربندی CI تغییر نکردن رفتار هیچ بررسی قدیمی را اثبات نمی‌کند. سرویس‌های خارجی و ابزارهای پلتفرم باید برای بررسی در حال اجرا در دسترس باشند.

## بومی‌سازی

راهنمای خط فرمان مشترک و پیام‌های تشخیصی از ۴۵ زبان و منطقه (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) با استفاده از کاتالوگ‌های داخلی بارگذاری‌شده توسط stdlib پشتیبانی می‌کنند. تشخیص زبان ابتدا `--lang` و سپس `LC_ALL`، `LC_MESSAGES` و `LANG` را بررسی می‌کند و در نهایت به `en` بازمی‌گردد. پیشوندهای وضعیت Nagios (`OK`، `WARNING`، `CRITICAL`، `UNKNOWN`)، داده‌های عملکرد و کلیدهای JSON در همه زبان‌ها بدون تغییر باقی می‌مانند.

## توسعه

آزمون‌ها و پیکربندی ابزارها در [pyproject.toml](../../../pyproject.toml)، [uv.lock](../../../uv.lock) و [گردش کار CI](../../../.github/workflows/ci.yml) قرار دارند؛ آزمون‌ها را با `uv run pytest` اجرا کنید. در اینجا هیچ درصد پوشش ثابت، موفقیت همه‌جانبه در بررسی سخت‌گیرانه نوع‌ها یا گواهی زنجیره تامین ادعا نمی‌شود.

## امنیت و مجوز

[SECURITY.md](../../../SECURITY.md) را ببینید. کد منبع از [مجوز Apache-2.0](../../../LICENSE) استفاده می‌کند. [packaging/license-policy.json](../../../packaging/license-policy.json) سیاست مجوز وابستگی‌ها را ثبت کرده است.
