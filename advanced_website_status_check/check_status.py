import httpx
import logging
import re
import sys

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def help():
    """Prints the usage of the script and exits."""
    print("Usage:")
    print(f"  {sys.argv[0]} <URL>")
    print("Description:")
    print("  Checks the status of a website or server at the specified URL.")
    print("  Exits with status code 0 if the response contains the expected string,")
    print("  or 2 if there is an error or mismatch.")
    sys.exit(2)


def check_status(url: str) -> int:
    """Checks the status of a website by sending a GET request to the specified URL.

    Args:
        url: The URL to check.

    Returns:
        0 if the response contains the expected string, 2 otherwise.
    """
    # Ensure URL starts with a valid scheme.
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        # Make the HTTP request.
        with httpx.Client(timeout=3) as client:
            response = client.get(url)
            response.raise_for_status()  # Raise an error for HTTP status codes >= 400

            # Check the response content.
            if re.search(r"(IB_\.O\.K\.|IB_\.O\.K\.__)", response.text):
                logger.info("CHECK #1 OK - Correct response received from %s", url)
                return 0
            else:
                logger.error("CHECK #1 CRITICAL - Unexpected response content from %s", url)
                return 2
    except httpx.RequestError as e:
        logger.error("CHECK #1 CRITICAL - Network error while accessing %s: %s", url, e)
    except Exception as e:
        logger.error("CHECK #1 CRITICAL - Unexpected error while accessing %s: %s", url, e)

    return 2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        help()

    target_url = sys.argv[1]
    sys.exit(check_status(target_url))
