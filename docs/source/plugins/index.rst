Plugins Reference
================

This section provides detailed documentation for each plugin in the Nagios Plugins Collection.

.. toctree::
   :maxdepth: 1
   :caption: Available Plugins:

   check_hadoop
   check_monghealth
   check_procs
   check_mounts
   check_counters_db
   check_dig
   check_etl
   check_http500
   check_jobs
   check_scribe
   check_statusthroughweb
   check_website_status
   check_advanced_website_status
   membase_stats
   url_monitor
   xml_url_checker

Plugin Categories
---------------

System Monitoring
~~~~~~~~~~~~~~~

- :doc:`check_procs` - Check processes on remote systems via SSH
- :doc:`check_mounts` - Check for read-only mounts on a system
- :doc:`check_jobs` - Monitor job execution

Database Monitoring
~~~~~~~~~~~~~~~~

- :doc:`check_monghealth` - Monitor MongoDB health and performance
- :doc:`check_counters_db` - Monitor Vertica database counters
- :doc:`membase_stats` - Monitor Membase/Couchbase statistics

Web Monitoring
~~~~~~~~~~~~

- :doc:`check_http500` - Check for HTTP 500 errors
- :doc:`check_statusthroughweb` - Check status through a web interface
- :doc:`check_website_status` - Check website status
- :doc:`check_advanced_website_status` - Advanced website status checking
- :doc:`url_monitor` - Monitor URLs for availability and content
- :doc:`xml_url_checker` - Check XML content from URLs

Infrastructure Monitoring
~~~~~~~~~~~~~~~~~~~~~

- :doc:`check_hadoop` - Monitor Hadoop clusters and HDFS
- :doc:`check_dig` - Check DNS resolution
- :doc:`check_scribe` - Monitor Scribe log aggregation

Data Processing Monitoring
~~~~~~~~~~~~~~~~~~~~~~~

- :doc:`check_etl` - Monitor ETL processes
