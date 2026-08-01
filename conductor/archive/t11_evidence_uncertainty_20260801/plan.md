# Implementation plan

## Phase 1 - Evidence contract

- [x] Add tests and a strict JSON schema for versioned parameter evidence
  records and packets (`334607b`).
- [x] Implement immutable evidence-record and packet parsing with fail-closed
  provenance, approval, marginality, unit, context, and uncertainty checks
  (`334607b`).
- [x] Automated review and focused validation checkpoint (`334607b`; five
  focused tests, Ruff, strict mypy, and JSON parsing passed).

## Phase 2 - Scenario calibration

- [x] Add tests for Scenario 1-4 evidence-role assembly and calibration
  receipts (`e06c75e`).
- [x] Implement compatible-record selection, scenario input assembly, and
  deterministic provenance receipts without duplicating Chapter 7 equations
  (`e06c75e`).
- [x] Automated review and focused validation checkpoint (`e06c75e`; four
  focused tests, Ruff, and strict mypy passed).

## Phase 3 - Atlas and Voiage boundaries

- [x] Strengthen the Atlas derived-export adapter to parse the governed packet
  contract and reject raw, unapproved, or incompatible records (`c90a31a`).
- [x] Prepare aligned parameter and strategy-value samples for the pinned
  Voiage `ParameterSet`/`ValueArray` API, with no local VOI algorithm
  (`e06c75e`, `c90a31a`).
- [x] Add a synthetic non-empirical fixture, CLI validation, examples, and
  boundary documentation (`334607b`, `c90a31a`).
- [x] Automated review and ecosystem integration checkpoint (`613d01c`,
  `c90a31a`; focused tests and actual pinned Voiage schema smoke passed).

## Review fixes

- [x] Prefer the explicit ignored bootstrap cache over equivalent sibling
  worktrees while retaining canonical-remote, pin, and cleanliness checks;
  this closed the Voiage discovery ambiguity without mutating siblings
  (`613d01c`).

## Phase 4 - Completion

- [x] Run the full repository quality gate, record commit-bound evidence, and
  reconcile Conductor registry, status, run log, and external gates (75 Python
  tests, 29 Rust tests, Ruff, strict mypy, full ecosystem discovery, and actual
  pinned Voiage schema smoke passed; closeout commit).

## Post-closeout reconciliation

- [x] Advance the Voiage pin to `4b93ee04231b` after README, Apache-2.0
  `LICENSE`, package metadata, and exact-head upstream CI aligned; regenerate
  the governance inventory and append the licence receipt. Atlas source terms
  and human evidence approval remain external.
