Usage
=====

This guide explains how to use the Nagios Plugins Collection.

Common Command-Line Options
--------------------------

All plugins in the collection share a common set of command-line options:

.. code-block:: text

    -v, --verbose         Increase verbosity (can be used multiple times)
    -t, --timeout SECONDS Timeout in seconds (default: 30)
    -w, --warning THRESHOLD
                          Warning threshold (plugin-specific)
    -c, --critical THRESHOLD
                          Critical threshold (plugin-specific)
    -h, --help            Show help message and exit

Threshold Formats
---------------

Thresholds follow the standard Nagios plugin threshold format:

- Simple threshold: ``VALUE``
- Range: ``START:END``
- Inclusive range: ``@START:END``
- Minimum value: ``VALUE:``
- Maximum value: ``:VALUE``

Examples:

- ``-w 80 -c 90``: Warning if >= 80, critical if >= 90
- ``-w 80: -c 90:``: Warning if < 80, critical if < 90
- ``-w 10:80 -c 5:90``: Warning if outside 10-80, critical if outside 5-90
- ``-w @10:80 -c @5:90``: Warning if inside 10-80, critical if inside 5-90

Basic Usage Examples
------------------

Check Hadoop Cluster
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    check_hadoop command --url=http://hadoop-master:8088/ws/v1/cluster/info

Check MongoDB Health
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    check_monghealth --host=mongodb.example.com --port=27017 --warning=80 --critical=90

Check Processes
~~~~~~~~~~~~~

.. code-block:: bash

    check_procs --host=server.example.com --process=nginx --min=1 --max=10

Check Read-Only Mounts
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    check_mounts --exclude=/proc,/sys,/dev

Check Website Status
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    check_website_status --url=https://example.com --pattern="Welcome" --timeout=10

Integration with Nagios
---------------------

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

Output Format
-----------

All plugins produce output in the standard Nagios plugin format:

.. code-block:: text

    STATUS - Message | metric1=value1 metric2=value2

Where:

- ``STATUS`` is one of: OK, WARNING, CRITICAL, UNKNOWN
- ``Message`` is a human-readable description of the check result
- The part after the pipe (``|``) contains performance data metrics

Example output:

.. code-block:: text

    OK - Hadoop cluster is healthy | nodes=10 memory_used=85% cpu_used=60%

Return Codes
----------

All plugins return standard Nagios return codes:

- 0: OK
- 1: WARNING
- 2: CRITICAL
- 3: UNKNOWN

Advanced Usage
------------

For more advanced usage and plugin-specific options, refer to the individual plugin documentation in the :doc:`plugins/index` section.
