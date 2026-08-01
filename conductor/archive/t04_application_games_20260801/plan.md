# Implementation plan

## Phase 1 - Game 1

- [x] Activate T04 and record its source/equation boundary (`f2a0438`).
- [x] Add the exact continuous-price grid conformance solver and variants
  (`a61f528`).
- [x] Add deterministic tests and source mapping (`a61f528`).

## Phase 2 - Games 2 and 3

- [x] Implement the Game 2 financing/R&amp;D decision model and payoffs
  (`a61f528`).
- [x] Implement the Game 3 lifecycle/innovation/contract model and spillovers
  (`a61f528`).
- [x] Add deterministic fixtures, tests, and documentation (`a61f528`).

## Phase 3 - Completion

- [x] Run phase reviews and the full repository quality gate (95 Python and
  29 Rust tests; scope, governance, extraction, hardening, compilation, and
  offline ecosystem checks passed).
- [x] Mark T04 completed, record evidence, and archive the track.

## Review fixes

- [x] Added the explicitly named bargaining, net-price rebate, and contract
  enforcement Game 1 variants after review (`c96bb55`); focused tests and Ruff
  passed.
