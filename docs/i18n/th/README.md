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

[Afrikaans](../af-ZA/README.md) · [አማርኛ](../am-ET/README.md) · [العربية (مصر)](../ar-EG/README.md) · [العربية (المغرب)](../ar-MA/README.md) · [বাংলা](../bn/README.md) · [فارسی](../fa/README.md) · [Filipino](../fil/README.md) · [Français (Maroc)](../fr-MA/README.md) · [Français (Sénégal)](../fr-SN/README.md) · [Hausa](../ha-NG/README.md) · [עברית](../he/README.md) · [Igbo](../ig-NG/README.md) · [Malagasy](../mg-MG/README.md) · [मराठी](../mr/README.md) · [Bahasa Melayu](../ms/README.md) · [Kinyarwanda](../rw-RW/README.md) · [Soomaali](../so-SO/README.md) · [Kiswahili](../sw-KE/README.md) · [தமிழ்](../ta/README.md) · [తెలుగు](../te/README.md) · **ไทย** · [اردو](../ur/README.md) · [isiXhosa](../xh-ZA/README.md) · [Yorùbá](../yo-NG/README.md) · [isiZulu](../zu-ZA/README.md)

</details>

ชุดปลั๊กอินตรวจสอบระบบภาษา Python พร้อมคำสั่งจุดเข้าใช้งาน (entry points) สำหรับบริการเว็บ ฐานข้อมูล DNS ใบรับรอง โครงสร้างพื้นฐาน และทรัพยากรคลาวด์ โดยการทำงานของแต่ละปลั๊กอินจะกำหนดตัวเลือก ความหมายของผลลัพธ์ และแพ็กเกจเสริมที่อาจต้องใช้ไว้เฉพาะตัว

## จุดเข้าใช้งานที่มีให้บริการ

รายชื่อต่อไปนี้ถูกประกาศไว้ใน [pyproject.toml](../../../pyproject.toml) และมีไฟล์ซอร์สโค้ดรองรับครบถ้วน:

| คำสั่ง | การนำไปใช้งาน |
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

โปรดอ่าน `--help` และซอร์สโค้ดของตัวตรวจสอบแต่ละตัวก่อนกำหนดค่าขีดจำกัด (thresholds) ไม่ควรเหมารวมว่าพฤติกรรมด้าน JSON, timeout, performance-data และการยืนยันตัวตนจะเหมือนกันในทุกปลั๊กอิน

## การติดตั้งจากซอร์สโค้ด

ไฟล์ manifest กำหนดให้ใช้ Python >=3.11,<3.15 และ [packaging/platform-support.json](../../../packaging/platform-support.json) บันทึกข้อมูลรันไทม์และเป้าหมายการทำแพ็กเกจที่ผ่านการตรวจสอบแล้ว จากไดเรกทอรีโค้ดนี้:

```bash
uv sync --locked --all-extras
uv run check_tls_expiry --help
```

`uv sync` จะติดตั้งแพ็กเกจที่ถูกล็อกเวอร์ชันไว้ เครื่องมือพัฒนา และโปรเจกต์ลงใน `.venv/` ส่วนสภาพแวดล้อมสำหรับใช้งานจริงอย่างเดียวให้ใช้ `uv sync --locked --no-dev --extra aws` (เป็นตัวอย่าง) ตัวเลือก extras ที่มีอยู่ถูกกำหนดไว้ใน manifest ให้ติดตั้งเฉพาะส่วนเชื่อมต่อที่คุณต้องการ การแสดงวิธีติดตั้งจากซอร์สโค้ดนี้ไม่ได้เป็นการยืนยันว่ามีการเผยแพร่บน package index

## ความเข้ากันได้และการปฏิบัติงาน

หากต้องการรันการตรวจสอบบน Kubernetes หรือ Nomad ให้ใช้ Helm chart ใน [charts/nagios-plugins-collection](../../../charts/nagios-plugins-collection) หรือ job ใน [deploy/nomad](../../../deploy/nomad) ดูตัวอย่างการใช้งาน Helm และ Nomad ฉบับสมบูรณ์ได้ใน[คู่มือการติดตั้ง](../../../docs/source/installation.rst#containers-and-kubernetes) รวมถึงการส่งค่าความลับจาก Kubernetes Secret หรือ Nomad Variable

ดูบันทึกการย้ายระบบย้อนหลังได้ที่ [MIGRATION.md](../../../MIGRATION.md) แต่โปรดตรวจสอบชื่อคำสั่งและตัวเลือกเทียบกับซอร์สโค้ดชุดนี้เสมอ การเปลี่ยนเวอร์ชัน Python, type hints หรือการตั้งค่า CI ไม่ได้เป็นการรับรองว่าตัวตรวจสอบรุ่นเก่าทุกตัวจะมีพฤติกรรมเหมือนเดิมทุกประการ ทั้งนี้บริการภายนอกและเครื่องมือของแพลตฟอร์มต้องพร้อมใช้งานสำหรับตัวตรวจสอบที่กำลังรัน

## การรองรับหลายภาษา (Localization)

ข้อความช่วยเหลือของ CLI และข้อความวินิจฉัยร่วมกันรองรับ 45 ภาษา (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`, `af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`, `bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`) โดยใช้แค็ตตาล็อกที่รวมมาในชุดและโหลดผ่านไลบรารีมาตรฐาน การตรวจสอบภาษาจะเช็ก `--lang` ตามด้วย `LC_ALL`, `LC_MESSAGES` และ `LANG` และใช้ `en` เป็นค่าเริ่มต้น คำนำหน้าสถานะของ Nagios (`OK`, `WARNING`, `CRITICAL`, `UNKNOWN`), ข้อมูลประสิทธิภาพ (performance data) และคีย์ JSON จะยังคงเดิมในทุกภาษา

## การพัฒนา

การทดสอบและการตั้งค่าเครื่องมืออยู่ใน [pyproject.toml](../../../pyproject.toml), [uv.lock](../../../uv.lock) และ[เวิร์กโฟลว์ CI](../../../.github/workflows/ci.yml) สามารถรันการทดสอบได้ด้วย `uv run pytest` ทั้งนี้ไม่มีการอ้างสิทธิ์เรื่องอัตราส่วนการทดสอบที่ครอบคลุม (coverage) ตายตัว การผ่าน type-checking แบบเข้มงวดทั้งหมด หรือการรับรอง supply-chain แต่อย่างใด

## ความปลอดภัยและสัญญาอนุญาต

ดูรายละเอียดที่ [SECURITY.md](../../../SECURITY.md) ซอร์สโค้ดเผยแพร่ภายใต้[สัญญาอนุญาต Apache-2.0](../../../LICENSE) และ [packaging/license-policy.json](../../../packaging/license-policy.json) บันทึกนโยบายสัญญาอนุญาตของแพ็กเกจที่พึ่งพา
