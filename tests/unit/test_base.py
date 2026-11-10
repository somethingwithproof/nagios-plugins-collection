# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Tests for the base module."""

import argparse
from unittest.mock import MagicMock, patch

import pytest

from nagios_plugins.base import (
    CheckResult,
    NagiosPlugin,
    PerfData,
    Status,
    ThresholdRange,
    threshold_check,
)


class TestStatus:
    """Tests for the Status enum."""

    def test_from_string(self) -> None:
        """Test the from_string method."""
        assert Status.from_string("OK") == Status.OK
        assert Status.from_string("WARNING") == Status.WARNING
        assert Status.from_string("CRITICAL") == Status.CRITICAL
        assert Status.from_string("UNKNOWN") == Status.UNKNOWN
        assert Status.from_string("INVALID") == Status.UNKNOWN

    def test_str(self) -> None:
        """Test the __str__ method."""
        assert str(Status.OK) == "OK"
        assert str(Status.WARNING) == "WARNING"
        assert str(Status.CRITICAL) == "CRITICAL"
        assert str(Status.UNKNOWN) == "UNKNOWN"


class TestCheckResult:
    """Tests for the CheckResult class."""

    def test_str_simple(self) -> None:
        """Test the __str__ method with a simple result."""
        result = CheckResult(Status.OK, "Everything is fine")
        assert str(result) == "OK - Everything is fine"

    def test_str_with_metrics(self) -> None:
        """Test the __str__ method with metrics."""
        result = CheckResult(
            Status.WARNING,
            "High CPU usage",
            metrics={"cpu": 85, "memory": 50},
        )
        assert str(result) == "WARNING - High CPU usage | cpu=85 memory=50"

    def test_str_with_details(self) -> None:
        """Test the __str__ method with details."""
        result = CheckResult(
            Status.CRITICAL,
            "Service is down",
            details="The service has been down for 10 minutes.",
        )
        assert (
            str(result) == "CRITICAL - Service is down\nThe service has been down for 10 minutes."
        )

    def test_str_with_metrics_and_details(self) -> None:
        """Test the __str__ method with metrics and details."""
        result = CheckResult(
            Status.UNKNOWN,
            "Unknown status",
            metrics={"uptime": 3600},
            details="Could not determine the status of the service.",
        )
        assert (
            str(result) == "UNKNOWN - Unknown status | uptime=3600\n"
            "Could not determine the status of the service."
        )


class TestPerfdataContract:
    """The status line and perfdata follow the Nagios Plugin Guidelines."""

    def test_full_perfdata_item(self) -> None:
        """Units, thresholds and bounds render in guideline order."""
        result = CheckResult(
            Status.OK,
            "fine",
            metrics={
                "used": PerfData(42.5, "%", warning="80", critical="90", minimum=0, maximum=100)
            },
        )
        assert str(result) == "OK - fine | used=42.5%;80;90;0;100"

    def test_trailing_empty_fields_are_omitted(self) -> None:
        """Only the fields up to the last populated one are emitted."""
        result = CheckResult(Status.OK, "fine", metrics={"t": PerfData(1, "s", critical="5")})
        assert str(result) == "OK - fine | t=1s;;5"

    def test_labels_with_spaces_equals_or_quotes_are_quoted(self) -> None:
        """Labels are quoted and embedded single quotes doubled."""
        result = CheckResult(
            Status.OK, "fine", metrics={"job a": 1, "a=b": 2, "it's": 3, "plain_label": 4}
        )
        assert str(result) == "OK - fine | 'job a'=1 'a=b'=2 'it''s'=3 plain_label=4"

    def test_non_numeric_and_non_finite_values_are_omitted(self) -> None:
        """Strings, None and inf/nan never reach perfdata."""
        result = CheckResult(
            Status.OK,
            "fine",
            metrics={"unit": "Percent", "state": "ok", "p95": float("inf"), "x": None, "n": 2},
        )
        assert str(result) == "OK - fine | n=2"

    def test_numbers_use_positional_notation(self) -> None:
        """Perfdata values never use exponent notation."""
        result = CheckResult(
            Status.OK, "fine", metrics={"tiny": 0.00001, "big": 1e20, "flag": True}
        )
        assert str(result) == "OK - fine | tiny=0.00001 big=100000000000000000000 flag=1"

    def test_message_is_a_single_line_without_pipes(self) -> None:
        """A message cannot split the status line or inject perfdata."""
        result = CheckResult(Status.CRITICAL, "a | b\nc", metrics={"n": 1}, details="x | y\nz")
        assert str(result).splitlines() == ["CRITICAL - a / b c | n=1", "x / y", "z"]

    def test_invalid_unit_is_rejected(self) -> None:
        """Only guideline units are accepted."""
        with pytest.raises(ValueError):
            PerfData(1, "Percent")

    def test_json_metrics_stay_plain_and_valid(self) -> None:
        """JSON keeps plain metric values and never emits Infinity."""
        import json

        result = CheckResult(
            Status.OK, "fine", metrics={"v": PerfData(1.5, "%"), "p95": float("inf"), "u": "Count"}
        )
        assert json.loads(result.to_json())["metrics"] == {"v": 1.5, "p95": None, "u": "Count"}
        assert "Infinity" not in result.to_json()


