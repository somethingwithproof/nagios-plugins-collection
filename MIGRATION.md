# Migrating to Nagios Plugins Collection 2.0

Use a maintained Python 3.11–3.14 interpreter. The wheel metadata excludes EOL
Python releases. CI exercises these four runtimes; Python 3.15 requires adoption
and testing before it becomes supported. Use `mise` to select a development runtime.

The unused `legacy` extra and its Pynag/pexpect dependencies were removed.
`[all]` now selects runtime clients; install development and security tools
explicitly through their extras or the hash-locked CI requirements.

HTTP checks verify certificates by default. `--verify-ssl` remains accepted for
compatibility; omitting it no longer disables verification. For an internal CA,
use `--ca-file /path/to/ca.pem`. Keep endpoint hostnames consistent with the
certificate SAN. An expired, untrusted or mismatched certificate fails the check.

Async utility functions no longer accept a `timeout` argument. Apply a caller
deadline instead:

```python
import asyncio
from nagios_plugins.utils import check_http_endpoint_async


async def check_endpoint():
    async with asyncio.timeout(10):
        return await check_http_endpoint_async("https://example.com")
```

Use the same pattern for `execute_command_async`; cancellation terminates and
reaps its child process. HTTP utilities also impose a 30-second transport ceiling.
CLI `--timeout` continues to bound each check. Catch `TimeoutError` when directly
calling the utilities; plugin wrappers translate deadlines into Nagios results.

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
