import pytest
from component_checker import component_checker

def test_component_checker():
    # Test with a valid URL and component name
    status, result = component_checker("example.com", "component1")
    assert status == "ok"
    assert isinstance(result, datetime.timedelta)

    # Test with an invalid URL
    status, result = component_checker("invalid.com", "component1")
    assert status == "error"
    assert isinstance(result, str)

    # Test with an invalid component name
    status, result = component_checker("example.com", "invalid")
    assert status == "error"
    assert isinstance(result, str)
