# Research-only release authorization

## Scope decision — 2026-08-01

The repository owner authorized proceeding with a research-software and
methodology release only. This covers reproducible code, synthetic scenarios,
candidate-only evidence fixtures, documentation, and validation artifacts.

It does **not** authorize a calibrated reimbursement recommendation, a
regulator-facing or policy claim, promotion of candidate or raw evidence,
redistribution of source-restricted data, or closure of the NHS, Atlas,
licensing, independent-review, upstream-contract, or extraction gates.

## Release conditions

Before publishing, maintainers must verify the exact release revision, green
hosted checks, reproducible package/build evidence, the fail-closed readiness
receipt, and the absence of restricted source data. Release notes must state
that Scenario 1 is `candidate_only`, Scenarios 2–4 are `not_identifiable`, and
`approved_calibration_permitted` is false.

The external-gate request template remains authoritative for later promotion.
No calibrated or regulatory claim may be added without the required owner and
human-review receipts.
