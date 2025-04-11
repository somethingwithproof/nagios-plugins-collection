Installation
============

This guide will help you install the Nagios Plugins Collection.

Requirements
-----------

- Python 3.8 or higher
- pip (Python package installer)
- Nagios 4.4.6 or higher (or compatible monitoring system)

Installation Methods
------------------

From PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~

The recommended way to install the Nagios Plugins Collection is from PyPI using pip:

.. code-block:: bash

    # Basic installation
    pip install nagios-plugins-collection

    # With development dependencies
    pip install "nagios-plugins-collection[dev]"

    # With security tools
    pip install "nagios-plugins-collection[security]"

    # With all extras
    pip install "nagios-plugins-collection[all]"

This will install the latest stable version of the package and all its dependencies.

For a specific version:

.. code-block:: bash

    pip install nagios-plugins-collection==1.1.0

From Source
~~~~~~~~~~

You can also install the package directly from the source code:

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/thomasvincent/nagios-plugins-collection.git
       cd nagios-plugins-collection

2. Install the package:

   .. code-block:: bash

       pip install .

   Or, for development:

   .. code-block:: bash

       pip install -e ".[dev,security]"

Installation for Nagios
----------------------

After installing the Python package, you need to configure Nagios to use the plugins:

1. Locate the installed plugins:

   .. code-block:: bash

       which check_hadoop

2. Create symbolic links in the Nagios plugins directory:

   .. code-block:: bash

       ln -s $(which check_hadoop) /usr/local/nagios/libexec/
       # Repeat for other plugins

3. Update Nagios configuration to use the plugins (example for check_hadoop):

   .. code-block:: text

       # In commands.cfg
       define command {
           command_name    check_hadoop
           command_line    $USER1$/check_hadoop $ARG1$
       }

4. Restart Nagios:

   .. code-block:: bash

       systemctl restart nagios

Verifying Installation
--------------------

To verify that the plugins are installed correctly, you can run:

.. code-block:: bash

    check_hadoop --help

This should display the help message for the plugin.

Troubleshooting
--------------

Common installation issues:

1. **Permission denied**: Ensure you have the necessary permissions to install Python packages. You may need to use `sudo` or set up a virtual environment.

2. **Missing dependencies**: If you encounter dependency errors, try installing with:

   .. code-block:: bash

       pip install nagios-plugins-collection[all]

3. **Plugin not found**: Ensure the plugin is in your PATH or use the full path to the plugin in your Nagios configuration.

4. **Python version**: Verify you're using Python 3.8 or higher:

   .. code-block:: bash

       python --version

For more help, please open an issue on the GitHub repository.
