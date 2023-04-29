#!/usr/bin/env python3

import httpx
import datetime
import sys

def fetch_url_content(url: str) -> str:
    """
    Fetch the content of the provided URL.
    :param url: The URL to fetch
    :return: The content of the URL
    """
    try:
        response = httpx.get(url)
        return response.text
    except httpx.HTTPError as e:
        print(f"CRITICAL - {e}")
        sys.exit(2)

def find_line(content: str, keyword: str) -> str:
    """
    Find the first line in the content containing the specified keyword.
    :param content: The content to search
    :param keyword: The keyword to search for
    :return: The line containing the keyword or an empty string if not found
    """
    for line in content.splitlines():
        if keyword.lower() in line.lower():
            return line
    return ""

def check_url(url: str) -> None:
    """
    Check the provided URL for certain characteristics and print the result.
    :param url: The URL to check
    """
    content = fetch_url_content(url)

    numdocs_line = find_line(content, "numdocs")
    last_modified_line = find_line(content, "lastmodified")
    time_since_last_index_line = find_line(content, "time since last index")

    if not numdocs_line:
        print("CHECK #4 CRITICAL - response does not contain numdocs variable.")
        sys.exit(2)

    if not last_modified_line or not time_since_last_index_line:
        print("CHECK #4 CRITICAL - response missing required information.")
        sys.exit(2)

    last_modified = last_modified_line.replace("lastmodified is ", "")
    last_modified_time = datetime.datetime.strptime(last_modified.replace("pdt ", ""), "%a %b %d %H:%M:%S %Y")
    current_time = datetime.datetime.utcnow()
    time_diff = current_time - last_modified_time

    num_docs = numdocs_line.replace("numdocs is ", "")

    if time_diff.days < 1:
        print(f"CHECK #4 OK - Numdocs = {num_docs}")
        sys.exit(0)
    else:
        print(f"CHECK #4 WARNING - time since last index bigger than one day. Numdocs = {num_docs}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: zenoss_check4.py YOUR_URL")
        sys.exit(3)
    check_url(sys.argv[1])
