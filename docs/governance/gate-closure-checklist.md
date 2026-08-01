# External gate closure checklist

Use this checklist when an external receipt arrives. A gate changes to
`satisfied` only after its required evidence is present, hash-bound, and
validated. Do not infer closure from a related source or local test.

## NHS displacement context

- [ ] Authoritative local payer/commissioner record attached or hash-bound.
- [ ] Service line and budget boundary identified.
- [ ] Decision date and price year recorded.
- [ ] Intervention and comparator recorded.
- [ ] Actual displaced programme and stable programme ID recorded.
- [ ] Baseline cost and unit recorded.
- [ ] Accountable owner confirms the context.

Fallback: retain TA1121 as a national candidate and leave `d` unresolved.

## Atlas-derived records

- [ ] Atlas packet ID and immutable revision recorded.
- [ ] `n`, `m`, and `d` roles align to the same programme context.
- [ ] Scenario 4 roles are present only if explicitly supported by the packet.
- [ ] Source hashes, terms, transformations, units, and uncertainty recorded.
- [ ] Atlas reviewer and approval date recorded.
- [ ] Approved packet schema and provenance validation pass.

Fallback: enable only complete scenarios and retain candidate-only status.

## Kairos contract

- [ ] Released DTO/API contract or maintainer acceptance exists.
- [ ] Exact pinned revision and contract version match.
- [ ] Exact-head CI or compatibility trace is attached.
- [ ] Native integration claim is explicitly authorized.

Fallback: keep the adapter isolated and describe compatibility as local only.

## Extraction and release

- [ ] Extraction owner identified.
- [ ] Allowed sources, fields, transformations, and destinations specified.
- [ ] Attribution and redistribution terms recorded per source.
- [ ] Raw/confidential/restricted material excluded or privately retained.
- [ ] Research-only release scope authorized.

Fallback: publish software, methodology, synthetic fixtures, and permitted
derived-only artifacts; keep extracted evidence private.

## Final promotion

- [ ] Matching Conductor gate updated with receipt path.
- [ ] Readiness and calibration receipts regenerated.
- [ ] Local tests, scope, licensing, and Conductor validation pass.
- [ ] Hosted Python and Rust checks pass.
- [ ] Unsupported HTA, reimbursement, regulatory, and policy claims remain
  disabled unless separately authorized.
