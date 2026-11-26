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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · **Português (BR)** · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Uma coleção em Python de verificações de monitoramento com pontos de entrada de linha de comando para serviços web, bancos de dados, DNS, certificados, infraestrutura e recursos em nuvem. A implementação de cada plugin define suas opções, semântica de resultados e dependências opcionais.

## Pontos de entrada disponíveis

Os seguintes nomes estão declarados em [pyproject.toml](../../../pyproject.toml) e possuem arquivos-fonte correspondentes:

| Comando | Implementação |
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

Leia o `--help` e a implementação de cada verificação antes de configurar os limites. Não presuma que o comportamento de JSON, tempo limite, dados de desempenho e autenticação seja idêntico em todos os plugins.

## Instalação a partir do código-fonte

O manifesto exige Python >=3.11,<3.15. [packaging/platform-support.json](../../../packaging/platform-support.json) registra os alvos de runtime e empacotamento revisados. A partir deste clone:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` instala as dependências fixadas, as ferramentas de desenvolvimento e o projeto em `.venv/`; use `uv sync --locked --no-dev --extra aws` (por exemplo) para um ambiente apenas de execução. Os extras disponíveis estão definidos no manifesto; instale somente as integrações de que você precisa. A instalação a partir do código-fonte é mostrada sem afirmar publicação em índice de pacotes.

## Compatibilidade e operações

Para executar verificações no Kubernetes ou no Nomad, use o chart Helm em [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) ou o job em [deploy/nomad](../../../deploy/nomad); o [guia de instalação](../../../docs/source/installation.rst#containers-and-kubernetes) traz exemplos completos de Helm e Nomad, incluindo segredos fornecidos a partir de um Kubernetes Secret ou de uma Nomad Variable.

Use [MIGRATION.md](../../../MIGRATION.md) para notas históricas de migração, mas verifique os nomes de comandos e opções neste clone. Uma mudança de versão do Python, anotações de tipo ou configuração de CI não garantem comportamento inalterado para todas as verificações legadas. Serviços externos e ferramentas de plataforma devem estar disponíveis para a verificação em execução.

## Localização

A ajuda compartilhada da CLI e as mensagens de diagnóstico oferecem suporte a 45 idiomas (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) usando catálogos empacotados carregados com a biblioteca padrão. A resolução verifica `--lang`, depois `LC_ALL`, `LC_MESSAGES` e `LANG`, recorrendo a `en` como padrão. Prefixos de status do Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), dados de desempenho e chaves JSON permanecem inalterados em todos os idiomas.

## Desenvolvimento

Os testes e a configuração das ferramentas ficam em [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock) e [no workflow de CI](../../../.github/workflows/ci.yml); execute os testes com `uv run pytest`. Nenhuma porcentagem fixa de cobertura, sucesso universal na verificação estrita de tipos ou certificação de cadeia de suprimentos é reivindicada aqui.

## Segurança e licença

Consulte [SECURITY.md](../../../SECURITY.md). O código-fonte usa a [licença Apache-2.0](../../../LICENSE). [packaging/license-policy.json](../../../packaging/license-policy.json) registra a política de licenças das dependências.
