.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

Introduction
============

The collection checks HTTP content and latency, certificates, DNS, filesystems,
Kubernetes nodes, PostgreSQL, Redis and AWS services. Use the plugin index for
the complete installed command set. Each command's ``--help`` is authoritative
for its arguments; legacy health checks retain their specific interfaces.

Supported platforms
-------------------

Python 3.11–3.14 are exercised in CI. Native Debian packages are tested on Ubuntu
24.04; RPMs are tested on Rocky Linux 9. The container uses maintained Python
3.14 on Debian slim. The Helm chart validates maintained Kubernetes 1.35–1.37.
Unmaintained platforms and Python releases are outside the support contract.
CI and release publication fail when a declared platform reaches its retirement
date; maintainers must update the matrix and policy before publishing again.

Python retirement dates conservatively use the first day of the upstream EOL
month. OS eligibility ends at standard/full support, before extended phases.
The policy was reviewed on 2026-10-06 against the upstream lifecycle pages:

* `Python lifecycle <https://devguide.python.org/versions/>`_
* `Ubuntu lifecycle <https://ubuntu.com/about/release-cycle>`_
* `Rocky Linux lifecycle <https://docs.rockylinux.org/latest/releases/>`_
* `Kubernetes releases <https://kubernetes.io/releases/>`_

Monitoring semantics
--------------------

Exit codes are OK=0, WARNING=1, CRITICAL=2 and UNKNOWN=3. HTTP/TLS checks verify
the peer; a private CA can be supplied explicitly. HTTP SLI latency thresholds
are milliseconds; website thresholds are seconds. JSON and performance data
accompany results where the command supports those outputs.

CI verifies Python APIs, all installed entrypoints, trust and freshness behavior,
service-client contracts, coverage, formatting, typing, documentation, security,
Helm manifests and disposable-container end-to-end checks. These checks test
the plugin protocol; they do not claim a live Nagios-server version matrix.
