#!/usr/bin/env python3

import sys
import re
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

class ServiceChecker:
    # Define constants
    PHP = 'PHP'
    MYSQL = 'MySQL'
    MEMCACHE = 'MemCache'
    CDN = 'CDN'
    URL_PREFIX = 'http://'
    FAILED_STATUS_MSG = '{} service down'

    def __init__(self, url):
        self.url = url

    def run(self):
        content = self.get_content()
        services_status = self.get_services_status(content)
        ip = self.get_ip_address(content)

        # If all services are up, print "OK" and exit with code 0
        if all(services_status.values()):
            print(f"OK - {', '.join(services_status.keys())} services are up at server {ip}")
            sys.exit(0)

        # If some services are down, print a warning and exit with code 1
        failed_services = [s for s, status in services_status.items() if not status]
        if failed_services:
            failed_services_str = ', '.join(self.FAILED_STATUS_MSG.format(s) for s in failed_services)
            print(f"WARNING - {failed_services_str} at server {ip}")
            sys.exit(1)

        # If all services are down, print a critical message and exit with code 2
        print(f"CRITICAL - Server failure at address {ip}")
        sys.exit(2)

    def get_content(self):
        try:
            response = urlopen(self.url)
            content = response.read().decode().lower()
            return content
        except (HTTPError, URLError) as e:
            print(f"CRITICAL - {e}")
            sys.exit(2)

    def get_services_status(self, content):
        services = {
            self.PHP: 'php up' in content,
            self.MYSQL: 'mysql up' in content,
            self.MEMCACHE: 'memcache up' in content,
            self.CDN: 'cdn up' in content
        }
        return services

    def get_ip_address(self, content):
        match = re.search(r'[0-9]+(?:\.[0-9]+){3}', content)
        if match:
            return match.group(0)
        return 'unknown'

def help():
    # Help function to display usage
    print("Usage:")
    print(f"{sys.argv[0]} YOUR_URL")
    sys.exit(3)

# Check if the correct number of arguments is passed, else display usage and exit
if len(sys.argv) != 2:
    help()

url = sys.argv[1]

# Prepend "http://" to the URL if it's not already present
if not url.startswith(ServiceChecker.URL_PREFIX):
    url = ServiceChecker.URL_PREFIX + url

checker = ServiceChecker(url)
checker.run()
