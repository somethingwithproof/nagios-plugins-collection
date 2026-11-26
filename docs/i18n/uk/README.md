<!--
SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
SPDX-License-Identifier: Apache-2.0
-->

# Колекція плагінів Nagios

[![CI](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/somethingwithproof/nagios-plugins-collection/actions/workflows/ci.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=somethingwithproof_nagios-plugins-collection&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=somethingwithproof_nagios-plugins-collection)
[![codecov](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection/branch/main/graph/badge.svg)](https://codecov.io/gh/somethingwithproof/nagios-plugins-collection)
[![Release](https://img.shields.io/github/v/release/somethingwithproof/nagios-plugins-collection)](https://github.com/somethingwithproof/nagios-plugins-collection/releases)
[![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/somethingwithproof/nagios-plugins-collection/main/pyproject.toml)](./pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/somethingwithproof/nagios-plugins-collection/badge)](https://scorecard.dev/viewer/?uri=github.com/somethingwithproof/nagios-plugins-collection)

**Languages:** [English](../../../README.md) · [Deutsch](../de/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md) · [Português (BR)](../pt-BR/README.md) · [Nederlands](../nl/README.md) · [Русский](../ru/README.md) · **Українська** · [日本語](../ja/README.md) · [한국어](../ko/README.md) · [简体中文](../zh-CN/README.md) · [繁體中文](../zh-TW/README.md) · [العربية](../ar/README.md) · [हिन्दी](../hi/README.md) · [Polski](../pl/README.md) · [Türkçe](../tr/README.md) · [Svenska](../sv/README.md) · [Tiếng Việt](../vi/README.md) · [Bahasa Indonesia](../id/README.md)

<details><summary>More languages (25 African &amp; Asian locales)</summary>

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · [ไทย](../th/README.md) · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

Колекція перевірок моніторингу на Python із точками входу команд для вебсервісів, баз даних, DNS, сертифікатів, інфраструктури та хмарних ресурсів. Реалізація кожного плагіна визначає його параметри, семантику результатів і необов'язкові залежності.

## Доступні точки входу

Наведені нижче назви оголошено у [pyproject.toml](../../../pyproject.toml), і вони мають відповідні файли вихідного коду:

| Команда | Реалізація |
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

Перед налаштуванням порогових значень ознайомтеся з довідкою `--help` та реалізацією конкретної перевірки. Не слід вважати, що поведінка JSON, тайм-аутів, даних продуктивності (performance data) та автентифікації є однаковою для всіх плагінів.

## Встановлення з вихідного коду

Маніфест вимагає Python >=3.11,<3.15. У файлі [packaging/platform-support.json](../../../packaging/platform-support.json) зафіксовано перевірені цільові середовища виконання та пакування. Із цієї локальної копії:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` встановлює зафіксовані залежності, інструменти розробки та сам проєкт у `.venv/`; використовуйте, наприклад, `uv sync --locked --no-dev --extra aws` для середовища лише для виконання. Доступні додаткові компоненти (extras) визначені в маніфесті; встановлюйте лише потрібні вам інтеграції. Встановлення з вихідного коду наведено без ствердження про публікацію в індексі пакетів.

## Сумісність та експлуатація

Щоб запускати перевірки в Kubernetes або Nomad, використовуйте Helm-чарт у [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) або завдання в [deploy/nomad](../../../deploy/nomad); [посібник зі встановлення](../../../docs/source/installation.rst#containers-and-kubernetes) містить повні приклади для Helm і Nomad, зокрема передачу секретів із Kubernetes Secret або Nomad Variable.

Зверніться до [MIGRATION.md](../../../MIGRATION.md) щодо історичних нотаток про міграцію, але перевіряйте назви команд і параметри за цією локальною копією. Зміна версії Python, анотації типів або конфігурація CI не гарантують незмінної поведінки для кожної застарілої перевірки. Для виконуваної перевірки мають бути доступні зовнішні сервіси та платформні інструменти.

## Локалізація

Спільна довідка CLI та діагностичні повідомлення підтримують 45 мов (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) за допомогою вбудованих каталогів, що завантажуються через стандартну бібліотеку (stdlib). Визначення локалі перевіряє `--lang`, далі `LC_ALL`, `LC_MESSAGES` і `LANG`, із переходом до `en` за замовчуванням. Префікси статусу Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), дані продуктивності та ключі JSON залишаються незмінними в усіх локалях.

## Розробка

Тести та конфігурація інструментів знаходяться у [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock) та [робочому процесі CI](../../../.github/workflows/ci.yml); запускайте тести командою `uv run pytest`. Тут не заявляється фіксований відсоток покриття, універсальне проходження суворої перевірки типів або сертифікація ланцюга постачання.

## Безпека та ліцензія

Дивіться [SECURITY.md](../../../SECURITY.md). Вихідний код використовує [ліцензію Apache-2.0](../../../LICENSE). Політика щодо ліцензій залежностей зафіксована у [packaging/license-policy.json](../../../packaging/license-policy.json).
