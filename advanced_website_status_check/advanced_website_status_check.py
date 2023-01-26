#!/usr/bin/env python3

import httpx
import logging
import sys

logger = logging.getLogger(__name__)

def help():
    """
    Prints the usage of the script and raises an exception.
    """
    print("Usage: main.py URL")
    print("Checks the status of a website or server at the specified URL.")
    print("Exits with status code 0 if the response is successful, or 2 if there is an error.")
    raise SystemExit("Script terminated intentionally by user.")

def check_status(url):
    """
    Checks the status of a website by sending a request to a specified URL and checking the response for certain strings.
    :param url: The URL to check the status of.
    :return: 0 if the response is successful, 2 if there is an error.
    """
    try:
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        with httpx.Client(timeout=3) as client:
            response = client.get(url)
            response.raise_for_status()

            content = response.text

            if "IB_.O.K." in content or "IB_.O.K.__" in content:
                dct = {}
                for line in content.split("\n"):
                    if "=" in line:
                        key, value = line.split("=")
                        dct[key] = value

                logger.info("CHECK #1 OK - Right response received, DB=%s, processors=%s, wCR=%s | mem_tot=%s, mem_max=%s, mem_free=%s",
                            dct["DB"], dct["PROCESSORs"], dct["worldCacheRefreshed"], dct["MEM_TOT"], dct["MEM_MAX"], dct["MEM_FREE"])
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

if len(sys.argv) != 2:
    help()
else:
    url = sys.argv[1]
    sys.exit(check_status(url))
