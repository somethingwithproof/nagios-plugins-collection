#!/usr/bin/env python3

"""
MIT License

Copyright (c) 2023-2024 Thomas Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


This script queries a DNS server for a given hostname over SSH.

It connects to a remote host via SSH and executes the `dig` command to 
perform the DNS query. The script supports various options for customizing 
the query, including specifying the record type, DNS server port, and 
expected address. It also provides warning and critical thresholds for 
monitoring purposes.

Usage:
  dns_query.py -R <SSH_HOST> -l <QUERY_ADDRESS> [-P <SSH_PASSWORD>] 
                [-U <SSH_USERNAME>] [-s <SSH_PORT>] [-p <DNS_PORT>] 
                [-T <RECORD_TYPE>] [-a <EXPECTED_ADDRESS>] 
                [-A <DIG_ARGUMENTS>] [-w <WARNING>] [-c <CRITICAL>] 
                [-t <TIMEOUT>] [-r <RETRIES>]

Options:
  -R <SSH_HOST>           The hostname or IP address of the remote host.
  -l <QUERY_ADDRESS>      The hostname or IP address to query.
  -P <SSH_PASSWORD>       The password for the remote host (optional).
  -U <SSH_USERNAME>       The username for the remote host (optional).
  -s <SSH_PORT>           The SSH port for the remote host (default: 22).
  -p <DNS_PORT>           The port number for the DNS server (default: 53).
  -T <RECORD_TYPE>        The type of DNS record (default: A).
  -a <EXPECTED_ADDRESS>  The expected address in the response (optional).
  -A <DIG_ARGUMENTS>      Additional arguments for the `dig` command (optional).
  -w <WARNING>            Warning threshold in seconds (optional).
  -c <CRITICAL>           Critical threshold in seconds (optional).
  -t <TIMEOUT>            Timeout for the `dig` command in seconds (default: 10).
  -r <RETRIES>            Number of retries for the `dig` command (default: 1).

Example:
  dns_query.py -R example.com -l www.google.com -T A
"""

import argparse
import subprocess
import sys
import time

# ... (SSHConnection class remains the same)

class DNSQuery:
    # ... (constructor remains the same) 

    def run(self):
        """Executes the DNS query with retries and handles the result."""
        retries = self.retries
        while retries > 0:
            try:
                dns_response = self.query_dns()
                result = self.process_response(dns_response)
                self.handle_result(result)  # Exit on success
            except Exception as e:
                print(f"Error: {e}")
                retries -= 1
                if retries > 0:
                    print(f"Retrying in {self.timeout} seconds...")
                    time.sleep(self.timeout)
                else:
                    sys.exit(2)  # Exit with error after all retries fail

    def query_dns(self):
        """Constructs and executes the `dig` command over SSH with a timeout."""
        dig_command = f"dig -p {self.dns_port} -t {self.record_type} +short {self.query_address}"
        if self.dig_arguments:
            dig_command += f" {self.dig_arguments}"
        try:
            return self.ssh_connection.execute_command(dig_command)
        except subprocess.TimeoutExpired as e:
            raise TimeoutError(f"dig command timed out: {e}") from e

    # ... (process_response and handle_result methods remain the same)

def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Query DNS over SSH.", 
                                     formatter_class=argparse.RawTextHelpFormatter)
    # ... (other argument parsing code remains the same)
    parser.add_argument("-t", "--timeout", type=int, required=False, default=10,
                        help="Timeout for the `dig` command in seconds (default: 10)")
    parser.add_argument("-r", "--retries", type=int, required=False, default=1,
                        help="Number of retries for the `dig` command (default: 1)")
    return parser.parse_args()

# ... (main function remains the same)
