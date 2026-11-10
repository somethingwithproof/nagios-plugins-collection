.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

Usage
=====

This guide explains how to use the Nagios Plugins Collection.

Common Command-Line Options
---------------------------

All plugins in the collection share a common set of command-line options:

.. code-block:: text

    -v, --verbose         Increase verbosity (can be used multiple times)
    -t, --timeout SECONDS Timeout in seconds for the whole run (default: 30)
    -w, --warning THRESHOLD
                          Warning threshold (plugin-specific)
    -c, --critical THRESHOLD
                          Critical threshold (plugin-specific)
    --json                Output results in JSON format
    -h, --help            Show help message and exit

Threshold Formats
-----------------

Plugins that accept ranges use the `Nagios Plugin Guidelines
<https://nagios-plugins.org/doc/guidelines.html#THRESHOLDFORMAT>`_ format,
``[@]start:end``. Both endpoints are part of the range. A value outside the range
raises the alert; with the ``@`` prefix a value inside the range does.

- ``10``: same as ``0:10``; alert when the value is below 0 or above 10
- ``10:``: alert when the value is below 10
- ``~:10``: alert when the value is above 10 (no lower bound)
- ``10:20``: alert when the value is below 10 or above 20
- ``@10:20``: alert when the value is 10 or more and 20 or less

``:10`` (empty start) is accepted for compatibility and means the same as ``~:10``.
Critical is evaluated before warning, so a value that matches both is CRITICAL.
A malformed range, or a start greater than its end, returns UNKNOWN.

Examples:

- ``-w 80 -c 90``: Warning if above 80, critical if above 90 (both if below 0)
- ``-w 80: -c 90:``: Warning if below 80, critical if below 90
- ``-w 10:80 -c 5:90``: Warning if outside 10-80, critical if outside 5-90
- ``-w @10:80 -c @5:90``: Warning if inside 10-80, critical if inside 5-90

Each plugin's ``--help`` states whether its ``-w``/``-c`` take ranges or a
plain number of a documented unit. Three commands keep plain numbers and reject
range forms as a usage error:

- ``check_tls_expiry``: days; alert when the days remaining are at or below
  the value, as ``check_http -C`` does
- ``check_website_status``: seconds; alert when the response takes longer
- ``check_component_status``: whole minutes since the last update; alert above

Basic Usage Examples
--------------------

Check Hadoop Cluster
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    check_hadoop command --url=http://hadoop-master:8088/ws/v1/cluster/info

Check MongoDB Health
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    check_monghealth --host=mongodb.example.com --port=27017 --warning=80 --critical=90

Check Read-Only Mounts
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    check_ro_mounts --exclude=/proc,/sys,/dev

Check Website Status
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    check_website_status --url=https://example.com --pattern="Welcome" --timeout=10

Integration with Nagios
-----------------------

Example Nagios configuration for the check_hadoop plugin:

.. code-block:: text

    # Command definition
    define command {
        command_name    check_hadoop_cluster
        command_line    $USER1$/check_hadoop command --url=$ARG1$
    }

    # Service definition
    define service {
        use                     generic-service
        host_name               hadoop-master
        service_description     Hadoop Cluster Status
        check_command           check_hadoop_cluster!http://hadoop-master:8088/ws/v1/cluster/info
        notifications_enabled   1
    }

Output Formats
--------------

Standard Output Format
~~~~~~~~~~~~~~~~~~~~~~

By default, all plugins produce output in the standard Nagios plugin format:

.. code-block:: text

    STATUS - Message | 'label'=value[UOM];[warn];[crit];[min];[max] ...
    optional long output lines

Where:

- ``STATUS`` is one of: OK, WARNING, CRITICAL, UNKNOWN
- ``Message`` is a human-readable description of the check result. It is always
  a single line; line breaks become spaces and ``|`` becomes ``/``
- The part after the pipe (``|``) contains performance data. Values are plain
  numbers with an optional guideline unit (``s``, ``ms``, ``us``, ``%``, ``B``,
  ``KB``, ``MB``, ``GB``, ``TB``, ``c``); labels containing spaces, ``=`` or
  ``'`` are single-quoted with ``'`` doubled. Text values stay in the message
  and the JSON output and are not published as perfdata.

Example output:

.. code-block:: text

    OK - Hadoop cluster is healthy | status=1 component_hdfs_status=1 mem=1048576KB

JSON Output Format
~~~~~~~~~~~~~~~~~~

All plugins also support JSON output format, which is useful for integration with other tools:

.. code-block:: bash

    check_website_status --url=https://example.com --pattern="Welcome" --json

Example JSON output:

.. code-block:: json

    {
      "status": "OK",
      "message": "HTTP 200 - https://example.com - 345.67ms",
      "metrics": {
        "response_time": 345.67
      },
      "timestamp": "2025-04-11 12:30:45"
    }

Timeouts
--------

``--timeout`` bounds the whole run, not only one request. Network requests and
commands use it as their own timeout, so a slow service is reported with the
plugin's usual result (for example ``CRITICAL`` for an HTTP timeout). One
second after it, the run is ended regardless of what it is waiting for, such as
DNS resolution, a TCP connect, a retry or a child process: the plugin prints
``UNKNOWN - Plugin timed out after N seconds`` (or the JSON equivalent), kills
any ``ssh``, ``dig`` or ``mount`` child it started and exits 3. Retries and
pauses between them stop when the timeout is spent.

Set ``--timeout`` at least two seconds below the scheduler's own limit (Nagios
``service_check_timeout``, 60 seconds by default, or the Icinga 2
CheckCommand ``timeout``), so the plugin's UNKNOWN result arrives before the
scheduler kills it. On POSIX the run is interrupted with ``SIGALRM``; where
that is unavailable, or the process cannot be interrupted, a watchdog thread
writes the result and exits one second later. ``--timeout`` must be a whole
number of seconds of at least 1.

