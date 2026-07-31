# Run log

## Handoff preparation

- Preserved the original ecosystem-first Git commit.
- Added deterministic bundle-first workstation bootstrap and repository activation.
- Added owner-controlled ecosystem clone discovery with local and portable manifests.
- Added baseline CI and repository-local Conductor tracks.
- Remote creation, authentication, sibling-clone resolution, and implementation are
  deliberately activated on the user's Codex workstation.

## Workstation activation — 2026-07-27

- Restored and verified the bundle history, annotated tags, and source-ZIP identity.
- Resolved clean cache clones for all four locked ecosystem components.
- Created and normalized the private GitHub repository and pushed required refs.
- Corrected baseline defects in `a31207b`; local gates and Actions run
  `30254455585` passed.
- Enabled the `Protect main` ruleset with stable `python` and `rust` checks.
- Created non-duplicate implementation issues #3 through #11 for T01-T09.

## Implementation milestones

- `0e6e968` (T01): added Python and Rust threshold sign, special-case,
  currency-rescaling, and fail-closed input invariants. The full gate passed
  with 27 Python tests and six Rust workspace tests.
- `9717125` (T02): added machine-readable validation failures for empty
  identifiers, duplicate actions, invalid payoffs, and unreachable nodes in the
  domain-neutral Rust game graph. The full Python/Rust gate remained green.
- Exact Chapter 7 technical-efficiency interpretation, independent
  health-economics review, and regulator-grade validation remain unresolved
  external/domain gates.
- `c2c95dd` (T01): added an independently written dimensional derivation and
  assumption ledger bound to executable scope checks; external source and
  health-economics review remain pending.
- `2477281` (T01): added a versioned economics fixture consumed independently
  by Python and Rust; 29 Python tests and eight Rust workspace tests passed.
- `e661e6a` (T01): added dependency-free deterministic monotonicity sweeps;
  31 Python tests and ten Rust workspace tests passed.
- `f2a065c` (T01 review fix): made the public Rust reallocation calculation
  fail closed and aligned fixture decisions with Python's scale-aware tolerance.
  The complete gate passed; T01 remains open only for its explicit source and
  independent health-economics review tasks.
- `2026-07-31T07:55:00Z` (T01 review): verified the authorized Pekarsky
  (2015) PDF by SHA-256 and visually reviewed Chapter 7 printed pages 116-119.
  An independent technical panel confirmed source fidelity for implemented
  Scenario 3 equations 7.2-7.5, `beta_c^alpha`, EVCI, and sign conditions.
  T01 is complete for that bounded scope; Scenario 4 `mu`/`beta_c^v` remains
  explicitly excluded.
- `2026-07-31T08:28:00Z` (T10 source expansion): obtained the public University
  of Adelaide repository copy of Pekarsky (2012), verified SHA-256
  `10b727b52872483ac60f3958c9e4dd2c6fba2d1e875b1fac5cd9d52469341723`,
  and visually reviewed Appendix 5 PDF pages 231-234. This supersedes the
  earlier Scenario 4 source gap without changing T01's historical scope.
- `217814e` (T10): implemented strict scenario-specific Python and Rust
  evaluators for all four Chapter 7 contexts, a shared cross-language fixture,
  fail-closed domain checks, a versioned schema, four examples, and a CLI
  surface. Scenario 4 validates the Appendix 5 dynamic identity and requires an
  evidence revision; empirical parameter estimation remains external.
- `2026-07-31T22:08:03Z` (T11 planning): specified an approved-derived
  parameter-evidence contract, deterministic Chapter 7 calibration receipts,
  and pinned-compatible Atlas/Voiage boundaries. Real calibration data and
  health-economics approval remain explicit external gates.
- `334607b` and `e06c75e` (T11): implemented strict evidence packets,
  all-scenario evidence selection, deterministic receipts, and aligned Voiage
  samples with synthetic decision-use prohibition.
- `613d01c` (T11 review fix): made the explicit ignored ecosystem cache
  deterministically outrank equivalent sibling worktrees; all four ecosystem
  pins resolve without mutating sibling checkouts.
- `c90a31a` (T11): integrated the governed Atlas reader, CLI, documentation,
  and pinned Voiage `ValueArray`/`ParameterSet` handoff. The complete gate
  passed with 75 Python and 29 Rust tests; real evidence, health-economics
  review, and Voiage licence reconciliation remain external.
