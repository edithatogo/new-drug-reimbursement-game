# T16 public-control evidence and gap assessment

## Disposition

Use aggregate or redacted outputs only, with public execution limited to code,
methodology, and explicitly synthetic demonstrations. Public control guidance
does not authorize access to confidential values or release of derived outputs.

The DHSC secure-data-environment policy, NHS Five Data Safes, ICO
anonymisation/pseudonymisation guidance, NCSC access-logging controls, and ONS
disclosure-control policy independently support default-deny access, data-owner
control, approved users and projects, protected settings, minimized audit logs,
case-specific output checking, and retained decision trails.

## Implemented repository-owned controls

- A default-deny disclosure matrix labels audience, status, synthetic-only
  eligibility, export permission, suppression baseline, destination, authorizer,
  and invalidation triggers.
- Public results are code/methodology or synthetic-only; restricted and
  reconstructable outputs remain non-exportable.
- The net-rebate application example is explicitly synthetic. Its output is not
  a confidential-safe result and must not be used with actual confidential values.
- Automated validation checks the disclosure matrix and research-only release
  boundary. Synthetic tests exercise suppression and public-serialization denial.

The initial `k >= 5`, rounding, complementary-suppression, and dominance-review
settings are a conservative synthetic control baseline, not NHS, owner, legal,
privacy, security, or output-release approval.

## Remaining external gates

1. Named data-owner permission and a complete field schedule.
2. Binding contract/NDA, lawful basis, privacy and information-governance approval.
3. Approved operators and an accredited or expressly approved controlled environment.
4. Per-output disclosure review and destination-specific authorization bound to
   the exact source packet, code, model, aggregation, recipient, and commit.

If any gate is absent, the mandatory contingency is public/synthetic-only work
and a negative receipt; no confidential access, computation, or export occurs.
