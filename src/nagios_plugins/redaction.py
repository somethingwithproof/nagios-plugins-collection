# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Remove credentials from text before it reaches plugin output or logs.

Exception messages from HTTP and database clients often embed the request URL
or connection string, and some checks echo parts of a response body.
:func:`redact` is applied centrally to the status line, long output, JSON
output, usage errors and log records, so individual plugins do not need to
scrub every message they format. It masks:

* every secret registered with :func:`register_secret` (resolved secret
  options, HTTP credentials, passwords in URLs given as options) as a literal,
  in its plain and URL-encoded forms, and any quoted fragment of one, which
  is how libpq echoes the part of a malformed connection string it rejected;
* URL user information up to the last ``@`` before the host;
* values of credential-like keys in ``key=value``, ``key: value`` and quoted
  JSON or Python ``"key": "value"`` form, and whole ``Authorization`` and
  cookie headers;
* bearer and basic credentials and AWS access key IDs.

Pattern matching cannot recognize every credential, so register the ones a
plugin knows about.
"""

from __future__ import annotations

import re
import threading
from collections.abc import Iterable
from urllib.parse import quote, quote_plus, unquote

MASK = "***"
#: Shorter registered values are ignored: masking them would garble output.
MIN_SECRET_LENGTH = 3

# scheme://user:password@host -> scheme://***@host. Greedy up to the last "@"
# before the path, so an unencoded "@" in the password is masked too.
_URL_USERINFO = re.compile(
    r"(?P<scheme>\b[a-zA-Z][a-zA-Z0-9+.-]{0,31}://)(?P<userinfo>[^/\s?#]{1,1024})@"
)

# Key names whose values are credentials, case-insensitive, with an optional
# prefix such as "aws_", "x-", "client_" or camelCase "client" (but a bare
# "key" only on its own, so "monkey" or "cache_key" are left alone).
_NAMES = (
    r"password|passwd|pwd|passphrase|sslpassword|secret|token|credentials?|auth"
    r"|api[_-]?key|apikey|private[_-]?key|access[_-]?key|secret[_-]?key"
    r"|secret[_-]?access[_-]?key|sig|signature"
)
_KEY = rf"(?:[a-z0-9_-]{{0,40}}?(?:{_NAMES})|key)"

# token=..., password: '...', "client_secret": "..." in query strings, form
# bodies, libpq key=value strings, headers and JSON or Python reprs.
# Dotted configuration keys (spring.datasource.password=...) count, but a key
# right after "/" is a path component (/run/secrets/secret: not found), not a
# parameter. Only a quoted key (JSON or a Python repr) ends an unquoted value
# at "}", "]" or ")"; elsewhere those may be part of the secret.
_SECRET_PARAMETER = re.compile(
    rf"(?i)(?<![\w./-])(?P<key>(?P<q>[\"'])?(?:[a-z0-9_-]{{1,80}}\.){{0,8}}{_KEY}(?(q)(?P=q)))"
    r"(?![\w-])"
    r"(?P<sep>\s{0,8}[=:]\s{0,8})"
    r"(?P<value>'[^']{0,4096}'|\"[^\"]{0,4096}\""
    r"|(?(q)[^\s&;,'\"}\])]{1,4096}|[^\s&;,'\"]{1,4096}))"
)

# Headers whose whole value is a credential, whatever its scheme.
_HEADER = re.compile(
    r"(?im)(?<![\w-])(?P<key>(?:proxy-)?authorization|cookie|set-cookie)(?P<sep>\s{0,8}:\s{0,8})"
    r"[^\r\n]{1,8192}"
)

# Authorization header values such as "Bearer abc".
_AUTH_SCHEME = re.compile(r"(?i)\b(?P<scheme>bearer|basic)\s{1,8}[a-z0-9._~+/=-]{8,}")

# AWS access key IDs (long-term AKIA, temporary ASIA, and other principals).
_AWS_KEY_ID = re.compile(r"\b(?:AKIA|ASIA|AGPA|AIDA|AROA|ANPA|ANVA|AIPA)[A-Z0-9]{16}\b")

# A quoted fragment, as libpq and other parsers echo a rejected token.
_QUOTED = re.compile(r"\"(?P<d>[^\"\r\n]{1,1024})\"|'(?P<s>[^'\r\n]{1,1024})'")

_lock = threading.Lock()
_secrets: frozenset[str] = frozenset()


def _forms(value: str) -> set[str]:
    """Return ``value`` as written, percent-decoded and percent-encoded."""
    forms = {value, unquote(value), quote(value, safe=""), quote_plus(value, safe="")}
    return {form for form in forms if len(form) >= MIN_SECRET_LENGTH}


def _add(values: Iterable[str]) -> None:
    """Add literals to the registry; readers see either the old or the new set."""
    global _secrets
    new = set(values)
    with _lock:
        if not new <= _secrets:
            _secrets = _secrets | new


def _embedded(text: str) -> set[str]:
    """Return the credentials embedded in ``text`` (URL passwords, key=value secrets)."""
    found: set[str] = set()
    for match in _URL_USERINFO.finditer(text):
        _, _, password = match["userinfo"].partition(":")
        found |= _forms(password)
    for match in _SECRET_PARAMETER.finditer(text):
        found |= _forms(match["value"].strip("'\""))
    return found


def register_secret(value: str | None) -> None:
    """Mask ``value`` and the credentials it embeds in all later output.

    Use it for any credential a plugin resolves: the whole value (a DSN or a
    URL with a password, for example) is masked, as are its URL-encoded forms
    and passwords found inside it.
    """
    if value:
        _add(_forms(value) | _embedded(value))


def register_embedded_secrets(text: str | None) -> None:
    """Mask only the credentials inside ``text``, such as a URL's password."""
    if text:
        _add(_embedded(text))


def clear_secrets() -> None:
    """Forget every registered secret (for tests and long-lived callers)."""
    global _secrets
    with _lock:
        _secrets = frozenset()


def _mask_parameter(match: re.Match[str]) -> str:
    """Mask a parameter's value, keeping its key, separator and quotes."""
    value = match["value"]
    quote_char = value[0] if value[0] in "'\"" else ""
    return f"{match['key']}{match['sep']}{quote_char}{MASK}{quote_char}"


def redact(text: str) -> str:
    """Return ``text`` with registered secrets and recognizable credentials masked."""
    secrets = _secrets
    for secret in sorted(secrets, key=len, reverse=True):
        text = text.replace(secret, MASK)
    if secrets:

        def fragment(match: re.Match[str]) -> str:
            """Mask a quoted fragment that is part of a registered secret."""
            inner = match["d"] if match["d"] is not None else match["s"]
            if len(inner) >= MIN_SECRET_LENGTH and any(inner in secret for secret in secrets):
                return match[0][0] + MASK + match[0][0]
            return match[0]

        text = _QUOTED.sub(fragment, text)
    text = _URL_USERINFO.sub(rf"\g<scheme>{MASK}@", text)
    text = _HEADER.sub(rf"\g<key>\g<sep>{MASK}", text)
    text = _SECRET_PARAMETER.sub(_mask_parameter, text)
    text = _AUTH_SCHEME.sub(rf"\g<scheme> {MASK}", text)
    return _AWS_KEY_ID.sub(MASK, text)
