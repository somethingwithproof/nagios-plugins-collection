#!/usr/bin/env python3.5
import os
import sys
import re
import urllib.request
import json
import time
import datetime

def print_usage():
    print("Usage:")
    print("hadoop.py -url=SOURCE_JSON_URL -t MAX_TIME_SINCE_LAST_UPDATE_IN_MINUTES (optional)")
    sys.exit(3)

def main():
    if len(sys.argv) < 2:
        print_usage()

    url_str = None
    time_str = None
    for arg in sys.argv[1:]:
        if arg.startswith("-url="):
            url_str = arg[5:]
        elif arg.startswith("-t"):
            time_str = arg[2:]
    if not url_str:
        print_usage()

    if not url_str.startswith("http"):
        url_str = "http://" + url_str

    try:
        request = urllib.request.urlopen(url_str)
        content = request.read()
        jsondict = json.loads(content)
        if jsondict["status"].lower() != "ok":
            print(f'WARNING - Hadoop: {jsondict["message"]}')
            sys.exit(2)

        subcomponents_lst = jsondict["subcomponents"]
        for component in subcomponents_lst:
            if component["status"].lower() != "ok":
                print(f'WARNING - component "{component["name"]}" has status "{component["status"]}" and message: {component["message"]}')
                sys.exit(2)
            if time_str:
                time_from_json = time.strptime(component["updated"], "%Y-%m-%d %H:%M:%S")
                time_now = time.localtime()
                time_from_json = datetime.datetime(*time_from_json[:6])
                time_now = datetime.datetime(*time_now[:6])
                time_delta = time_now - time_from_json
                if time_delta.days > 0 or time_delta.seconds // 60 > int(time_str):
                    print(f'WARNING - Component "{component["name"]}" has time since last update which is greater than {time_str} minutes')
                    sys.exit(1)

        mem_component = subcomponents_lst[-1]
        if mem_component["name"].lower() != "mem":
            print("CRITICAL - Source URL has wrong content")
            sys.exit(1)
        else:
            print(f"OK - mem: {mem_component['message'].replace('k','')}")
    except Exception as e:
        print(f'CRITICAL - {str(e)}')
        sys.exit(2)

if __name__ == "__main__":
    main()
