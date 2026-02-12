from __future__ import annotations

import datetime as dt
import socket
import ssl
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass
class TlsCertInfo:
    not_after: dt.datetime
    issuer: str
    subject: str
    san_count: int


def fetch_server_cert(host: str, port: int = 443, timeout: int = 10) -> TlsCertInfo:
    context = ssl.create_default_context()
    with context.wrap_socket(
        socket.create_connection((host, port), timeout=timeout), server_hostname=host
    ) as ssock:
        cert = ssock.getpeercert() or {}
    not_after_obj = cert.get("notAfter")
    if not isinstance(not_after_obj, str):
        raise ValueError("Peer certificate missing notAfter")
    not_after = dt.datetime.strptime(not_after_obj, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=dt.UTC)
    from typing import cast

    issuer_tuples = cast(
        Sequence[Sequence[tuple[str, str]]], cert.get("issuer") or ((("CN", "?"),),)
    )
    subject_tuples = cast(
        Sequence[Sequence[tuple[str, str]]], cert.get("subject") or ((("CN", "?"),),)
    )
    issuer = ", ".join(f"{k}={v}" for k, v in issuer_tuples[0])
    subject = ", ".join(f"{k}={v}" for k, v in subject_tuples[0])
    san_list = cast(list[tuple[str, str]], list(cert.get("subjectAltName") or []))
    return TlsCertInfo(not_after=not_after, issuer=issuer, subject=subject, san_count=len(san_list))


def days_remaining(info: TlsCertInfo, now: dt.datetime | None = None) -> int:
    now = now or dt.datetime.now(dt.UTC)
    delta = info.not_after - now
    return max(0, int(delta.total_seconds() // 86400))
