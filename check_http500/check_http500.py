#!/usr/bin/env python3.6
import os
import sys
import re
import urllib.request
import json
import time
from datetime import datetime


def print_usage():
    """Prints the usage information."""
    print("Usage:")
    print("hadoop.py -url=SOURCE_JSON_URL -t MAX_TIME_SINCE_LAST_UPDATE_IN_MINUTES (optional)")
    sys.exit(3)


def main():
    """The main entry point of the program."""

    # Parse the command line arguments.
    args = sys.argv[1:]
    url_str = None
    time_str = None
    for arg in args:
        if arg.startswith("-url="):
            url_str = arg[5:]
        elif arg.startswith("-t"):
            time_str = arg[2:]
    if not url_str:
        print_usage()

    # Check if the URL starts with "http://".
    if not url_str.startswith("http"):
        url_str = "http://" + url_str

    # Validate URL scheme (for security)
    if not url_str.startswith(("http://", "https://")):
        print(f"UNKNOWN - Invalid URL scheme: {url_str}")
        sys.exit(3)
        
    try:
        # Make a request to the URL with timeout
        with urllib.request.urlopen(url_str, timeout=30) as request:
            content = request.read()
    except urllib.error.URLError as e:
        print(f"CRITICAL - Connection error: {e}")
        sys.exit(2)
    except TimeoutError:
        print(f"CRITICAL - Connection to {url_str} timed out")
        sys.exit(2)
        
    # Decode the JSON response safely
    try:
        jsondict = json.loads(content)
    except json.JSONDecodeError:
        print("CRITICAL - Invalid JSON response")
        sys.exit(2)

    # Check the status of the response.
    if jsondict["status"].lower() != "ok":
        print(f'WARNING - Hadoop: {jsondict["message"]}')
        sys.exit(2)

    # Iterate over the subcomponents.
    for component in jsondict["subcomponents"]:
        # Check the status of the subcomponent.
        if component["status"].lower() != "ok":
            print(f'WARNING - component "{component["name"]}" has status "{component["status"]}" and message: {component["message"]}')
            sys.exit(2)

        # Check the time since the subcomponent was last updated.
        if time_str:
            time_from_json = datetime.strptime(component["updated"], "%Y-%m-%d %H:%M:%S")
            time_now = datetime.now()
            time_delta = time_now - time_from_json
            if time_delta.days > 0 or time_delta.seconds // 60 > int(time_str):
                print(f'WARNING - Component "{component["name"]}" has time since last update which is greater than {time_str} minutes')
                sys.exit(1)

    # Get the memory component.
    mem_component = jsondict["subcomponents"][-1]

    # Check the name of the memory component.
    if mem_component["name"].lower() != "mem":
        print("CRITICAL - Source URL has wrong content")
        sys.exit(1)

    # Print the memory usage.
    print(f"OK - mem: {mem_component['message'].replace('k','')}")


if __name__ == "__main__":
    main()
