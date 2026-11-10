# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Remove credentials from text before it reaches plugin output or logs.

Exception messages from HTTP and database clients often embed the request URL
or connection string. :func:`redact` is applied centrally to the status line,
long output, JSON output and log records, so individual plugins do not need to
scrub every message they format.
"""

from __future__ import annotations

import re

MASK = "***"

# scheme://user:password@host -> scheme://***@host
_URL_USERINFO = re.compile(r"(?P<scheme>\b[a-zA-Z][a-zA-Z0-9+.-]{0,31}://)[^/\s@?#]{1,1024}@")

# token=..., password='...', client_secret="..." in query strings, form bodies
# and libpq-style key=value connection strings.
_SECRET_PARAMETER = re.compile(
    r"(?i)(?P<key>\b(?:password|passwd|pwd|secret|client_secret|token|access_token"
    r"|refresh_token|id_token|api[_-]?key|apikey|auth|key|sig|signature|sslpassword))"
    r"(?P<sep>\s{0,8}=\s{0,8})"
    r"(?:'[^']{0,4096}'|\"[^\"]{0,4096}\"|[^\s&;,'\"]{1,4096})"
)

# Authorization header values such as "Bearer abc".
_AUTH_SCHEME = re.compile(r"(?i)\b(?P<scheme>bearer|basic)\s{1,8}[A-Za-z0-9._~+/=-]{8,}")


def redact(text: str) -> str:
    """Return ``text`` with URL userinfo, secret parameters and bearer tokens masked."""
    text = _URL_USERINFO.sub(rf"\g<scheme>{MASK}@", text)
    text = _SECRET_PARAMETER.sub(rf"\g<key>\g<sep>{MASK}", text)
    return _AUTH_SCHEME.sub(rf"\g<scheme> {MASK}", text)
