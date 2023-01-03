import pytest

def test_success():
    # Test a successful response
    url = "http://example.com"
    status_code = check_status(url)
    assert status_code == 0

def test_error():
    # Test an HTTP error
    url = "http://nonexistent.example.com"
    status_code = check_status(url)
    assert status_code == 2

def test_invalid_url():
    # Test an invalid URL
    url = "invalid:url"
    status_code = check_status(url)
    assert status_code == 2
