#!/usr/bin/env python3

"""
MIT License

Copyright (c) 2023-2025 Thomas Vincent

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

This script performs DNS queries via SSH.

It connects to a remote SSH host, executes a DNS query using the `dig` command,
and returns the results. It includes robust retry mechanisms, timeout handling,
and allows specification of warning and critical thresholds for monitoring.

Usage:
  dns_query.py -R <SSH_HOST> -l <QUERY_ADDRESS> [-P <SSH_PASSWORD>] 
               [-U <SSH_USERNAME>] [-s <SSH_PORT>] [-p <DNS_PORT>] 
               [-T <RECORD_TYPE>] [-a <EXPECTED_ADDRESS>] 
               [-A <DIG_ARGUMENTS>] [-w <WARNING>] [-c <CRITICAL>] 
               [-t <TIMEOUT>] [-r <RETRIES>]

Example:
  dns_query.py -R example.com -l www.google.com -T A
"""

import argparse
import subprocess
import sys
import time

# SSHConnection class handles the execution of SSH commands on remote hosts.
class SSHConnection:
    def __init__(self, hostname, username=None, password=None, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

    def execute_command(self, command, timeout):
        """Executes a command on the remote SSH host with a specified timeout."""
        ssh_cmd = ["ssh", "-p", str(self.port)]
        if self.username:
            ssh_cmd.extend(["-l", self.username])
        ssh_cmd.append(self.hostname)
        ssh_cmd.append(command)

        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode, ssh_cmd, result.stdout, result.stderr)

        return result.stdout.strip()

# DNSQuery class performs DNS queries via SSH, manages retries, and checks thresholds.
class DNSQuery:
    def __init__(self, ssh_connection, query_address, dns_port=53, record_type='A',
                 dig_arguments=None, expected_address=None, timeout=10, retries=1,
                 warning=None, critical=None):
        self.ssh_connection = ssh_connection
        self.query_address = query_address
        self.dns_port = dns_port
        self.record_type = record_type
        self.dig_arguments = dig_arguments
        self.expected_address = expected_address
        self.timeout = timeout
        self.retries = retries
        self.warning = warning
        self.critical = critical

    def run(self):
        """Runs DNS query with retries and handles response checking."""
        attempt = 0
        while attempt < self.retries:
            try:
                start_time = time.time()
                response = self.query_dns()
                duration = time.time() - start_time
                self.handle_result(response, duration)
                return
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                attempt += 1
                if attempt < self.retries:
                    print(f"Retrying in {self.timeout} seconds...")
                    time.sleep(self.timeout)
                else:
                    sys.exit(2)

    def query_dns(self):
        """Executes the DNS query via SSH using `dig`."""
        dig_cmd = f"dig -p {self.dns_port} -t {self.record_type} +short {self.query_address}"
        if self.dig_arguments:
            dig_cmd += f" {self.dig_arguments}"
        return self.ssh_connection.execute_command(dig_cmd, timeout=self.timeout)

    def handle_result(self, response, duration):
        """Evaluates DNS query response against expected results and timing thresholds."""
        if self.expected_address and self.expected_address not in response:
            print(f"CRITICAL: Expected address '{self.expected_address}' not found. Response: {response}")
            sys.exit(2)

        if self.critical and duration > self.critical:
            print(f"CRITICAL: Query took {duration:.2f}s")
            sys.exit(2)
        elif self.warning and duration > self.warning:
            print(f"WARNING: Query took {duration:.2f}s")
            sys.exit(1)

        print(f"OK: DNS response '{response}' received in {duration:.2f}s")
        sys.exit(0)

# parse_args function parses command-line arguments for the script.
def parse_args():
    parser = argparse.ArgumentParser(description="DNS query via SSH")

    parser.add_argument("-R", required=True, help="SSH hostname or IP")
    parser.add_argument("-l", required=True, help="DNS query hostname or IP")
    parser.add_argument("-U", help="SSH username")
    parser.add_argument("-P", help="SSH password")
    parser.add_argument("-s", type=int, default=22, help="SSH port (default: 22)")
    parser.add_argument("-p", type=int, default=53, help="DNS port (default: 53)")
    parser.add_argument("-T", default="A", help="DNS record type (default: A)")
    parser.add_argument("-A", help="Additional dig arguments")
    parser.add_argument("-a", help="Expected DNS response")
    parser.add_argument("-w", type=float, help="Warning threshold in seconds")
    parser.add_argument("-c", type=float, help="Critical threshold in seconds")
    parser.add_argument("-t", type=int, default=10, help="Timeout in seconds (default: 10)")
    parser.add_argument("-r", type=int, default=1, help="Number of retries (default: 1)")

    return parser.parse_args()

# main function sets up and executes the DNS query.
def main():
    args = parse_args()

    ssh_conn = SSHConnection(args.R, args.U, args.P, args.s)
    dns_query = DNSQuery(
        ssh_conn,
        args.l,
        dns_port=args.p,
        record_type=args.T,
        dig_arguments=args.A,
        expected_address=args.a,
        timeout=args.t,
        retries=args.r,
        warning=args.w,
        critical=args.c
    )

    dns_query.run()

if __name__ == "__main__":
    main()
