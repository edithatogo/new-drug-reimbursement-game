# Implementation plan

## Phase 1 - Source and candidate contract

- [x] Record the verified source inventory and semantic distinctions.
- [x] Add the candidate-dossier schema, parser, and fail-closed tests.
- [x] Automated review and focused validation checkpoint (11 focused tests,
  Ruff, strict mypy, JSON parsing, scope validation, and exact receipt drift
  check passed; three independent reviews approved `c9efd96`).

## Phase 2 - Scenario readiness

- [x] Add deterministic role/scenario readiness assessment and tests for all
  four Chapter 7 scenarios.
- [x] Create the NHS England candidate dossier and readiness receipt.
- [x] Prove the dossier cannot enter the approved calibration path.
- [x] Automated review and focused validation checkpoint.

## Phase 3 - Interface and completion

- [x] Add the CLI readiness command and pilot documentation.
- [x] Run CLI and source-receipt smoke checks.
- [x] Run whole-track review and full repository validation (86 Python and 29
  Rust tests; Ruff, strict mypy, packaging, scope, governance, extraction,
  hardening, and all four pinned ecosystem checks passed at `cb6d3d2`).
- [x] Record hash-chained evidence and reconcile Conductor state while leaving
  external gates pending.

## Review fixes

- [x] In `c9efd96`, aligned candidate units with the approved packet, separated
  decision alignment from Scenario 4 investment-programme identity, bounded
  dossier size, replaced Cartesian compatibility searches with grouped checks,
  corrected PDF locations and source hashes, and separated study periods from
  unknown monetary price years.
- [x] In the T12 review remediation, applied Ruff's deterministic import and
  `__all__` ordering fix in `src/reimbursement_game/__init__.py` after hosted
  CI reported `I001` and `RUF022`.
