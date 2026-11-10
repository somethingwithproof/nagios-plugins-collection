# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Read backup object timestamps through the S3 API."""

from __future__ import annotations

import datetime as dt

from nagios_plugins.services import aws


def latest_object_age_seconds(
    bucket: str, prefix: str = "", region: str | None = None, timeout: int = 10
) -> int:
    """Return the age in seconds of the newest object under an S3 prefix."""
    s3 = aws.client("s3", region=region, timeout=timeout)
    paginator = s3.get_paginator("list_objects_v2")
    latest: dt.datetime | None = None
    for page in paginator.paginate(
        Bucket=bucket, Prefix=prefix, PaginationConfig={"PageSize": 1000}
    ):
        for obj in page.get("Contents", []) or []:
            lm = obj["LastModified"]
            if latest is None or lm > latest:
                latest = lm
    if latest is None:
        raise RuntimeError("No objects found")
    now = dt.datetime.now(dt.UTC)
    return int((now - latest).total_seconds())
