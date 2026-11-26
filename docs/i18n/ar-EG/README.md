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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · **العربية (مصر)** · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

مجموعة فحوصات مراقبة مكتوبة بـ Python وفيها نقاط دخول كأوامر لخدمات الويب، قواعد البيانات، DNS، الشهادات، البنية التحتية، وموارد السحابة. تنفيذ كل إضافة هو اللي بيحدد خياراتها، دلالات نتائجها، والاعتماديات الاختيارية بتاعتها.

## نقاط الدخول المتاحة

الأسماء دي متعرفة في [pyproject.toml](../../../pyproject.toml) وليها ملفات كود مقابلة ليها:

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

اقرا `--help` والكود بتاع كل فحص لوحده قبل ما تضبط حدود التنبيه (thresholds). متفترضش إن سلوك JSON أو المهلة الزمنية (timeout) أو بيانات الأداء أو المصادقة واحد في كل الإضافات.

## التثبيت من الكود المصدري

ملف الـ manifest محتاج Python >=3.11,<3.15. ملف [packaging/platform-support.json](../../../packaging/platform-support.json) بيسجل بيئات التشغيل وأهداف التغليف اللي اتراجعت. من النسخة المحلية دي:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

أمر `uv sync` بيثبت الاعتماديات المثبتة، أدوات التطوير، والمشروع جوه `.venv/`؛ واستخدم `uv sync --locked --no-dev --extra aws` (مثلاً) لو عايز بيئة تشغيل بس. الإضافات الاختيارية (extras) المتاحة متعرفة في الـ manifest؛ ثبت بس التكاملات اللي محتاجها. التثبيت من المصدر معروض هنا من غير تأكيد إن الحزمة منشورة على فهرس حزم.

## التوافق والتشغيل

عشان تشغل الفحوصات على Kubernetes أو Nomad، استخدم الـ Helm chart اللي في [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) أو الـ job اللي في [deploy/nomad](../../../deploy/nomad)؛ و[دليل التثبيت](../../../docs/source/installation.rst#containers-and-kubernetes) فيه أمثلة كاملة لـ Helm وNomad، بما فيها تمرير الأسرار من Kubernetes Secret أو Nomad Variable.

استخدم [MIGRATION.md](../../../MIGRATION.md) عشان ملاحظات الترحيل التاريخية، بس راجع أسماء الأوامر والخيارات قدام النسخة المحلية دي. تغيير إصدار Python أو type hints أو إعدادات الـ CI مش معناه إن سلوك كل فحص قديم فضل زي ما هو من غير تغيير. الخدمات الخارجية وأدوات النظام لازم تكون موجودة للفحص اللي بتشغله.

## الترجمة واللغات (Localization)

مساعدة سطر الأوامر المشتركة ورسائل التشخيص بتدعم 45 لغة ومحلية (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) باستخدام كتالوجات مدمجة بتتحمل بالمكتبة القياسية. تحديد اللغة بيدور الأول في `--lang`، بعد كده `LC_ALL` و`LC_MESSAGES` و`LANG`، وبيرجع لـ `en` لو مفيش. بادئات حالة Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`) وبيانات الأداء ومفاتيح JSON بتفضل زي ما هي في كل اللغات.

## التطوير

الاختبارات وإعدادات الأدوات موجودة في [pyproject.toml](../../../pyproject.toml) و[uv.lock](../../../uv.lock) و[ملف الـ CI workflow](../../../.github/workflows/ci.yml)؛ شغل الاختبارات بأمر `uv run pytest`. مش بندعي هنا نسبة تغطية ثابتة، ولا نجاح شامل لفحص الأنواع الصارم، ولا شهادة لأمان سلسلة التوريد.

## الأمان والرخصة

شوف [SECURITY.md](../../../SECURITY.md). الكود المصدري بيستخدم [رخصة Apache-2.0](../../../LICENSE). و[packaging/license-policy.json](../../../packaging/license-policy.json) بيسجل سياسة رخص الاعتماديات.
