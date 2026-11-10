# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Every installed command honors the plugin contract against fake backends.

Each command runs end to end (argument parsing, the shared runner and output)
with its backend replaced at the library boundary it uses: httpx transports,
boto3, redis, psycopg, kubernetes, dnspython, TLS sockets or the SSH/mount
subprocess. Five scenarios are injected: a healthy answer, a timeout, an
authentication failure, an empty answer and a malformed answer. Only the
healthy answer may be OK; for every scenario the command must print exactly
one status line whose keyword matches its exit code, perfdata that follows the
guidelines (checked by :mod:`tests.perfdata_grammar`), log records only on
stderr, and never the configured secret.
"""

from __future__ import annotations

import datetime as dt
import importlib
import re
import ssl
import tomllib
from collections.abc import Callable
from contextlib import ExitStack
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import botocore.exceptions
import dns.exception
import dns.resolver
import httpx
import kubernetes
import psycopg
import pytest
import redis

from nagios_plugins.utils import CommandResult
from tests.fakes import FakeHttpBackend
from tests.perfdata_grammar import KEYWORDS, parse_output

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["scripts"]
SCENARIOS = ("success", "timeout", "auth", "empty", "malformed")
#: Configured as a credential wherever a command accepts one; must never be printed.
SECRET = "s3cr3t-Contract-Value"
LOG_RECORD = re.compile(r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL) [\w.]+: ", re.M)
NOW = dt.datetime.now(dt.UTC)

Arrange = Callable[[str, ExitStack, FakeHttpBackend], None]


@dataclass(frozen=True)
class Spec:
    """How to run one command and fake its backend for each scenario."""

    args: list[str]
    arrange: Arrange
    #: Scenarios that cannot occur for this command, with the reason.
    inapplicable: dict[str, str] = field(default_factory=dict)


# HTTP ------------------------------------------------------------------------

HEALTH = {
    "status": "ok",
    "alive": True,
    "mongrations_current": True,
    "search_reachable": True,
    "site_api_reachable": True,
    "subcomponents": [],
    "components": [],
    "updated": NOW.isoformat(),
}


def _http(healthy: Callable[[httpx.Request], httpx.Response]) -> Arrange:
    def arrange(scenario: str, stack: ExitStack, backend: FakeHttpBackend) -> None:
        def respond(request: httpx.Request) -> httpx.Response:
            if scenario == "timeout":
                raise httpx.ReadTimeout("timed out", request=request)
            if scenario == "auth":
                return httpx.Response(401, headers={"WWW-Authenticate": 'Basic realm="x"'})
            if scenario == "empty":
                return httpx.Response(200, content=b"")
            if scenario == "malformed":
                return httpx.Response(200, content=b'{"status": "ok", "hits": ')
            return healthy(request)

        backend.respond = respond

    return arrange


def _json(body: Any) -> Callable[[httpx.Request], httpx.Response]:
    return lambda request: httpx.Response(200, json=body)


CREDENTIALS = ["--username", "monitor", "--password", SECRET]

# boto3 -----------------------------------------------------------------------

AWS_ERRORS = {
    "timeout": botocore.exceptions.ReadTimeoutError(endpoint_url="https://aws.example"),
    "auth": botocore.exceptions.ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "not authorized"}}, "Call"
    ),
}


def _aws(answers: dict[str, dict[str, Any]]) -> Arrange:
    """``answers[scenario]`` maps a client method to its return value."""

    def arrange(scenario: str, stack: ExitStack, backend: FakeHttpBackend) -> None:
        def client(service: str, **kwargs: Any) -> MagicMock:
            fake = MagicMock()
            for method, value in answers.get(scenario, {}).items():
                getattr(fake, method).return_value = value
            if scenario in AWS_ERRORS:
                error = AWS_ERRORS[scenario]
                for method in ("get_queue_attributes", "get_cost_and_usage"):
                    getattr(fake, method).side_effect = error
                fake.get_metric_statistics.side_effect = error
                fake.get_paginator.return_value.paginate.side_effect = error
            return fake

        stack.enter_context(patch("boto3.client", side_effect=client))

    return arrange


def _pages(pages: list[dict[str, Any]]) -> dict[str, Any]:
    paginator = MagicMock()
    paginator.paginate.return_value = pages
    return {"get_paginator": paginator}


# Other libraries -------------------------------------------------------------


def _redis(scenario: str, stack: ExitStack, backend: FakeHttpBackend) -> None:
    info: dict[str, Any] = {
        "success": {
            "used_memory": 100,
            "maxmemory": 1000,
            "evicted_keys": 0,
            "blocked_clients": 0,
            "keyspace_hits": 9,
            "keyspace_misses": 1,
        },
        "empty": {},
        "malformed": {"used_memory": "lots", "maxmemory": None},
    }
    client = MagicMock()
    client.info.side_effect = {
        "timeout": redis.exceptions.TimeoutError("Timeout reading from socket"),
        "auth": redis.exceptions.AuthenticationError("invalid username-password pair"),
    }.get(scenario)
    client.info.return_value = info.get(scenario)
    stack.enter_context(patch("redis.from_url", return_value=client))


def _postgres(scenario: str, stack: ExitStack, backend: FakeHttpBackend) -> None:
    errors = {
        "timeout": psycopg.OperationalError("connection timeout expired"),
        "auth": psycopg.OperationalError('password authentication failed for user "monitor"'),
    }
    cursor = MagicMock()
    cursor.fetchone.return_value = {"success": (1.5,), "empty": None, "malformed": ("abc",)}.get(
        scenario
    )
    connection = MagicMock()
    connection.__enter__.return_value.cursor.return_value.__enter__.return_value = cursor
    stack.enter_context(
        patch("psycopg.connect", side_effect=errors.get(scenario), return_value=connection)
    )


def _kubernetes(scenario: str, stack: ExitStack, backend: FakeHttpBackend) -> None:
    ready = SimpleNamespace(
        status=SimpleNamespace(conditions=[SimpleNamespace(type="Ready", status="True")])
    )
    api = MagicMock()
    api.list_node.side_effect = {
        "timeout": TimeoutError("read timed out"),
        "auth": kubernetes.client.exceptions.ApiException(status=401, reason="Unauthorized"),
    }.get(scenario)
    api.list_node.return_value = SimpleNamespace(
        items={
            "success": [ready],
            "empty": [],
            "malformed": [SimpleNamespace(status="garbage")],
        }.get(scenario, [])
    )
    stack.enter_context(
        patch(
            "kubernetes.config.load_incluster_config",
            side_effect=kubernetes.config.ConfigException("not in a cluster"),
        )
    )
    stack.enter_context(patch("kubernetes.config.load_kube_config"))
    stack.enter_context(patch("kubernetes.client.CoreV1Api", return_value=api))


def _dns(scenario: str, stack: ExitStack, backend: FakeHttpBackend) -> None:
    answer = MagicMock()
    answer.__len__.return_value = 1
    answer.response.time = 0.012
    resolver = MagicMock()
    resolver.resolve.side_effect = {
        "timeout": dns.exception.Timeout(),
        # REFUSED from every server: the resolver is not allowed to answer.
        "auth": dns.resolver.NoNameservers(),
        "empty": dns.resolver.NoAnswer(),
        "malformed": dns.exception.FormError("truncated answer"),
    }.get(scenario)
    resolver.resolve.return_value = answer
    stack.enter_context(patch("dns.resolver.Resolver", return_value=resolver))


def _tls(scenario: str, stack: ExitStack, backend: FakeHttpBackend) -> None:
    expiry = (NOW + dt.timedelta(days=90)).strftime("%b %d %H:%M:%S %Y GMT")
    certs = {
        "success": {
            "notAfter": expiry,
            "issuer": ((("commonName", "Example CA"),),),
            "subject": ((("commonName", "www.example"),),),
        },
        "empty": {},
        "malformed": {"notAfter": "soon", "issuer": "nobody"},
    }
    connection = MagicMock()
    if scenario == "timeout":
        connection.side_effect = TimeoutError("timed out")
    stack.enter_context(patch("nagios_plugins.services.tls.socket.create_connection", connection))
    tls_socket = MagicMock()
    tls_socket.__enter__.return_value.getpeercert.return_value = certs.get(scenario)
    wrap = MagicMock(return_value=tls_socket)
    if scenario == "auth":
        wrap.side_effect = ssl.SSLCertVerificationError(
            1, "certificate verify failed: unable to get local issuer certificate"
        )
    stack.enter_context(patch.object(ssl.SSLContext, "wrap_socket", wrap))


SSH_DENIED = "monitor@host: Permission denied (publickey)."


def _dig(scenario: str, stack: ExitStack, backend: FakeHttpBackend) -> None:
    results = {
        "success": CommandResult(0, "192.0.2.1\n", "", 0.01),
        "auth": CommandResult(255, "", SSH_DENIED, 0.01),
        "empty": CommandResult(0, "", "", 0.01),
        "malformed": CommandResult(
            0, ";; connection timed out; no servers could be reached\n", "", 0.01
        ),
    }
    command = AsyncMock(return_value=results.get(scenario))
    if scenario == "timeout":
        command.side_effect = TimeoutError()
    stack.enter_context(patch("nagios_plugins.plugins.check_dig.execute_command_async", command))


def _mounts(scenario: str, stack: ExitStack, backend: FakeHttpBackend) -> None:
    results = {
        "success": (0, "/dev/root on / type ext4 (rw,relatime)\n", ""),
        "timeout": (1, "", "Command timed out after 30 seconds: ssh"),
        "auth": (255, "", SSH_DENIED),
        "empty": (0, "", ""),
        "malformed": (0, "\x00\x01 garbage without mount fields\n", ""),
    }
    stack.enter_context(
        patch(
            "nagios_plugins.plugins.check_ro_mounts.execute_command", return_value=results[scenario]
        )
    )


# The table -------------------------------------------------------------------

SPECS: dict[str, Spec] = {
    "check_website_status": Spec(
        ["--url", "https://www.example/", "--pattern", "Welcome", *CREDENTIALS],
        _http(lambda request: httpx.Response(200, text="<h1>Welcome</h1>")),
    ),
    "check_component_status": Spec(
        ["--url", "https://status.example", "--components", "db", *CREDENTIALS],
        _http(_json(HEALTH)),
    ),
    "check_mongodb_health": Spec(
        ["--url", "https://mongo.example/health", "--mode", "2", *CREDENTIALS], _http(_json(HEALTH))
    ),
    "check_monghealth": Spec(
        ["--host", "mongo.example", "--ssl", "--mode", "2", *CREDENTIALS], _http(_json(HEALTH))
    ),
    "check_hadoop": Spec(
        ["--url", "https://hadoop.example/status", *CREDENTIALS], _http(_json(HEALTH))
    ),
    "check_jobs": Spec(["--url", "https://jobs.example/api", *CREDENTIALS], _http(_json(HEALTH))),
    "check_prometheus_query": Spec(
        ["--server", "https://prom.example", "--query", "up", "-c", "@0", *CREDENTIALS],
        _http(
            _json(
                {
                    "status": "success",
                    "data": {"resultType": "vector", "result": [{"metric": {}, "value": [0, "1"]}]},
                }
            )
        ),
    ),
    "check_log_errors": Spec(
        ["--endpoint", "https://es.example:9200", "--index", "logs", "-w", "5", *CREDENTIALS],
        _http(_json({"hits": {"total": {"value": 0, "relation": "eq"}}})),
    ),
    "check_oauth2_token": Spec(
        [
            "--token-url",
            "https://idp.example/token",
            "--client-id",
            "monitor",
            "--client-secret",
            SECRET,
        ],
        _http(_json({"access_token": "token-value", "token_type": "Bearer", "expires_in": 3600})),
    ),
    "check_http_sli": Spec(
        ["--url", "https://www.example/", "--samples", "2", *CREDENTIALS],
        _http(lambda request: httpx.Response(200, text="ok")),
        inapplicable={
            "empty": "measures latency and status codes, never the body",
            "malformed": "measures latency and status codes, never the body",
        },
    ),
    "check_tls_expiry": Spec(["--host", "www.example"], _tls),
    "check_dns_health": Spec(["--name", "www.example"], _dns),
    "check_k8s_node_status": Spec([], _kubernetes),
    "check_postgres_replication_lag": Spec(
        ["--dsn", f"postgresql://monitor:{SECRET}@db.example/postgres"], _postgres
    ),
    "check_redis_saturation": Spec(["--url", f"redis://:{SECRET}@cache.example:6379/0"], _redis),
    "check_queue_depth": Spec(
        ["--queue-url", "https://sqs.example/123/jobs"],
        _aws(
            {
                "success": {
                    "get_queue_attributes": {"Attributes": {"ApproximateNumberOfMessages": "3"}}
                },
                "empty": {"get_queue_attributes": {"Attributes": {}}},
                "malformed": {
                    "get_queue_attributes": {"Attributes": {"ApproximateNumberOfMessages": "many"}}
                },
            }
        ),
    ),
    "check_backup_freshness": Spec(
        ["--bucket", "backups"],
        _aws(
            {
                "success": _pages(
                    [{"Contents": [{"LastModified": NOW - dt.timedelta(minutes=5)}]}]
                ),
                "empty": _pages([{}]),
                "malformed": _pages([{"Contents": [{"LastModified": "yesterday"}]}]),
            }
        ),
    ),
    "check_cloud_budget": Spec(
        ["--budget", "100"],
        _aws(
            {
                "success": {
                    "get_cost_and_usage": {
                        "ResultsByTime": [{"Total": {"UnblendedCost": {"Amount": "12.5"}}}]
                    }
                },
                "empty": {"get_cost_and_usage": {"ResultsByTime": []}},
                "malformed": {
                    "get_cost_and_usage": {
                        "ResultsByTime": [{"Total": {"UnblendedCost": {"Amount": "n/a"}}}]
                    }
                },
            }
        ),
    ),
    "check_aws_cloudwatch": Spec(
        ["--namespace", "AWS/EC2", "--metric", "CPUUtilization", "--instance-id", "i-1"],
        _aws(
            {
                "success": {
                    "get_metric_statistics": {
                        "Datapoints": [{"Timestamp": NOW, "Average": 5.0, "Unit": "Percent"}]
                    }
                },
                "empty": {"get_metric_statistics": {"Datapoints": []}},
                "malformed": {
                    "get_metric_statistics": {"Datapoints": [{"Timestamp": NOW, "Maximum": 5.0}]}
                },
            }
        ),
    ),
    "check_dig": Spec(["--host", "dns.example", "--query", "www.example", "--retries", "1"], _dig),
    "check_ro_mounts": Spec(["--host", "server.example"], _mounts),
}


def test_every_installed_command_has_a_contract() -> None:
    assert set(SPECS) == set(SCRIPTS)


def _run(name: str, scenario: str, backend: FakeHttpBackend, verbosity: list[str]) -> int:
    spec = SPECS[name]
    if scenario in spec.inapplicable:
        pytest.skip(spec.inapplicable[scenario])
    main = importlib.import_module(SCRIPTS[name].partition(":")[0]).main
    with ExitStack() as stack:
        spec.arrange(scenario, stack, backend)
        stack.enter_context(patch("sys.argv", [name, *verbosity, *spec.args]))
        return int(main())


@pytest.mark.parametrize("scenario", SCENARIOS)
@pytest.mark.parametrize("name", sorted(SPECS))
def test_command_contract(
    name: str,
    scenario: str,
    http_backend: FakeHttpBackend,
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = _run(name, scenario, http_backend, ["-vv"])
    out, err = capsys.readouterr()

    assert code in KEYWORDS.values(), code
    result = parse_output(out)  # one status line, guideline perfdata, no stray '|'
    assert KEYWORDS[result.keyword] == code, out
    if scenario == "success":
        assert code == 0, out
    else:
        assert code != 0, f"{scenario} reported OK: {out}"
    assert not LOG_RECORD.search(out), "log records belong on stderr"
    assert SECRET not in out
    assert SECRET not in err


def test_logs_reach_stderr(
    http_backend: FakeHttpBackend, capsys: pytest.CaptureFixture[str]
) -> None:
    """The negative assertion above is meaningful: -vv does produce records, on stderr."""
    _run("check_website_status", "auth", http_backend, ["-vv"])
    out, err = capsys.readouterr()
    assert LOG_RECORD.search(err)
    assert not LOG_RECORD.search(out)
