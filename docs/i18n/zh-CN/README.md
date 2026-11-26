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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · **简体中文** · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

这是一个 Python 监控检查插件集合，提供用于 Web 服务、数据库、DNS、证书、基础设施及云资源的命令入口点。每个插件的选项、结果语义和可选依赖均由其各自的实现决定。

## 可用入口点

以下名称声明于 [pyproject.toml](../../../pyproject.toml) 中，并有对应的源文件：

| 命令 | 实现 |
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

配置阈值前，请先阅读各个检查插件的 `--help` 说明及具体实现。切勿假定所有插件的 JSON 输出、超时处理、性能数据（performance-data）和认证行为完全一致。

## 从源码安装

项目清单要求 Python >=3.11,<3.15。[packaging/platform-support.json](../../../packaging/platform-support.json) 记录了经过评审的运行时和打包目标。在当前检出目录中执行：

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` 会将锁定的依赖、开发工具及本项目安装到 `.venv/` 中；如果仅需运行时环境，可使用例如 `uv sync --locked --no-dev --extra aws` 的命令。可用的扩展依赖项（extras）定义在清单文件中；请仅安装你需要的集成组件。此处仅展示从源码安装的方式，并不代表已发布至软件包索引。

## 兼容性与运维

要在 Kubernetes 或 Nomad 上运行检查，请使用 [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) 中的 Helm chart 或 [deploy/nomad](../../../deploy/nomad) 中的作业配置；[安装指南](../../../docs/source/installation.rst#containers-and-kubernetes)提供了完整的 Helm 和 Nomad 示例，包括从 Kubernetes Secret 或 Nomad Variable 提供密钥的配置方法。

历史迁移说明请参阅 [MIGRATION.md](../../../MIGRATION.md)，但请务必以当前检出目录核实命令名称和选项。Python 版本变更、类型提示或 CI 配置的更新，并不意味着所有历史遗留检查插件的行为都保持不变。所运行检查依赖的外部服务和平台工具必须处于可用状态。

## 本地化

共享 CLI 帮助和诊断消息通过随包附带、由标准库加载的语言目录支持 45 种语言区域（`en`、`de`、`es`、`fr`、`it`、`pt-BR`、`nl`、`ru`、`uk`、`ja`、`ko`、`zh-CN`、`zh-TW`、`ar`、`hi`、`pl`、`tr`、`sv`、`vi`、`id`、`af-ZA`、`am-ET`、`ar-EG`、`ar-MA`、`fr-MA`、`fr-SN`、`ha-NG`、`ig-NG`、`mg-MG`、`rw-RW`、`so-SO`、`sw-KE`、`xh-ZA`、`yo-NG`、`zu-ZA`、`bn`、`fa`、`he`、`mr`、`ta`、`te`、`th`、`ur`、`ms`、`fil`）。语言区域解析依次检查 `--lang`、`LC_ALL`、`LC_MESSAGES` 和 `LANG`，最后回退到 `en`。Nagios 状态前缀（`OK`、`WARNING`、`CRITICAL`、`UNKNOWN`）、性能数据和 JSON 键名在所有语言区域中均保持不变。

## 开发

测试与工具配置位于 [pyproject.toml](../../../pyproject.toml)、[uv.lock](../../../uv.lock) 和 [CI 工作流](../../../.github/workflows/ci.yml)中；使用 `uv run pytest` 运行测试。本仓库不对固定的测试覆盖率百分比、全局严格类型检查通过率或供应链认证作任何承诺。

## 安全与许可证

请参阅 [SECURITY.md](../../../SECURITY.md)。源码采用 [Apache-2.0 许可证](../../../LICENSE)。[packaging/license-policy.json](../../../packaging/license-policy.json) 记录了依赖项的许可证策略。
