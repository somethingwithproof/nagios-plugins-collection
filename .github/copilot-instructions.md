<!--
SPDX-FileCopyrightText: 2025 Thomas Vincent
SPDX-License-Identifier: Apache-2.0
-->

# nagios-plugins-collection implementation and review instructions

Read [AGENTS.md](../AGENTS.md) for the complete repository-specific guidance.

## Review priorities

Preserve Nagios exit codes, threshold/performance-data contracts, bounded requests and safe failure states.

Require focused regression evidence for changed behavior and preserve existing
correctness/security checks. `mise exec python@3.12 -- tox -e py312,lint,type` and the focused plugin tests.

Flag unsupported maturity claims, hidden failures, credentials in code/logs, and
generated output presented as first-party implementation. Review permissions,
immutable Action pins and fork-secret isolation when workflows change. A skipped
check or absent check result is not proof that validation ran.

Keep changes within the requested scope and use `mise` for language runtimes.
