# Zenoss Check 4

This script checks a provided URL for certain characteristics and prints the result. I don't even remember the purpose, so updating it was more of a coding exercise. 

## Usage

`zenoss_check4.py YOUR_URL`

## Description

The script sends a request to the provided URL using the httpx library and checks the response for certain strings. If the response contains the strings "numdocs", "lastmodified", and "time since last index", the script proceeds to check the time since the last index and the number of documents. If the time since the last index is less than one day, the script prints "CHECK #4 OK - Numdocs = [number of docs]". If the time since the last index is greater than one day, the script prints "CHECK #4 WARNING - time since last index bigger than one day. Numdocs = [number of docs]". If the response does not contain one of the required strings, the script prints "CHECK #4 CRITICAL - response does not contain [missing string]". If there is an error in sending the request, the script prints "CRITICAL - [error message]".

The script uses the datetime library to handle the time calculations and the httpx library to send the request.

### Exit Codes

0: CHECK #4 OK
1: CHECK #4 WARNING
2: CHECK #4 CRITICAL
3: Invalid usage
