#!/usr/bin/env python3

"""
MIT License

Copyright (c) 2023 Thomas Vincent

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

This script is used to query the DNS server for a given hostname.
Requires at least 3.6

Usage:

    dns_query.py [-h] [-R SSH_HOST] [-P SSH_PASSWORD] [-U SSH_USERNAME] [-s SSH_PORT]
                 [-l QUERY_ADDRESS] [-p DNS_PORT] [-T RECORD_TYPE] [-a EXPECTED_ADDRESS]
                 [-A DIG_ARGUMENTS] [-w WARNING] [-c CRITICAL]

Options:

    -h, --help            show this help message and exit
    -R SSH_HOST           The hostname or IP address of the remote host to connect to.
    -P SSH_PASSWORD       The password for the remote host.
    -U SSH_USERNAME       The username for the remote host.
    -s SSH_PORT           The port number for the remote host.
    -l QUERY_ADDRESS      The hostname or IP address to query the DNS server for.
    -p DNS_PORT           The port number for the DNS server.
    -T RECORD_TYPE        The type of record to query the DNS server for.
    -a EXPECTED_ADDRESS   The expected address in the answer section of the DNS response.
    -A DIG_ARGUMENTS      Additional arguments to pass to the `dig` command.
    -w WARNING            The warning threshold in seconds.
    -c CRITICAL           The critical threshold in seconds.
"""

import argparse
import os
import subprocess
import sys


class SSHConnection:
    """Class for establishing an SSH connection"""

    def __init__(self, host: str, username: str, password: str, port: int):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ssh_process = None

    def connect(self):
        """Connect to the remote host via SSH"""
        ssh_command = [
            "ssh",
            "-p",
            str(self.port),
            f"{self.username}@{self.host}",
            "echo Connected"
        ]

        try:
            self.ssh_process = subprocess.Popen(ssh_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE, universal_newlines=True)
            _, stderr = self.ssh_process.communicate(input=self.password)

            if self.ssh_process.returncode != 0:
                raise ConnectionError(f"Failed to connect to the remote host via SSH: {stderr.strip()}")

        except subprocess.SubprocessError as e:
            raise ConnectionError(f"Failed to connect to the remote host via SSH: {str(e)}")

        finally:
            if self.ssh_process:
                self.ssh_process.stdin.close()
                self.ssh_process.stdout.close()
                self.ssh_process.stderr.close()


class DNSQuery:
    """Class for querying DNS server for a given hostname"""

    def __init__(self, ssh_connection: SSHConnection, query_address: str, dns_port: int,
                 record_type: str, expected_address: str, dig_arguments: str,
                 warning: float, critical: float):
        self.ssh_connection = ssh_connection
        self.query_address = query_address
        self.dns_port = dns_port
        self.record_type = record_type
        self.expected_address = expected_address
        self.dig_arguments = dig_arguments
        self.warning = warning
        self.critical = critical

    def run(self):
        """Run the DNS query and process the result"""
        try:
            self.ssh_connection.connect()
            dns_response = self.query_dns_server()
            result = self.process_dns_response(dns_response)
            self.handle_result(result)

        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(2)

    def query_dns_server(self) -> str:
        """Query the DNS server for the given hostname"""
        dig_command = [
            "dig",
            "-p",
            str(self.dns_port),
            "-t",
            self.record_type,
            "+short",
            self.query_address
        ]

        try:
            dig_process = subprocess.Popen(dig_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           universal_newlines=True)
            output, error = dig_process.communicate()

            if dig_process.returncode != 0:
                raise RuntimeError(f"Failed to query the DNS server: {error.strip()}")

            return output.strip()

        except subprocess.SubprocessError as e:
            raise RuntimeError(f"Failed to query the DNS server: {str(e)}")

    def process_dns_response(self, dns_response: str) -> str:
        """Process the DNS response"""
        if self.expected_address and self.expected_address not in dns_response:
            return f"CRITICAL: Unexpected address in the DNS response. Expected: {self.expected_address}, " \
                   f"Response: {dns_response}"

        return f"OK: DNS response received. Response: {dns_response}"

    def handle_result(self, result: str):
        """Handle the result based on the warning and critical thresholds"""
        if self.critical and result.startswith("CRITICAL"):
            print(result)
            sys.exit(2)

        if self.warning and result.startswith("OK"):
            print(result)
            sys.exit(1)

        print(result)
        sys.exit(0)


def parse_args() -> argparse.Namespace:
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(description="Query the DNS server for a given hostname.")
    parser.add_argument("-R", "--ssh_host", type=str, required=True,
                        help="The hostname or IP address of the remote host to connect to.")
    parser.add_argument("-P", "--ssh_password", type=str, required=False,
                        help="The password for the remote host.")
    parser.add_argument("-U", "--ssh_username", type=str, required=False,
                        help="The username for the remote host.")
    parser.add_argument("-s", "--ssh_port", type=int, required=False, default=22,
                        help="The port number for the remote host.")
    parser.add_argument("-l", "--query_address", type=str, required=True,
                        help="The hostname or IP address to query the DNS server for.")
    parser.add_argument("-p", "--dns_port", type=int, required=False, default=53,
                        help="The port number for the DNS server.")
    parser.add_argument("-T", "--record_type", type=str, required=False, default="A",
                        help="The type of record to query the DNS server for.")
    parser.add_argument("-a", "--expected_address", type=str, required=False,
                        help="The expected address in the answer section of the DNS response.")
    parser.add_argument("-A", "--dig_arguments", type=str, required=False,
                        help="Additional arguments to pass to the `dig` command.")
    parser.add_argument("-w", "--warning", type=float, required=False, default=0,
                        help="The warning threshold in seconds.")
    parser.add_argument("-c", "--critical", type=float, required=False,
                        help="The critical threshold in seconds.")
    return parser.parse_args()


def main() -> None:
    """Main function of the script"""
    args = parse_args()

    ssh_connection = SSHConnection(
        host=args.ssh_host,
        username=args.ssh_username,
        password=args.ssh_password,
        port=args.ssh_port
    )

    dns_query = DNSQuery(
        ssh_connection=ssh_connection,
        query_address=args.query_address,
        dns_port=args.dns_port,
        record_type=args.record_type,
        expected_address=args.expected_address,
        dig_arguments=args.dig_arguments,
        warning=args.warning,
        critical=args.critical
    )

    dns_query.run()


if __name__ == '__main__':
    main()
