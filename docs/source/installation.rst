Installation
============

Use maintained Python 3.11–3.14. Supported native targets are Ubuntu 24.04 and
Rocky Linux 9. See :doc:`introduction` for the lifecycle contract.

GitHub release packages
-----------------------

Download the wheel, source archive or native package and ``SHA256SUMS`` from
the same GitHub release. Verify the files before installing:

.. code-block:: bash

   sha256sum --check SHA256SUMS
   sudo apt install ./nagios-plugins-collection_2.0.0_all.deb
   # On Rocky Linux 9:
   sudo dnf install ./nagios-plugins-collection_2.0.0_noarch.rpm
   /usr/lib/nagios/plugins/check_website_status --help

Native packages bundle portable monitoring clients and require system libpq.
The RPM selects Python 3.12; the Debian package uses supported system Python.
Native installed commands reside under ``/usr/lib/nagios/plugins``. When Nagios
uses another plugin directory, reference those absolute paths in command
definitions or create explicit administrator-managed links.

Wheel or source installation
----------------------------

Install into an isolated environment rather than modifying system Python:

.. code-block:: bash

   mise exec python@3.12 -- python -m venv .venv
   .venv/bin/python -m pip install ./nagios_plugins_collection-2.0.0-py3-none-any.whl
   .venv/bin/check_website_status --help

For source development, clone the public repository, install the hash-locked
CI dependencies and install the first-party source without resolving new deps:

.. code-block:: bash

   git clone https://github.com/somethingwithproof/nagios-plugins-collection.git
   cd nagios-plugins-collection
   mise exec python@3.12 -- python -m venv .venv
   .venv/bin/python -m pip install --only-binary=:all: --require-hashes -r packaging/ci-requirements.txt
   .venv/bin/python -m pip install --no-deps --no-build-isolation -e .

PyPI publishing is an explicit manual workflow and requires a configured PyPI
credential. A GitHub release does not automatically publish to PyPI. Choose
extras such as ``[aws]``, ``[dns]``, ``[k8s]``, ``[pg]`` and ``[redis]`` when
installing a published Python distribution for those monitoring targets.

Containers and Kubernetes
-------------------------

The GHCR image runs as UID/GID 10001 and defaults to website-status CLI help.
Pass another installed plugin as the container command. Deploy the release's Helm chart on
maintained Kubernetes 1.35–1.37. Enable token automount and ``rbac.create`` only
for Kubernetes node monitoring; the opt-in ClusterRole grants list access to
nodes. Use the README's complete Helm and Nomad examples.

Troubleshooting
---------------

Use the installed command's ``--help`` to verify its options and path. For
certificate failures, verify hostname/SAN, validity and CA trust; supply a CA
file rather than disabling verification. Report OS, Python and package versions
with a redacted reproducer through the repository's issue tracker.
