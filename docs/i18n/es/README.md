<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: Apache-2.0
-->

# Colección de plugins de Nagios

[![CI](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=somethingwithproof_nagios-plugins-collection&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=somethingwithproof_nagios-plugins-collection)
[![codecov](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection/branch/main/graph/badge.svg)](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection)
[![Release](https://img.shields.io/github/v/release/somethingwithproof/nagios-plugins-collection)](https://github.com/somethingwithproof/nagios-plugins-collection/releases)
[![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/somethingwithproof/nagios-plugins-collection/main/pyproject.toml)](./pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/nagios-plugins-collection/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/nagios-plugins-collection)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · **Español** · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · [Українська](../uk/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Una colección en Python de comprobaciones de monitorización con puntos de entrada de comandos para servicios web, bases de datos, DNS, certificados, infraestructura y recursos en la nube. La implementación de cada plugin define sus opciones, la semántica de sus resultados y sus dependencias opcionales.

## Puntos de entrada disponibles

Los siguientes nombres están declarados en [pyproject.toml](../../../pyproject.toml) y tienen sus archivos fuente correspondientes:

| Comando | Implementación |
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

Lee el `--help` y la implementación de cada comprobación individual antes de configurar los umbrales. No debe asumirse que el comportamiento de JSON, tiempo de espera, datos de rendimiento y autenticación sea idéntico en todos los plugins.

## Instalación desde el código fuente

El manifiesto requiere Python >=3.11,<3.15. [packaging/platform-support.json](../../../packaging/platform-support.json) registra los entornos de ejecución y objetivos de empaquetado revisados. Desde esta copia del repositorio:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` instala las dependencias fijadas, las herramientas de desarrollo y el proyecto en `.venv/`; usa `uv sync --locked --no-dev --extra aws` (por ejemplo) para un entorno exclusivo de ejecución. Los extras disponibles están definidos en el manifiesto; instala solo las integraciones que necesites. Se muestra la instalación desde el código fuente sin afirmar la publicación en índices de paquetes.

## Compatibilidad y operaciones

Para ejecutar comprobaciones en Kubernetes o Nomad, usa el chart de Helm en [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) o el trabajo en [deploy/nomad](../../../deploy/nomad); la [guía de instalación](../../../docs/source/installation.rst#containers-and-kubernetes) incluye ejemplos completos de Helm y Nomad, incluidos secretos proporcionados desde un Secret de Kubernetes o una Variable de Nomad.

Usa [MIGRATION.md](../../../MIGRATION.md) para consultar notas históricas de migración, pero verifica los nombres de comandos y opciones frente a esta copia del repositorio. Un cambio de versión de Python, las anotaciones de tipos o la configuración de CI no garantizan un comportamiento sin cambios para todas las comprobaciones heredadas. Los servicios externos y las herramientas de plataforma deben estar disponibles para la comprobación que se vaya a ejecutar.

## Localización

La ayuda compartida de la CLI y los mensajes de diagnóstico admiten 45 configuraciones regionales (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) mediante catálogos integrados cargados con la biblioteca estándar. La resolución comprueba `--lang`, luego `LC_ALL`, `LC_MESSAGES` y `LANG`, recurriendo a `en`. Los prefijos de estado de Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), los datos de rendimiento y las claves JSON permanecen sin cambios en todas las configuraciones regionales.

## Desarrollo

Las pruebas y la configuración de herramientas se encuentran en [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock) y [el flujo de trabajo de CI](../../../.github/workflows/ci.yml); ejecuta las pruebas con `uv run pytest`. No se afirma aquí ningún porcentaje fijo de cobertura, éxito universal de comprobación estricta de tipos ni certificación de la cadena de suministro.

## Seguridad y licencia

Consulta [SECURITY.md](../../../SECURITY.md). El código fuente utiliza la [licencia Apache-2.0](../../../LICENSE). [packaging/license-policy.json](../../../packaging/license-policy.json) registra la política de licencias de dependencias.
