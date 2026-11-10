.. SPDX-FileCopyrightText: 2026 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

Monitoring Definitions and Man Pages
====================================

Icinga 2 CheckCommands, Nagios command definitions and a man page for every
command are generated from the commands' own option parsers, so they list
exactly the options ``--help`` shows. ``scripts/generate_monitoring_config.py``
writes them to ``contrib/``; CI fails when a change to an option leaves them
out of date, and it validates the Icinga 2 file with Icinga 2 itself.

Where to find them
------------------

======================================  ==============================================================
Source                                  Files
======================================  ==============================================================
Debian and RPM packages                 ``/usr/share/nagios-plugins-collection/icinga2/nagios-plugins-collection.conf``,
                                        ``/usr/share/nagios-plugins-collection/nagios/nagios-plugins-collection.cfg``,
                                        ``/usr/share/man/man1/check_*.1.gz``
GitHub release                          ``nagios-plugins-collection-monitoring-config-X.Y.Z.tar.gz``
                                        (the ``contrib/`` tree), also in the source distribution
Repository                              ``contrib/icinga2``, ``contrib/nagios``, ``contrib/man/man1``
======================================  ==============================================================

After installing a package, ``man check_tls_expiry`` shows that command's
options, the environment variables it reads secrets from and its exit
statuses. Minimal container images often exclude ``/usr/share/man``; the pages
are also in the release archive.

Icinga 2
--------

Include the file, for example from ``/etc/icinga2/icinga2.conf``:

.. code-block:: text

   include "/usr/share/nagios-plugins-collection/icinga2/nagios-plugins-collection.conf"

Each option is a custom variable named ``<command>_<option>``, with dashes
replaced by underscores. Switches such as ``--insecure`` use ``set_if``, options
that may repeat take an array, and options the command requires are marked
``required``, so Icinga 2 reports a missing value before running the check.
Secrets are passed through the command's environment variables, never as
arguments, so they do not appear in the process list:

.. code-block:: text

   object Service "idp-token" {
     host_name = "idp.example.com"
     check_command = "check_oauth2_token"
     vars.check_oauth2_token_token_url = "https://idp.example.com/oauth2/token"
     vars.check_oauth2_token_client_id = "monitoring"
     vars.check_oauth2_token_scope = [ "openid", "profile" ]
     // Sets CHECK_OAUTH2_CLIENT_SECRET for the plugin. OAuth2ClientSecret is a
     // const defined in a file that only the Icinga 2 user can read.
     vars.check_oauth2_token_client_secret = OAuth2ClientSecret
     vars.check_oauth2_token_warning = "300:"
   }

Alternatively set ``vars.check_oauth2_token_client_secret_file`` to a file only
the Icinga 2 user can read. The commands run from
``vars.nagios_plugins_collection_dir`` (``/usr/lib/nagios/plugins``, where the
packages install them); set it on a Host or Service, or in a template that
imports ``nagios-plugins-collection``, when the commands are installed
elsewhere, for example in a virtual environment.

Nagios
------

Include the file with ``cfg_file`` in ``nagios.cfg``. Each command takes the
options it requires as ``$ARG1$``, ``$ARG2$`` and so on, in the order the
comment above each definition lists, followed by one argument for any further
options:

.. code-block:: text

   cfg_file=/usr/share/nagios-plugins-collection/nagios/nagios-plugins-collection.cfg

   define service {
       use                     generic-service
       host_name               www
       service_description     Website
       check_command           check_website_status!https://www.example.com/!-w 2 -c 5
   }

Nagios cannot set environment variables per command, so pass secrets with the
``-file`` options, for example ``--password-file /etc/nagios/secrets/api``, or
set the ``CHECK_*`` variables in the environment Nagios runs in. Never put a
secret value in ``$ARGn$``: it would be visible in the process list and in the
Nagios configuration.

Regenerating
------------

After changing a command's options, run:

.. code-block:: bash

   uv run python scripts/generate_monitoring_config.py

and commit the updated ``contrib/`` files with the change.
