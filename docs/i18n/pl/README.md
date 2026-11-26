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

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · **Polski** · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Zestaw wtyczek monitorujących w języku Python z punktami wejścia wiersza poleceń dla usług sieciowych, baz danych, DNS, certyfikatów, infrastruktury oraz zasobów chmurowych. Implementacja każdej wtyczki definiuje jej opcje, semantykę wyników oraz opcjonalne zależności.

## Dostępne punkty wejścia

Następujące nazwy są zadeklarowane w [pyproject.toml](../../../pyproject.toml) i posiadają odpowiadające im pliki źródłowe:

| Polecenie | Implementacja |
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

Przed skonfigurowaniem progów zapoznaj się z `--help` oraz implementacją konkretnego testu. Nie należy zakładać, że obsługa JSON, limitów czasu, danych wydajnościowych (performance data) i uwierzytelniania jest identyczna w każdej wtyczce.

## Instalacja ze źródeł

Manifest wymaga Pythona >=3.11,<3.15. Plik [packaging/platform-support.json](../../../packaging/platform-support.json) zawiera zweryfikowane docelowe środowiska uruchomieniowe oraz pakietowania. Z poziomu tej kopii repozytorium:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` instaluje zablokowane zależności, narzędzia programistyczne oraz projekt w `.venv/`; użyj np. `uv sync --locked --no-dev --extra aws`, aby uzyskać środowisko wyłącznie uruchomieniowe. Dostępne pakiety dodatkowe (extras) są zdefiniowane w manifeście; instaluj tylko potrzebne integracje. Przedstawiono instalację ze źródeł bez deklarowania publikacji w indeksie pakietów.

## Zgodność i obsługa operacyjna

Aby uruchamiać testy na Kubernetes lub Nomad, skorzystaj z wykresu Helm w [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) lub zadania w [deploy/nomad](../../../deploy/nomad); [przewodnik instalacji](../../../docs/source/installation.rst#containers-and-kubernetes) zawiera kompletne przykłady dla Helm i Nomad, w tym sekrety przekazywane z Kubernetes Secret lub Nomad Variable.

Sprawdź [MIGRATION.md](../../../MIGRATION.md) w celu zapoznania się z historycznymi uwagami dotyczącymi migracji, ale zweryfikuj nazwy poleceń i opcje w tej kopii repozytorium. Zmiana wersji Pythona, adnotacje typów czy konfiguracja CI nie gwarantują niezmienionego zachowania każdego starszego testu. Usługi zewnętrzne i narzędzia platformowe muszą być dostępne dla uruchamianego testu.

## Lokalizacja

Wspólna pomoc CLI oraz komunikaty diagnostyczne obsługują 45 języków (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) przy użyciu wbudowanych katalogów ładowanych przez bibliotekę standardową. Rozpoznawanie języka sprawdza `--lang`, następnie `LC_ALL`, `LC_MESSAGES` i `LANG`, z powrotem do `en`. Prefiksy statusu Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), dane wydajnościowe oraz klucze JSON pozostają niezmienione we wszystkich językach.

## Rozwój

Testy i konfiguracja narzędzi znajdują się w [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock) oraz [przepływie pracy CI](../../../.github/workflows/ci.yml); testy uruchamiaj poleceniem `uv run pytest`. Nie deklaruje się tu żadnego stałego progu pokrycia testami, powszechnego przechodzenia ścisłego sprawdzania typów ani certyfikacji łańcucha dostaw.

## Bezpieczeństwo i licencja

Zobacz [SECURITY.md](../../../SECURITY.md). Kod źródłowy korzysta z [licencji Apache-2.0](../../../LICENSE). Plik [packaging/license-policy.json](../../../packaging/license-policy.json) określa politykę dotyczącą licencji zależności.
