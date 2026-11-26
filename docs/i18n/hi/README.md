<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: Apache-2.0
-->

# Nagios प्लगइन संग्रह

[![CI](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=somethingwithproof_nagios-plugins-collection&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=somethingwithproof_nagios-plugins-collection)
[![codecov](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection/branch/main/graph/badge.svg)](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection)
[![Release](https://img.shields.io/github/v/release/somethingwithproof/nagios-plugins-collection)](https://github.com/somethingwithproof/nagios-plugins-collection/releases)
[![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/somethingwithproof/nagios-plugins-collection/main/pyproject.toml)](../../../pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](../../../LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/nagios-plugins-collection/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/nagios-plugins-collection)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · **हिन्दी** · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

वेब सेवाओं, डेटाबेस, DNS, प्रमाणपत्रों, बुनियादी ढांचे और क्लाउड संसाधनों के लिए कमांड प्रवेश बिंदुओं के साथ निगरानी जांचों का एक Python संग्रह। प्रत्येक प्लगइन का कार्यान्वयन उसके विकल्पों, परिणाम शब्दार्थ और वैकल्पिक निर्भरताओं को परिभाषित करता है।

## उपलब्ध प्रवेश बिंदु

निम्नलिखित नाम [pyproject.toml](../../../pyproject.toml) में घोषित हैं और उनकी संबंधित सोर्स फ़ाइलें मौजूद हैं:

| कमांड | कार्यान्वयन |
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

सीमा मान कॉन्फ़िगर करने से पहले व्यक्तिगत जांच के `--help` और कार्यान्वयन को पढ़ें। JSON, टाइमआउट, प्रदर्शन-डेटा और प्रमाणीकरण व्यवहार को प्रत्येक प्लगइन में समान नहीं माना जाना चाहिए।

## सोर्स से स्थापना

मैनिफेस्ट के लिए Python >=3.11,<3.15 आवश्यक है। [packaging/platform-support.json](../../../packaging/platform-support.json) समीक्षित रनटाइम और पैकेजिंग लक्ष्यों को दर्ज करता है। इस चेकआउट से:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` लॉक की गई निर्भरताओं, विकास टूल और परियोजना को `.venv/` में स्थापित करता है; केवल-रनटाइम वातावरण के लिए (उदाहरण के लिए) `uv sync --locked --no-dev --extra aws` का उपयोग करें। उपलब्ध एक्स्ट्रा मैनिफेस्ट में परिभाषित हैं; केवल उन्हीं एकीकरणों को स्थापित करें जिनकी आपको आवश्यकता है। पैकेज-इंडेक्स प्रकाशन का दावा किए बिना सोर्स स्थापना दिखाई गई है।

## संगतता और संचालन

Kubernetes या Nomad पर जांच चलाने के लिए, [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) में Helm चार्ट या [deploy/nomad](../../../deploy/nomad) में जॉब का उपयोग करें; [स्थापना मार्गदर्शिका](../../../docs/source/installation.rst#containers-and-kubernetes) में Kubernetes Secret या Nomad Variable से प्रदान किए गए सीक्रेट्स सहित संपूर्ण Helm और Nomad उदाहरण हैं।

ऐतिहासिक माइग्रेशन नोट्स के लिए [MIGRATION.md](../../../MIGRATION.md) का उपयोग करें, लेकिन इस चेकआउट के साथ कमांड नाम और विकल्पों को सत्यापित करें। Python-संस्करण परिवर्तन, टाइप संकेत या CI कॉन्फ़िगरेशन प्रत्येक विरासत जांच के लिए अपरिवर्तित व्यवहार स्थापित नहीं करते हैं। चलाए जा रहे जांच के लिए बाहरी सेवाएं और प्लेटफ़ॉर्म टूल उपलब्ध होने चाहिए।

## स्थानीयकरण

साझा CLI सहायता और डायग्नोस्टिक संदेश बंडल किए गए stdlib-लोडेड कैटलॉग का उपयोग करके 45 लोकेल (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) का समर्थन करते हैं। रिज़ॉल्यूशन `--lang`, फिर `LC_ALL`, `LC_MESSAGES`, और `LANG` की जांच करता है, और कुछ न मिलने पर `en` पर वापस आ जाता है। Nagios स्थिति उपसर्ग (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), प्रदर्शन डेटा और JSON कुंजियाँ सभी लोकेल में अपरिवर्तित रहती हैं।

## विकास

परीक्षण और टूल कॉन्फ़िगरेशन [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock), और [CI वर्कफ़्लो](../../../.github/workflows/ci.yml) में रहते हैं; `uv run pytest` के साथ परीक्षण चलाएं। यहाँ कोई निश्चित कवरेज प्रतिशत, सार्वभौमिक सख्त-प्रकार-जांच सफलता या सप्लाई-चेन प्रमाणन का दावा नहीं किया गया है।

## सुरक्षा और लाइसेंस

[SECURITY.md](../../../SECURITY.md) देखें। सोर्स [Apache-2.0 लाइसेंस](../../../LICENSE) का उपयोग करता है। [packaging/license-policy.json](../../../packaging/license-policy.json) निर्भरता-लाइसेंस नीति को दर्ज करता है।
