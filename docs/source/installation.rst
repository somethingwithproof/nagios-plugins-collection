.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

Installation
============

Use maintained Python 3.11–3.14. Supported native targets are Ubuntu 24.04 and
Rocky Linux 9. See :doc:`introduction` for the lifecycle contract.

GitHub release packages
-----------------------

Download the wheel, source archive or native package and ``SHA256SUMS`` from
the same GitHub release. Verify the files before installing:

.. Release-please bumps versions between these markers; see release-please-config.json.
.. x-release-please-start-version

.. code-block:: bash

   sha256sum --check --ignore-missing SHA256SUMS

   sudo apt install ./nagios-plugins-collection_2.0.1_amd64.deb
   # On Rocky Linux 9:
   sudo dnf install ./nagios-plugins-collection_2.0.1_x86_64.rpm
   /usr/lib/nagios/plugins/check_website_status --help

.. x-release-please-end

Require the artifact you selected to report ``OK`` in the checksum output.

Native packages target Linux x86-64 and Python 3.12, bundle the required client
extensions, and require system libpq. Both package formats require Python 3.12.
Native installed commands reside under ``/usr/lib/nagios/plugins``. When Nagios
uses another plugin directory, reference those absolute paths in command
definitions or create explicit administrator-managed links.

Wheel or source installation
----------------------------

Install into an isolated environment rather than modifying system Python:

.. code-block:: bash

   mise exec python@3.12 -- python -m venv .venv
   .venv/bin/python -m pip install ./nagios_plugins_collection-*-py3-none-any.whl
   .venv/bin/check_website_status --help

For source development, clone the public repository and install the locked
dependencies, development tools and first-party source with uv:

.. code-block:: bash

   git clone https://github.com/somethingwithproof/nagios-plugins-collection.git
   cd nagios-plugins-collection
   mise exec python@3.12 -- uv sync --locked --all-extras --python 3.12
   uv run check_website_status --help

PyPI publishing is an explicit manual workflow that uses PyPI trusted
publishing and must be enabled by a maintainer (see :doc:`releasing`). A GitHub
release does not automatically publish to PyPI. Choose
extras such as ``[aws]``, ``[dns]``, ``[k8s]``, ``[pg]`` and ``[redis]`` when
installing a published Python distribution for those monitoring targets.

Containers and Kubernetes
-------------------------

The GHCR image runs as UID/GID 10001 and defaults to website-status CLI help.
Pass another installed plugin as the container command. Deploy the release's Helm chart on
maintained Kubernetes 1.35–1.37. Enable token automount and ``rbac.create`` only
for Kubernetes node monitoring; the opt-in ClusterRole grants list access to
nodes. The chart and the Nomad job run one check per schedule and treat every
exit as final, so a WARNING, CRITICAL or UNKNOWN result is not retried; read
the result from the job's log and exit status.

Helm
^^^^

The chart ships as ``nagios-plugins-collection-<version>.tgz`` in each GitHub
release. Download and verify it, then install it with a values file that names
the check to run. This example monitors an OAuth2 token endpoint and reads the
client secret from a Kubernetes Secret instead of the command line:

.. code-block:: yaml

   # oauth-values.yaml
   schedule: "*/5 * * * *"
   command: ["check_oauth2_token"]
   args:
     - --token-url=https://issuer.example/oauth2/token
     - --client-id=monitor
     - --scope=openid
     - --timeout=10
   env:
     - name: CHECK_OAUTH2_CLIENT_SECRET
       valueFrom:
         secretKeyRef: {name: oauth-monitor, key: client-secret}

.. x-release-please-start-version

.. code-block:: bash

   gh release download v2.0.1 --repo somethingwithproof/nagios-plugins-collection \
     --pattern 'nagios-plugins-collection-2.0.1.tgz' --pattern SHA256SUMS
   sha256sum --check --ignore-missing SHA256SUMS
   kubectl create secret generic oauth-monitor --from-file=client-secret=./client-secret
   helm install oauth-monitor ./nagios-plugins-collection-2.0.1.tgz -f oauth-values.yaml
   # Run once now and read the status line:
   kubectl create job oauth-monitor-now --from=cronjob/oauth-monitor-nagios-plugins-collection
   kubectl logs job/oauth-monitor-now

.. x-release-please-end

``image.tag`` defaults to the chart's ``appVersion``; set
``image.repository`` to ``ghcr.io/somethingwithproof/nagios-plugins-collection@sha256``
and ``image.tag`` to the digest to pin by digest. Keep ``job.activeDeadlineSeconds``
above the plugin ``--timeout``.

Node monitoring needs the API token and the opt-in, list-only ClusterRole:

.. code-block:: yaml

   # nodes-values.yaml
   command: ["check_k8s_node_status"]
   args: ["--label=node-role.kubernetes.io/worker"]
   serviceAccount:
     automountServiceAccountToken: true
   rbac:
     create: true

.. x-release-please-start-version

.. code-block:: bash

   helm install node-monitor ./nagios-plugins-collection-2.0.1.tgz -f nodes-values.yaml

.. x-release-please-end

Nomad
^^^^^

``deploy/nomad/nagios-plugins-collection.nomad.hcl`` is a periodic batch job
with restarts and rescheduling disabled. Edit the task's ``command`` and
``args`` for the check to run, then submit it with a pinned image:

.. x-release-please-start-version

.. code-block:: bash

   nomad job run \
     -var image=ghcr.io/somethingwithproof/nagios-plugins-collection:2.0.1 \
     deploy/nomad/nagios-plugins-collection.nomad.hcl

.. x-release-please-end

To pass a secret, store it as a Nomad Variable readable by the job and render
it into the task environment with a ``template`` block inside ``task "plugin"``:

.. code-block:: hcl

   template {
     destination = "secrets/check.env"
     env         = true
     data        = <<-EOT
       {{ with nomadVar "nomad/jobs/nagios-plugins-collection" }}
       CHECK_OAUTH2_CLIENT_SECRET={{ .client_secret }}
       {{ end }}
     EOT
   }

.. code-block:: bash

   nomad var put nomad/jobs/nagios-plugins-collection client_secret=@client-secret

Troubleshooting
---------------

Use the installed command's ``--help`` to verify its options and path. For
certificate failures, verify hostname/SAN, validity and CA trust; supply a CA
file rather than disabling verification. Report OS, Python and package versions
with a redacted reproducer through the repository's issue tracker.
