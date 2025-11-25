# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | :white_check_mark: |
| 1.x.x   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please report it responsibly.

### How to Report

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. Email security concerns to: **thomas@thomasvincent.io**
3. Include the following in your report:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

| Action | Timeline |
|--------|----------|
| Initial acknowledgment | Within 48 hours |
| Preliminary assessment | Within 1 week |
| Patch for critical issues | Within 2 weeks |
| Patch for non-critical issues | Within 30 days |
| Public disclosure | After patch is released |

### What to Expect

1. **Acknowledgment**: We will confirm receipt of your report
2. **Assessment**: We will investigate and assess the severity
3. **Communication**: We will keep you informed of our progress
4. **Credit**: With your permission, we will credit you in the release notes

## Security Best Practices

When using these Nagios plugins, follow these security recommendations:

### Authentication

- **Use SSH keys** instead of passwords where possible
- Store credentials in **environment variables**, not command-line arguments
- Use a dedicated monitoring user with **minimal privileges**
- Rotate credentials regularly

### Environment Variables

The following environment variables are supported for credential management:

| Variable | Purpose |
|----------|---------|
| `NAGIOS_SSH_USER` | SSH username for remote checks |
| `NAGIOS_SSH_PASS` | SSH password (use keys instead when possible) |
| `NAGIOS_SSH_KEY` | Path to SSH private key file |
| `MONGO_PASSWORD` | MongoDB authentication password |
| `MEMBASE_PASSWORD` | Membase/Couchbase password |

### Network Security

- Run plugins from within your **trusted network**
- Use **TLS/SSL** for all HTTP-based checks
- Verify **SSL certificates** (don't disable verification)
- Use **firewalls** to restrict access to monitoring ports

### Plugin Execution

- Run Nagios/monitoring daemons as a **non-root user**
- Use **NRPE** or **SSH** for remote checks (not direct execution)
- Regularly **update** plugins to get security fixes
- Review plugin code before deployment in production

## Known Security Considerations

### SSH-Based Plugins

Plugins that use SSH (check_procs, check_ro_mounts, check_dig) should:

1. Use key-based authentication
2. Restrict the monitoring user's shell access
3. Use SSH key passphrases where possible
4. Limit commands the monitoring user can execute via `authorized_keys` restrictions

### HTTP-Based Plugins

Plugins making HTTP requests should:

1. Always verify SSL certificates
2. Use timeouts to prevent hanging
3. Sanitize any data displayed in output
4. Be aware of SSRF risks when accepting URLs as input

## Security Updates

Security updates will be released as:

1. **Patch versions** for non-breaking security fixes
2. **Minor versions** if fixes require API changes
3. **Security advisories** via GitHub Security Advisories

Subscribe to releases to stay informed about security updates.

## Vulnerability Disclosure History

| Date | CVE | Severity | Description | Fixed In |
|------|-----|----------|-------------|----------|
| - | - | - | No known vulnerabilities | - |

## Acknowledgments

We thank the following individuals for responsibly disclosing security issues:

- (Your name could be here!)
