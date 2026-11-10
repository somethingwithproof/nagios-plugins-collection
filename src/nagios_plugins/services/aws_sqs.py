# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Read SQS queue backlog and in-flight counts."""

from __future__ import annotations

from nagios_plugins.services import aws


def queue_depth(queue_url: str, region: str | None = None, timeout: int = 10) -> dict[str, int]:
    """Return visible and in-flight message counts for an SQS queue."""
    sqs = aws.client("sqs", region=region, timeout=timeout)
    attrs = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=[
            "ApproximateNumberOfMessages",
            "ApproximateNumberOfMessagesNotVisible",
            "ApproximateNumberOfMessagesDelayed",
        ],
    )["Attributes"]
    return {
        "depth": int(attrs.get("ApproximateNumberOfMessages", 0)),
        "inflight": int(attrs.get("ApproximateNumberOfMessagesNotVisible", 0)),
        "delayed": int(attrs.get("ApproximateNumberOfMessagesDelayed", 0)),
    }
