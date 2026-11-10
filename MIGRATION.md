<!--
SPDX-FileCopyrightText: 2025 Thomas Vincent
SPDX-License-Identifier: Apache-2.0
-->

# Migration guide

## Upgrading to 3.0

3.0.0 is a major release. Most of the changes since 2.0.1 below alter options,
exit codes, output or threshold semantics for existing command definitions;
review each one against your Nagios or Icinga configuration before upgrading.

- Every HTTP check now uses one shared client (`nagios_plugins.services.http`);
  see "HTTP Options" in the usage guide. All of them accept `--ca-file`,
  `--insecure`, `--client-cert`/`--client-key`, `--retries`/`--retry-delay`,
  and `--username`/`--password`,
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
- HTTP checks read at most `--max-response-bytes` (10 MiB by default) of a
  response body, after decompression, and report a larger one as UNKNOWN
  instead of buffering it; `check_http_sli` counts it as a failed probe. Every
  check cuts its status message to 4,096 and its long output to 32,768
  characters, marked `[truncated N characters]`.
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
  number keeps its meaning (alert above it). Checks without thresholds
  (`check_mongodb_health`, `check_monghealth`, `check_hadoop`, `check_jobs`,
  `check_ro_mounts`) reject `-w`/`-c` as a usage error. `--help` prints the
  description without source indentation. The unused
  `nagios_plugins.base.run_async_check` helper is removed; derive from
  `AsyncNagiosPlugin` instead.
- A bare `@` is no longer accepted as a range (it silently meant `@0:`,
  alerting on every non-negative value); it is a usage error (exit 3), as is
  a malformed `check_http_sli` `--latency-*`/`--error-rate-*` range. Ranges
  are repeated in perfdata in canonical form: `:10` as `~:10` and `1e1` as
  `10`.
- A malformed `-w`/`-c` range is a usage error (exit 3) for every command whose
  thresholds are ranges, reported before the check contacts anything.
  Previously `check_dig` retried and reported CRITICAL, and other commands
  reported UNKNOWN only after running the check.
- Empty or malformed answers that were reported OK are now UNKNOWN or
  CRITICAL: `check_ro_mounts` when `mount` lists no filesystems (an SSH
  wrapper that prints nothing, for example), `check_queue_depth` when SQS
  returns no or non-numeric queue attributes, `check_redis_saturation` when
  `INFO` has no `used_memory`, `check_aws_cloudwatch` when the latest
  datapoint lacks the requested statistic (it reported 0), and `check_dig`
  when dig prints `;;` diagnostics such as "connection timed out" instead of
  an answer. Perfdata labels replace tabs and other non-printable characters
  with `_`.
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
- `check_backup_freshness` reports a backup dated in the future (clock skew)
  as age 0 instead of a negative age that alerted as CRITICAL. A listing that
  is still running with less than one second of `--timeout` left is UNKNOWN
  with the number of objects listed; S3 lists by key, not date, so keep
  `--prefix` narrow.
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
  blocked clients and hit ratio are perfdata by default (`evicted_keys` as a
  `c` counter for rate graphs); to alert on the others, give them their own
  ranges with `--blocked-warning`/`--blocked-critical` and
  `--hitratio-warning`/`--hitratio-critical`. To keep the old hit-ratio
  cutoffs, use `--hitratio-warning 0.8: --hitratio-critical 0.5:`. The result
  is the most severe of the configured measurements. `--timeout` is now
  honored.
- `check_log_errors`, `check_postgres_replication_lag`, `check_queue_depth`,
  `check_backup_freshness` and `check_cloud_budget` take Nagios ranges for
  `-w`/`-c` like the other checks. A plain number `N` still alerts above `N`,
  but a value equal to `N` no longer alerts (they compared with `>=`): for
  example `check_queue_depth -w 100` is now OK at a depth of exactly 100. Use
  `-w 99` to keep alerting at 100 for integer measurements. Range forms such
  as `@10:20` and `5:` now work instead of reporting UNKNOWN.
