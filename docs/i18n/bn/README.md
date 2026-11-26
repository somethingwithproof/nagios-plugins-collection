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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · **বাংলা** · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

ওয়েব সার্ভিস, ডেটাবেস, DNS, সার্টিফিকেট, অবকাঠামো এবং ক্লাউড রিসোর্সের জন্য কমান্ড এন্ট্রি পয়েন্টসহ মনিটরিং চেকের একটি Python সংগ্রহ। প্রতিটি প্লাগইনের বাস্তবায়ন তার বিকল্পসমূহ, ফলাফলের অর্থ এবং ঐচ্ছিক ডিপেন্ডেন্সি নির্ধারণ করে।

## উপলব্ধ এন্ট্রি পয়েন্টসমূহ

নিম্নলিখিত নামগুলো [pyproject.toml](../../../pyproject.toml)-এ ঘোষিত আছে এবং এগুলোর সংশ্লিষ্ট সোর্স ফাইল রয়েছে:

| কমান্ড | বাস্তবায়ন |
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

থ্রেশহোল্ড কনফিগার করার আগে প্রতিটি চেকের `--help` এবং বাস্তবায়ন পড়ুন। প্রতিটি প্লাগইনে JSON, টাইমআউট, পারফরম্যান্স-ডেটা এবং প্রমাণীকরণ আচরণ অভিন্ন বলে ধরে নেওয়া উচিত নয়।

## সোর্স থেকে ইনস্টল করুন

ম্যানিফেস্টে Python >=3.11,<3.15 প্রয়োজন। [packaging/platform-support.json](../../../packaging/platform-support.json) পর্যালোচিত রানটাইম এবং প্যাকেজিং টার্গেটগুলো নথিভুক্ত করে। এই চেকআউট থেকে:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` লক করা ডিপেন্ডেন্সি, ডেভেলপমেন্ট টুল এবং প্রকল্পটিকে `.venv/`-এ ইনস্টল করে; কেবল রানটাইম পরিবেশের জন্য (উদাহরণস্বরূপ) `uv sync --locked --no-dev --extra aws` ব্যবহার করুন। উপলব্ধ এক্সট্রাগুলো ম্যানিফেস্টে নির্ধারিত আছে; কেবল আপনার প্রয়োজনীয় ইন্টিগ্রেশনগুলোই ইনস্টল করুন। প্যাকেজ-ইনডেক্সে প্রকাশের দাবি না করেই সোর্স ইনস্টলেশন দেখানো হয়েছে।

## সামঞ্জস্য এবং পরিচালনা

Kubernetes বা Nomad-এ চেকগুলো চালাতে [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection)-এ থাকা Helm চার্ট অথবা [deploy/nomad](../../../deploy/nomad)-এ থাকা জব ব্যবহার করুন; Kubernetes Secret বা Nomad Variable থেকে সিক্রেট সরবরাহ করাসহ সম্পূর্ণ Helm এবং Nomad উদাহরণ [ইনস্টলেশন গাইডে](../../../docs/source/installation.rst#containers-and-kubernetes) রয়েছে।

ঐতিহাসিক মাইগ্রেশন নোটের জন্য [MIGRATION.md](../../../MIGRATION.md) ব্যবহার করুন, তবে এই চেকআউটের বিপরীতে কমান্ডের নাম ও বিকল্পগুলো যাচাই করে নিন। Python সংস্করণের পরিবর্তন, টাইপ হিন্ট বা CI কনফিগারেশন প্রতিটি লিগ্যাসি চেকের অপরিবর্তিত আচরণ নিশ্চিত করে না। যে চেকটি চালানো হচ্ছে তার জন্য বহিরাগত সার্ভিস এবং প্ল্যাটফর্ম টুলগুলো অবশ্যই উপলব্ধ থাকতে হবে।

## লোকালাইজেশন

শেয়ার্ড CLI সাহায্য এবং ডায়াগনস্টিক বার্তাগুলো বান্ডিল করা stdlib-লোডেড ক্যাটালগ ব্যবহার করে ৪৫টি লোকেল (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) সমর্থন করে। লোকেল নির্ধারণে প্রথমে `--lang`, তারপর `LC_ALL`, `LC_MESSAGES` এবং `LANG` পরীক্ষা করা হয়, এবং না পাওয়া গেলে `en`-এ ফিরে যায়। Nagios স্ট্যাটাস প্রিফিক্স (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), পারফরম্যান্স ডেটা এবং JSON কীগুলো সব লোকেলেই অপরিবর্তিত থাকে।

## উন্নয়ন

টেস্ট এবং টুল কনফিগারেশন [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock) এবং [CI ওয়ার্কফ্লোতে](../../../.github/workflows/ci.yml) থাকে; `uv run pytest` দিয়ে টেস্ট চালান। এখানে কোনো নির্দিষ্ট কভারেজ শতাংশ, সর্বজনীন স্ট্রিক্ট-টাইপ-চেকিং সাফল্য বা সাপ্লাই-চেইন সার্টিফিকেশনের দাবি করা হচ্ছে না।

## নিরাপত্তা এবং লাইসেন্স

[SECURITY.md](../../../SECURITY.md) দেখুন। সোর্স কোড [Apache-2.0 লাইসেন্স](../../../LICENSE) ব্যবহার করে। [packaging/license-policy.json](../../../packaging/license-policy.json) ডিপেন্ডেন্সি-লাইসেন্স নীতি নথিভুক্ত করে।