HTTP Options
------------

Every check that talks HTTP (``check_component_status``, ``check_hadoop``,
``check_http_sli``, ``check_jobs``, ``check_log_errors``,
``check_mongodb_health``, ``check_monghealth``, ``check_oauth2_token``,
``check_prometheus_query`` and ``check_website_status``) uses one client with
the same options and behavior:

TLS
   Certificates and hostnames are verified against the bundled Mozilla CA
   store (``certifi``), or the bundle in ``SSL_CERT_FILE``. ``--ca-file PATH`` trusts a private CA
   instead. ``--client-cert PATH`` (and ``--client-key PATH`` when the key is in
   a separate file) presents a client certificate for mutual TLS.
   ``--insecure`` turns verification off and logs a warning on every run; it
   cannot be combined with ``--ca-file``. ``check_tls_expiry`` accepts
   ``--ca-file`` but not ``--insecure``, because verification is what it checks.

Credentials
   ``--username`` with ``--password`` sends HTTP basic authentication,
   ``--bearer-token`` an ``Authorization: Bearer`` header and ``--api-key`` the
   header named by ``--api-key-header`` (``X-API-Key`` by default). Each secret
   is read from, in order, the flag, ``--NAME-file PATH``, the environment
   variable ``CHECK_<COMMAND>_<NAME>`` (for example
   ``CHECK_PROMETHEUS_QUERY_BEARER_TOKEN``) or a file named by the same variable
   with ``_FILE`` appended, the convention for mounted container secrets.
   Values on the command line are visible to other local users, so prefer the
   file or environment forms. User information in a URL
   (``https://user:pass@host``) is basic authentication when no other is
   configured. Credentials are sent only to the scheme, host and
   port of the URL the check requests: a redirect to another origin is followed
   without them, and a redirect from HTTPS to plain HTTP is refused (CRITICAL)
   when credentials are configured. ``check_oauth2_token`` keeps its own
   ``--client-secret``.

Retries
   ``--retries N`` (2 by default; 0 for ``check_website_status``) repeats a
   request that failed transiently, pausing ``--retry-delay`` seconds and
   doubling the pause each time, up to 5 seconds. A connection that was never
   established is retried for any method; a 502, 503 or 504 response, or an
   error after the request was sent, is retried only for idempotent methods
   (``GET``, ``HEAD``, ``OPTIONS``, ``PUT``, ``DELETE``), so a search ``POST`` is
   never sent twice. Retries and each attempt's timeout fit inside
   ``--timeout``. ``check_http_sli`` never retries: every sample is a
   measurement.

Response size
   ``--max-response-bytes BYTES`` (10 MiB by default) bounds the body a check
   reads, counted after decompression. A larger answer is UNKNOWN, naming the
   URL; for ``check_http_sli`` it counts as a failed probe. The status message
   and long output of every check are cut to 4,096 and 32,768 characters,
   ending with ``[truncated N characters]``.

Proxies and identification
   ``HTTP_PROXY``, ``HTTPS_PROXY``, ``ALL_PROXY`` and ``NO_PROXY`` are honored.
   Requests carry ``User-Agent: nagios-plugins-collection/VERSION (COMMAND)``.
   Error messages show request URLs without credentials, query string or
   fragment.

Return Codes
------------

All plugins return standard Nagios return codes:

- 0: OK
- 1: WARNING
- 2: CRITICAL
- 3: UNKNOWN

Invalid or missing command-line arguments exit 3 (UNKNOWN) with an
``UNKNOWN - <command>: <error>`` line on standard output and the usage on
standard error. ``--help`` exits 0.

Advanced Usage
--------------

Asynchronous Execution
~~~~~~~~~~~~~~~~~~~~~~

Many plugins now support asynchronous execution for improved performance in high-load environments. This is particularly useful when monitoring multiple endpoints or services simultaneously.

Secrets
~~~~~~~

Command-line arguments are visible to other local users in the process list.
Options that carry a secret also accept a file or an environment variable:

.. list-table::
   :header-rows: 1

   * - Option
     - File option
     - Environment variable
   * - ``check_oauth2_token --client-secret``
     - ``--client-secret-file``
     - ``CHECK_OAUTH2_CLIENT_SECRET``
   * - ``check_postgres_replication_lag --dsn``
     - ``--dsn-file``
     - ``CHECK_POSTGRES_DSN``
   * - ``check_redis_saturation --url``
     - ``--url-file``
     - ``CHECK_REDIS_URL``
   * - ``check_monghealth --password``
     - ``--password-file``
     - ``CHECK_MONGHEALTH_PASSWORD``

The command-line option wins over the file, and the file over the environment
variable. Line breaks around a file's content are ignored. A secret file must
be a regular file of UTF-8 text no larger than 64 KiB; anything else, such as a
FIFO, a directory or binary content, is a usage error (exit 3). Secret files are
read within ``--timeout``, so a stuck mount ends the run with the timeout
result. Plugin output, JSON
output and log records mask every resolved secret and every password in a URL
option wherever it appears (also URL-encoded or as a quoted fragment), URL
credentials (``scheme://***@host``), secret parameters such as ``token=***``,
``password: ***`` or ``"password": "***"``, ``Authorization`` and cookie
headers, bearer tokens and AWS access keys.

Diagnostics
~~~~~~~~~~~

Plugins write only the result to standard output. Log records go to standard
error: warnings by default, informational records with ``-v`` and debug
records with ``-vv``.

Plugin-Specific Options
~~~~~~~~~~~~~~~~~~~~~~~

For more advanced usage and plugin-specific options, refer to the individual plugin documentation in the :doc:`plugins/index` section.
