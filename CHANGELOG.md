<!--
SPDX-FileCopyrightText: 2025 Thomas Vincent
SPDX-License-Identifier: Apache-2.0
-->

# Changelog

Release Please writes each release's section from the Conventional Commit
titles of the pull requests merged since the previous release; see
[Versioning](docs/source/contributing.rst) for what makes a release major,
minor or patch. Upgrade steps for breaking changes are in
[MIGRATION.md](MIGRATION.md).

## [3.0.0](https://github.com/somethingwithproof/nagios-plugins-collection/compare/v2.0.1...v3.0.0) (2026-11-12)


### ⚠ BREAKING CHANGES

* -w/-c now change the result of check_dns_health, check_k8s_node_status (unready node count) and check_oauth2_token (expires_in; use a lower bound such as 300:). With thresholds, a token response without expires_in is UNKNOWN.
* **thresholds:** -w/-c "@" is a usage error (exit 3), and perfdata thresholds are written in canonical form.
* **http:** HTTP checks report a response body larger than --max-response-bytes (10 MiB by default) as UNKNOWN, and long status messages and output are truncated.
* **check_component_status:** a component with status ok but no valid updated timestamp is UNKNOWN instead of OK.
* **check_log_errors:** a search answer whose hits.total relation is gte is UNKNOWN instead of being thresholded as an exact count.
* **secrets:** secret files that are not regular files, including pipes from shell process substitution, are rejected as usage errors, as are files larger than 64 KiB or not UTF-8 text.
* **thresholds:** check_tls_expiry and check_website_status reject range forms, fractional days and negative or non-finite seconds for -w/-c as usage errors, and their perfdata now includes the warning and critical thresholds.
* for check_log_errors, check_postgres_replication_lag, check_queue_depth, check_backup_freshness and check_cloud_budget a value equal to the -w/-c number no longer alerts (a plain N alerts above N); use N-1 to keep alerting at N for integer measurements. See MIGRATION.md.
* **http:** HTTP checks share one option set (--ca-file, --insecure, --client-cert/--client-key, --retries/--retry-delay, --username/--password, --bearer-token, --api-key/--api-key-header); credentials are dropped on cross-origin redirects and an HTTPS to HTTP redirect with credentials is CRITICAL; transient failures are retried by default; contradictory credential or TLS options exit 3; nagios_plugins.utils.check_http_endpoint(_async) and nagios_plugins.services.http_tls are removed and WebsiteStatusChecker takes settings instead of retries. See MIGRATION.md.
* every plugin run ends "UNKNOWN - Plugin timed out after N seconds" (exit 3) one second after --timeout, even inside DNS resolution, retries or child processes; --timeout must be a whole number of at least 1; check_dig --retries attempts share the timeout and wait 1 second between attempts. See MIGRATION.md.
* check_component_status and check_mongodb_health status lines lose the doubled "CRITICAL - CRITICAL - " prefix; commands without thresholds reject -w/-c; a malformed -w/-c range exits 3 before the check runs; nagios_plugins.base.run_async_check is removed (derive from AsyncNagiosPlugin). See MIGRATION.md.
* **release:** the 2.x fixes in #212-#218 change results for existing command definitions: Nagios ranges follow the plugin guidelines (a plain N alerts outside 0..N, endpoints inclusive) and perfdata uses the standard warn;crit;min;max fields; usage errors exit 3 and logs go to stderr only; missing or malformed monitoring data reports UNKNOWN or CRITICAL instead of OK; credentials are redacted and secrets can come from files or the environment; check_http_sli takes separate latency and error-rate thresholds; the Helm and Nomad deployments no longer retry check results and pin the plugin image; and the TLS, Cost Explorer, mount-exclude and Redis threshold checks were corrected. See MIGRATION.md, Upgrading to 3.0.

### Features

