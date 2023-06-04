import pytest
from unittest.mock import patch
from component_status_checker import ComponentStatusChecker

@pytest.fixture
def mock_response():
    with patch("component_status_checker.requests.get") as mock_get:
        mock_response = mock_get.return_value
        yield mock_response

@pytest.fixture
def checker(mock_response):
    return ComponentStatusChecker("example.com")

def test_get_component_status_success(mock_response, checker):
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "OK", "updated": "2023-06-03T10:00:00"}

    status, updated = checker.get_component_status("componentA")

    assert status == "ok"
    assert updated == "2023-06-03T10:00:00"
    mock_response.json.assert_called_once()

def test_get_component_status_error(mock_response, checker):
    mock_response.status_code = 404

    status, updated = checker.get_component_status("componentA")

    assert status == "error"
    assert updated is None
    mock_response.json.assert_not_called()

def test_check_components(caplog, checker):
    components = ["componentA", "componentB"]
    threshold = 10

    checker.get_component_status = lambda component: ("ok", "2023-06-03T10:00:00")

    checker.check_components(components, threshold)

    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == "WARNING"
    assert caplog.records[1].levelname == "INFO"
