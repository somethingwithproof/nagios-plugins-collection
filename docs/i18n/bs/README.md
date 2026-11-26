<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: Apache-2.0
-->

# Kolekcija Nagios dodataka

[![CI](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=somethingwithproof_nagios-plugins-collection&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=somethingwithproof_nagios-plugins-collection)
[![codecov](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection/branch/main/graph/badge.svg)](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection)
[![Release](https://img.shields.io/github/v/release/somethingwithproof/nagios-plugins-collection)](https://github.com/somethingwithproof/nagios-plugins-collection/releases)
[![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/somethingwithproof/nagios-plugins-collection/main/pyproject.toml)](../../../pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](../../../LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/nagios-plugins-collection/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/nagios-plugins-collection)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (28 locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · **Bosanski** · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Hrvatski](../hr/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Српски](../sr/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Python kolekcija provjera za nadzor sa komandnim ulaznim tačkama za web servise, baze podataka, DNS, certifikate, infrastrukturu i resurse u oblaku. Implementacija svakog dodatka određuje njegove opcije, semantiku rezultata i opcionalne zavisnosti.

## Dostupne ulazne tačke

Sljedeći nazivi su navedeni u [pyproject.toml](../../../pyproject.toml) i imaju odgovarajuće datoteke izvornog koda:

| Komanda | Implementacija |
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

Prije podešavanja pragova pročitajte `--help` i implementaciju pojedinačne provjere. Ne treba pretpostavljati da je ponašanje za JSON, vremensko ograničenje, podatke o performansama i autentifikaciju isto za svaki dodatak.

## Instalacija iz izvornog koda

Manifest zahtijeva Python >=3.11,<3.15. Datoteka [packaging/platform-support.json](../../../packaging/platform-support.json) evidentira provjerena okruženja izvršavanja i ciljeve pakovanja. Iz ove lokalne kopije repozitorija:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` instalira zaključane zavisnosti, razvojne alate i projekat u `.venv/`; za okruženje samo za izvršavanje koristite npr. `uv sync --locked --no-dev --extra aws`. Dostupni dodatni paketi (extras) definisani su u manifestu; instalirajte samo integracije koje su vam potrebne. Instalacija iz izvornog koda prikazana je bez tvrdnje o objavi u indeksu paketa.

## Kompatibilnost i rad u produkciji

Za pokretanje provjera na Kubernetesu ili Nomadu koristite Helm chart u [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) ili definiciju posla u [deploy/nomad](../../../deploy/nomad); [vodič za instalaciju](../../../docs/source/installation.rst#containers-and-kubernetes) sadrži potpune primjere za Helm i Nomad, uključujući prosljeđivanje tajni iz Kubernetes Secret objekta ili Nomad Variable zapisa.

Za historijske bilješke o migraciji pogledajte [MIGRATION.md](../../../MIGRATION.md), ali provjerite nazive komandi i opcije u odnosu na ovu kopiju koda. Promjena verzije Pythona, tipovi ili CI postavke ne garantuju nepromijenjeno ponašanje za svaku naslijeđenu provjeru. Vanjski servisi i alati platforme moraju biti dostupni na računaru ili serveru gdje se provjera izvršava.

## Lokalizacija

Zajednička CLI pomoć i dijagnostičke poruke podržavaju 48 lokala (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`, `bs`, `hr`, `sr`) koristeći ugrađene kataloge koji se učitavaju putem standardne biblioteke. Određivanje jezika provjerava `--lang`, zatim `LC_ALL`, `LC_MESSAGES` i `LANG`, te se vraća na `en`. Nagios statusni prefiksi (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), podaci o performansama i JSON ključevi ostaju nepromijenjeni u svim lokalima.

## Razvoj

Testovi i postavke alata nalaze se u [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock) i [CI radnom toku](../../../.github/workflows/ci.yml); pokrenite testove komandom `uv run pytest`. Ovdje se ne tvrdi fiksni procenat pokrivenosti, univerzalna stroga provjera tipova niti certifikacija lanca snabdijevanja.

## Sigurnost i licenca

Pogledajte [SECURITY.md](../../../SECURITY.md). Izvorni kod koristi [Apache-2.0 licencu](../../../LICENSE). Datoteka [packaging/license-policy.json](../../../packaging/license-policy.json) evidentira politiku licenci za zavisnosti.
