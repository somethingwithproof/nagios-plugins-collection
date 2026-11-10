# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Property tests for the Nagios range parser and the perfdata formatter.

The oracles come from the Monitoring Plugins Development Guidelines, not from
the implementation: a range ``[@]start:end`` alerts outside ``start..end``
(both endpoints inclusive), or inside it with ``@``; perfdata is checked with
the independent parser in :mod:`tests.perfdata_grammar`.
"""

from __future__ import annotations

import argparse
import math
from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from nagios_plugins.base import (
    PERFDATA_UOMS,
    PerfData,
    Status,
    ThresholdRange,
    format_perfdata,
    nagios_range,
    single_line,
    threshold_check,
)
from tests.perfdata_grammar import GrammarError, parse_output, parse_perfdata

BOUND = st.decimals(min_value=-(10**6), max_value=10**6, places=3, allow_nan=False)
VALUE = st.floats(min_value=-2e6, max_value=2e6, allow_nan=False)


def _text(number: Decimal) -> str:
    return format(number.normalize() if number else Decimal(0), "f")


@st.composite
def ranges(draw: st.DrawFn) -> tuple[str, float, float, bool]:
    """A range string with the bounds and inversion it denotes."""
    low, high = sorted((draw(BOUND), draw(BOUND)))
    inside = draw(st.booleans())
    prefix = "@" if inside else ""
    form = draw(st.sampled_from(["start:end", "end", "start:", "~:end"]))
    if form == "end":
        high = abs(high)
        return f"{prefix}{_text(high)}", 0.0, float(high), inside
    if form == "start:":
        return f"{prefix}{_text(low)}:", float(low), math.inf, inside
    if form == "~:end":
        return f"{prefix}~:{_text(high)}", -math.inf, float(high), inside
    return f"{prefix}{_text(low)}:{_text(high)}", float(low), float(high), inside


def _alerts(value: float, low: float, high: float, inside: bool) -> bool:
    within = low <= value <= high
    return within if inside else not within


@given(ranges(), VALUE)
def test_range_alerts_follow_the_guidelines(
    spec: tuple[str, float, float, bool], value: float
) -> None:
    text, low, high, inside = spec
    assert ThresholdRange.from_string(text).check(value) is not _alerts(value, low, high, inside)


@given(ranges())
def test_range_endpoints_are_inclusive(spec: tuple[str, float, float, bool]) -> None:
    text, low, high, inside = spec
    parsed = ThresholdRange.from_string(text)
    for endpoint in (low, high):
        if math.isfinite(endpoint):
            # On an endpoint the value is within the range: OK, or an alert with @.
            assert parsed.check(endpoint) is not inside


@given(BOUND, BOUND)
def test_a_start_above_the_end_is_rejected(first: Decimal, second: Decimal) -> None:
    if first == second:
        return
    low, high = sorted((first, second))
    with pytest.raises(ValueError):
        ThresholdRange.from_string(f"{_text(high)}:{_text(low)}")


@given(st.text(max_size=12))
def test_arbitrary_text_is_accepted_or_rejected_with_value_error(text: str) -> None:
    """The option type and the parser agree, and nothing but ValueError escapes."""
    try:
        ThresholdRange.from_string(text)
    except ValueError:
        with pytest.raises(argparse.ArgumentTypeError):
            nagios_range(text)
    else:
        assert nagios_range(text) == text


@given(ranges(), ranges(), VALUE)
def test_critical_takes_precedence(
    warning: tuple[str, float, float, bool],
    critical: tuple[str, float, float, bool],
    value: float,
) -> None:
    status = threshold_check(value, warning[0], critical[0])
    if _alerts(value, *critical[1:]):
        assert status is Status.CRITICAL
    elif _alerts(value, *warning[1:]):
        assert status is Status.WARNING
    else:
        assert status is Status.OK


# Perfdata --------------------------------------------------------------------

LABEL = st.text(min_size=1, max_size=20).filter(lambda text: bool(single_line(text).strip()))
NUMBER = st.one_of(st.integers(-(10**12), 10**12), st.floats(allow_nan=True, allow_infinity=True))
BOUNDS = st.one_of(st.none(), st.integers(-1000, 1000), st.floats(-1e6, 1e6, allow_nan=False))
THRESHOLD = st.one_of(st.none(), ranges().map(lambda spec: spec[0]))


@st.composite
def metrics(draw: st.DrawFn) -> dict[str, PerfData | float]:
    labels = draw(
        st.lists(
            LABEL,
            min_size=1,
            max_size=5,
            unique_by=lambda text: "".join(
                c if c.isprintable() else "_" for c in single_line(text)
            ),
        )
    )
    out: dict[str, PerfData | float] = {}
    for label in labels:
        value = draw(NUMBER)
        if draw(st.booleans()):
            out[label] = value
        else:
            out[label] = PerfData(
                value,
                draw(st.sampled_from(sorted(PERFDATA_UOMS))),
                draw(THRESHOLD),
                draw(THRESHOLD),
                draw(BOUNDS),
                draw(BOUNDS),
            )
    return out


def _label(text: str) -> str:
    """Guidelines: one line, printable; the formatter maps anything else to '_'."""
    return "".join(char if char.isprintable() else "_" for char in single_line(text))


def _finite(value: object) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(value)


@given(metrics())
def test_formatted_perfdata_parses_and_round_trips(data: dict[str, PerfData | float]) -> None:
    items = parse_perfdata(format_perfdata(data))
    expected = {
        _label(label): metric if isinstance(metric, PerfData) else PerfData(metric)
        for label, metric in data.items()
    }
    expected = {label: perf for label, perf in expected.items() if _finite(perf.value)}
    assert [item.label for item in items] == list(expected)
    for item in items:
        perf = expected[item.label]
        assert item.value == perf.value  # exact: no rounding, no exponent notation
        assert item.uom == perf.uom
        assert item.warn == (perf.warning or "")
        assert item.crit == (perf.critical or "")
        assert item.minimum == perf.minimum
        assert item.maximum == perf.maximum


@pytest.mark.parametrize(
    "text",
    [
        "x=1;2;3;4;5;6",  # too many fields
        "x=1furlongs",  # unit not in the guidelines
        "x=1e3",  # exponent: a unit 'e3'
        "x=1;abc",  # warn is not a range
        "'x=1",  # unterminated quote
        "x y=1",  # unquoted space
        "=1",  # empty label
        "x=;;;",  # no value
    ],
)
def test_grammar_parser_rejects_invalid_perfdata(text: str) -> None:
    """The oracle is strict, so the properties above are not vacuous."""
    with pytest.raises(GrammarError):
        parse_perfdata(text)


@pytest.mark.parametrize(
    "stdout",
    ["OK - fine", "OK - fine\nOK - again\n", "OK - fine\nlong | output\n", "BROKEN - x\n"],
)
def test_grammar_parser_rejects_invalid_status_output(stdout: str) -> None:
    with pytest.raises(GrammarError):
        parse_output(stdout)


def test_grammar_parser_accepts_guideline_examples() -> None:
    items = parse_perfdata("'time taken'=0.5s;1;2;0; size=12KB load=U 'it''s'=3c")
    assert [(i.label, i.value, i.uom) for i in items] == [
        ("time taken", 0.5, "s"),
        ("size", 12.0, "KB"),
        ("load", None, ""),
        ("it's", 3.0, "c"),
    ]
    assert items[0].warn == "1" and items[0].minimum == 0
