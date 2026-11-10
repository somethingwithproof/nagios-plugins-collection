# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Create AWS clients with the bounded network behavior every check needs."""

from __future__ import annotations

from typing import Any

# Standard-mode retries with a small cap keep a throttled or unreachable
# endpoint from outlasting the monitoring system's own check timeout.
RETRY_POLICY = {"max_attempts": 3, "mode": "standard"}


def client(service: str, region: str | None = None, timeout: int = 10) -> Any:
    """Return a boto3 client with connect/read timeouts and bounded retries."""
    try:
        import boto3  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError("boto3 extra not installed") from e

    return boto3.client(  # type: ignore
        service,
        region_name=region,
        config=boto3.session.Config(
            connect_timeout=timeout, read_timeout=timeout, retries=RETRY_POLICY
        ),
    )
