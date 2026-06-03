# Security Policy

## Supported versions

| Version | Supported          |
|---------|--------------------|
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a vulnerability

If you discover a security issue in **Paleontology Research Skills**, please
report it **privately** so it can be fixed before disclosure:

1. **Preferred**: Email the maintainer at **syxemail@yeah.net**
   with the subject line `SECURITY: <short description>`.
2. **Alternative**: Open a
   [private security advisory](https://github.com/syxscott/Paleontology-Research-Skills/security/advisories/new)
   on GitHub.

Please include:

- Affected skill / script / version
- Steps to reproduce
- Impact assessment (data exposure, RCE, DoS, etc.)
- Suggested mitigation (if any)

We aim to acknowledge reports within **5 business days** and to publish a
patch within **30 days** for high-severity issues.

## Scope

In-scope security concerns include:

- Command injection via user input passed to subprocess
- Path traversal in profile / memory / session paths
- Excessive resource consumption (memory, CPU) from crafted input
- Vulnerabilities in bundled data (e.g. malformed ICS JSON)
- Leakage of credentials or local data to upstream APIs

**Out-of-scope** (not security issues — open a regular Issue):

- Bugs in scientific results (use Issues, not security)
- Rate-limiting from upstream APIs (PBDB, CrossRef, etc.)
- Failures of the optional `Pillow` / `openpyxl` dependencies

## Disclosure

After a fix is released, we will publish a CVE-style advisory in the
[Security tab](https://github.com/syxscott/Paleontology-Research-Skills/security)
and credit reporters who wish to be acknowledged.
