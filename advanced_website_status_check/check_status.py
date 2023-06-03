import httpx
import logging
import re
import sys

logger = logging.getLogger(__name__)

def help():
    """
    Prints the usage of the script.
    """
    print(f"Usage: {sys.argv[0]} URL")
    print(f"Checks the status of a website or server at the specified URL.")
    print(f"Exits with status code 0 if the response is successful, or 2 if there is an error.")
    sys.exit(2)

def check_status(url: str) -> int:
    """
    Checks the status of a website by sending a request to a specified URL and checking the response for certain strings.
    :param url: The URL to check the status of.
    :return: 0 if the response is successful, 2 if there is an error.
    """

    # Check the number of arguments.
    if len(sys.argv) != 2:
        help()

    # Check the URL.
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    # Make the request.
    with httpx.Client(timeout=3) as client:
        response = client.get(url)
        if response.status_code != 200:
            raise httpx.HTTPError(response)

        # Parse the response.
        content = response.text
        match = re.search(r"(IB_\.O\.K\.|IB_\.O\.K\.__)", content)

        # Check the response.
        if match:
            logger.info("CHECK #1 OK - Right response received")
            return 0
        else:
            logger.error("CHECK #1 CRITICAL - Wrong response received")
            return 2

    # Handle errors.
    except httpx.HTTPError as e:
        logger.error("CHECK #1 CRITICAL - HTTP Error: %s", e)
        return 2
    except httpx.ReadTimeout as e:
        logger.error("CHECK #1 CRITICAL - Timeout Error: %s", e)
        return 2

if __name__ == "__main__":
    url = sys.argv[1]
    sys.exit(check_status(url))
