import pytest

from check_status import check_status


@pytest.mark.parametrize("url, expected_status_code, test_description", [
    (
            "https://www.google.com",
            200,
            "A successful request.",
    ),
    (
            "https://www.google.com.invalid",
            404,
            "A request to a non-existent URL.",
    ),
    (
            "https://www.google.com/does-not-exist",
            404,
            "A request to a path that does not exist.",
    ),
    (
            "https://www.google.com/?timeout=1",
            408,
            "A request that times out after 1 second.",
    ),
    (
            "https://www.google.com/?timeout=2",
            408,
            "A request that times out after 2 seconds.",
    ),
])
def test_check_status(url, expected_status_code, test_description):
    # Arrange
    response = check_status(url)
    actual_status_code = response.status_code

    # Assert
    assert actual_status_code == expected_status_code, test_description


if __name__ == "__main__":
    pytest.main()
