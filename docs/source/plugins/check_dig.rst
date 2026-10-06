.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_dig
=========

Run ``check_dig --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_dig
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_dig [-h] --host HOST --query QUERY [--ssh-user SSH_USER]
                    [--ssh-port SSH_PORT] [--dns-port DNS_PORT]
                    [--record-type RECORD_TYPE] [--dig-arguments DIG_ARGUMENTS]
                    [--expected EXPECTED] [--warning WARNING]
                    [--critical CRITICAL] [--timeout TIMEOUT] [--retries RETRIES]
                    [--json] [--verbose]

   Check DNS via SSH using dig

   options:
     -h, --help            show this help message and exit
     --host HOST           SSH host to connect to (default: None)
     --query QUERY         DNS name to query (default: None)
     --ssh-user SSH_USER   SSH username (default: None)
     --ssh-port SSH_PORT   SSH port (default: 22)
     --dns-port DNS_PORT   DNS port (default: 53)
     --record-type RECORD_TYPE
                           DNS record type (A, AAAA, MX, etc.) (default: A)
     --dig-arguments DIG_ARGUMENTS
                           Additional dig command arguments (default: None)
     --expected EXPECTED   Expected result from the DNS query (default: None)
     --warning WARNING     Warning threshold in seconds (default: None)
     --critical CRITICAL   Critical threshold in seconds (default: None)
     --timeout TIMEOUT     Command timeout in seconds (default: 30)
     --retries RETRIES     Number of retries on failure (default: 1)
     --json                Output in JSON format (default: False)
     --verbose             Increase verbosity (can be used multiple times)
                           (default: 0)
