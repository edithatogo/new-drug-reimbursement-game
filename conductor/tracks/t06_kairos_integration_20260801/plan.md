# Implementation plan

## Phase 1 - Activate and establish the boundary

- [x] Activate T06 and record the pinned Kairos contract.
- [x] Harden event normalization and add a deterministic trace receipt
  (`953491b`).

## Phase 2 - Validate integration

- [x] Add focused tests and trace documentation (`953491b`).
- [x] Run the pinned contract smoke and record any environment boundary; the
  adapter remains proposal-only until Kairos releases stable event-code/DTO
  agreement.

## Phase 3 - Completion

- [x] Run review and the full repository quality gate (99 Python and 29 Rust
  tests; scope, governance, extraction, hardening, compilation, and offline
  ecosystem checks passed).
- [x] Mark T06 complete, record evidence, and archive the track.
