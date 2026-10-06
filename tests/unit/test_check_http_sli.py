"""Exercise the synchronous CLI with actual async HTTP client behavior."""

from datetime import timedelta
from unittest.mock import patch

import httpx
import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_http_sli import CheckHttpSli


@pytest.mark.parametrize("samples", [1, 2])
def test_http_sli_ok(samples: int) -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        response = httpx.Response(200, request=request)
        response.elapsed = timedelta(milliseconds=50)
        return response

    client = httpx.AsyncClient(transport=httpx.MockTransport(respond))
    with patch("httpx.AsyncClient", return_value=client):
        code = CheckHttpSli().run(["--url", "https://example.com", "--samples", str(samples)])
    assert code == Status.OK.value


@pytest.mark.parametrize("thresholds", [[], ["--warning", "200"], ["--critical", "500"]])
def test_all_failed_probes_are_critical(thresholds: list[str]) -> None:
    client = httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(503)))
    with patch("httpx.AsyncClient", return_value=client):
        code = CheckHttpSli().run(["--url", "https://example.com", *thresholds])
    assert code == Status.CRITICAL.value
