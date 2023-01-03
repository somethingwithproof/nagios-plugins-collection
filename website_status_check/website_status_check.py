#!/opt/zenoss/bin/python

import os
import sys
import re
import urllib.request
import urllib.error
import time

def help():
    print("Usage: main.py URL")
    print("Checks the status of a website or server at the specified URL.")
    print("Exits with status code 0 if the response is successful, or 2 if there is an error.")
    raise SystemExit("Script terminated intentionally by user.")

def check_status(url):
    try:
        if "http://" not in url:
            url="http://"+url
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        content = response.read()

        if ("IB_.O.K." in content or "IB_.O.K.__" in content):
            tm = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
            lines = content.split("\n")
            dct = {}
            for each in lines:
                if ('=' in each):
                    dct[each.split("=")[0]]=each.split("=")[1]
            db = dct['DB']
            procs = dct['PROCESSORs']
            mem_tot = dct['MEM_TOT']
            mem_max = dct['MEM_MAX']
            mem_FREE = dct['MEM_FREE']
            wcR = dct['worldCacheRefreshed']
            print('CHECK #1 OK - Right response received at %s, DB=%s, processors=%s, wCR=%s | mem_tot=%s, mem_max=%s, mem_free=%s' % (tm, db, procs, wcR, mem_tot, mem_max, mem_FREE,))
            return 0

        else:
            tm = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
            print('CHECK #1 CRITICAL - Wrong response received at %s | mem_tot=0, mem_max=0, mem_free=0' % tm)
            return 2

    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print("CHECK #1 CRITICAL - HTTP/URL Error: "+str(e))
        return 2

if len(sys.argv) != 2:
    help()
else:
    url = sys.argv[1]
    sys.exit(check_status(url))
