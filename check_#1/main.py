#!/opt/zenoss/bin/python

import os
import sys
import re
import urllib.request
import urllib.error
import time

def help():
    print("Usage:")
    print("main.py YOUR_URL")
    sys.exit(3)

#if len(sys.argv) != 2 or ("--url=" not in sys.argv[1]):
#    help()
if len(sys.argv) != 2:
    help()
else:
    url = sys.argv[1]
    #url = url[6:]
    try:
        if "http://" not in url:
            url="http://"+url
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        content = response.read()
        ####################################
        ######## Script main logic #########
        ####################################

        if ("IB_.O.K." in content or "IB_.O.K.__" in content):
            #Things going good
            lines = content.split("\n")
            dct = {}
            for each in lines:
                if ('=' in each):
                    dct[each.split("=")[0]]=each.split("=")[1]
            #print dct
            #Now we have dictionary with needed variables.
            #It looks like this:
            #{'PROCESSORs': '2',
            # 'currentTime': 'Mon Jun 18 08:09:02 PDT 2012',
            # 'MEM_FREE': '497',
            # 'worldCacheRefreshed': 'Mon Jun 18 07:59:46 PDT 2012',
            # 'DB': 'true',
            # 'MEM_MAX': '3665',
            # 'MEM_TOT': '899'}
            tm = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
            db = dct['DB']
            procs = dct['PROCESSORs']
            mem_tot = dct['MEM_TOT']
            mem_max = dct['MEM_MAX']
            mem_FREE = dct['MEM_FREE']
            wcR = dct['worldCacheRefreshed']
            print('CHECK #1 OK - Right response received at %s, DB=%s, processors=%s, wCR=%s | mem_tot=%s, mem_max=%s, mem_free=%s' % (tm, db, procs, wcR, mem_tot, mem_max, mem_FREE,))
            sys.exit(0)

        else:
            #Things going bed (very bed)
            tm = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
            print('CHECK #1 CRITICAL - Wrong response received at %s | mem_tot=0, mem_max=0, mem_free=0' % tm)
            sys.exit(2)

        ####################################
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print("CHECK #1 CRITICAL - HTTP/URL Error: "+str(e))
        sys.exit(2)

