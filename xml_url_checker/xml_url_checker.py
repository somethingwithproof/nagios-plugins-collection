import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET


class XMLError(Exception):
    """Custom exception for XML parsing errors"""


class URLConnectionError(Exception):
    """Custom exception for URL connection errors"""


def check_reserved_prefixes(url: str) -> None:
    """
    Check if the XML at the specified URL contains the "reservedPrefixes" element

    Args:
        url (str): The URL to check

    Raises:
        XMLError: If there is an error parsing the XML or if "reservedPrefixes" is not found
        URLConnectionError: If there is an error connecting to the URL
    """
    try:
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        response = urllib.request.urlopen(url)
        content = response.read()

        try:
            root = ET.fromstring(content)
        except ET.ParseError as e:
            raise XMLError(f"XML parsing error: {str(e)}")

        reserved_prefixes_flag = False

        for element in root.iter("reservedPrefixes"):
            reserved_prefixes_flag = True
            break

        if reserved_prefixes_flag:
            print("CHECK #2 OK - reservedPrefixes has been found.")
        else:
            raise XMLError("reservedPrefixes not found.")
    except urllib.error.URLError as e:
        raise URLConnectionError(f"URL connection error: {str(e)}")


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