* apply -w/-c in check_dns_health, check_k8s_node_status and check_oauth2_token ([#238](https://github.com/somethingwithproof/nagios-plugins-collection/issues/238)) ([2358cce](https://github.com/somethingwithproof/nagios-plugins-collection/commit/2358cce29cadce61db0ab8868840f71224571754))
* end every run UNKNOWN shortly after --timeout ([#222](https://github.com/somethingwithproof/nagios-plugins-collection/issues/222)) ([8d53392](https://github.com/somethingwithproof/nagios-plugins-collection/commit/8d5339298cd52cafe28c25911c92d8d8a5bed2f3))
* evaluate the remaining -w/-c thresholds as Nagios ranges ([#227](https://github.com/somethingwithproof/nagios-plugins-collection/issues/227)) ([8f5fef9](https://github.com/somethingwithproof/nagios-plugins-collection/commit/8f5fef9e45ef886cdbe14a7f34d4d28eecb69cba))
* generate Icinga 2, Nagios and man page definitions from the parsers ([#228](https://github.com/somethingwithproof/nagios-plugins-collection/issues/228)) ([6a547cf](https://github.com/somethingwithproof/nagios-plugins-collection/commit/6a547cf89514fd9c5377d0315217ef5494b0acd9))
* **helm:** pin the plugin image with image.digest ([#241](https://github.com/somethingwithproof/nagios-plugins-collection/issues/241)) ([9632592](https://github.com/somethingwithproof/nagios-plugins-collection/commit/9632592363599dee772450f56fb5f6b5886e51f9))
* **http:** share one HTTP client, credential and retry policy across checks ([#223](https://github.com/somethingwithproof/nagios-plugins-collection/issues/223)) ([faadbc4](https://github.com/somethingwithproof/nagios-plugins-collection/commit/faadbc4e104dafa070963e9384d85bcff15a4c75))


### Bug Fixes

* **check_backup_freshness:** treat future timestamps as fresh and bound the listing ([#235](https://github.com/somethingwithproof/nagios-plugins-collection/issues/235)) ([b321e2e](https://github.com/somethingwithproof/nagios-plugins-collection/commit/b321e2eaf885664318d4af3f428cd334a895c48d))
* **check_component_status:** report components without an update time as UNKNOWN ([#237](https://github.com/somethingwithproof/nagios-plugins-collection/issues/237)) ([23d9202](https://github.com/somethingwithproof/nagios-plugins-collection/commit/23d9202036ac92d64e47bba1c2bf01df5dfde75e))
* **check_http_sli:** keep latency percentiles within the measured samples ([#232](https://github.com/somethingwithproof/nagios-plugins-collection/issues/232)) ([9798176](https://github.com/somethingwithproof/nagios-plugins-collection/commit/97981764c920c463e1d6da5b1186b28c947a5e73))
* **check_http_sli:** separate latency and error-rate thresholds ([#217](https://github.com/somethingwithproof/nagios-plugins-collection/issues/217)) ([7038b17](https://github.com/somethingwithproof/nagios-plugins-collection/commit/7038b17efaabc0a5e7b25ddfbeda508bd4b04b43))
* **check_log_errors:** count every matching hit instead of stopping at 10,000 ([#236](https://github.com/somethingwithproof/nagios-plugins-collection/issues/236)) ([cb33281](https://github.com/somethingwithproof/nagios-plugins-collection/commit/cb33281e55ecf60b128746d80e99d520f180db0b))
* **ci:** attest the SPDX JSON SBOM with cosign --type spdxjson ([#211](https://github.com/somethingwithproof/nagios-plugins-collection/issues/211)) ([bcb9d14](https://github.com/somethingwithproof/nagios-plugins-collection/commit/bcb9d14129cefe747a88e7bb5d96d97f7a0a1944))
* correct TLS, Cost Explorer, mount-exclude and Redis threshold checks ([#218](https://github.com/somethingwithproof/nagios-plugins-collection/issues/218)) ([41b17fd](https://github.com/somethingwithproof/nagios-plugins-collection/commit/41b17fd4e888dfcf51d247e1bcd037134589a7e9))
* **deploy:** stop retrying check results and pin the plugin image ([#216](https://github.com/somethingwithproof/nagios-plugins-collection/issues/216)) ([99883f3](https://github.com/somethingwithproof/nagios-plugins-collection/commit/99883f328962bc0e9a401d77d9c7c1df3497243a))
* **deps:** keep docutils compatible with myst-parser ([#74](https://github.com/somethingwithproof/nagios-plugins-collection/issues/74)) ([9857491](https://github.com/somethingwithproof/nagios-plugins-collection/commit/985749169563e34300385b073817fe4e2ba1626e))
* **deps:** keep multidict compatible with aiohttp ([#73](https://github.com/somethingwithproof/nagios-plugins-collection/issues/73)) ([30d4cc1](https://github.com/somethingwithproof/nagios-plugins-collection/commit/30d4cc16dc436fa0b6edf7657ef048c1398bc12c))
* **deps:** regenerate hashed lockfiles broken by dependency bumps ([#175](https://github.com/somethingwithproof/nagios-plugins-collection/issues/175)) ([0107448](https://github.com/somethingwithproof/nagios-plugins-collection/commit/01074489a8dd7f1ad2293a3a940792cc640046f5))
* **deps:** update Pydantic and core as a compatible pair ([#72](https://github.com/somethingwithproof/nagios-plugins-collection/issues/72)) ([b0b11bc](https://github.com/somethingwithproof/nagios-plugins-collection/commit/b0b11bc9fa25ea7550cffbd9bf28ba161d576066))
* **deps:** update vulnerable certificate and build-tool pins ([#145](https://github.com/somethingwithproof/nagios-plugins-collection/issues/145)) ([c4e90cb](https://github.com/somethingwithproof/nagios-plugins-collection/commit/c4e90cb72526a50542770c80238c35baa803ee03))
* **deps:** upgrade Kubernetes and preserve native package imports ([#102](https://github.com/somethingwithproof/nagios-plugins-collection/issues/102)) ([f1c401d](https://github.com/somethingwithproof/nagios-plugins-collection/commit/f1c401db4a14a43d991f1906ec3f2abf18bdb271))
* **docker:** clear Trivy HIGH findings in the runtime image ([#210](https://github.com/somethingwithproof/nagios-plugins-collection/issues/210)) ([219a4d9](https://github.com/somethingwithproof/nagios-plugins-collection/commit/219a4d94c095036ea5a20e02672f515559a96b17))
* exit UNKNOWN on usage errors and keep logs off stdout ([#214](https://github.com/somethingwithproof/nagios-plugins-collection/issues/214)) ([1fba8f6](https://github.com/somethingwithproof/nagios-plugins-collection/commit/1fba8f64ab7b521a094378a848e38c9242048d0b))
* follow Nagios range and perfdata guidelines in the shared result ([#212](https://github.com/somethingwithproof/nagios-plugins-collection/issues/212)) ([2b7916c](https://github.com/somethingwithproof/nagios-plugins-collection/commit/2b7916cf26bda813e3a99a99bb372b85a1820e8e))
* **http:** cap response bodies and plugin output ([#239](https://github.com/somethingwithproof/nagios-plugins-collection/issues/239)) ([8e15c50](https://github.com/somethingwithproof/nagios-plugins-collection/commit/8e15c502fd09a47967d9f2b1e46d397af30d3ac9))
* never report OK for empty or malformed backend answers ([#229](https://github.com/somethingwithproof/nagios-plugins-collection/issues/229)) ([50a8f03](https://github.com/somethingwithproof/nagios-plugins-collection/commit/50a8f03906599cee434507a5a825975b63cd4ece))
* redact credentials from output and accept secrets outside argv ([#215](https://github.com/somethingwithproof/nagios-plugins-collection/issues/215)) ([59fda3a](https://github.com/somethingwithproof/nagios-plugins-collection/commit/59fda3aaf5dd78e089114435f97e06e0f3b21fa2))
* **redaction:** mask registered secrets as literals and more credential forms ([#234](https://github.com/somethingwithproof/nagios-plugins-collection/issues/234)) ([cb4072c](https://github.com/somethingwithproof/nagios-plugins-collection/commit/cb4072c0f600d70593e19a22a9885325a04e4295))
* report missing monitoring data as UNKNOWN or CRITICAL, never OK ([#213](https://github.com/somethingwithproof/nagios-plugins-collection/issues/213)) ([32cb1a2](https://github.com/somethingwithproof/nagios-plugins-collection/commit/32cb1a24b4d8586305a8b20a45def13d151b4538))
* restore compatible dependency locks and validate developer installs ([#71](https://github.com/somethingwithproof/nagios-plugins-collection/issues/71)) ([1b4b024](https://github.com/somethingwithproof/nagios-plugins-collection/commit/1b4b0248f36de11e92baf24c180d2b75ff77d406))
* **secrets:** read secret files within the run deadline and refuse non-regular files ([#233](https://github.com/somethingwithproof/nagios-plugins-collection/issues/233)) ([37fcf8f](https://github.com/somethingwithproof/nagios-plugins-collection/commit/37fcf8fb306699686eae06e8e6a577e9d23d40c8))
* **thresholds:** keep plain-number -w/-c for check_tls_expiry and check_website_status ([#231](https://github.com/somethingwithproof/nagios-plugins-collection/issues/231)) ([be9eefd](https://github.com/somethingwithproof/nagios-plugins-collection/commit/be9eefdd7215948dca378f65bf4d4008482a121a))
* **thresholds:** reject a bare @ range and write ranges in canonical form ([#242](https://github.com/somethingwithproof/nagios-plugins-collection/issues/242)) ([9cfdfc5](https://github.com/somethingwithproof/nagios-plugins-collection/commit/9cfdfc5f0b4bf1437b978080fcea979dbc6ff318))


### Build and Packaging

* **deps:** drop the unused rich runtime dependency ([#219](https://github.com/somethingwithproof/nagios-plugins-collection/issues/219)) ([b9646cf](https://github.com/somethingwithproof/nagios-plugins-collection/commit/b9646cfdb7390b455e8759aef43b11a699f09830))
* **docker:** pin python base images by digest ([#240](https://github.com/somethingwithproof/nagios-plugins-collection/issues/240)) ([f3a0e76](https://github.com/somethingwithproof/nagios-plugins-collection/commit/f3a0e765b5ef805916cb662389cd74e28719965f))
* make uv.lock the single dependency lock ([#207](https://github.com/somethingwithproof/nagios-plugins-collection/issues/207)) ([be991cc](https://github.com/somethingwithproof/nagios-plugins-collection/commit/be991cc8cad2f03d7d0e79a5097120cb8fbf2521))


### Documentation

* add monitoring-specific agent guidance and local-state exclusions ([#81](https://github.com/somethingwithproof/nagios-plugins-collection/issues/81)) ([c963751](https://github.com/somethingwithproof/nagios-plugins-collection/commit/c963751f62af34487d64e4e0b0e0fc25bca01369))
* add README status badges and Scorecard workflow ([#83](https://github.com/somethingwithproof/nagios-plugins-collection/issues/83)) ([ef25e95](https://github.com/somethingwithproof/nagios-plugins-collection/commit/ef25e9550c2e9489761ce360018c038e776afcb7))
* add the Helm and Nomad examples the installation guide references ([#220](https://github.com/somethingwithproof/nagios-plugins-collection/issues/220)) ([d620b4c](https://github.com/somethingwithproof/nagios-plugins-collection/commit/d620b4c76a820f3d0f0b1c12c095a75e9f675dd9))
* clarify project scope and verify README badges ([#82](https://github.com/somethingwithproof/nagios-plugins-collection/issues/82)) ([4dce5ba](https://github.com/somethingwithproof/nagios-plugins-collection/commit/4dce5ba850bb4198717516c0e378862ce86a78aa))


### Code Refactoring

* run every command on the NagiosPlugin base ([#221](https://github.com/somethingwithproof/nagios-plugins-collection/issues/221)) ([8e07fbe](https://github.com/somethingwithproof/nagios-plugins-collection/commit/8e07fbee6d3a1b35886414dda5bc6f026e75d3e2))


### Continuous Integration

* **release:** version releases with release-please and Conventional Commits ([#224](https://github.com/somethingwithproof/nagios-plugins-collection/issues/224)) ([9e90576](https://github.com/somethingwithproof/nagios-plugins-collection/commit/9e905767ced1fda2278a71f04c704727d796abc1))

## 2.0.1 — 2026-10-06

- Align package metadata and SPDX headers with the existing Apache-2.0 LICENSE.
- Add file-level SPDX identifiers and REUSE mappings for non-commentable files.
- Parse shipping license expressions without regex backtracking.
- Supersede the unpublished 2.0.0 candidate after the license consistency audit.

## 2.0.0 — 2026-10-06 (unpublished candidate)

Verified TLS defaults, async cancellation ownership, maintained-platform policy and wheel/Helm/DEB/RPM releases.

Documentation includes migration, installation, release checks, SVG project branding and operational diagrams.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2025-12-27

### Changed
- Python 3 modernization across the repo; removed legacy standalone scripts and vendored third-party code.
- Security: disallow shell=True in execute_command.
- Adopted Ruff + pre-commit; tightened lint/type gates and standardized formatting.
- CI cleanup and stability improvements.

### Fixed
- Multiple lint issues (flake8/ruff) and minor type issues in runtime code.

## [1.1.0] - 2025-04-11

### Added
- JSON output format support for all plugins
- Asynchronous execution support for improved performance
- Rich terminal output with progress indicators
- New `ThresholdRange` class for better threshold handling
- Added `get_directory_size` utility function
- Added `get_system_info` utility function
- Added security scanning with Bandit and pip-audit
- Added CommandResult dataclass for better command execution results
- Added timestamp to CheckResult for better tracking
- Added to_json method to CheckResult for JSON serialization

### Changed
- Modernized codebase to use maintained Python 3.11–3.14 features
- Updated all dependencies to latest versions
- Improved error handling with better error messages
- Refactored base plugin class for better extensibility
- Enhanced HTTP endpoint checking with more options
- Improved process checking across different operating systems
- Updated GitHub Actions workflow with modern actions
- Switched to modern Python packaging with pyproject.toml
- Improved documentation with more examples
- Enhanced test coverage and test organization

### Removed
- Support for Python 3.7 (now requires maintained Python 3.11–3.14)
- Deprecated utility functions replaced with modern alternatives

## [1.0.0] - 2024-01-01

### Added
- Initial release of nagios-plugins-collection
- Base plugin framework
- Core utility functions
- Initial set of monitoring plugins
- Documentation and examples
- Test suite
