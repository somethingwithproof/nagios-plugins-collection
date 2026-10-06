.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

Releases and migration
======================

.. image:: _static/release-flow.svg
   :alt: Validate source, run CI, install packages, publish release artifacts

The project version in ``pyproject.toml`` and both Helm version fields must
agree. Use complete SemVer, with a ``v`` prefix on Git tags. The Release workflow
accepts a matching tag or a manual version on main. It checks that an existing
tag identifies the checked-out commit and that the source belongs to main.

Publication reuses full CI, including native package builds and installation
on Ubuntu 24.04 and Rocky Linux 9. GitHub assets include the wheel, source
archive, Helm chart, Debian package, RPM, commit metadata and ``SHA256SUMS``.
Public assets receive GitHub build provenance attestations. GHCR images are
scanned, signed by immutable digest and promoted to the SemVer tag after checks;
prereleases do not replace the latest image tag. Build metadata maps ``+`` to
``_`` in container tags because OCI tags do not accept plus signs.

Version 2.0 changes
-------------------

HTTP checks now verify certificates by default; use ``--ca-file`` for private
trust. The async command and HTTP utilities no longer accept timeout parameters:
wrap calls in ``asyncio.timeout(seconds)``. CLI deadlines remain supported and
HTTP requests also have a 30-second transport ceiling. HTTP SLI latency units
are milliseconds; website-status latency units are seconds. All failed probes
remain CRITICAL and cancellation reaps subprocess children.

All 21 entrypoints are exercised by native-package installation tests. Native
packages use portable Python implementations and OS libpq; the container uses
platform-specific runtime wheels. The public repository's ``MIGRATION.md``
provides the complete version-2 upgrade checklist.

Third-party clients retain their original notices. The runtime license audit
uses the locked shipping distributions and explicit named exceptions for the
existing Paramiko and Psycopg LGPL clients; development tools do not expand
the runtime distribution policy.
