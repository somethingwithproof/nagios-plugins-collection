"""Tests for HTTP SLI plugin."""

from unittest.mock import MagicMock, patch

import pytest

from nagios_plugins.base import Status
from nagios_plugins.plugins.check_http_sli import CheckHttpSli


@pytest.mark.asyncio
async def test_http_sli_ok() -> None:
    plugin = CheckHttpSli()

    # Mock AsyncClient.get to return elapsed times
    class Resp:
        def __init__(self, t: float):
            self.elapsed = MagicMock(total_seconds=lambda: t)

        def raise_for_status(self) -> None:
            return None

    async def fake_get(url: str, follow_redirects: bool = True) -> Resp:
        return Resp(0.05)

    with (
        patch("httpx.AsyncClient.__aenter__", new=MagicMock()),
        patch("httpx.AsyncClient.get", side_effect=fake_get),
    ):
        # Build args
        code = plugin.run(["--url", "https://example.com", "--samples", "2"])
        assert code == Status.OK.value
