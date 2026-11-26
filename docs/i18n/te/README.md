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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · **తెలుగు** · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

వెబ్ సేవలు, డేటాబేస్‌లు, DNS, సర్టిఫికేట్‌లు, మౌలిక సదుపాయాలు మరియు క్లౌడ్ వనరుల కోసం కమాండ్ ఎంట్రీ పాయింట్‌లతో కూడిన పర్యవేక్షణ తనిఖీల Python సమాహారం. ప్రతి ప్లగిన్ అమలు దాని ఎంపికలు, ఫలిత అర్థాలు మరియు ఐచ్ఛిక డిపెండెన్సీలను నిర్వచిస్తుంది.

## అందుబాటులో ఉన్న ఎంట్రీ పాయింట్‌లు

కింది పేర్లు [pyproject.toml](../../../pyproject.toml)లో ప్రకటించబడ్డాయి మరియు వాటికి సంబంధిత సోర్స్ ఫైల్‌లు ఉన్నాయి:

| కమాండ్ | అమలు |
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

పరిమితులను కాన్ఫిగర్ చేసే ముందు సంబంధిత తనిఖీ యొక్క `--help` మరియు అమలును చదవండి. ప్రతి ప్లగిన్‌లో JSON, టైమ్‌అవుట్, పనితీరు-డేటా మరియు ప్రామాణీకరణ ప్రవర్తన ఒకేలా ఉంటాయని భావించవద్దు.

## సోర్స్ నుండి ఇన్‌స్టాల్ చేయడం

మానిఫెస్ట్‌కు Python >=3.11,<3.15 అవసరం. సమీక్షించబడిన రన్‌టైమ్ మరియు ప్యాకేజింగ్ లక్ష్యాలను [packaging/platform-support.json](../../../packaging/platform-support.json) నమోదు చేస్తుంది. ఈ చెక్అవుట్ నుండి:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` లాక్ చేసిన డిపెండెన్సీలు, డెవలప్‌మెంట్ టూల్స్ మరియు ప్రాజెక్ట్‌ను `.venv/`లో ఇన్‌స్టాల్ చేస్తుంది; కేవలం రన్‌టైమ్ వాతావరణం కోసం `uv sync --locked --no-dev --extra aws` (ఉదాహరణకు) ఉపయోగించండి. అందుబాటులో ఉన్న ఎక్స్‌ట్రాలు మానిఫెస్ట్‌లో నిర్వచించబడ్డాయి; మీకు అవసరమైన ఇంటిగ్రేషన్‌లను మాత్రమే ఇన్‌స్టాల్ చేయండి. ప్యాకేజీ-ఇండెక్స్ ప్రచురణను నిర్ధారించకుండా సోర్స్ ఇన్‌స్టాలేషన్ చూపబడింది.

## అనుకూలత మరియు కార్యకలాపాలు

Kubernetes లేదా Nomadపై తనిఖీలను అమలు చేయడానికి, [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection)లోని Helm చార్ట్‌ను లేదా [deploy/nomad](../../../deploy/nomad)లోని జాబ్‌ను ఉపయోగించండి; Kubernetes Secret లేదా Nomad Variable నుండి అందించబడిన సీక్రెట్‌లతో సహా పూర్తి Helm మరియు Nomad ఉదాహరణలు [ఇన్‌స్టాలేషన్ గైడ్](../../../docs/source/installation.rst#containers-and-kubernetes)లో ఉన్నాయి.

చారిత్రక మైగ్రేషన్ గమనికల కోసం [MIGRATION.md](../../../MIGRATION.md) ఉపయోగించండి, కానీ కమాండ్ పేర్లు మరియు ఎంపికలను ఈ చెక్అవుట్‌తో సరిపోల్చి ధృవీకరించండి. Python వెర్షన్ మార్పు, టైప్ హింట్‌లు లేదా CI కాన్ఫిగరేషన్ ప్రతి పాత తనిఖీకి మారని ప్రవర్తనను నిర్ధారించవు. అమలు చేయబడుతున్న తనిఖీకి బాహ్య సేవలు మరియు ప్లాట్‌ఫారమ్ టూల్స్ అందుబాటులో ఉండాలి.

## స్థానికీకరణ

భాగస్వామ్య CLI సహాయం మరియు డయాగ్నస్టిక్ సందేశాలు బండిల్ చేసిన stdlib-లోడ్ చేసిన కేటలాగ్‌లను ఉపయోగించి 45 లోకేల్స్‌కు (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) మద్దతు ఇస్తాయి. నిర్ధారణ `--lang`, ఆపై `LC_ALL`, `LC_MESSAGES`, మరియు `LANG`లను తనిఖీ చేసి, చివరకు `en`కు తిరిగి వస్తుంది. Nagios స్థితి ఉపసర్గలు (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), పనితీరు డేటా మరియు JSON కీలు అన్ని లోకేల్స్‌లో మారకుండా అలాగే ఉంటాయి.

## అభివృద్ధి

పరీక్షలు మరియు టూల్ కాన్ఫిగరేషన్ [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock), మరియు [CI వర్క్‌ఫ్లో](../../../.github/workflows/ci.yml)లో ఉన్నాయి; `uv run pytest`తో పరీక్షలను అమలు చేయండి. ఇక్కడ నిర్దిష్ట కవరేజ్ శాతం, సార్వత్రిక స్ట్రిక్ట్-టైప్-చెకింగ్ విజయం లేదా సప్లై-చైన్ ధృవీకరణ గురించి ఎటువంటి హామీ ఇవ్వబడలేదు.

## భద్రత మరియు లైసెన్స్

[SECURITY.md](../../../SECURITY.md) చూడండి. సోర్స్ [Apache-2.0 లైసెన్స్](../../../LICENSE)ను ఉపయోగిస్తుంది. [packaging/license-policy.json](../../../packaging/license-policy.json) డిపెండెన్సీ-లైసెన్స్ విధానాన్ని నమోదు చేస్తుంది.
