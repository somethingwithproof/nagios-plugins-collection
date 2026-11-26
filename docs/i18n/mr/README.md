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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · **मराठी** · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

वेब सेवा, डेटाबेस, DNS, प्रमाणपत्रे, पायाभूत सुविधा आणि क्लाउड संसाधनांसाठी कमांड एंट्री पॉइंट्ससह मॉनिटरिंग तपासण्यांचा Python संग्रह. प्रत्येक प्लगइनची अंमलबजावणी त्याचे पर्याय, परिणाम अर्थशास्त्र (semantics) आणि वैकल्पिक अवलंबित्व परिभाषित करते.

## उपलब्ध एंट्री पॉइंट्स

खालील नावे [pyproject.toml](../../../pyproject.toml) मध्ये घोषित केली आहेत आणि त्यांच्या संबंधित सोर्स फाइल्स आहेत:

| कमांड | अंमलबजावणी |
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

मर्यादा (thresholds) कॉन्फिगर करण्यापूर्वी प्रत्येक तपासणीचे `--help` आणि अंमलबजावणी वाचा. प्रत्येक प्लगइनमध्ये JSON, टाइमआउट, कार्यप्रदर्शन-डेटा आणि प्रमाणीकरण वर्तन एकसारखे असेल असे गृहीत धरू नये.

## सोर्समधून इंस्टॉल करा

मॅनिफेस्टला Python >=3.11,<3.15 आवश्यक आहे. [packaging/platform-support.json](../../../packaging/platform-support.json) मध्ये पुनरावलोकन केलेले रनटाइम आणि पॅकेजिंग लक्ष्ये नोंदवलेली आहेत. या चेकआउटमधून:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` लॉक केलेली अवलंबित्वे, डेव्हलपमेंट टूल्स आणि प्रकल्प `.venv/` मध्ये इंस्टॉल करते; फक्त-रनटाइम वातावरणासाठी (उदाहरणार्थ) `uv sync --locked --no-dev --extra aws` वापरा. उपलब्ध एक्स्ट्राज मॅनिफेस्टमध्ये परिभाषित केले आहेत; तुम्हाला आवश्यक असलेलेच एकत्रीकरण इंस्टॉल करा. पॅकेज-इंडेक्स प्रकाशनाचा दावा न करता सोर्स इंस्टॉलेशन दाखवले आहे.

## सुसंगतता आणि ऑपरेशन्स

Kubernetes किंवा Nomad वर तपासण्या चालवण्यासाठी, [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) मधील Helm चार्ट किंवा [deploy/nomad](../../../deploy/nomad) मधील जॉब वापरा; [इंस्टॉलेशन मार्गदर्शकामध्ये](../../../docs/source/installation.rst#containers-and-kubernetes) Kubernetes Secret किंवा Nomad Variable मधून पुरवलेल्या सीक्रेट्ससह संपूर्ण Helm आणि Nomad उदाहरणे आहेत.

ऐतिहासिक स्थलांतर टिपांसाठी [MIGRATION.md](../../../MIGRATION.md) वापरा, परंतु या चेकआउटनुसार कमांड नावे आणि पर्याय तपासून पहा. Python-आवृत्ती बदल, टाइप हिंट्स किंवा CI कॉन्फिगरेशन प्रत्येक लेगसी तपासणीसाठी अपरिवर्तित वर्तन सिद्ध करत नाहीत. चालवल्या जाणाऱ्या तपासणीसाठी बाह्य सेवा आणि प्लॅटफॉर्म साधने उपलब्ध असणे आवश्यक आहे.

## स्थानिकीकरण

बंडल केलेल्या stdlib-लोड केलेल्या कॅटलॉगचा वापर करून सामायिक CLI मदत आणि निदान संदेश 45 लोकेल्स (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) ला समर्थन देतात. रिझोल्यूशन `--lang`, नंतर `LC_ALL`, `LC_MESSAGES`, आणि `LANG` तपासते आणि शेवटी `en` वर परत येते. Nagios स्थिती उपसर्ग (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), कार्यप्रदर्शन डेटा आणि JSON की सर्व लोकेल्समध्ये अपरिवर्तित राहतात.

## विकास

चाचण्या आणि टूल कॉन्फिगरेशन [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock), आणि [CI वर्कफ्लो](../../../.github/workflows/ci.yml) मध्ये आहेत; `uv run pytest` सह चाचण्या चालवा. येथे कोणतीही निश्चित कव्हरेज टक्केवारी, सार्वत्रिक कठोर-टाइप-चेकिंग यश किंवा सप्लाय-चेन प्रमाणपत्राचा दावा केलेला नाही.

## सुरक्षा आणि परवाना

[SECURITY.md](../../../SECURITY.md) पहा. सोर्स [Apache-2.0 परवाना](../../../LICENSE) वापरतो. [packaging/license-policy.json](../../../packaging/license-policy.json) अवलंबित्व-परवाना धोरण नोंदवते.
