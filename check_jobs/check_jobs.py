#!/usr/bin/env python3

from typing import Optional

import os
import sys
import re
import urllib.request
import json
import time
import datetime


def check_jobs(url: str, debug: bool = False) -> None:
    """Check the status of jobs at the given URL.

    Args:
        url: The URL of the job list.
        debug: Whether to print debug messages.
    """

    # Check the number of arguments.
    if len(sys.argv) != 2:
        print("Usage:")
        print("check_jobs.py -url=JSON_URL")
        sys.exit(3)

    # Get the URL and protocol.
    args_str = sys.argv[1]
    args_str = args_str.lower()
    if "-url=" in args_str:
        url_arg = args_str.replace("http://", "").replace("-url=", "").replace("https://", "")
        proto = "http://"
        if "http://" in sys.argv[1]:
            proto = "http://"
        else:
            if "https://" in sys.argv[1]:
                proto = "https://"
        clean_url = f"{proto}{url_arg}"
    else:
        print("UNKNOWN - Wrong arguments!")
        sys.exit(3)

    # Check the URL.
    if not clean_url.startswith(("http://", "https://")):
        print("UNKNOWN - Invalid URL:", clean_url)
        sys.exit(3)

    # Make the request.
    try:
        with urllib.request.urlopen(clean_url) as request:
            content = request.read()
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"UNKNOWN - URL/HTTP Error: {e}")
        sys.exit(3)

    # Parse the JSON response.
    json_dict = json.loads(content)

    # Check the status.
    status = json_dict["status"].lower()
    if status == "ok":
        for component in json_dict["components"]:
            component_status = component["status"].lower()
            component_message = ""
            if component["message"]:
                component_message = component["message"].replace("\n", "; ")
            else:
                component_message = " "

            if component_status != "ok":
                print(f"WARNING - Component {component['name']} has status {component_status.upper()}, message: {component_message}")
                sys.exit(1)

        print("SUCCESS - Root status is OK. All components has status OK.")
        sys.exit(0)
    else:
        print(f"WARNING - Root status {json_dict['title'].upper()} is {status.upper()}. Message: {json_dict['message'].replace('\n','; ')}")
        sys.exit(1)


if __name__ == "__main__":
    # Parse the command-line arguments.
    url = sys.argv[1]
    debug = False
    if len(sys.argv) == 3:
        if sys.argv[2] == "-debug":
            debug = True

    # Check the jobs.
    check_jobs(url, debug)
