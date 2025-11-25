"""Tests for the base module."""

import pytest

from nagios_plugins.base import (
    CheckResult,
    Status,
    ThresholdRange,
    get_env_or_arg,
)


class TestStatus:
    """Tests for the Status enum."""

    def test_status_values(self):
        """Test that status codes match Nagios convention."""
        assert Status.OK == 0
        assert Status.WARNING == 1
        assert Status.CRITICAL == 2
        assert Status.UNKNOWN == 3

    def test_status_names(self):
        """Test status name access."""
        assert Status.OK.name == "OK"
        assert Status.WARNING.name == "WARNING"
        assert Status.CRITICAL.name == "CRITICAL"
        assert Status.UNKNOWN.name == "UNKNOWN"


class TestThresholdRange:
    """Tests for the ThresholdRange class."""

    def test_parse_simple_value(self):
        """Test parsing simple threshold like '10'."""
        tr = ThresholdRange.parse("10")
        assert tr.start == 0
        assert tr.end == 10
        assert tr.inside is False

    def test_parse_min_only(self):
        """Test parsing threshold like '10:' (minimum only)."""
        tr = ThresholdRange.parse("10:")
        assert tr.start == 10
        assert tr.end is None
        assert tr.inside is False

    def test_parse_max_only(self):
        """Test parsing threshold like '~:10' (maximum only)."""
        tr = ThresholdRange.parse("~:10")
        assert tr.start is None
        assert tr.end == 10
        assert tr.inside is False

    def test_parse_range(self):
        """Test parsing threshold like '10:20' (range)."""
        tr = ThresholdRange.parse("10:20")
        assert tr.start == 10
        assert tr.end == 20
        assert tr.inside is False

    def test_parse_inside_range(self):
        """Test parsing threshold like '@10:20' (inside range)."""
        tr = ThresholdRange.parse("@10:20")
        assert tr.start == 10
        assert tr.end == 20
        assert tr.inside is True

    def test_parse_none(self):
        """Test parsing None returns None."""
        assert ThresholdRange.parse(None) is None
        assert ThresholdRange.parse("") is None

    def test_check_simple_value_ok(self):
        """Test check with simple value - OK case."""
        tr = ThresholdRange.parse("10")
        assert tr.check(5) is False  # 5 is in range 0-10, no alert
        assert tr.check(10) is False  # 10 is in range 0-10, no alert

    def test_check_simple_value_alert(self):
        """Test check with simple value - alert case."""
        tr = ThresholdRange.parse("10")
        assert tr.check(11) is True  # 11 is outside range, alert
        assert tr.check(-1) is True  # -1 is outside range, alert

    def test_check_range_ok(self):
        """Test check with range - OK case."""
        tr = ThresholdRange.parse("10:20")
        assert tr.check(15) is False  # 15 is in range, no alert

    def test_check_range_alert(self):
        """Test check with range - alert case."""
        tr = ThresholdRange.parse("10:20")
        assert tr.check(5) is True  # 5 is outside range, alert
        assert tr.check(25) is True  # 25 is outside range, alert

    def test_check_inside_range(self):
        """Test check with inside range (@prefix)."""
        tr = ThresholdRange.parse("@10:20")
        assert tr.check(15) is True  # 15 is inside range, alert
        assert tr.check(5) is False  # 5 is outside range, no alert


class TestCheckResult:
    """Tests for the CheckResult class."""

    def test_simple_result(self):
        """Test basic result formatting."""
        result = CheckResult(Status.OK, "All good")
        assert str(result) == "OK - All good"

    def test_result_with_simple_perfdata(self):
        """Test result with simple perfdata."""
        result = CheckResult(
            Status.WARNING,
            "High load",
            {"load": 5.5},
        )
        assert str(result) == "WARNING - High load | load=5.5"

    def test_result_with_full_perfdata(self):
        """Test result with full perfdata format."""
        result = CheckResult(
            Status.OK,
            "Process count OK",
            {
                "procs": {
                    "value": 10,
                    "warn": 20,
                    "crit": 30,
                    "min": 0,
                    "max": 100,
                    "unit": "",
                }
            },
        )
        output = str(result)
        assert "OK - Process count OK |" in output
        assert "procs=10;20;30;0;100" in output

    def test_result_with_units(self):
        """Test result with unit in perfdata."""
        result = CheckResult(
            Status.OK,
            "Memory OK",
            {
                "memory": {
                    "value": 512,
                    "unit": "MB",
                    "warn": "",
                    "crit": "",
                    "min": "",
                    "max": "",
                }
            },
        )
        assert "memory=512MB" in str(result)


class TestGetEnvOrArg:
    """Tests for the get_env_or_arg function."""

    def test_arg_takes_precedence(self, monkeypatch):
        """Test that argument value takes precedence over env var."""
        monkeypatch.setenv("TEST_VAR", "env_value")
        result = get_env_or_arg("TEST_VAR", "arg_value")
        assert result == "arg_value"

    def test_env_used_when_no_arg(self, monkeypatch):
        """Test that env var is used when arg is None."""
        monkeypatch.setenv("TEST_VAR", "env_value")
        result = get_env_or_arg("TEST_VAR", None)
        assert result == "env_value"

    def test_default_used_when_no_arg_or_env(self, monkeypatch):
        """Test that default is used when neither arg nor env is set."""
        monkeypatch.delenv("TEST_VAR", raising=False)
        result = get_env_or_arg("TEST_VAR", None, "default_value")
        assert result == "default_value"

    def test_none_when_nothing_set(self, monkeypatch):
        """Test that None is returned when nothing is set."""
        monkeypatch.delenv("TEST_VAR", raising=False)
        result = get_env_or_arg("TEST_VAR", None)
        assert result is None
