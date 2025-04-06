"""Tests for the base module."""

from unittest.mock import MagicMock, patch

import pytest

from nagios_plugins.base import CheckResult, NagiosPlugin, Status, threshold_check


class TestStatus:
    """Tests for the Status enum."""

    def test_from_string(self):
        """Test the from_string method."""
        assert Status.from_string("OK") == Status.OK
        assert Status.from_string("WARNING") == Status.WARNING
        assert Status.from_string("CRITICAL") == Status.CRITICAL
        assert Status.from_string("UNKNOWN") == Status.UNKNOWN
        assert Status.from_string("INVALID") == Status.UNKNOWN

    def test_str(self):
        """Test the __str__ method."""
        assert str(Status.OK) == "OK"
        assert str(Status.WARNING) == "WARNING"
        assert str(Status.CRITICAL) == "CRITICAL"
        assert str(Status.UNKNOWN) == "UNKNOWN"


class TestCheckResult:
    """Tests for the CheckResult class."""

    def test_str_simple(self):
        """Test the __str__ method with a simple result."""
        result = CheckResult(Status.OK, "Everything is fine")
        assert str(result) == "OK - Everything is fine"

    def test_str_with_metrics(self):
        """Test the __str__ method with metrics."""
        result = CheckResult(
            Status.WARNING,
            "High CPU usage",
            metrics={"cpu": 85, "memory": 50},
        )
        assert str(result) == "WARNING - High CPU usage | cpu=85 memory=50"

    def test_str_with_details(self):
        """Test the __str__ method with details."""
        result = CheckResult(
            Status.CRITICAL,
            "Service is down",
            details="The service has been down for 10 minutes.",
        )
        assert (
            str(result) == "CRITICAL - Service is down\n"
            "The service has been down for 10 minutes."
        )

    def test_str_with_metrics_and_details(self):
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


class TestNagiosPlugin:
    """Tests for the NagiosPlugin class."""

    class TestPlugin(NagiosPlugin):
        """Test plugin implementation."""

        def check(self, args):
            """Perform the check."""
            if args.fail:
                return CheckResult(Status.CRITICAL, "Test failed")
            return CheckResult(Status.OK, "Test passed")

    @pytest.fixture
    def plugin(self):
        """Create a test plugin."""
        plugin = self.TestPlugin()
        plugin.parser.add_argument("--fail", action="store_true", help="Fail the test")
        return plugin

    def test_parse_args(self, plugin):
        """Test the parse_args method."""
        args = plugin.parse_args(["--verbose"])
        assert args.verbose == 1
        assert args.timeout == 30
        assert args.warning is None
        assert args.critical is None
        assert args.fail is False

    def test_parse_args_with_custom_args(self, plugin):
        """Test the parse_args method with custom arguments."""
        args = plugin.parse_args(["--fail", "--timeout", "60"])
        assert args.verbose == 0
        assert args.timeout == 60
        assert args.warning is None
        assert args.critical is None
        assert args.fail is True

    def test_run_success(self, plugin):
        """Test the run method with a successful check."""
        with patch("sys.stdout", new=MagicMock()) as mock_stdout:
            exit_code = plugin.run(["--verbose"])
            assert exit_code == 0
            mock_stdout.write.assert_called_with("OK - Test passed\n")

    def test_run_failure(self, plugin):
        """Test the run method with a failed check."""
        with patch("sys.stdout", new=MagicMock()) as mock_stdout:
            exit_code = plugin.run(["--fail"])
            assert exit_code == 2
            mock_stdout.write.assert_called_with("CRITICAL - Test failed\n")

    def test_run_exception(self, plugin):
        """Test the run method with an exception."""
        with patch.object(
            plugin, "check", side_effect=ValueError("Test error")
        ):
            with patch("sys.stdout", new=MagicMock()) as mock_stdout:
                exit_code = plugin.run([])
                assert exit_code == 3
                mock_stdout.write.assert_called_with(
                    "UNKNOWN - Unhandled exception: Test error\n"
                )


class TestThresholdCheck:
    """Tests for the threshold_check function."""

    def test_simple_thresholds(self):
        """Test simple thresholds."""
        # Value below warning threshold
        assert threshold_check(50, warning="75", critical="90") == Status.OK
        # Value above warning threshold but below critical threshold
        assert threshold_check(80, warning="75", critical="90") == Status.WARNING
        # Value above critical threshold
        assert threshold_check(95, warning="75", critical="90") == Status.CRITICAL

    def test_range_thresholds(self):
        """Test range thresholds."""
        # Value within range (OK)
        assert threshold_check(50, warning="10:90", critical="5:95") == Status.OK
        # Value outside warning range but within critical range
        assert threshold_check(92, warning="10:90", critical="5:95") == Status.WARNING
        # Value outside critical range
        assert threshold_check(97, warning="10:90", critical="5:95") == Status.CRITICAL

    def test_inverted_thresholds(self):
        """Test inverted thresholds."""
        # Value outside inverted range (OK)
        assert threshold_check(5, warning="@10:90", critical="@5:95") == Status.OK
        # Value inside inverted warning range but outside inverted critical range
        assert threshold_check(7, warning="@10:90", critical="@5:95") == Status.OK
        # Value inside inverted critical range
        assert threshold_check(50, warning="@10:90", critical="@5:95") == Status.CRITICAL

    def test_min_only_thresholds(self):
        """Test thresholds with only a minimum value."""
        # Value above minimum (OK)
        assert threshold_check(50, warning="10:", critical="5:") == Status.OK
        # Value below warning minimum but above critical minimum
        assert threshold_check(7, warning="10:", critical="5:") == Status.WARNING
        # Value below critical minimum
        assert threshold_check(3, warning="10:", critical="5:") == Status.CRITICAL

    def test_max_only_thresholds(self):
        """Test thresholds with only a maximum value."""
        # Value below maximum (OK)
        assert threshold_check(50, warning=":90", critical=":95") == Status.OK
        # Value above warning maximum but below critical maximum
        assert threshold_check(92, warning=":90", critical=":95") == Status.WARNING
        # Value above critical maximum
        assert threshold_check(97, warning=":90", critical=":95") == Status.CRITICAL

    def test_no_thresholds(self):
        """Test with no thresholds."""
        assert threshold_check(50) == Status.OK
        assert threshold_check(50, warning=None, critical=None) == Status.OK