- `check_tls_expiry` and `check_website_status` keep plain-number `-w`/`-c`
  instead of Nagios ranges. `check_tls_expiry` alerts when the days remaining
  are at or below the value (the `check_http -C` convention) and
  `check_website_status` when the response takes longer than the value in
  seconds. A range form such as `30:` or `@0:30`, a fractional number of days
  and a negative or non-finite number of seconds are usage errors (exit 3);
  previously a range crashed the check. `check_tls_expiry -c 0` now alerts on
  the expiry day. Perfdata carries the thresholds as equivalent ranges, for
  example `days_remaining=12;@~:30;@~:7` and `duration=0.4;1;2` (the default
  1 and 2 seconds are always published).
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
  `inf` when every probe fails. Percentiles interpolate between the measured
  samples, so p50, p95 and p99 never exceed the slowest probe; with the default
  3 samples p95 was previously extrapolated above it and could alert on a
  latency no probe measured.
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
  become `***`. Every resolved secret option, HTTP credential and password in a
  URL option is also masked as a literal wherever it appears, including its
  URL-encoded forms and quoted fragments (libpq echoes part of a malformed
  DSN), as are `key: value` and JSON `"key": "value"` credentials,
  `Authorization` and cookie headers and AWS access keys.
  `check_prometheus_query` reports the API's `errorType` and `error` instead
  of the whole response body.
- Secrets can be supplied without putting them on the command line, where the
  process list exposes them: `check_oauth2_token --client-secret-file` or
  `CHECK_OAUTH2_CLIENT_SECRET`, `check_postgres_replication_lag --dsn-file` or
  `CHECK_POSTGRES_DSN`, `check_redis_saturation --url-file` or
  `CHECK_REDIS_URL`, and `check_monghealth --password-file` or
  `CHECK_MONGHEALTH_PASSWORD`. The existing options keep working. A secret
  file must be a regular UTF-8 file of at most 64 KiB, or the run is a usage
  error (exit 3), and it is read within `--timeout`. Pipes are refused, so
  shell process substitution (`--password-file <(...)`) no longer works; pass
  the secret in the environment variable instead.
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
  `check_component_status` returns UNKNOWN for a healthy component whose
  `updated` timestamp is missing or unparseable (it reported OK without
  checking freshness) and adds an `unknown_components` count;
  `check_log_errors` returns UNKNOWN when the response has no `hits.total`
  (ES 6 integer totals are now read too), asks for an exact count
  (`track_total_hits`) so counts above 10,000 are no longer capped, and
  returns UNKNOWN for a lower-bound (`relation: gte`) count; `check_k8s_node_status` returns
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

## Upgrading to 2.0

Use a maintained Python 3.11–3.14 interpreter. The wheel metadata excludes EOL
Python releases. CI exercises these four runtimes; Python 3.15 requires adoption
and testing before it becomes supported. Use `mise` to select a development runtime.

The unused `legacy` extra and its Pynag/pexpect dependencies were removed.
`[all]` now selects runtime clients; development and security tools are
dependency groups in `uv.lock`, installed by `uv sync`.

HTTP checks verify certificates by default. `--verify-ssl` remains accepted for
compatibility; omitting it no longer disables verification. For an internal CA,
use `--ca-file /path/to/ca.pem`. Keep endpoint hostnames consistent with the
certificate SAN. An expired, untrusted or mismatched certificate fails the check.

`nagios_plugins.utils.check_http_endpoint` and `check_http_endpoint_async` were
removed. Build clients with `nagios_plugins.services.http.client()` or
`async_client()`, which apply the shared TLS, credential, retry, proxy and
User-Agent policy, and register the options with `add_http_arguments()`:

```python
from nagios_plugins.services import http

settings = http.HttpSettings(timeout=10, bearer_token=token)
with http.client(settings) as client:
    response = client.get("https://example.com/health")
```

`execute_command_async` no longer accepts a `timeout` argument; wrap it in
`asyncio.timeout()`. Cancellation terminates and reaps its child process. CLI
`--timeout` bounds the whole run (see the usage guide); catch `TimeoutError` when
calling utilities directly.

HTTP SLI thresholds are **milliseconds** (`--warning 200 --critical 500`), while
website-status thresholds are seconds (`--warning 1 --critical 2`). All failed
SLI probes stay CRITICAL, even with only a warning threshold. One successful
sample yields valid equal p50/p95/p99 values.

The native packages install 21 commands under `/usr/lib/nagios/plugins` and their
portable clients under `/usr/lib/nagios-plugins-collection`. Ubuntu 24.04 uses
Python 3.12 from the OS; Rocky Linux 9 packages require Python 3.12. PostgreSQL
checks use system libpq. Native packages exclude optional compiled accelerators;
the container installs its platform-specific wheels. Python wheel installs place
commands in their environment's `bin` directory.

Containers run as UID/GID 10001. The default command displays website-status
help; pass any installed plugin as the container command. Helm targets maintained Kubernetes
1.35–1.37. Node monitoring needs token automount and the chart's opt-in, list-only
node RBAC. Other checks do not need those permissions.

See [the README](README.md), [platform policy](packaging/platform-support.json),
and the [release workflow](.github/workflows/release.yml) for installation and
publication details. The weekly and release CI gates reject retired platforms.
