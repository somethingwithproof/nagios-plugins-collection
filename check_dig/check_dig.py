#!/usr/bin/env python3

"""
This script is used to query the DNS server for a given hostname.

Usage:

    dns_query.py [-h] [-R SSH_HOST] [-P SSH_PASSWORD] [-U SSH_USERNAME] [-s SSH_PORT]
                 [-l QUERY_ADDRESS] [-p DNS_PORT] [-T RECORD_TYPE] [-a EXPECTED_ADDRESS]
                 [-A DIG_ARGUMENTS] [-w WARNING] [-c CRITICAL]

Options:

    -h, --help            show this help message and exit
    -R SSH_HOST          The hostname or IP address of the remote host to connect to.
    -P SSH_PASSWORD      The password for the remote host.
    -U SSH_USERNAME      The username for the remote host.
    -s SSH_PORT          The port number for the remote host.
    -l QUERY_ADDRESS     The hostname or IP address to query the DNS server for.
    -p DNS_PORT          The port number for the DNS server.
    -T RECORD_TYPE       The type of record to query the DNS server for.
    -a EXPECTED_ADDRESS  The expected address in the answer section of the DNS response.
    -A DIG_ARGUMENTS      Additional arguments to pass to the `dig` command.
    -w WARNING          The warning threshold in seconds.
    -c CRITICAL         The critical threshold in seconds.
"""

from __future__ import annotations

import argparse
import os
import sys
import subprocess
import re

from pynag.Plugins import WARNING, CRITICAL, OK, UNKNOWN, simple as Plugin
from pexpect import ANSI, fdpexpect, FSM, pexpect, pxssh, screen


def parse_args() -> argparse.Namespace:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(description="Query the DNS server for a given hostname.")
    parser.add_argument(
        "-R",
        "--ssh_host",
        type=str,
        required=True,
        help="The hostname or IP address of the remote host to connect to.",
    )
    parser.add_argument(
        "-P",
        "--ssh_password",
        type=str,
        required=False,
        help="The password for the remote host.",
    )
    parser.add_argument(
        "-U",
        "--ssh_username",
        type=str,
        required=False,
        help="The username for the remote host.",
    )
    parser.add_argument(
        "-s",
        "--ssh_port",
        type=int,
        required=False,
        default=22,
        help="The port number for the remote host.",
    )
    parser.add_argument(
        "-l",
        "--query_address",
        type=str,
        required=True,
        help="The hostname or IP address to query the DNS server for.",
    )
    parser.add_argument(
        "-p",
        "--dns_port",
        type=int,
        required=False,
        default=53,
        help="The port number for the DNS server.",
    )
    parser.add_argument(
        "-T",
        "--record_type",
        type=str,
        required=False,
        default="A",
        help="The type of record to query the DNS server for.",
    )
    parser.add_argument(
        "-a",
        "--expected_address",
        type=str,
        required=False,
        help="The expected address in the answer section of the DNS response.",
    )
    parser.add_argument(
        "-A",
        "--dig_arguments",
        type=str,
        required=False,
        help="Additional arguments to pass to the `dig` command.",
    )
    parser.add_argument(
        "-w",
        "--warning",
        type=float,
        required=False,
        default=0,
        help="The warning threshold in seconds.",
    )
    parser.add_argument(
        "-c",
        "--critical",
        type=
