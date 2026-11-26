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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · **Français (Maroc)** · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Une collection Python de sondes de supervision dotées de points d'entrée en ligne de commande pour les services web, bases de données, DNS, certificats, infrastructures et ressources cloud. L'implémentation de chaque plugin définit ses options, la sémantique de ses résultats et ses dépendances optionnelles.

## Points d'entrée disponibles

Les noms suivants sont déclarés dans [pyproject.toml](../../../pyproject.toml) et disposent de fichiers sources correspondants :

| Commande | Implémentation |
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

Consultez l'option `--help` ainsi que l'implémentation de chaque sonde avant de paramétrer vos seuils. Le comportement relatif au format JSON, aux délais d'expiration, aux données de performance et à l'authentification ne doit pas être supposé identique d'un plugin à l'autre.

## Installation depuis les sources

Le manifeste exige Python >=3.11,<3.15. Le fichier [packaging/platform-support.json](../../../packaging/platform-support.json) consigne les environnements d'exécution et les cibles d'empaquetage validés. Depuis cette copie locale :

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` installe les dépendances verrouillées, les outils de développement et le projet dans `.venv/` ; utilisez par exemple `uv sync --locked --no-dev --extra aws` pour un environnement d'exécution uniquement. Les extras disponibles sont définis dans le manifeste ; n'installez que les intégrations dont vous avez besoin. L'installation depuis les sources est présentée sans affirmer de publication sur un index de paquets.

## Compatibilité et exploitation

Pour exécuter les sondes sur Kubernetes ou Nomad, utilisez le chart Helm dans [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) ou le job dans [deploy/nomad](../../../deploy/nomad) ; le [guide d'installation](../../../docs/source/installation.rst#containers-and-kubernetes) propose des exemples complets pour Helm et Nomad, y compris des secrets fournis depuis un Kubernetes Secret ou une Nomad Variable.

Consultez [MIGRATION.md](../../../MIGRATION.md) pour les notes historiques de migration, mais vérifiez les noms de commandes et les options sur cette copie locale. Un changement de version Python, l'ajout d'annotations de types ou une configuration CI ne garantissent pas un comportement inchangé pour chaque ancienne sonde. Les services externes et les outils système requis doivent être disponibles pour la sonde exécutée.

## Localisation

L'aide en ligne de commande partagée et les messages de diagnostic prennent en charge 45 locales (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) à l'aide de catalogues intégrés chargés via la bibliothèque standard. La résolution vérifie `--lang`, puis `LC_ALL`, `LC_MESSAGES` et `LANG`, avec repli sur `en`. Les préfixes d'état Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), les données de performance et les clés JSON demeurent inchangés dans toutes les locales.

## Développement

Les tests et la configuration des outils se trouvent dans [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock) et [le workflow CI](../../../.github/workflows/ci.yml) ; exécutez les tests avec `uv run pytest`. Aucun pourcentage fixe de couverture, aucun succès universel de vérification stricte des types ni aucune certification de chaîne d'approvisionnement ne sont revendiqués ici.

## Sécurité et licence

Voir [SECURITY.md](../../../SECURITY.md). Le code source utilise la [licence Apache-2.0](../../../LICENSE). Le fichier [packaging/license-policy.json](../../../packaging/license-policy.json) définit la politique de licences des dépendances.
