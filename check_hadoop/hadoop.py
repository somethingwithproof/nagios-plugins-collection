import os
import re
import sys
import time
import datetime
import json
import httpx

def help():
    """Print usage information and exit with status code 3."""
    print("Usage:")
    print("hadoop.py -url=SOURCE_JSON_URL -t MAX_TIME_SINCE_LAST_UPDATE_IN_MINUTES (optional)")
    sys.exit(3)

def main():
    """Check the status of a Hadoop cluster and its components.

    The Hadoop cluster and its components are checked by querying a JSON API specified
    with the -url command line argument. The status of each component is checked, and if
    any component has a status other than "ok", the script will exit with a warning status.
    If the -t command line argument is provided, the time since the last update of each
    component is checked. If the time since the last update exceeds the value specified
    with the -t argument, the script will exit with a warning status. If all components
    have an "ok" status and (if the -t argument is provided) the time since the last
    update is within the acceptable range, the script will print the memory usage and exit
    with an "ok" status.
    """
    if len(sys.argv) < 2:
        help()

    url_str = None
    time_str = None
    for arg in sys.argv[1:]:
        if arg.startswith("-url="):
            url_str = arg.replace("-url=", "")
        elif arg.startswith("-t"):
            time_str = arg.replace("-t", "")

    if url_str is None:
        help()

    if not url_str.startswith(("http://", "https://")):
        url_str = "http://" + url_str

    try:
        response = httpx.get(url_str)
        response.raise_for_status()
        jsondict = response.json()
    except (httpx.HTTPError, ValueError):
        print("CRITICAL - Could not retrieve JSON data from specified URL")
        sys.exit(2)

    if jsondict["status"].lower() != "ok":
        print(f'WARNING - Hadoop: {jsondict["status"]}')
        sys.exit(1)

    subcomponents_lst = jsondict["subcomponents"]
    for component in subcomponents_lst:
        if component["status"].lower() != "ok":
            print(f'WARNING - component "{component["name"]}" has status "{component["status"]}" and message: {component["message"]}')
            sys.exit(2)

        if time_str is not None:
            time_from_json = time.strptime(component["updated"], "%Y-%m-%d %H:%M:%S")
            time_from_json = datetime.datetime(*time_from_json[:6])
            time_now = datetime.datetime.now()
            time_delta = time_now - time_from_json
            if time_delta.days > 0 or (time_delta.seconds // 60) >
            if time_delta.days > 0 or (time_delta.seconds // 60) > int(time_str):
                print(f'WARNING - component "{component["name"]}" has not been updated in {time_delta}')
                sys.exit(1)

    print(f'OK - All components have status "ok" and (if specified) have been updated within {time_str} minutes')
    sys.exit(0)

if __name__ == '__main__':
    main()
