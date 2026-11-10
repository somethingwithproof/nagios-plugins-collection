.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

check_http_sli
==============

Run ``check_http_sli --help`` for the installed command arguments. Exit codes follow
the Nagios convention: 0 OK, 1 WARNING, 2 CRITICAL, and 3 UNKNOWN.

.. automodule:: nagios_plugins.plugins.check_http_sli
   :members:
   :show-inheritance:

Installed command options
-------------------------

.. code-block:: text

   usage: check_http_sli [-h] [-v] [-t TIMEOUT] [-w WARNING] [-c CRITICAL]
                         [--json] --url URL [--samples SAMPLES]
                         [--latency-warning RANGE] [--latency-critical RANGE]
                         [--error-rate-warning RANGE]
                         [--error-rate-critical RANGE] [--ca-file PATH]
                         [--insecure] [--client-cert PATH] [--client-key PATH]
                         [--max-response-bytes BYTES] [--username USERNAME]
                         [--password PASSWORD | --password-file PATH]
                         [--bearer-token BEARER_TOKEN | --bearer-token-file PATH]
                         [--api-key API_KEY | --api-key-file PATH]
                         [--api-key-header NAME]

   Probe one or more URLs concurrently and report p50/p95/p99 and error-rate.

   Latency and error rate have separate Nagios ranges. -w/-c are aliases for
   --latency-warning/--latency-critical (p95 in milliseconds).

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
     --url URL             URL to probe (repeatable)
     --samples SAMPLES     Samples per URL
     --latency-warning RANGE
                           p95 latency range in ms for WARNING (alias: -w)
     --latency-critical RANGE
                           p95 latency range in ms for CRITICAL (alias: -c)
     --error-rate-warning RANGE
                           Range for the fraction of failed requests (0-1) for
                           WARNING
     --error-rate-critical RANGE
                           Range for the fraction of failed requests (0-1) for
                           CRITICAL
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

   HTTP authentication:
     --username USERNAME   User name for HTTP basic authentication
     --password PASSWORD   password for HTTP basic authentication (visible in the
                           process list; prefer --password-file or
                           $CHECK_HTTP_SLI_PASSWORD)
     --password-file PATH  Read password for HTTP basic authentication from PATH
                           (or the file named by $CHECK_HTTP_SLI_PASSWORD_FILE)
     --bearer-token BEARER_TOKEN
                           bearer token sent in the Authorization header (visible
                           in the process list; prefer --bearer-token-file or
                           $CHECK_HTTP_SLI_BEARER_TOKEN)
     --bearer-token-file PATH
                           Read bearer token sent in the Authorization header
                           from PATH (or the file named by
                           $CHECK_HTTP_SLI_BEARER_TOKEN_FILE)
     --api-key API_KEY     API key sent in the --api-key-header header (visible
                           in the process list; prefer --api-key-file or
                           $CHECK_HTTP_SLI_API_KEY)
     --api-key-file PATH   Read API key sent in the --api-key-header header from
                           PATH (or the file named by
                           $CHECK_HTTP_SLI_API_KEY_FILE)
     --api-key-header NAME
                           Header that carries --api-key (default: X-API-Key)
