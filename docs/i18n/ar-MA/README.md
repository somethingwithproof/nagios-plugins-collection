<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: Apache-2.0
-->

# مجموعة إضافات Nagios

[![CI](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=somethingwithproof_nagios-plugins-collection&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=somethingwithproof_nagios-plugins-collection)
[![codecov](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection/branch/main/graph/badge.svg)](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection)
[![Release](https://img.shields.io/github/v/release/somethingwithproof/nagios-plugins-collection)](https://github.com/somethingwithproof/nagios-plugins-collection/releases)
[![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/somethingwithproof/nagios-plugins-collection/main/pyproject.toml)](../../../pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](../../../LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/nagios-plugins-collection/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/nagios-plugins-collection)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · **العربية (المغرب)** · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

مجموعة بـ Python ديال فحوصات المراقبة مع نقط دخول أوامر لخدمات الويب، قواعد البيانات، DNS، الشهادات، البنية التحتية، وموارد الكلاود. التنفيذ ديال كل إضافة كيحدد الخيارات ديالها، دلالات النتائج، والاعتماديات الاختيارية.

## نقط الدخول المتوفرة

السميات اللي لتحت معلن عليها فـ [pyproject.toml](../../../pyproject.toml) وعندها ملفات مصدرية مقابلة ليها:

| الأمر | التنفيذ |
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

قرا `--help` والتنفيذ ديال كل فحص بوحدو قبل ما تريكل العتبات (thresholds). ما خاصكش تفترض باللي سلوك JSON، ولا مهلة الانتظار (timeout)، ولا بيانات الأداء، ولا المصادقة متطابق بين كاع الإضافات.

## التثبيت من الكود المصدري

ملف الـ manifest كيحتاج Python >=3.11,<3.15. الملف [packaging/platform-support.json](../../../packaging/platform-support.json) كيسجل بيئات التشغيل وأهداف التحزيم اللي تراجعات. من هاد النسخة المحلية:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` كيتبت الاعتماديات المتبتة، أدوات التطوير والمشروع داخل `.venv/`؛ استعمل `uv sync --locked --no-dev --extra aws` (كمثال) لبيئة تشغيل فقط. الـ extras المتوفرة محددة فـ manifest؛ تبت غير التكاملات اللي محتاجها. التثبيت من المصدر مبين هنا بلا ما ندعيو باللي الحزمة منشورة فشي فهرس حزم.

## التوافق والتشغيل

باش تشغل الفحوصات على Kubernetes ولا Nomad، استعمل Helm chart اللي كاين فـ [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) ولا الـ job فـ [deploy/nomad](../../../deploy/nomad)؛ [دليل التثبيت](../../../docs/source/installation.rst#containers-and-kubernetes) فيه أمثلة كاملة لـ Helm وNomad، بما فيها الأسرار اللي كتجي من Kubernetes Secret ولا Nomad Variable.

استعمل [MIGRATION.md](../../../MIGRATION.md) لملاحظات الانتقال التاريخية، ولكن تحقق من سميات الأوامر والخيارات مقابل هاد النسخة المحلية. تغيير إصدار Python، ولا type hints، ولا إعدادات CI ما كيثبتوش باللي السلوك بقى هو هو لكل فحص قديم. الخدمات الخارجية وأدوات المنصة خاصها تكون متوفرة للفحص اللي كتخدمو.

## التوطين واللغات

مساعدة سطر الأوامر المشتركة ورسائل التشخيص كيدعمو 45 لغة محلية (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) باستعمال كاطالوغات مدمجة كتشارجا من المكتبة القياسية (stdlib). اختيار اللغة كيقلب فـ `--lang`، من بعد فـ `LC_ALL`، و`LC_MESSAGES`، و`LANG`، وكيرجع لـ `en` إلا ما لقاش. بادئات حالة Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`)، وبيانات الأداء، ومفاتيح JSON كيبقاو بلا تغيير فكاع اللغات.

## التطوير

الاختبارات وإعدادات الأدوات كاينين فـ [pyproject.toml](../../../pyproject.toml)، و[uv.lock](../../../uv.lock)، و[سير عمل CI](../../../.github/workflows/ci.yml)؛ شغل الاختبارات بـ `uv run pytest`. ما كاينش هنا أي ادعاء بنسبة تغطية ثابتة، ولا نجاح شامل لفحص الأنواع الصارم، ولا شهادة سلسلة التوريد.

## الأمان والرخصة

شوف [SECURITY.md](../../../SECURITY.md). الكود المصدري كيستعمل [رخصة Apache-2.0](../../../LICENSE). الملف [packaging/license-policy.json](../../../packaging/license-policy.json) كيسجل سياسة رخص الاعتماديات.
