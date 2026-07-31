# Security

Do not report sensitive prices, confidential agreements, identifiable patient
data, credentials, or restricted source payloads in public issues. This
repository is not approved to process confidential reimbursement data. Use the
owner's private disclosure channel for vulnerabilities.

## Reporting a vulnerability

Do not open a public issue for an exploitable vulnerability. Contact the
maintainer through the private GitHub security-advisory channel for this
repository, including a minimal reproduction, affected commit or release, and
impact. Do not include patient data, confidential prices, credentials, or
restricted source material. If private advisory access is unavailable, pause
disclosure and ask the maintainer for a private channel; do not send secrets in
pull requests or issues.

The checked-in `scripts/repository_hardening.py --check` command validates the
repository-owned security/contribution context and workflow controls. GitHub
branch rulesets, visibility, and required-check settings are external controls
and must be verified in GitHub separately.
