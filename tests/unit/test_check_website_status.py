"""Tests for the check_website_status plugin."""

import pytest
from unittest.mock import MagicMock, patch

from nagios_plugins.base import Status
from nagios_plugins.check_website_status import CheckWebsiteStatus


class TestCheckWebsiteStatus:
    """Tests for the CheckWebsiteStatus plugin."""

    @pytest.fixture
    def plugin(self):
        """Create a CheckWebsiteStatus instance for testing."""
        return CheckWebsiteStatus()

    @pytest.fixture
    def mock_response(self):
        """Create a mock HTTP response."""
        response = MagicMock()
        response.status_code = 200
        response.text = "Hello World"
        response.content = b"Hello World"
        response.headers = {"content-type": "text/html"}
        return response

    @patch("nagios_plugins.check_website_status.HAS_HTTPX", True)
    def test_check_ok(self, plugin, mock_response):
        """Test check returns OK for successful request."""
        with patch.object(plugin, "_make_request", return_value=(mock_response, 0.5)):
            args = MagicMock()
            args.url = "https://example.com"
            args.string = None
            args.regex = None
            args.expect = "200"
            args.insecure = False
            args.follow_redirects = False
            args.method = "GET"
            args.data = None
            args.header = None
            args.auth = None
            args.warning = None
            args.critical = None
            args.content_type = None
            args.min_size = None
            args.max_size = None
            args.timeout = 30

            result = plugin.check(args)

            assert result.status == Status.OK
            assert "200" in result.message

    @patch("nagios_plugins.check_website_status.HAS_HTTPX", True)
    def test_check_string_found(self, plugin, mock_response):
        """Test check returns OK when search string is found."""
        mock_response.text = "Welcome to our website"

        with patch.object(plugin, "_make_request", return_value=(mock_response, 0.5)):
            args = MagicMock()
            args.url = "https://example.com"
            args.string = "Welcome"
            args.regex = None
            args.expect = "200"
            args.insecure = False
            args.follow_redirects = False
            args.method = "GET"
            args.data = None
            args.header = None
            args.auth = None
            args.warning = None
            args.critical = None
            args.content_type = None
            args.min_size = None
            args.max_size = None
            args.timeout = 30

            result = plugin.check(args)

            assert result.status == Status.OK

    @patch("nagios_plugins.check_website_status.HAS_HTTPX", True)
    def test_check_string_not_found(self, plugin, mock_response):
        """Test check returns CRITICAL when search string is not found."""
        mock_response.text = "Something else"

        with patch.object(plugin, "_make_request", return_value=(mock_response, 0.5)):
            args = MagicMock()
            args.url = "https://example.com"
            args.string = "Welcome"
            args.regex = None
            args.expect = "200"
            args.insecure = False
            args.follow_redirects = False
            args.method = "GET"
            args.data = None
            args.header = None
            args.auth = None
            args.warning = None
            args.critical = None
            args.content_type = None
            args.min_size = None
            args.max_size = None
            args.timeout = 30

            result = plugin.check(args)

            assert result.status == Status.CRITICAL
            assert "not found" in result.message

    @patch("nagios_plugins.check_website_status.HAS_HTTPX", True)
    def test_check_regex_match(self, plugin, mock_response):
        """Test check returns OK when regex matches."""
        mock_response.text = "Version: 1.2.3"

        with patch.object(plugin, "_make_request", return_value=(mock_response, 0.5)):
            args = MagicMock()
            args.url = "https://example.com"
            args.string = None
            args.regex = r"Version: \d+\.\d+\.\d+"
            args.expect = "200"
            args.insecure = False
            args.follow_redirects = False
            args.method = "GET"
            args.data = None
            args.header = None
            args.auth = None
            args.warning = None
            args.critical = None
            args.content_type = None
            args.min_size = None
            args.max_size = None
            args.timeout = 30

            result = plugin.check(args)

            assert result.status == Status.OK

    @patch("nagios_plugins.check_website_status.HAS_HTTPX", True)
    def test_check_wrong_status_code(self, plugin, mock_response):
        """Test check returns CRITICAL for unexpected status code."""
        mock_response.status_code = 500

        with patch.object(plugin, "_make_request", return_value=(mock_response, 0.5)):
            args = MagicMock()
            args.url = "https://example.com"
            args.string = None
            args.regex = None
            args.expect = "200"
            args.insecure = False
            args.follow_redirects = False
            args.method = "GET"
            args.data = None
            args.header = None
            args.auth = None
            args.warning = None
            args.critical = None
            args.content_type = None
            args.min_size = None
            args.max_size = None
            args.timeout = 30

            result = plugin.check(args)

            assert result.status == Status.CRITICAL
            assert "500" in result.message

    @patch("nagios_plugins.check_website_status.HAS_HTTPX", True)
    def test_check_timing_warning(self, plugin, mock_response):
        """Test check returns WARNING when response time exceeds threshold."""
        with patch.object(plugin, "_make_request", return_value=(mock_response, 1.5)):
            args = MagicMock()
            args.url = "https://example.com"
            args.string = None
            args.regex = None
            args.expect = "200"
            args.insecure = False
            args.follow_redirects = False
            args.method = "GET"
            args.data = None
            args.header = None
            args.auth = None
            args.warning = "1"  # 1 second warning threshold
            args.critical = "5"
            args.content_type = None
            args.min_size = None
            args.max_size = None
            args.timeout = 30

            result = plugin.check(args)

            assert result.status == Status.WARNING

    @patch("nagios_plugins.check_website_status.HAS_HTTPX", True)
    def test_check_timing_critical(self, plugin, mock_response):
        """Test check returns CRITICAL when response time exceeds critical threshold."""
        with patch.object(plugin, "_make_request", return_value=(mock_response, 6.0)):
            args = MagicMock()
            args.url = "https://example.com"
            args.string = None
            args.regex = None
            args.expect = "200"
            args.insecure = False
            args.follow_redirects = False
            args.method = "GET"
            args.data = None
            args.header = None
            args.auth = None
            args.warning = "1"
            args.critical = "5"  # 5 second critical threshold
            args.content_type = None
            args.min_size = None
            args.max_size = None
            args.timeout = 30

            result = plugin.check(args)

            assert result.status == Status.CRITICAL

    @patch("nagios_plugins.check_website_status.HAS_HTTPX", True)
    def test_check_size_constraints(self, plugin, mock_response):
        """Test check validates response size constraints."""
        mock_response.content = b"X" * 100

        with patch.object(plugin, "_make_request", return_value=(mock_response, 0.5)):
            args = MagicMock()
            args.url = "https://example.com"
            args.string = None
            args.regex = None
            args.expect = "200"
            args.insecure = False
            args.follow_redirects = False
            args.method = "GET"
            args.data = None
            args.header = None
            args.auth = None
            args.warning = None
            args.critical = None
            args.content_type = None
            args.min_size = 200  # Response is only 100 bytes
            args.max_size = None
            args.timeout = 30

            result = plugin.check(args)

            assert result.status == Status.WARNING
            assert "too small" in result.message
