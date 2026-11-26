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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · **한국어** · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

웹 서비스, 데이터베이스, DNS, 인증서, 인프라 및 클라우드 리소스를 위한 명령 진입점을 제공하는 Python 기반 모니터링 검사 모음입니다. 각 플러그인의 구현이 옵션, 결과 의미론 및 선택적 종속성을 정의합니다.

## 사용 가능한 진입점

다음 이름들은 [pyproject.toml](../../../pyproject.toml)에 선언되어 있으며 해당 소스 파일을 가지고 있습니다:

| 명령 | 구현 |
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

임계값을 구성하기 전에 개별 검사의 `--help`와 구현을 확인하세요. JSON, 타임아웃, 성능 데이터 및 인증 동작은 모든 플러그인에서 동일하다고 가정해서는 안 됩니다.

## 소스에서 설치

매니페스트는 Python >=3.11,<3.15를 요구합니다. [packaging/platform-support.json](../../../packaging/platform-support.json)에는 검토된 런타임 및 패키징 대상이 기록되어 있습니다. 이 체크아웃 디렉터리에서 다음을 실행하세요:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync`는 잠긴(locked) 종속성, 개발 도구 및 프로젝트를 `.venv/`에 설치합니다. 런타임 전용 환경에는 예를 들어 `uv sync --locked --no-dev --extra aws`를 사용하세요. 사용 가능한 extra 항목은 매니페스트에 정의되어 있으므로 필요한 통합 기능만 설치하세요. 소스 설치 방법은 패키지 인덱스 배포 여부를 단정하지 않고 안내됩니다.

## 호환성 및 운영

Kubernetes 또는 Nomad에서 검사를 실행하려면 [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection)의 Helm 차트 또는 [deploy/nomad](../../../deploy/nomad)의 작업을 사용하세요. [설치 가이드](../../../docs/source/installation.rst#containers-and-kubernetes)에는 Kubernetes Secret 또는 Nomad Variable에서 비밀을 제공하는 방법을 포함한 전체 Helm 및 Nomad 예제가 있습니다.

이전 마이그레이션 참고 사항은 [MIGRATION.md](../../../MIGRATION.md)를 참조하되, 명령 이름과 옵션은 현재 체크아웃을 기준으로 확인하세요. Python 버전 변경, 타입 힌트 또는 CI 구성이 모든 레거시 검사의 동작 불변을 보장하지는 않습니다. 실행하려는 검사에 필요한 외부 서비스와 플랫폼 도구가 사용 가능해야 합니다.

## 지역화

공유 CLI 도움말과 진단 메시지는 번들된 stdlib 로드 카탈로그를 사용하여 45개 로캘(`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`)을 지원합니다. 로캘 확인은 `--lang`, `LC_ALL`, `LC_MESSAGES`, `LANG` 순서로 확인하며 기본값은 `en`입니다. Nagios 상태 접두사(`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), 성능 데이터 및 JSON 키는 모든 로캘에서 동일하게 유지됩니다.

## 개발

테스트 및 도구 구성은 [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock) 및 [CI 워크플로](../../../.github/workflows/ci.yml)에 있으며, 테스트는 `uv run pytest`로 실행합니다. 여기에서는 고정된 커버리지 비율, 보편적인 엄격한 타입 검사 성공 또는 공급망 인증을 주장하지 않습니다.

## 보안 및 라이선스

[SECURITY.md](../../../SECURITY.md)를 참조하세요. 소스는 [Apache-2.0 라이선스](../../../LICENSE)를 사용합니다. [packaging/license-policy.json](../../../packaging/license-policy.json)에는 종속성 라이선스 정책이 기록되어 있습니다.
