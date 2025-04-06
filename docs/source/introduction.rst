Introduction
============

The Nagios Plugins Collection is a comprehensive set of monitoring plugins for Nagios and compatible monitoring systems. These plugins are designed to be enterprise-grade, with a focus on reliability, maintainability, and extensibility.

Features
--------

- **Consistent Interface**: All plugins follow the same command-line interface pattern, making them easy to use and integrate.
- **Comprehensive Documentation**: Each plugin is thoroughly documented, with examples and usage information.
- **Extensive Test Coverage**: All plugins have unit and integration tests to ensure they work correctly.
- **Multi-Version Support**: The plugins support multiple Python versions (3.7+) and Nagios versions.
- **Performance Data**: All plugins provide performance data that can be used for trending and analysis.
- **Threshold Handling**: Consistent threshold handling across all plugins, following Nagios plugin development guidelines.
- **Error Handling**: Robust error handling to ensure plugins fail gracefully and provide useful error messages.

Available Plugins
----------------

The collection includes plugins for monitoring:

- **check_hadoop**: Monitor Hadoop clusters and HDFS
- **check_monghealth**: Monitor MongoDB health and performance
- **check_procs**: Check processes on remote systems via SSH
- **check_mounts**: Check for read-only mounts on a system
- **check_counters_db**: Monitor Vertica database counters
- **check_dig**: Check DNS resolution
- **check_etl**: Monitor ETL processes
- **check_http500**: Check for HTTP 500 errors
- **check_jobs**: Monitor job execution
- **check_scribe**: Monitor Scribe log aggregation
- **check_statusthroughweb**: Check status through a web interface
- **check_website_status**: Check website status
- **check_advanced_website_status**: Advanced website status checking
- **membase_stats**: Monitor Membase/Couchbase statistics
- **url_monitor**: Monitor URLs for availability and content
- **xml_url_checker**: Check XML content from URLs

Requirements
-----------

- Python 3.7 or higher
- Nagios 4.4.6 or higher (or compatible monitoring system)
- Required Python packages (installed automatically when using pip)

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.
