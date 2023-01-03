# Website Status Checker

This script checks the status of a website by sending a request to a specified URL and checking the response for certain strings.

## Usage


## Exit Codes

- 0: The response was "OK".
- 2: The response was "CRITICAL" or there was an error sending the request or receiving the response.

## Requirements

- Python 3

## Changes Made

The following changes were made to the original code to update it for Python 3:

1. `urllib2` was replaced with `urllib.request` and `urllib.error`.
2. `print` statements were changed to use parentheses.
3. `HTTPError` and `URLError` are now accessed using `urllib.error` instead of just `urllib2`.
4. In the `except` clause, the exception is now assigned to the variable `e` using the `as` keyword.
5. The `except` clause now uses the `as` keyword to assign the exception to the variable `e`.
6. A `,` was added at the end of the `print` statement in line 44.
