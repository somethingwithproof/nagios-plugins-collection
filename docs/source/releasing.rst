.. SPDX-FileCopyrightText: 2025 Thomas Vincent
.. SPDX-License-Identifier: Apache-2.0

Releases and migration
======================

.. image:: _static/release-flow.svg
   :alt: Validate source, run CI, install packages, publish release artifacts

``pyproject.toml`` holds the version. Release Please
(``.github/workflows/release-please.yml``, configured by
``release-please-config.json``) computes the next SemVer version from the
Conventional Commit titles merged since the last release, and its release pull
request bumps every other copy: ``uv.lock``, both Helm version fields, the chart
test, the Nomad job's default image and the installation guide. The container
image's ``org.opencontainers.image.version`` label and the documentation's
version are read from ``pyproject.toml`` at build time. A test fails when the
source version appears in a tracked file that Release Please does not update.

Merging the release pull request tags ``vX.Y.Z`` on that commit, creates the
GitHub release with the generated notes and calls the Release workflow with the
version. The Release workflow can also be run by hand on main for an existing
version; it checks that the version is complete SemVer matching the source,
that an existing tag identifies the checked-out commit and that the source
belongs to main. Pushing a tag by hand does not publish.

The release pull request is opened with ``GITHUB_TOKEN`` unless the
``RELEASE_PLEASE_TOKEN`` secret holds a fine-grained token or GitHub App token
with contents and pull-request write access. GitHub does not start workflows
for pull requests opened with ``GITHUB_TOKEN``, so without that secret, close
and reopen the release pull request to run CI before merging it.

Publication reuses full CI, including native package builds and installation
on Ubuntu 24.04 and Rocky Linux 9. GitHub assets include the wheel, source
archive, Helm chart, Debian package, RPM, commit metadata and ``SHA256SUMS``.
Public assets receive GitHub build provenance attestations. GHCR images are
scanned, signed by immutable digest and promoted to the SemVer tag after checks;
prereleases do not replace the latest image tag. Build metadata maps ``+`` to
``_`` in container tags because OCI tags do not accept plus signs.

The separate ``Publish verified Python release`` workflow on main downloads
the matching GitHub release's wheel and source archive, verifies checksums and
the Release workflow's tag-bound attestations, then runs Twine checks. Dry-run
is the default and may validate a review branch. Uploads require main and
select the PyPI or TestPyPI environment;
it publishes those verified assets without rebuilding them. The repository's
configured environment credentials supply upload authentication.

Version 3.0 changes
-------------------

The public repository's ``MIGRATION.md`` lists the 3.0 changes to options,
exit codes, thresholds and output, and the steps to upgrade command
definitions.

Version 2.0 changes
-------------------

HTTP checks now verify certificates by default; use ``--ca-file`` for private
trust. The async command and HTTP utilities no longer accept timeout parameters:
wrap calls in ``asyncio.timeout(seconds)``. CLI deadlines remain supported and
HTTP requests also have a 30-second transport ceiling. HTTP SLI latency units
are milliseconds; website-status latency units are seconds. All failed probes
remain CRITICAL and cancellation reaps subprocess children.

All 21 entrypoints are exercised by native-package installation tests. Native
packages bundle Linux x86-64/Python 3.12 wheels and use OS libpq; the container
uses platform-specific runtime wheels. The public repository's ``MIGRATION.md``
provides the complete version-2 upgrade checklist.

Third-party clients retain their original notices. The runtime license audit
uses the locked shipping distributions and explicit named exceptions for the
existing Paramiko and Psycopg LGPL clients; development tools do not expand
the runtime distribution policy.
