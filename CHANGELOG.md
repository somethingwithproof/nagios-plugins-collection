<!--
SPDX-FileCopyrightText: 2025 Thomas Vincent
SPDX-License-Identifier: Apache-2.0
-->

# Changelog

## Unreleased

- **Breaking:** every HTTP check now uses one shared client
  (`nagios_plugins.services.http`); see "HTTP Options" in the usage guide.
  All of them accept `--ca-file`, `--insecure`, `--client-cert`/`--client-key`,
  `--retries`/`--retry-delay`, and `--username`/`--password`,
  `--bearer-token` and `--api-key`/`--api-key-header`, each secret with a
  `-file` option, a `CHECK_<COMMAND>_<NAME>` variable and a `*_FILE` variable.
  Every secret option, including the existing `--client-secret` and
  `--password`, now also reads the file named by its variable plus `_FILE`.
  Credentials are sent only to the requested origin: redirects to another
  scheme, host or port drop them, and an HTTPS to HTTP redirect with
  credentials configured is CRITICAL. Transient failures are retried within
  `--timeout` (2 retries by default; `POST` only when the connection was never
  made; none for `check_website_status` unless `--retries` is given, and none
  for `check_http_sli`). Proxy variables are honored, requests send a
  versioned User-Agent, and HTTP errors name the URL without credentials or
  query string. `check_website_status --retry-delay` is now the first pause
  and doubles for each further retry (capped at 5 seconds), and only transient
  failures are retried. `--password` without `--username`, `--bearer-token` with
  `--username`, `--insecure` with `--ca-file` and `--client-key` without
  `--client-cert` are usage errors (exit 3); `check_monghealth --password`
  without `--username` previously sent no credentials. Library callers:
  `nagios_plugins.utils.check_http_endpoint`, `check_http_endpoint_async` and
  `nagios_plugins.services.http_tls` are removed in favor of
  `nagios_plugins.services.http`, and `WebsiteStatusChecker` takes a
  `settings` argument instead of `retries`.
- `--timeout` now bounds the whole run of every plugin. One second after it
  the run ends with `UNKNOWN - Plugin timed out after N seconds` (or the JSON
  equivalent) and exit 3, even while it waits on DNS resolution, a TCP
  connect, retries or a child process; `ssh`, `dig` and `mount` children are
  killed. Previously a stuck resolver or a retry loop could run until the
  scheduler killed the plugin with no result. Per-request timeouts still use
  `--timeout`, so their specific errors (for example an HTTP timeout reported
  as CRITICAL) are unchanged. `check_dig --retries` attempts now share the
  timeout and wait 1 second between attempts instead of `--timeout` seconds,
  and its failure message counts the attempts actually made. `--timeout` must
  be a whole number of at least 1; `0` or a negative value is a usage error
  (exit 3). Keep `--timeout` at least two seconds below the scheduler's check
  timeout.
- Every command now runs on the shared `NagiosPlugin` base class.
  `check_component_status`, `check_mongodb_health`, `check_monghealth`,
  `check_hadoop`, `check_jobs`, `check_dig` and `check_ro_mounts` had their own
  parsers and runner; their options, defaults (including `--timeout`) and exit
  codes are unchanged, and they gain the shared `-v`/`-t` short options. The
  `CRITICAL - CRITICAL - ` and `OK - OK - ` double prefixes in
  `check_component_status` and `check_mongodb_health` status lines are gone.
  `check_component_status` also accepts `-w`/`-c` for its minute thresholds.
  `check_dig -w`/`-c` take Nagios ranges for the query time in seconds; a plain
  number keeps its meaning (alert above it). A malformed `-w`/`-c` range is now a
  usage error (exit 3) for every command whose thresholds are ranges, reported
  before the check contacts anything; previously `check_dig` retried and
  reported CRITICAL, and other commands reported UNKNOWN after running. Checks without thresholds
  (`check_mongodb_health`, `check_monghealth`, `check_hadoop`, `check_jobs`,
  `check_ro_mounts`) reject `-w`/`-c` as a usage error. `--help` prints the
  description without source indentation. The unused
  `nagios_plugins.base.run_async_check` helper is removed; derive from
  `AsyncNagiosPlugin` instead.
- The installation guide's Kubernetes section pointed to Helm and Nomad
  examples in the README that did not exist. It now has complete examples: a
  Helm values file that reads a secret from a Kubernetes Secret, the opt-in
  node-monitoring RBAC values, and a Nomad job run with a pinned image and a
  secret rendered from a Nomad Variable. The README links to them.
- `rich` is no longer a runtime dependency. No plugin has imported it since
  logging moved to plain stderr records, so a base install and the native
  packages no longer pull it in. Install it separately if other code relied on
  it arriving with this package.
- `check_tls_expiry` reports an expired, untrusted or hostname-mismatched
  certificate as CRITICAL with the verification reason instead of UNKNOWN,
  and accepts `--ca-file` for private CAs like the HTTP checks.
- `check_cloud_budget` no longer fails on the first day of the month: the Cost
  Explorer period ends tomorrow (End is exclusive), so it always includes
  today. An empty Cost Explorer result is UNKNOWN instead of $0, and the
  client honors `--timeout`.
- All AWS clients come from one helper with connect/read timeouts and capped
  standard-mode retries (3 attempts).
- `check_ro_mounts --exclude` ignores empty entries, so a trailing comma no
  longer excludes every mount, and excludes match whole path components:
  the default `/run` exclude no longer hides `/runner`, and only `/var` and
  paths below it (not `/variant`) are CRITICAL.
- `check_redis_saturation` changes what `-w`/`-c` mean: they are now Nagios
  ranges for `used_memory` as a percentage of `maxmemory` (UNKNOWN when
  thresholds are given and `maxmemory` is 0). Previously `-w` was compared with
  `evicted_keys`, a counter that only grows until restart, so a single
  eviction latched WARNING; `-c` was compared with `blocked_clients`, and fixed
  hit-ratio cutoffs (0.8/0.5) applied whenever a threshold was set. Evictions,
  blocked clients and hit ratio are now perfdata only (`evicted_keys` as a
  `c` counter for rate graphs). `--timeout` is now honored.
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
