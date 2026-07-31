# Implementation plan

## Phase 1 - Contract and tests

- [x] Add the shared all-scenario fixture and failing Python/Rust conformance and
  invalid-domain tests (`217814e`, `9800575`).
- [x] Automated review and focused validation checkpoint (`7272b29`).

## Phase 2 - Scenario engines

- [x] Implement the strict Python Chapter 7 scenario API and public exports
  (`217814e`).
- [x] Implement the independent Rust Chapter 7 scenario evaluator in the
  reimbursement application crate (`217814e`).
- [x] Automated review and focused cross-language validation checkpoint
  (`9800575`, `7272b29`).

## Phase 3 - Interfaces and evidence

- [x] Add the versioned CLI/schema contract and examples for all four scenarios
  (`217814e`, `7272b29`).
- [x] Update equation, assumption, status, model-risk, and source-conformance
  records, explicitly bounding Scenario 4 to evidence-bound inputs (`9800575`).
- [x] Automated review and full repository quality-gate checkpoint (`7272b29`;
  60 Python tests and all 29 Rust workspace tests passed).

## Phase 4 - Completion

- [x] Record commit-bound evidence, reconcile registry/metadata/status, and
  close the track without claiming external validation (closeout commit).
