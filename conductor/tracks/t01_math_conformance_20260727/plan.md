# Implementation plan

- [x] Add threshold-zero, sign, special-case, unit-rescaling, and invalid-input
  invariants in Python and Rust (`0e6e968`).
- [x] Write the independent dimensional derivation and assumption ledger
  (`c2c95dd`).
- [x] Add a versioned shared conformance fixture with Python and Rust consumers
  (`2477281`).
- [x] Add monotonicity/property sweeps without introducing a capability
  dependency (`e661e6a`).
- [x] Apply review fixes for Rust fail-closed semantics and decision tolerance
  (`f2a065c`).
- [x] Run automated review and the complete repository quality gate.
- [x] Record exact Chapter 7 source verification and independent technical-panel
  review for implemented Scenario 3; keep Scenario 4 `mu` explicitly excluded
  (`4ef89bc`, current evidence update).
