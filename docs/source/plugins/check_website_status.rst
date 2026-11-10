.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_website_status
====================

Run ``check_website_status --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_website_status
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_website_status [-h] [-v] [-t TIMEOUT] [-w SECONDS] [-c SECONDS]
                               [--json] --url URL [--pattern PATTERN]
                               [--method {GET,HEAD,POST}] [--ca-file PATH]
                               [--insecure] [--client-cert PATH]
                               [--client-key PATH] [--max-response-bytes BYTES]
                               [--retries RETRIES] [--retry-delay SECONDS]
                               [--username USERNAME]
                               [--password PASSWORD | --password-file PATH]
                               [--bearer-token BEARER_TOKEN | --bearer-token-file PATH]
                               [--api-key API_KEY | --api-key-file PATH]
                               [--api-key-header NAME]

   Check website content, status and response time in seconds.

   -w/-c are response times in seconds, not Nagios ranges: the check alerts
   when the response takes longer.

   options:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity (can be used multiple times)
     -t TIMEOUT, --timeout TIMEOUT
                           Timeout in seconds for the whole run (default: 30);
                           the plugin exits UNKNOWN 1 second after it
     -w SECONDS, --warning SECONDS
                           WARNING when the response takes longer (default: 1.0;
                           not a range)
     -c SECONDS, --critical SECONDS
                           CRITICAL when the response takes longer (default: 2.0;
                           not a range)
     --json                Output results in JSON format
     --url URL
     --pattern PATTERN
     --method {GET,HEAD,POST}
     --max-response-bytes BYTES
                           Largest response body read, after decompression; a
                           larger one is UNKNOWN (default: 10485760)

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
                           (default: 0)
     --retry-delay SECONDS
                           First retry pause, doubled for each retry (default:
                           1.0)

   HTTP authentication:
     --username USERNAME   User name for HTTP basic authentication
     --password PASSWORD   password for HTTP basic authentication (visible in the
                           process list; prefer --password-file or
                           $CHECK_WEBSITE_STATUS_PASSWORD)
     --password-file PATH  Read password for HTTP basic authentication from PATH
                           (or the file named by
                           $CHECK_WEBSITE_STATUS_PASSWORD_FILE)
     --bearer-token BEARER_TOKEN
                           bearer token sent in the Authorization header (visible
                           in the process list; prefer --bearer-token-file or
                           $CHECK_WEBSITE_STATUS_BEARER_TOKEN)
     --bearer-token-file PATH
                           Read bearer token sent in the Authorization header
                           from PATH (or the file named by
                           $CHECK_WEBSITE_STATUS_BEARER_TOKEN_FILE)
     --api-key API_KEY     API key sent in the --api-key-header header (visible
                           in the process list; prefer --api-key-file or
                           $CHECK_WEBSITE_STATUS_API_KEY)
     --api-key-file PATH   Read API key sent in the --api-key-header header from
                           PATH (or the file named by
                           $CHECK_WEBSITE_STATUS_API_KEY_FILE)
     --api-key-header NAME
                           Header that carries --api-key (default: X-API-Key)
