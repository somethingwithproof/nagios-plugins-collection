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

   usage: check_dig [-h] [-v] [-t TIMEOUT] [-w WARNING] [-c CRITICAL] [--json]
                    --host HOST --query QUERY [--ssh-user SSH_USER]
                    [--ssh-port SSH_PORT] [--dns-port DNS_PORT]
                    [--record-type RECORD_TYPE] [--dig-arguments DIG_ARGUMENTS]
                    [--expected EXPECTED] [--retries RETRIES]

   Check DNS via SSH using dig.

   -w/-c are Nagios ranges for the query time in seconds.

   options:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity (can be used multiple times)
     -t TIMEOUT, --timeout TIMEOUT
                           Timeout in seconds for the whole run (default: 30);
                           the plugin exits UNKNOWN 1 second after it
     -w WARNING, --warning WARNING
                           Warning threshold (plugin-specific)
     -c CRITICAL, --critical CRITICAL
                           Critical threshold (plugin-specific)
     --json                Output results in JSON format
     --host HOST           SSH host to connect to
     --query QUERY         DNS name to query
     --ssh-user SSH_USER   SSH username
     --ssh-port SSH_PORT   SSH port (default: 22)
     --dns-port DNS_PORT   DNS port (default: 53)
     --record-type RECORD_TYPE
                           DNS record type (A, AAAA, MX, etc.; default: A)
     --dig-arguments DIG_ARGUMENTS
                           Additional dig command arguments
     --expected EXPECTED   Expected result from the DNS query
     --retries RETRIES     Number of attempts (default: 1)
