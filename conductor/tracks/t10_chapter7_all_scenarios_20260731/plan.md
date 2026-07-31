# Implementation plan

## Phase 1 - Contract and tests

- [ ] Add the shared all-scenario fixture and failing Python/Rust conformance and
  invalid-domain tests.
- [ ] Automated review and focused validation checkpoint.

## Phase 2 - Scenario engines

- [ ] Implement the strict Python Chapter 7 scenario API and public exports.
- [ ] Implement the independent Rust Chapter 7 scenario evaluator in the
  reimbursement application crate.
- [ ] Automated review and focused cross-language validation checkpoint.

## Phase 3 - Interfaces and evidence

- [ ] Add the versioned CLI/schema contract and examples for all four scenarios.
- [ ] Update equation, assumption, status, model-risk, and source-conformance
  records, explicitly bounding Scenario 4 to caller-supplied `mu`.
- [ ] Automated review and full repository quality-gate checkpoint.

## Phase 4 - Completion

- [ ] Record commit-bound evidence, reconcile registry/metadata/status, and
  close the track without claiming external validation.
