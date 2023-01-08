#!/usr/bin/env python

import os
import sys
import re
import urllib.request
import json
import time
import datetime

DEBUG_Flag = False

def help():
    print("Usage:")
    print("check_jobs.py -url=JSON_URL")
    sys.exit(3)

if len(sys.argv) == 2:
    args_str = sys.argv[1]
    args_str = args_str.lower()
    if "-url=" in args_str:
        proto = "http://"
        if "http://" in sys.argv[1]:
            proto = "http://"
        else:
            if "https://" in sys.argv[1]:
                proto = "https://"

        url_arg = sys.argv[1].replace("http://", "").replace("-url=", "").replace("https://", "")
        clean_url = f"{proto}{url_arg}"
        if DEBUG_Flag:
            print(f"Got url proto: {proto}")
            print(f"Got clean url: {url_arg}")
            print(f"Constructed url: {clean_url}")

        try:
            request = urllib.request.urlopen(clean_url)
            content = request.read()
            if DEBUG_Flag:
                print(content)

            json_dict = json.loads(content)
            if DEBUG_Flag:
                print(repr(json_dict))
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

        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            print(f"UNKNOWN - URL/HTTP Error: {e}")
            sys.exit(3)
else:
    print("UNKNOWN - Wrong arguments!")
    sys.exit(3)
