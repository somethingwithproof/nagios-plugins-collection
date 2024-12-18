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


def check_status(url: str) ->
