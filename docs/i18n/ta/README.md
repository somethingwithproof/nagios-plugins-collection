<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: Apache-2.0
-->

# Nagios செருகுநிரல்களின் தொகுப்பு

[![CI](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=somethingwithproof_nagios-plugins-collection&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=somethingwithproof_nagios-plugins-collection)
[![codecov](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection/branch/main/graph/badge.svg)](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection)
[![Release](https://img.shields.io/github/v/release/somethingwithproof/nagios-plugins-collection)](https://github.com/somethingwithproof/nagios-plugins-collection/releases)
[![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/somethingwithproof/nagios-plugins-collection/main/pyproject.toml)](./pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/nagios-plugins-collection/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/nagios-plugins-collection)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · **தமிழ்** · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

வலைச் சேவைகள், தரவுத்தளங்கள், DNS, சான்றிதழ்கள், உள்கட்டமைப்பு மற்றும் மேகக்கணி வளங்களுக்கான கட்டளை நுழைவுப் புள்ளிகளைக் கொண்ட கண்காணிப்புச் சோதனைகளின் Python தொகுப்பு. ஒவ்வொரு செருகுநிரலின் செயலாக்கமும் அதன் விருப்பங்கள், முடிவுப் பொருள்கள் மற்றும் விருப்பச் சார்புகளை வரையறுக்கிறது.

## கிடைக்கும் நுழைவுப் புள்ளிகள்

பின்வரும் பெயர்கள் [pyproject.toml](../../../pyproject.toml) இல் அறிவிக்கப்பட்டுள்ளன, மேலும் அவற்றுக்குரிய மூலக் கோப்புகளைக் கொண்டுள்ளன:

| கட்டளை | செயலாக்கம் |
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

வரம்புகளை உள்ளமைப்பதற்கு முன்பு தனிப்பட்ட சோதனையின் `--help` மற்றும் செயலாக்கத்தைப் படிக்கவும். JSON, காலாவதி நேரம், செயல்திறன் தரவு மற்றும் அங்கீகார நடத்தை ஒவ்வொரு செருகுநிரலிலும் ஒரே மாதிரியாக இருக்கும் என்று கருதக்கூடாது.

## மூலத்திலிருந்து நிறுவுதல்

தொகுப்பு விவரக்குறிப்புக்கு Python >=3.11,<3.15 தேவைப்படுகிறது. [packaging/platform-support.json](../../../packaging/platform-support.json) மதிப்பாய்வு செய்யப்பட்ட இயக்க நேரம் மற்றும் தொகுப்பு இலக்குகளைப் பதிவு செய்கிறது. இந்தக் களஞ்சிய நகலிலிருந்து:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` பூட்டப்பட்ட சார்புகள், வளர்ச்சிக் கருவிகள் மற்றும் திட்டத்தை `.venv/` இல் நிறுவுகிறது; இயக்க-நேரச் சூழலுக்கு மட்டுமே (எடுத்துக்காட்டாக) `uv sync --locked --no-dev --extra aws` ஐப் பயன்படுத்தவும். கிடைக்கும் கூடுதல் தொகுப்புகள் விவரக்குறிப்பில் வரையறுக்கப்பட்டுள்ளன; உங்களுக்குத் தேவையான ஒருங்கிணைப்புகளை மட்டும் நிறுவவும். தொகுப்பு-அட்டவணை வெளியீட்டை வலியுறுத்தாமல் மூல நிறுவல் காட்டப்பட்டுள்ளது.

## இணக்கத்தன்மை மற்றும் செயல்பாடுகள்

Kubernetes அல்லது Nomad இல் சோதனைகளை இயக்க, [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) இல் உள்ள Helm chart ஐ அல்லது [deploy/nomad](../../../deploy/nomad) இல் உள்ள வேலையைப் பயன்படுத்தவும்; [நிறுவல் வழிகாட்டியில்](../../../docs/source/installation.rst#containers-and-kubernetes) Kubernetes Secret அல்லது Nomad Variable இலிருந்து வழங்கப்படும் ரகசியங்கள் உட்பட முழுமையான Helm மற்றும் Nomad எடுத்துக்காட்டுகள் உள்ளன.

வரலாற்று இடம்பெயர்வுக் குறிப்புகளுக்கு [MIGRATION.md](../../../MIGRATION.md) ஐப் பயன்படுத்தவும், ஆனால் இந்தக் களஞ்சிய நகலுடன் கட்டளைப் பெயர்களையும் விருப்பங்களையும் சரிபார்க்கவும். Python பதிப்பு மாற்றம், வகைக் குறிப்புகள் அல்லது CI உள்ளமைவு ஆகியவை ஒவ்வொரு மரபுச் சோதனைக்கும் மாறாத நடத்தையை உறுதிப்படுத்தாது. இயக்கப்படும் சோதனைக்கு வெளிப்புறச் சேவைகளும் தளக் கருவிகளும் கிடைக்க வேண்டும்.

## உள்ளூர்மயமாக்கல்

பகிரப்பட்ட CLI உதவி மற்றும் நோயறிதல் செய்திகள் தொகுக்கப்பட்ட stdlib-ஏற்றப்பட்ட பட்டியல்களைப் பயன்படுத்தி 45 மொழிகளை (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) ஆதரிக்கின்றன. தீர்மானம் முதலில் `--lang`, பின்னர் `LC_ALL`, `LC_MESSAGES` மற்றும் `LANG` ஆகியவற்றைச் சரிபார்த்து, இறுதியில் `en` க்குத் திரும்புகிறது. Nagios நிலை முன்னொட்டுகள் (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), செயல்திறன் தரவு மற்றும் JSON விசைகள் அனைத்து மொழிகளிலும் மாறாமல் இருக்கும்.

## வளர்ச்சி

சோதனைகளும் கருவி உள்ளமைவும் [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock) மற்றும் [CI பணிப்பாய்வு](../../../.github/workflows/ci.yml) ஆகியவற்றில் உள்ளன; `uv run pytest` உடன் சோதனைகளை இயக்கவும். நிலையான சோதனைக் கவரேஜ் சதவீதம், உலகளாவிய கடுமையான-வகை-சரிபார்ப்பு வெற்றி அல்லது விநியோகச் சங்கிலிச் சான்றிதழ் எதுவும் இங்கே கோரப்படவில்லை.

## பாதுகாப்பு மற்றும் உரிமம்

[SECURITY.md](../../../SECURITY.md) ஐப் பார்க்கவும். மூலம் [Apache-2.0 உரிமத்தைப்](../../../LICENSE) பயன்படுத்துகிறது. [packaging/license-policy.json](../../../packaging/license-policy.json) சார்பு-உரிமக் கொள்கையைப் பதிவு செய்கிறது.
