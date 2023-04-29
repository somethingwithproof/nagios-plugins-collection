import pytest
from unittest.mock import patch
import argparse
import json
import urllib.request
import urllib.error
import datetime
from component_checker import main, parse_args, component_checker


@pytest.mark.parametrize("status, expected_result, expected_log_message", [
    ("ok", 0, "OK - Component component1 has been updated within the last 30 minutes"),
    ("warning", 1, "WARNING - Component component1 has not been updated in more than 30 minutes"),
    ("error", 2, "CRITICAL - Component component1 is in error state"),
])
def test_main(status, expected_result, expected_log_message):
    with patch("component_checker.component_checker") as mocked_component_checker:
        mocked_component_checker.return_value = (status, datetime.timedelta(minutes=10))
        args = parse_args(["-url=example.com", "-component=component1", "-t=30"])
        result = main(args)
        assert result == expected_result
        assert mocked_component_checker.called
        assert mocked_component_checker.call_args == (args.url, args.component)
        assert main.logger.info.call_args == (expected_log_message,)


if __name__ == "__main__":
    pytest.main()
