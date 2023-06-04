import httpx
import logging
import re
import sys

logger = logging.getLogger(__name__)


def help():
    """Prints the usage of the script."""
    print(f"Usage: {sys.argv[0]} URL")
    print(f"Checks the status of a website or server at the specified URL.")
    print(f"Exits with status code 0 if the response is successful, or 2 if there is an error.")
    sys.exit(2)


def check_status(url: str) -> int:
    """Checks the status of a website by sending a request to a specified URL and checking the response for certain strings.

    Args:
        url: The URL to check the status of.

    Returns:
        0 if the response is successful, 2 if there is an error.
    """
    # Check the number of arguments.
    if len(sys.argv) != 2:
        help()

    # Check the URL.
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        # Make the request.
        with httpx.Client(timeout=3) as client:
            response = client.get(url)
            response.raise_for_status()  # Raises an exception if the response has an HTTP error status code

            # Check the response.
            match = re.search(r"(IB_\.O\.K\.|IB_\.O\.K\.__)", response.text)

            if match:
                logger.info("CHECK #1 OK - Right response received")
                return 0
            else:
                logger.error("CHECK #1 CRITICAL - Wrong response received")
                return 2
    except httpx.HTTPError as e:
        logger.error("CHECK #1 CRITICAL - HTTP Error: %s", e)
        return 2
    except httpx.ReadTimeout as e:
        logger.error("CHECK #1 CRITICAL - Timeout Error: %s", e)
        return 2
    except httpx.RequestError as e:
        logger.error("CHECK #1 CRITICAL - Request Error: %s", e)
        return 2


if __name__ == "__main__":
    if len(sys.argv) < 2:
        help()

    url = sys.argv[1]
    sys.exit(check_status(url))
