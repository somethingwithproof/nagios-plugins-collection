# Website/Server Status Checker

This script checks the status of a website or server at a specified URL. It sends an HTTP request to the URL and checks the content of the response for certain strings. If the strings are found, the script exits with a status code of 0, indicating success. If the strings are not found, the script exits with a status code of 2, indicating a critical error. If there is an HTTP or URL error when sending the request, the script exits with a status code of 2.

## Usage
$. website_status_check.py URL

## Requirements

- Python 3
- urllib library

## Example

$ ./main.py http://example.com
CHECK #1 OK - Right response received at Mon, 03 Jan 2023 10:47:35 +0000, DB=true, processors=2, wCR=Mon Jun 18 07:59:46 PDT 2012 | mem_tot=899, mem_max=3665, mem_free=497


## Exit Codes

- 0: Success
- 2: Critical error

## Note

The script assumes that the content of the response from the server will be in a specific format. Modify the script as needed if the content has a different format.