class TestNagiosPlugin:
    """Tests for the NagiosPlugin class."""

    class TestPlugin(NagiosPlugin):
        """Test plugin implementation."""

        def check(self, args: argparse.Namespace) -> CheckResult:
            """Perform the check."""
            if args.fail:
                return CheckResult(Status.CRITICAL, "Test failed")
            return CheckResult(Status.OK, "Test passed")

    @pytest.fixture
    def plugin(self) -> "TestNagiosPlugin.TestPlugin":
        """Create a test plugin."""
        plugin = self.TestPlugin()
        plugin.parser.add_argument("--fail", action="store_true", help="Fail the test")
        return plugin

    def test_parse_args(self, plugin: "TestNagiosPlugin.TestPlugin") -> None:
        """Test the parse_args method."""
        args = plugin.parse_args(["--verbose"])
        assert args.verbose == 1
        assert args.timeout == 30
        assert args.warning is None
        assert args.critical is None
        assert args.fail is False

    def test_parse_args_with_custom_args(self, plugin: "TestNagiosPlugin.TestPlugin") -> None:
        """Test the parse_args method with custom arguments."""
        args = plugin.parse_args(["--fail", "--timeout", "60"])
        assert args.verbose == 0
        assert args.timeout == 60
        assert args.warning is None
        assert args.critical is None
        assert args.fail is True

    def test_run_success(self, plugin: "TestNagiosPlugin.TestPlugin") -> None:
        """Test the run method with a successful check."""
        with patch("sys.stdout", new=MagicMock()) as mock_stdout:
            exit_code = plugin.run(["--verbose"])
            assert exit_code == 0
            mock_stdout.write.assert_called_with("OK - Test passed\n")

    def test_run_failure(self, plugin: "TestNagiosPlugin.TestPlugin") -> None:
        """Test the run method with a failed check."""
        with patch("sys.stdout", new=MagicMock()) as mock_stdout:
            exit_code = plugin.run(["--fail"])
            assert exit_code == 2
            mock_stdout.write.assert_called_with("CRITICAL - Test failed\n")

    def test_run_exception(self, plugin: "TestNagiosPlugin.TestPlugin") -> None:
        """Test the run method with an exception."""
        with (
            patch.object(plugin, "check", side_effect=ValueError("Test error")),
            patch("sys.stdout", new=MagicMock()) as mock_stdout,
        ):
            exit_code = plugin.run([])
            assert exit_code == 3
            mock_stdout.write.assert_called_with("UNKNOWN - Unhandled exception: Test error\n")


