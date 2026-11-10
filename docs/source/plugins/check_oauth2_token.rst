.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_oauth2_token
==================

Run ``check_oauth2_token --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_oauth2_token
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_oauth2_token [-h] [-v] [-t TIMEOUT] [-w WARNING] [-c CRITICAL]
                             [--json] --token-url TOKEN_URL --client-id CLIENT_ID
                             [--client-secret CLIENT_SECRET | --client-secret-file PATH]
                             [--scope SCOPE] [--ca-file PATH] [--insecure]
                             [--client-cert PATH] [--client-key PATH]
                             [--retries RETRIES] [--retry-delay SECONDS]

   Obtain an OAuth2 token and report time-to-expiry; validate scopes if provided.

   -w/-c are Nagios ranges for expires_in in seconds. A short lifetime is the
   usual concern, so give a lower bound: -w 300: alerts when the token is
   issued for less than 300 seconds (a plain 300 would alert above it).

   options:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity (can be used multiple times)
     -t TIMEOUT, --timeout TIMEOUT
                           Timeout in seconds for the whole run (default: 30);
                           the plugin exits UNKNOWN 1 second after it
     -w WARNING, --warning WARNING
                           Warning threshold (Nagios range for expires_in in
                           seconds, for example 300:)
     -c CRITICAL, --critical CRITICAL
                           Critical threshold (Nagios range for expires_in in
                           seconds, for example 300:)
     --json                Output results in JSON format
     --token-url TOKEN_URL
     --client-id CLIENT_ID
     --client-secret CLIENT_SECRET
                           OAuth2 client secret (visible in the process list;
                           prefer --client-secret-file or
                           $CHECK_OAUTH2_CLIENT_SECRET)
     --client-secret-file PATH
                           Read OAuth2 client secret from PATH (or the file named
                           by $CHECK_OAUTH2_CLIENT_SECRET_FILE)
     --scope SCOPE

   TLS:
     --ca-file PATH        PEM CA bundle (default: the bundled Mozilla CA store
                           or $SSL_CERT_FILE)
     --insecure            Do not verify TLS certificates or hostnames (for
                           testing; prefer --ca-file)
     --client-cert PATH    PEM client certificate for mutual TLS
     --client-key PATH     PEM private key for --client-cert (when not in the
                           same file)

   HTTP retries:
     --retries RETRIES     Retries for transient failures within --timeout
                           (default: 2)
     --retry-delay SECONDS
                           First retry pause, doubled for each retry (default:
                           0.5)
