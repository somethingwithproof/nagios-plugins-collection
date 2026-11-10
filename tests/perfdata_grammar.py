# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""An independent parser for Nagios plugin output, written from the guidelines.

It deliberately shares no code with :mod:`nagios_plugins.base`, so tests that
use it check the formatter against the specification rather than against
itself. Grammar (Monitoring Plugins Development Guidelines, "Performance
data")::

    output    = status-line *( LF long-line )
    perfdata  = item *( SP item )
    item      = label "=" value [uom] [";" [warn] [";" [crit] [";" [min] [";" [max]]]]]
    label     = 1*( %x21-7E except "=" and "'" )  |  "'" 1*( char | "''" ) "'"
    value     = number | "U"
    uom       = "s" | "ms" | "us" | "%" | "B" | "KB" | "MB" | "GB" | "TB" | "c"
    warn/crit = range   ; [@][start:]end, start may be "~" or empty
"""

from __future__ import annotations

import re
from dataclasses import dataclass

#: The guidelines allow [-0-9.]: plain positional notation, no exponent.
NUMBER = r"-?(?:\d+(?:\.\d*)?|\.\d+)"
UOMS = ("us", "ms", "s", "%", "KB", "MB", "GB", "TB", "B", "c", "")
RANGE = re.compile(rf"@?(?:(?:~|{NUMBER})?:)?(?:{NUMBER})?")
STATUS_LINE = re.compile(r"(OK|WARNING|CRITICAL|UNKNOWN) - (?P<text>[^|\n]*)(?:\|(?P<perf>.*))?")
KEYWORDS = {"OK": 0, "WARNING": 1, "CRITICAL": 2, "UNKNOWN": 3}


class GrammarError(ValueError):
    """The text does not follow the plugin output grammar."""


@dataclass(frozen=True)
class Item:
    """One performance data item."""

    label: str
    value: float | None  # None for "U" (unknown)
    uom: str
    warn: str
    crit: str
    minimum: float | None
    maximum: float | None


def _label(text: str, start: int) -> tuple[str, int]:
    if text.startswith("'", start):
        out, i = [], start + 1
        while i < len(text):
            if text[i] == "'":
                if text.startswith("''", i):
                    out.append("'")
                    i += 2
                    continue
                if not out:
                    raise GrammarError("empty quoted label")
                if not text.startswith("=", i + 1):
                    raise GrammarError(f"expected '=' after label at {i + 1}")
                return "".join(out), i + 2
            out.append(text[i])
            i += 1
        raise GrammarError("unterminated quoted label")
    end = text.find("=", start)
    label = text[start:end] if end > start else ""
    if not label or any(c in label for c in " '") or not label.isprintable():
        raise GrammarError(f"bad label at {start}: {text[start:]!r}")
    return label, end + 1


def _number(text: str, what: str) -> float | None:
    if text == "":
        return None
    if not re.fullmatch(NUMBER, text):
        raise GrammarError(f"{what} is not a number: {text!r}")
    return float(text)


def parse_perfdata(text: str) -> list[Item]:
    """Parse the text after ``|``; raise :class:`GrammarError` on any deviation."""
    items, i, text = [], 0, text.strip()
    while i < len(text):
        label, i = _label(text, i)
        end = text.find(" ", i)
        end = len(text) if end == -1 else end
        fields = text[i:end].split(";")
        if len(fields) > 5:
            raise GrammarError(f"too many fields for {label!r}")
        fields += [""] * (5 - len(fields))
        raw, warn, crit, low, high = fields
        if raw == "U":
            value, uom = None, ""
        else:
            match = re.match(NUMBER, raw)
            if not match:
                raise GrammarError(f"value of {label!r} is not a number: {raw!r}")
            value, uom = float(match.group()), raw[match.end() :]
            if uom not in UOMS:
                raise GrammarError(f"unit of {label!r} is not allowed: {uom!r}")
        for name, threshold in (("warn", warn), ("crit", crit)):
            if threshold and not RANGE.fullmatch(threshold):
                raise GrammarError(f"{name} of {label!r} is not a range: {threshold!r}")
        items.append(Item(label, value, uom, warn, crit, _number(low, "min"), _number(high, "max")))
        i = end + 1
        while i < len(text) and text[i] == " ":
            i += 1
    return items


@dataclass(frozen=True)
class Output:
    """A parsed plugin result."""

    keyword: str
    text: str
    perfdata: list[Item]
    long_output: list[str]


def parse_output(stdout: str) -> Output:
    """Parse a complete plugin stdout: one status line, then optional long output."""
    if not stdout.endswith("\n"):
        raise GrammarError("output must end with a newline")
    first, *rest = stdout[:-1].split("\n")
    match = STATUS_LINE.fullmatch(first)
    if not match:
        raise GrammarError(f"not a status line: {first!r}")
    for line in rest:
        if "|" in line:
            raise GrammarError(f"'|' in long output would start perfdata: {line!r}")
        if STATUS_LINE.match(line):
            raise GrammarError(f"a second status line: {line!r}")
    perf = parse_perfdata(match["perf"]) if match["perf"] is not None else []
    return Output(match.group(1), match["text"], perf, rest)
