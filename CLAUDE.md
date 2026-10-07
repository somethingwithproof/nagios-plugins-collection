<!--
SPDX-FileCopyrightText: 2025 Thomas Vincent
SPDX-License-Identifier: Apache-2.0
-->

# nagios-plugins-collection coding guide

Read [AGENTS.md](AGENTS.md) before making changes. It contains the repository's
architecture, canonical commands, supported boundaries and operating rules.
Follow any applicable nested instructions and the checked-out CI configuration.

## Project priorities

Preserve Nagios exit codes, threshold/performance-data contracts, bounded requests and safe failure states.

## Verification

`mise exec python@3.12 -- tox -e py312,lint,type` and the focused plugin tests.

Separate offline checks from operations that change hosts, databases, firewalls
or published artifacts. State verification limits and preserve existing controls.
Select language runtimes through `mise`; never commit local session state or secrets.
