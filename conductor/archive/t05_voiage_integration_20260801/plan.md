# Implementation plan

## Review fixes

- [x] Tightened direct-bundle validation for finite parameter samples, unique
  roles, and non-empty strategy names (`9ebf993`).

## Phase 1 - Activate and inspect the boundary

- [x] Activate T05 and record the pinned Voiage boundary.
- [x] Implement a deterministic handoff receipt over validated samples
  (`c76486f`).

## Phase 2 - Adapter validation

- [x] Add focused tests for receipt determinism and fail-closed inputs
  (`c76486f`).
- [x] Run the pinned optional-runtime schema smoke where available; the pinned
  checkout was found, but NumPy failed to load due to missing
  `libcblas.3.dylib`, and the adapter returned its documented fail-closed
  error.
- [x] Update integration documentation and evidence (`c76486f`).

## Phase 3 - Completion

- [x] Run review and the full repository quality gate (96 Python and 29 Rust
  tests; scope, governance, extraction, hardening, compilation, and offline
  ecosystem checks passed).
- [x] Mark T05 complete, record evidence, and archive the track.
