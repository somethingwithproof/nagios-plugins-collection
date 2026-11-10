<!--
SPDX-FileCopyrightText: 2025 Thomas Vincent
SPDX-License-Identifier: Apache-2.0
-->

# Changelog

## Unreleased

- `check_http_sli` thresholds are split by measurement. `-w`/`-c` compared one
  number with both the error rate (a 0-1 fraction) and p95 latency (ms), so a
  value meant for one was meaningless for the other. `--latency-warning` and
  `--latency-critical` take p95 latency ranges in milliseconds, and `-w`/`-c`
  remain as their aliases, which keeps existing latency-style definitions such
  as `-w 300 -c 1000` working. The new `--error-rate-warning` and
  `--error-rate-critical` take ranges for the failed-request fraction (for
  example `--error-rate-critical 0.05`). A definition that passed an error-rate
  fraction to `-w`/`-c` must move it to the new options. All values use Nagios
  ranges, so a p95 exactly equal to the threshold is no longer an alert.
  Perfdata carries each threshold, and the message reads `p95=n/a` instead of
  `inf` when every probe fails.
- Helm: the CronJob sets `concurrencyPolicy: Forbid`, `backoffLimit: 0`,
  `activeDeadlineSeconds: 300` and `ttlSecondsAfterFinished`, so a WARNING,
  CRITICAL or UNKNOWN exit is no longer retried up to six times per run (all
  configurable under `job` and the top-level history limits). `env` entries
  accept `valueFrom` (for example `secretKeyRef`) as well as literal values.
  `image.tag` now defaults to the chart appVersion (`2.0.1`); the previous
  default `2.0.0` was never published as an image.
- Nomad: the job sets `command`, since the image has no ENTRYPOINT and
  `args` alone were executed as the program, pins the image through an `image`
  variable (default `...:2.0.1`, accepts an `@sha256` digest) instead of
  `latest`, and disables restarts and rescheduling so a non-OK result is not
  rerun.
- Credentials are masked in the status line, long output, JSON output and log
  records, including exception text from HTTP clients that embeds the request
  URL: URL userinfo becomes `scheme://***@host`, and parameters such as
  `token`, `password`, `client_secret` and `api_key`, as well as bearer tokens,
  become `***`.
- Secrets can be supplied without putting them on the command line, where the
  process list exposes them: `check_oauth2_token --client-secret-file` or
  `CHECK_OAUTH2_CLIENT_SECRET`, `check_postgres_replication_lag --dsn-file` or
  `CHECK_POSTGRES_DSN`, `check_redis_saturation --url-file` or
  `CHECK_REDIS_URL`, and `check_monghealth --password-file` or
  `CHECK_MONGHEALTH_PASSWORD`. The existing options keep working.
- Usage errors (unknown or missing arguments, invalid values) exit 3 (UNKNOWN)
  with an `UNKNOWN - <command>: <error>` status line instead of argparse's exit
  2, which Nagios reads as CRITICAL. `--help` still exits 0.
- Logging is configured once per run, after argument parsing, and always
  writes to stderr. Seven plugins previously configured a Rich handler on
  stdout at import time, so log lines could precede the status line. Log
  records are now plain `LEVEL logger: message` text. Standalone plugins share
  one runner that also reports an unhandled exception as UNKNOWN instead of a
  traceback with exit 1.
- Missing data no longer reports OK. `check_prometheus_query` returns UNKNOWN
  for an empty or sample-less result instead of treating it as `0`;
  `check_log_errors` returns UNKNOWN when the response has no `hits.total`
  (ES 6 integer totals are now read too); `check_k8s_node_status` returns
  UNKNOWN when no node matches; `check_oauth2_token` returns CRITICAL for a
  success response without an `access_token` and no longer publishes a missing
  `expires_in` as `0`; `check_postgres_replication_lag` returns CRITICAL when
  no standby is connected; and `check_dig` returns CRITICAL when `dig +short`
  prints no answer (NXDOMAIN, SERVFAIL or NODATA) even without `--expected`.
