# T16 evidence sourcing playbook

## Ranked sources

1. Confidential-data owner contract, field schedule, disclosure rules, and signed authorization.
2. Approved internal information-governance, legal, privacy, and security policies.
3. Official standards and regulator guidance for secure processing and disclosure control.
4. Public aggregate reports and redacted contract summaries.
5. Secondary security/privacy commentary for discovery only.

## Autonomous acquisition

- Retrieve and receipt only public policies, standards, aggregate reports,
  redacted templates, disclosure-control guidance, and public metadata.
- Build a proposed field classification, threat model, access matrix, output
  audience matrix, aggregation/redaction tests, and secure-environment specification.
- Use synthetic confidential-like fixtures to test leakage, reconstruction,
  logging, telemetry, export, deletion, and revocation controls.
- Never source actual confidential values from the web, email, local stores, or
  owner systems without the exact authorization and controlled environment.

## Options

1. **Recommended — aggregate/redacted outputs only.** Lowest disclosure risk and easiest release separation.
2. **Secure enclave computation with approved derived outputs.** Use only after all owner, contract, operator, and disclosure gates pass.
3. **Local restricted analysis with no export.** Appropriate when derived disclosure is not authorized.
4. **No-use fallback.** Preserve public/synthetic research and a negative receipt.

## Contingencies and stops

- Inaccessible policy/contract: use public standards for control design but keep data access blocked.
- Conflicting owner and destination terms: choose the more restrictive rule and seek an authoritative disposition.
- Incomplete field schedule: treat every unspecified field as confidential and prohibited.
- Stop before accessing values, credentials, agreements, secure stores, or
  external communications; also stop before any output whose disclosure risk is unresolved.

## Refresh

Reauthorize and rerun disclosure review when the contract, owner, field set,
operator, key/access policy, purpose, aggregation rule, output audience,
destination, code, model, or repository commit changes, and at every restricted release.
