<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: Apache-2.0
-->

# Nagios 外掛程式集

[![CI](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=somethingwithproof_nagios-plugins-collection&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=somethingwithproof_nagios-plugins-collection)
[![codecov](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection/branch/main/graph/badge.svg)](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection)
[![Release](https://img.shields.io/github/v/release/somethingwithproof/nagios-plugins-collection)](https://github.com/somethingwithproof/nagios-plugins-collection/releases)
[![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/somethingwithproof/nagios-plugins-collection/main/pyproject.toml)](../../../pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](../../../LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/nagios-plugins-collection/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/nagios-plugins-collection)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · **繁體中文** · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

一套以 Python 編寫的監控檢查外掛程式集合，提供適用於 Web 服務、資料庫、DNS、憑證、基礎設施與雲端資源的命令進入點。各項外掛程式的選項、結果語意與選用相依套件皆由其實作本身定義。

## 可用的進入點

以下名稱皆已宣告於 [pyproject.toml](../../../pyproject.toml)，並具備對應的原始碼檔案：

| 指令 | 實作檔案 |
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

設定閾值前，請先閱讀個別檢查工具的 `--help` 說明與實作內容。請勿假設每個外掛程式的 JSON 格式、逾時處理、效能資料與身分驗證行為皆完全相同。

## 從原始碼安裝

專案資訊清單要求 Python >=3.11,<3.15。[packaging/platform-support.json](../../../packaging/platform-support.json) 記錄了經過審視的執行期與封裝目標。在此簽出複本中執行：

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` 會將已鎖定版本的相依套件、開發工具與本專案安裝至 `.venv/`；若需要僅含執行環境的設定，可使用例如 `uv sync --locked --no-dev --extra aws` 的指令。可用的額外套件組（extras）皆定義於資訊清單中，請僅安裝您需要的整合項目。此處所示為從原始碼安裝的方式，並不代表已發佈至套件索引。

## 相容性與維運

若要在 Kubernetes 或 Nomad 上執行檢查，請使用位於 [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) 的 Helm chart 或位於 [deploy/nomad](../../../deploy/nomad) 的作業設定；[安裝指南](../../../docs/source/installation.rst#containers-and-kubernetes) 提供完整的 Helm 與 Nomad 範例，包含從 Kubernetes Secret 或 Nomad Variable 供給機密資訊的做法。

歷史遷移說明請參閱 [MIGRATION.md](../../../MIGRATION.md)，但請務必以此簽出複本核對指令名稱與選項。Python 版本變更、型別提示或 CI 設定並不保證所有舊版檢查工具的行為皆維持不變。執行檢查時，必須確保目標外部服務與平台工具處於可用狀態。

## 在地化

共用的 CLI 說明與診斷訊息透過內建由標準程式庫載入的語系目錄，支援 45 種語系（`en`、`de`、`es`、`fr`、`it`、`pt-BR`、`nl`、`ru`、`uk`、`ja`、`ko`、`zh-CN`、`zh-TW`、`ar`、`hi`、`pl`、`tr`、`sv`、`vi`、`id`、`af-ZA`、`am-ET`、`ar-EG`、`ar-MA`、`fr-MA`、`fr-SN`、`ha-NG`、`ig-NG`、`mg-MG`、`rw-RW`、`so-SO`、`sw-KE`、`xh-ZA`、`yo-NG`、`zu-ZA`、`bn`、`fa`、`he`、`mr`、`ta`、`te`、`th`、`ur`、`ms`、`fil`）。解析順序為檢查 `--lang`，接著是 `LC_ALL`、`LC_MESSAGES` 與 `LANG`，最後備援至 `en`。Nagios 狀態前綴（`OK`、`WARNING`、`CRITICAL`、`UNKNOWN`）、效能資料與 JSON 鍵值在所有語系中皆保持不變。

## 開發

測試與工具設定位於 [pyproject.toml](../../../pyproject.toml)、[uv.lock](../../../uv.lock) 與 [CI 工作流程](../../../.github/workflows/ci.yml)；請使用 `uv run pytest` 執行測試。本處不宣稱任何固定的測試覆蓋率百分比、全面通過嚴格型別檢查或供應鏈認證。

## 安全性與授權條款

請參閱 [SECURITY.md](../../../SECURITY.md)。原始碼採用 [Apache-2.0 授權條款](../../../LICENSE)。[packaging/license-policy.json](../../../packaging/license-policy.json) 記錄了相依套件的授權原則。
