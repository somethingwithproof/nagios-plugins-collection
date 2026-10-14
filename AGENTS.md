<!--
SPDX-FileCopyrightText: 2025 Thomas Vincent
SPDX-License-Identifier: Apache-2.0
-->

# Nagios Plugins Collection agent instructions

## Project and layout

Python Nagios/Icinga plugins use the `src/nagios_plugins/` package layout.
`base.py`, `plugin_framework.py` and `utils.py` define shared monitoring behavior;
`plugins/` contains CLI checks and `services/` contains client helpers.
`pyproject.toml` declares entry points and optional integration extras.
Tests live under `tests/unit/`; Sphinx documentation is under `docs/source/`.

## Commands and dependencies

Use a supported Python from `pyproject.toml` and the CI/tox matrix. In an isolated
environment, install CI tools using the hashed `packaging/ci-requirements.txt`:

```sh
mise exec python@3.12 -- python -m pip install --only-binary=:all: --require-hashes -r packaging/ci-requirements.txt
mise exec python@3.12 -- tox -e py312,lint,type
mise exec python@3.12 -- tox -e coverage
mise exec python@3.12 -- python scripts/check_spdx.py
mise exec python@3.12 -- python scripts/check_licenses.py
```

Read `tox.ini` and `.github/workflows/ci.yml` for docs, security, container,
Helm, integration and release checks. Dependency-lock regeneration is a separate
change: preserve hashes, binary-only installation and the reviewed license policy.

## Monitoring contracts and review

Preserve Nagios statuses: OK=0, WARNING=1, CRITICAL=2, UNKNOWN=3, plus existing
output/performance-data conventions and CLI thresholds. Timeouts, authentication
errors, malformed responses and missing data must not produce OK. Redact secrets,
bound network requests and retain TLS verification. Test client behavior using
mocks or isolated fixtures; do not contact real databases/cloud accounts by default.

Add behavior-focused regression tests for changed checks and verify console entry
points and optional extras. Do not restore removed standalone legacy scripts.
Use `packaging/platform-support.json` and `packaging/license-policy.json` for
support/license assertions; keep SPDX coverage and native package validation.

## Working rules

Select required language runtimes through `mise`. Read the checked-out manifests,
lockfiles and GitHub Actions before choosing versions or commands; do not infer
support from an old README example. Keep changes focused and preserve public
interfaces, licenses and existing correctness/security checks.

Keep credentials, customer data, `.omc/`, `.worktrees/` and generated output out
of commits. Never disable checks or suppress findings just to obtain a passing
result. Report the commands run, results and untested environments. Publishing,
deploying, modifying live systems and merging require task authorization.
