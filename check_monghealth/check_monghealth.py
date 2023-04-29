#!/usr/bin/env python3

import os
import sys
import re
import urllib.request
import json

def check_engine_status(url, timeout=1):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            content = response.read()
            json_data = json.load(content, object_pairs_hook=dict)
            return json_data["alive"]
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        return False


def main():
    url = sys.argv[1]
    mode = int(sys.argv[2])

    if len(sys.argv) != 3:
        help()

    checks = {
        1: [("mongrations_current", True), ("search_reachable", True)],
        2: [("search_reachable", True), ("site_api_reachable", True)],
        3: [("mongrations_current", True), ("search_reachable", True)],
    }

    status = check_engine_status(url)
    if status:
        for check in checks[mode]:
            if check[0] not in json_data:
                print("CRITICAL - " + check[1])
                sys.exit(2)
        print("OK - ", json.dumps(json_data))
        sys.exit(0)
    else:
        print("CRITICAL - Engine is not alive!")
        sys.exit(2)


if __name__ == "__main__":
    main()
