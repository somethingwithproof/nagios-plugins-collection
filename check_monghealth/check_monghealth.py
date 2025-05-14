#!/usr/bin/env python3

import os
import sys
import re
import urllib.request
import urllib.parse
import json

def check_engine_status(url, timeout=5):
    """Check the status of the MongoDB engine.
    
    Args:
        url: The URL to check
        timeout: Timeout in seconds (default: 5)
        
    Returns:
        A tuple of (is_alive, json_data) where is_alive is a boolean and json_data is the parsed JSON response
    """
    # Validate URL scheme for security
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    # Parse the URL to ensure it's valid
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme not in ('http', 'https'):
        print(f"Error: Invalid URL scheme: {url}")
        return False, None
        
    try:
        # Create a proper Request object for better security
        request = urllib.request.Request(
            url,
            headers={'User-Agent': 'NagiosCheck/1.0'}
        )
        # Add explicit timeout for security
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content = response.read()
            json_data = json.loads(content)
            return json_data.get("alive", False), json_data
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError, ValueError) as e:
        print(f"Error checking MongoDB status: {e}")
        return False, None


def print_help():
    """Print help information."""
    print("Usage: check_monghealth.py URL MODE")
    print("  URL: The URL to check")
    print("  MODE: Check mode (1, 2, or 3)")
    sys.exit(3)

def main():
    # Validate command-line arguments
    if len(sys.argv) != 3:
        print_help()
    
    url = sys.argv[1]
    try:
        mode = int(sys.argv[2])
        if mode not in (1, 2, 3):
            raise ValueError("Invalid mode")
    except ValueError:
        print("UNKNOWN - Mode must be 1, 2, or 3")
        sys.exit(3)

    # Different check configurations based on mode
    checks = {
        1: [("mongrations_current", True), ("search_reachable", True)],
        2: [("search_reachable", True), ("site_api_reachable", True)],
        3: [("mongrations_current", True), ("search_reachable", True)],
    }

    # Check MongoDB status with timeout
    is_alive, json_data = check_engine_status(url, timeout=10)
    
    if is_alive:
        if json_data:
            # Verify all required checks based on mode
            for check_name, _ in checks[mode]:
                if check_name not in json_data:
                    print(f"CRITICAL - Required check '{check_name}' missing from response")
                    sys.exit(2)
            
            # All checks passed
            print("OK - ", json.dumps(json_data))
            sys.exit(0)
        else:
            print("CRITICAL - Invalid response format")
            sys.exit(2)
    else:
        print("CRITICAL - Engine is not alive!")
        sys.exit(2)


if __name__ == "__main__":
    main()
