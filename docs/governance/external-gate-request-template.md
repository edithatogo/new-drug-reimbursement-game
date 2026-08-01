# External-gate request template

Use this template when requesting the evidence and approvals needed to move
the NHS pilot beyond candidate-only readiness. Do not fill unknown fields with
inferences. A blank or explicitly unavailable field keeps the corresponding
gate pending.

## Request metadata

| Field | Value |
|---|---|
| Request ID | |
| Requesting repository revision | |
| Request date (UTC) | |
| Intended use | NHS methodological pilot only |
| Requested disposition | candidate / approved-derived / declined |

## NHS decision context

| Field | Value | Source or owner |
|---|---|---|
| Jurisdiction | | |
| Accountable payer/commissioner | | |
| Budget boundary | | |
| Service line | | |
| Decision date | | |
| Price year | | |
| Intervention | | |
| Comparator | | |
| Displaced programme | | |
| Stable programme ID | | |
| Baseline cost and unit | | |

Attach a signed owner receipt confirming that the displaced programme is the
actual decision-context source for `d`, not a generic opportunity-cost proxy.

## Atlas evidence request

Request that Reimbursement Atlas provide:

- approved-derived packet ID and immutable revision;
- parameter names, units, and price-year treatment;
- source provenance and transformation ledger;
- uncertainty representation and sampling contract;
- context alignment for `n`, `m`, `d`, `mu`, `phi`, horizon, and discounting;
- source-specific licence and redistribution terms; and
- Atlas reviewer identity, disposition, and approval date.

Raw or candidate records must not be promoted by this repository.

## Independent review request

| Field | Value |
|---|---|
| Lead health economist | |
| Organization and role | |
| Conflict declaration | |
| Independent panel members | |
| Reviewed repository revision | |
| Reviewed Atlas packet revision | |
| Primary discounting convention | |
| Sensitivities retained | DHSC 1.5% / NICE 3.5% |
| Findings and required changes | |
| Final disposition | |
| Sign-off date | |

The reviewer must explicitly address role mappings, transformations, unit
consistency, programme identity, uncertainty, discounting, and the boundary
between methodological output and reimbursement advice.

## Acceptance and closure

The request is closable only when each applicable section has an owner, exact
revision or hash, date, and explicit disposition. Until then, retain the
canonical readiness state: Scenario 1 `candidate_only`, Scenarios 2–4
`not_identifiable`, and `approved_calibration_permitted: false`.
