import os
import re
import urllib2
import xml.parsers.expat
from xml.dom.minidom import parseString

class XMLError(Exception):
    """Custom exception for XML parsing errors"""
    pass

class URLConnectionError(Exception):
    """Custom exception for URL connection errors"""
    pass

def check_reserved_prefixes(url: str) -> None:
    """
    Check if the XML at the specified URL contains the "reservedPrefixes" element
    :param url: The URL to check
    :raises XMLError: If there is an error parsing the XML
    :raises URLConnectionError: If there is an error connecting to the URL
    """
    try:
        if "http://" not in url:
            url = "http://" + url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        content = response.read()
        xmldoc = parseString(content)
        reserved_prefixes_flag = False
        for node in xmldoc.childNodes:
            if node.nodeName.lower() == "reservedPrefixes".lower():
                reserved_prefixes_flag = True
                break
        if reserved_prefixes_flag:
            print("CHECK #2 OK - reservedPrefixes has been found.")
        else:
            raise XMLError("reservedPrefixes not found.")
    except urllib2.URLError as e:
        raise URLConnectionError(str(e))
    except xml.parsers.expat.ExpatError as e:
        raise XMLError(str(e))

def main() -> None:
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: main.py YOUR_URL")
        sys.exit(3)
    else:
        url = sys.argv[1]
        try:
            check_reserved_prefixes(url)
        except XMLError as e:
            print(f"CHECK #2 CRITICAL - XML Error: {e}")
            sys.exit(2)
        except URLConnectionError as e:
            print(f"CHECK #2 CRITICAL - URL Error: {e}")
            sys.exit(2)

if __name__ == "__main__":
    main()
