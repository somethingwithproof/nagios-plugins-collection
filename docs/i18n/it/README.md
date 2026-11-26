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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · **Italiano** · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Una raccolta Python di controlli di monitoraggio con entry point da riga di comando per servizi web, database, DNS, certificati, infrastruttura e risorse cloud. L'implementazione di ciascun plugin ne definisce opzioni, semantica dei risultati e dipendenze opzionali.

## Entry point disponibili

I seguenti nomi sono dichiarati in [pyproject.toml](../../../pyproject.toml) e dispongono dei corrispondenti file sorgente:

| Comando | Implementazione |
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

Leggi il `--help` e l'implementazione del singolo controllo prima di configurare le soglie. Non dare per scontato che JSON, timeout, dati sulle prestazioni e gestione dell'autenticazione siano identici per ogni plugin.

## Installazione dai sorgenti

Il manifest richiede Python >=3.11,<3.15. [packaging/platform-support.json](../../../packaging/platform-support.json) registra i target di runtime e pacchettizzazione esaminati. Da questo checkout:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` installa le dipendenze bloccate, gli strumenti di sviluppo e il progetto in `.venv/`; usa `uv sync --locked --no-dev --extra aws` (ad esempio) per un ambiente di solo runtime. Gli extra disponibili sono definiti nel manifest; installa solo le integrazioni di cui hai bisogno. L'installazione dai sorgenti è mostrata senza affermare la pubblicazione su un indice di pacchetti.

## Compatibilità e operatività

Per eseguire i controlli su Kubernetes o Nomad, usa il chart Helm in [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) o il job in [deploy/nomad](../../../deploy/nomad); la [guida all'installazione](../../../docs/source/installation.rst#containers-and-kubernetes) contiene esempi completi per Helm e Nomad, inclusi segreti forniti da un Secret di Kubernetes o da una Variable di Nomad.

Consulta [MIGRATION.md](../../../MIGRATION.md) per le note storiche sulla migrazione, ma verifica i nomi dei comandi e le opzioni rispetto a questo checkout. Un cambio di versione di Python, le annotazioni di tipo o la configurazione CI non attestano che il comportamento sia rimasto invariato per ogni controllo legacy. I servizi esterni e gli strumenti di piattaforma devono essere disponibili per il controllo eseguito.

## Localizzazione

La guida condivisa della CLI e i messaggi diagnostici supportano 45 lingue (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) utilizzando cataloghi integrati caricati tramite stdlib. La risoluzione controlla `--lang`, poi `LC_ALL`, `LC_MESSAGES` e `LANG`, ripiegando su `en`. I prefissi di stato Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), i dati sulle prestazioni e le chiavi JSON restano invariati in tutte le lingue.

## Sviluppo

I test e la configurazione degli strumenti si trovano in [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock) e [nel workflow CI](../../../.github/workflows/ci.yml); esegui i test con `uv run pytest`. Qui non vengono dichiarate percentuali di copertura fisse, esito positivo universale del controllo dei tipi rigoroso o certificazioni della supply chain.

## Sicurezza e licenza

Consulta [SECURITY.md](../../../SECURITY.md). I sorgenti utilizzano la [licenza Apache-2.0](../../../LICENSE). [packaging/license-policy.json](../../../packaging/license-policy.json) registra la policy sulle licenze delle dipendenze.
