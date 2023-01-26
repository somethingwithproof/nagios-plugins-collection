#!/usr/bin/env python3

import httpx
import datetime

def check_url(url: str) -> None:
    """
    Check the provided URL for certain characteristics and print the result.
    :param url: The URL to check
    """
    # Send a request to the URL
    try:
        response = httpx.get(url)
        content = response.text
    except httpx.HTTPError as e:
        print(f"CRITICAL - {e}")
        exit(2)
    
    # Check for certain strings in the response
    if "numdocs" in content.lower():
        if "lastmodified" in content.lower():
            if "time since last index" in content.lower():
                # Get the time since last index from the lastModified line
                for line in content.splitlines():
                    if "lastmodified" in line.lower():
                        last_modified = line.replace("lastmodified is ","")
                        break
                last_modified_time = datetime.datetime.strptime(last_modified.replace("pdt ",""), "%a %b %d %H:%M:%S %Y")
                current_time = datetime.datetime.utcnow()
                time_diff = current_time - last_modified_time
                if time_diff.days < 1:
                    # Get the number of docs from the response
                    for line in content.splitlines():
                        if "numdocs" in line.lower():
                            num_docs = line.replace("numdocs is ", "")
                            break
                    print(f"CHECK #4 OK - Numdocs = {num_docs}")
                    exit(0)
                else:
                    for line in content.splitlines():
                        if "numdocs" in line.lower():
                            num_docs = line.replace("numdocs is ", "")
                            break
                    print(f"CHECK #4 WARNING - time since last index bigger than one day. Numdocs = {num_docs}")
                    exit(1)
            else:
                print("CHECK #4 CRITICAL - response does not contain time since last index line.")
                exit(2)
        else:
            print("CHECK #4 CRITICAL - response does not contain last modified time line.")
            exit(2)
    else:
        print("CHECK #4 CRITICAL - response does not contain numdocs variable.")
        exit(2)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: zenoss_check4.py YOUR_URL")
        exit(3)
    check_url(sys.argv[1])
