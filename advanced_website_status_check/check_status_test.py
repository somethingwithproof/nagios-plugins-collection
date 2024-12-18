import pytest
from check_status import check_status


@pytest.mark.parametrize("url, expected_status_code, test_description", [
    (
        "https://www.google.com",
        200,
        "A successful request to a valid URL.",
    ),
    (
        "https://nonexistent-url.com",
        404,
        "A request to a non-existent domain.",
    ),
    (
        "https://www.google.com/nonexistent-path",
        404,
        "A request to a valid domain but a non-existent path.",
    ),
])
def test_check_status(url, expected_status_code, test_description):
    """
    Test the check_status function with various URLs and expected status codes.
    """
    try:
        # Act
 
