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

Example:
  dns_query.py -R example.com -l www.google.com -T A
"""

import argparse
import subprocess
import sys

class SSHConnection:
    """Establishes an SSH connection and executes commands."""

    def __init__(self, host, username, password, port):
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    def execute_command(self, command):
        """Executes a command over SSH."""
        ssh_command = [
            "ssh",
            "-p", str(self.port),
            f"{self.username}@{self.host}",
            command
        ]
        try:
            process = subprocess.run(ssh_command, input=(self.password + '\n') if self.password else None,
                                   capture_output=True, text=True, check=True)
            return process.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise ConnectionError(f"SSH command failed: {e.stderr.strip()}") from e

class DNSQuery:
    """Performs a DNS query over SSH."""

    def __init__(self, ssh_connection, query_address, dns_port=53, record_type="A", 
                 expected_address=None, dig_arguments=None, warning=0, critical=0):
        self.ssh_connection = ssh_connection
        self.query_address = query_address
        self.dns_port = dns_port
        self.record_type = record_type
        self.expected_address = expected_address
        self.dig_arguments = dig_arguments
        self.warning = warning
        self.critical = critical

    def run(self):
        """Executes the DNS query and handles the result."""
        try:
            dns_response = self.query_dns()
            result = self.process_response(dns_response)
            self.handle_result(result)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(2)

    def query_dns(self):
        """Constructs and executes the `dig` command over SSH."""
        dig_command = f"dig -p {self.dns_port} -t {self.record_type} +short {self.query_address}"
        if self.dig_arguments:
            dig_command += f" {self.dig_arguments}"
        return self.ssh_connection.execute_command(dig_command)

    def process_response(self, dns_response):
        """Checks the DNS response against the expected address."""
        if self.expected_address and self.expected_address not in dns_response:
            return f"CRITICAL: Unexpected address: Expected {self.expected_address}, got {dns_response}"
        return f"OK: Response received: {dns_response}"

    def handle_result(self, result):
        """Handles the result based on thresholds and exit codes."""
        if self.critical and result.startswith("CRITICAL"):
            print(result)
            sys.exit(2)
        if self.warning and result.startswith("OK"):
            print(result)
            sys.exit(1)
        print(result)
        sys.exit(0)

def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Query DNS over SSH.", 
                                     formatter_class=argparse.RawTextHelpFormatter)
    # ... (rest of the argument parsing code remains the same)
    return parser.parse_args()

def main():
    """Main function to run the script."""
    args = parse_args()
    ssh_connection = SSHConnection(args.ssh_host, args.ssh_username, args.ssh_password, args.ssh_port)
    dns_query = DNSQuery(ssh_connection, args.query_address, args.dns_port, args.record_type,
                         args.expected_address, args.dig_arguments, args.warning, args.critical)
    dns_query.run()

if __name__ == '__main__':
    main()