- Thresholds follow the Nagios Plugin Guidelines range format in one shared
  parser: `@a:b` now alerts when `a <= value <= b` (endpoints were excluded),
  `~:10` is accepted, a bare `10` means `0:10` so negative values alert, and a
  value inside a critical `@` range is CRITICAL even when the warning range is
  narrower. Malformed ranges, including a start above its end, return UNKNOWN.
  `check_prometheus_query` now uses these ranges instead of a plain upper bound
  that silently ignored malformed thresholds.
- Performance data uses one formatter: `'label'=value[UOM];warn;crit;min;max`.
  Labels with spaces, `=` or `'` are quoted, and non-numeric or non-finite
  values (for example CloudWatch `unit=Percent`, component `status=ok`, Hadoop
  memory text, `p95_ms=inf`) are no longer emitted as perfdata. CloudWatch
  values carry their unit as a UOM (for example `value=45.5%;70;90`) and Hadoop
  memory is `mem=<n>KB`. The status message is always one line, with `|`
  replaced by `/`. JSON output keeps plain metric values and writes `null`
  instead of the invalid `Infinity`.
- `check_monghealth` uses the shared result type, so its JSON output now
  includes `timestamp` and `details` like the other plugins.
- Make `uv.lock` the single dependency lock. Development tools moved from the
  `dev` and `security` extras to PEP 735 dependency groups; install them with
  `uv sync`. The runtime extras, including `prom` and `es`, are unchanged.
- Replace tox and the `packaging/*-requirements` files with `uv sync --locked`
  and `uv run`. The container image and native packages export hashed
  requirements from `uv.lock` at build time.

## 2.0.1 — 2026-10-06

- Align package metadata and SPDX headers with the existing Apache-2.0 LICENSE.
- Add file-level SPDX identifiers and REUSE mappings for non-commentable files.
- Parse shipping license expressions without regex backtracking.
- Supersede the unpublished 2.0.0 candidate after the license consistency audit.

## 2.0.0 — 2026-10-06 (unpublished candidate)

Verified TLS defaults, async cancellation ownership, maintained-platform policy and wheel/Helm/DEB/RPM releases.

Documentation includes migration, installation, release checks, SVG project branding and operational diagrams.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2025-12-27

### Changed
- Python 3 modernization across the repo; removed legacy standalone scripts and vendored third-party code.
- Security: disallow shell=True in execute_command.
- Adopted Ruff + pre-commit; tightened lint/type gates and standardized formatting.
- CI cleanup and stability improvements.

### Fixed
- Multiple lint issues (flake8/ruff) and minor type issues in runtime code.

## [1.1.0] - 2025-04-11

### Added
- JSON output format support for all plugins
- Asynchronous execution support for improved performance
- Rich terminal output with progress indicators
- New `ThresholdRange` class for better threshold handling
- Added `get_directory_size` utility function
- Added `get_system_info` utility function
- Added security scanning with Bandit and pip-audit
- Added CommandResult dataclass for better command execution results
- Added timestamp to CheckResult for better tracking
- Added to_json method to CheckResult for JSON serialization

### Changed
- Modernized codebase to use maintained Python 3.11–3.14 features
- Updated all dependencies to latest versions
- Improved error handling with better error messages
- Refactored base plugin class for better extensibility
- Enhanced HTTP endpoint checking with more options
- Improved process checking across different operating systems
- Updated GitHub Actions workflow with modern actions
- Switched to modern Python packaging with pyproject.toml
- Improved documentation with more examples
- Enhanced test coverage and test organization

### Removed
- Support for Python 3.7 (now requires maintained Python 3.11–3.14)
- Deprecated utility functions replaced with modern alternatives

## [1.0.0] - 2024-01-01

### Added
- Initial release of nagios-plugins-collection
- Base plugin framework
- Core utility functions
- Initial set of monitoring plugins
- Documentation and examples
- Test suite