class TestThresholdCheck:
    """Tests for the threshold_check function."""

    def test_simple_thresholds(self) -> None:
        """Test simple thresholds."""
        # Value below warning threshold
        assert threshold_check(50, warning="75", critical="90") == Status.OK
        # Value above warning threshold but below critical threshold
        assert threshold_check(80, warning="75", critical="90") == Status.WARNING
        # Value above critical threshold
        assert threshold_check(95, warning="75", critical="90") == Status.CRITICAL

    def test_range_thresholds(self) -> None:
        """Test range thresholds."""
        # Value within range (OK)
        assert threshold_check(50, warning="10:90", critical="5:95") == Status.OK
        # Value outside warning range but within critical range
        assert threshold_check(92, warning="10:90", critical="5:95") == Status.WARNING
        # Value outside critical range
        assert threshold_check(97, warning="10:90", critical="5:95") == Status.CRITICAL

    def test_inverted_thresholds(self) -> None:
        """``@a:b`` alerts when a <= value <= b; critical wins when both alert."""
        # Outside both inverted ranges (OK)
        assert threshold_check(4, warning="@10:90", critical="@5:95") == Status.OK
        assert threshold_check(96, warning="@10:90", critical="@5:95") == Status.OK
        # Inside the critical range only: CRITICAL, as documented in usage.rst
        assert threshold_check(7, warning="@10:80", critical="@5:90") == Status.CRITICAL
        # Endpoints are inside the range
        assert threshold_check(5, warning="@10:90", critical="@5:95") == Status.CRITICAL
        assert threshold_check(10, warning="@10:90") == Status.WARNING
        assert threshold_check(90, warning="@10:90") == Status.WARNING
        # Inside both ranges
        assert threshold_check(50, warning="@10:90", critical="@5:95") == Status.CRITICAL

    def test_min_only_thresholds(self) -> None:
        """Test thresholds with only a minimum value."""
        # Value above minimum (OK)
        assert threshold_check(50, warning="10:", critical="5:") == Status.OK
        # Value below warning minimum but above critical minimum
        assert threshold_check(7, warning="10:", critical="5:") == Status.WARNING
        # Value below critical minimum
        assert threshold_check(3, warning="10:", critical="5:") == Status.CRITICAL

    def test_max_only_thresholds(self) -> None:
        """Test thresholds with only a maximum value."""
        # Value below maximum (OK)
        assert threshold_check(50, warning=":90", critical=":95") == Status.OK
        # Value above warning maximum but below critical maximum
        assert threshold_check(92, warning=":90", critical=":95") == Status.WARNING
        # Value above critical maximum
        assert threshold_check(97, warning=":90", critical=":95") == Status.CRITICAL

    def test_bare_value_means_zero_to_value(self) -> None:
        """A bare ``10`` is ``0:10``: negative values alert as well as values above 10."""
        assert threshold_check(10, critical="10") == Status.OK
        assert threshold_check(0, critical="10") == Status.OK
        assert threshold_check(-1, critical="10") == Status.CRITICAL
        assert threshold_check(10.5, critical="10") == Status.CRITICAL

    def test_negative_infinity_start(self) -> None:
        """``~:10`` has no lower bound and alerts only above 10."""
        assert threshold_check(-1000, critical="~:10") == Status.OK
        assert threshold_check(11, critical="~:10") == Status.CRITICAL
        assert threshold_check(-1000, critical="@~:0") == Status.CRITICAL

    def test_range_endpoints_are_inclusive(self) -> None:
        """``10:20`` accepts both endpoints."""
        assert threshold_check(10, warning="10:20") == Status.OK
        assert threshold_check(20, warning="10:20") == Status.OK
        assert threshold_check(9.99, warning="10:20") == Status.WARNING

    @pytest.mark.parametrize("threshold", ["abc", "1:2:3", "20:10", "~:x", "nan", "1:inf"])
    def test_malformed_threshold_raises(self, threshold: str) -> None:
        """Malformed ranges are rejected rather than ignored."""
        with pytest.raises(ValueError):
            threshold_check(1, critical=threshold)

    def test_nan_value_is_unknown(self) -> None:
        """A NaN measurement cannot be compared with a range."""
        assert threshold_check(float("nan"), warning="1", critical="2") == Status.UNKNOWN

    @pytest.mark.parametrize(
        ("threshold", "rendered"),
        [("10", "10"), ("10:", "10:"), ("~:10", "~:10"), ("@1.5:2", "@1.5:2"), ("", "")],
    )
    def test_range_round_trips_to_nagios_syntax(self, threshold: str, rendered: str) -> None:
        """ThresholdRange renders standard syntax usable in perfdata."""
        assert str(ThresholdRange.from_string(threshold)) == rendered

    def test_no_thresholds(self) -> None:
        """Test with no thresholds."""
        assert threshold_check(50) == Status.OK
        assert threshold_check(50, warning=None, critical=None) == Status.OK


def test_most_severe_follows_nagios_precedence() -> None:
    from nagios_plugins.base import most_severe

    assert most_severe() is Status.OK
    assert most_severe(Status.OK, Status.UNKNOWN) is Status.UNKNOWN
    assert most_severe(Status.UNKNOWN, Status.WARNING) is Status.WARNING
    assert most_severe(Status.WARNING, Status.CRITICAL, Status.OK) is Status.CRITICAL
