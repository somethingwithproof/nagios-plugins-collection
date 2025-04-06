Changelog
=========

This document records all notable changes to the Nagios Plugins Collection.

1.0.0 (2025-04-06)
----------------

Initial release of the refactored and enterprise-grade Nagios Plugins Collection.

Features
~~~~~~~

- Restructured project as a proper Python module
- Added comprehensive documentation
- Implemented enterprise-grade base classes and utilities
- Added support for multiple Python versions (3.7+)
- Added support for multiple Nagios versions (4.4.6+)
- Implemented consistent error handling and output formatting
- Added performance data collection
- Added threshold handling
- Added extensive test coverage
- Set up GitHub CI/CD workflows

Plugins
~~~~~~

- check_hadoop: Monitor Hadoop clusters and HDFS
- check_monghealth: Monitor MongoDB health and performance
- check_procs: Check processes on remote systems via SSH
- check_mounts: Check for read-only mounts on a system
- check_counters_db: Monitor Vertica database counters
- check_dig: Check DNS resolution
- check_etl: Monitor ETL processes
- check_http500: Check for HTTP 500 errors
- check_jobs: Monitor job execution
- check_scribe: Monitor Scribe log aggregation
- check_statusthroughweb: Check status through a web interface
- check_website_status: Check website status
- check_advanced_website_status: Advanced website status checking
- membase_stats: Monitor Membase/Couchbase statistics
- url_monitor: Monitor URLs for availability and content
- xml_url_checker: Check XML content from URLs

0.1.0 (Historical)
----------------

Original collection of individual Nagios plugins.
