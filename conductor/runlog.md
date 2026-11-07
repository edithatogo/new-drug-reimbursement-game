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
- `2026-07-31T22:35:49Z` (T12 planning): selected the NHS England
  methodological pilot and verified DHSC/CHE source PDFs outside Git. The
  pilot remains candidate-only until Atlas and health-economics review.
- `c9efd96` and `cb6d3d2` (T12): implemented and independently reviewed a
  bounded candidate-only source contract, NHS England dossier, role/scenario
  readiness engine, exact CLI receipt, and non-promotion boundary. The full
  gate passed with 86 Python and 29 Rust tests, Ruff, strict mypy, reproducible
  packaging, governance and scope checks, and clean resolution of all four
  pinned ecosystem repositories. Scenario 1 is `candidate_only`; Scenarios
  2-4 are `not_identifiable`. Atlas approval, independent health-economic
  approval, and a specific displaced programme remain external gates.


## 2026-11-08 — Paignia source seed and PR #101 reconciliation

- Started from main `f6c1c87b6b00875b33c1e19401c1de09481913ce` (PR #102) and
  incorporated PR #101 head `c7b2539b60ecb6457c75164c2a759730f5c1ec7c` without
  replacing main's seventeen-leaf static/dynamic qualification plan.
- Renamed the existing generic Rust packages to `paignia-core` / `paignia-solve`
  inside the incubator; updated active manifests/imports/commands/guards and
  preserved Apache-2.0 notices in root and both package directories. Solver
  behavior is unchanged: source comparison normalized only crate-doc comments
  and the core import name and matched both old implementations exactly.
- Added `paignia_static_game` in the application: a finite offer/response model
  calls existing valuation and native Paignia backward induction. The analytic
  case predicts offer 25,000, total firm revenue 100,000 and institution benefit
  zero. It does not modify the full economic model or qualify released artifacts.
- Reconciled PN01–PN04 as aliases to existing T17 ownership; retained S01–S04,
  optional adapter separation and the two-real-consumer gate. T17.03/.09 record
  partial source progress; none of the seventeen leaves is closed.
- Python 3.12.14: scope, extraction (2 crates), governance inventory, compileall
  and offline ecosystem contract validation (4 components, no clone claims)
  passed. Full unittest discovery passed **141 tests in 3.106s**. Two temporary
  guard mutations (missing core version, wrong source path) were rejected.
  Manifest/context checks and `git diff --check` passed.
- Rust/Cargo are absent. `cargo fmt`, `cargo clippy` and `cargo test` could not
  run; hosted CI must execute the native test before native success is claimed.
  `python -m ty` and `python -m basedpyright` also reported unavailable modules.
  No provider pin, standalone package publication or consumer release receipt
  is changed by this source seed.
- The user subsequently supplied `edithatogo/paignia`; the coordinating agent
  verified it as an empty repository. This local seed is transferable source for
  that next step. Standalone population and the immutable consumer switch need
  their own exact commit records; this entry does not claim either occurred.


## 2026-11-08 — immutable Paignia consumer and provider handoff

- Paignia PR #2 merged as `12b22ce7571b9c590405bf53c2c1c5862b49cd64`, with
  reviewed tree `f438caa902e07a7ec5b7be3020c94d5b7e4868e8`. Provider hosted native
  CI run `42420971781` passed on stable and Rust 1.75 before this pin was chosen.
- Removed both generic source packages from the application workspace. Cargo
  dependencies, Cargo-generated lockfile, ecosystem lock and the source manifest
  identify the same actual Paignia revision. Original source history and notices
  are preserved; generic implementation now has one owner.
- Local T17 has only application .09/.11 active. Its handoff table/metadata
  retain all 17 original IDs; 14 provider leaves moved to Paignia and .10 stays
  with the distinct second application. S01–S04 and release qualification remain
  open with their owners. No other existing provider pin was upgraded.
- Added 6 source-boundary tests: the real immutable contract passes; local core
  copy, mutable branch, Cargo lock drift, patch override and ecosystem pin drift
  are rejected. Initial discovery test expected 4 providers; its explicit
  inventory now includes the actual fifth provider, Paignia.
- Actual Rust 1.75 format, Clippy-Dwarnings and native workspace tests passed:
  **14 existing application tests plus 1 analytic Paignia consumer test**. The
  first format check corrected only the new offer-array layout. Three existing
  fixture-only vector matches were changed to checked get/copied/expect access
  for Rust 1.75 Clippy. Economic model functions are unchanged.
- Full Python discovery passed **147 tests in 2.320s**. Source guard, generated
  inventory and offline 5-component contract checks pass. The actual native
  offer test still predicts price 25,000, total revenue 100,000 and zero
  institution benefit; its domain construction remains in the application.
- Local native/Git integration is not .crate publication, full economic-model
  validity, a second real consumer, or closure of application .09/.11. Hosted
  consumer CI and its retained ty/basedpyright checks remain to run; those two
  Python tools are unavailable locally.


## 2026-11-08 — concurrent scientific plan and consumer guard reconciliation

- Observed PR #101 advance to `1d94de7238ace89af0cf10c510d0026e0e87337d`
  before publication. Reconciled its scientific supplement with the locally
  tested consumer candidate `1b83a7cf9d18fe966dee1f4cd1aa8969872824ce` in a
  fresh worktree, preserving both histories and the original main/PR #102 work.
- Retained honest solution/completeness contracts, lawful observations and
  action-mask negative controls, solver/exogenous RNG isolation, distinct signed
  information-value semantics, separate uncertainty/replicate identities and
  medicines observation/effective-known-at requirements. Provider algorithms and
  generic contracts remain in Paignia; Voiage retains arithmetic, while only
  application T17.09/.11 gain bounded future acceptance slices. Existing PR #103
  retains its strategic-pilot work. All seventeen T17 IDs remain assigned once.
- Independent review found that a local `paignia-core` at an alternate workspace
  path could bypass the original directory-only guard. The guard now requires
  the workspace's sole application member; an alternate-path regression fails
  under the old rule and passes with the new rejection. No generic core or
  compatibility package was restored.
- Moved the earlier seed's `repository_created=false`, four-component and
  Cargo-unavailable records into explicitly historical snapshots with source
  revisions. Current state records the existing provider, five components,
  available Cargo and the actual immutable revision.
- Focused guard discovery passed **7 tests in 0.012s**; full Python discovery
  passed **148 tests in 1.786s**. Scope, source guard, governance inventory,
  compileall and offline five-component contract validation passed. Rust source,
  native test, Cargo manifests/lock and ecosystem lock are byte-identical to
  the prior consumer checkpoint, where format, Clippy and all 15 native tests
  passed on Rust 1.75. This documentation/guard reconciliation makes no new
  native or scientific implementation claim.
- Provider remains `12b22ce7571b9c590405bf53c2c1c5862b49cd64`. Hosted consumer
  CI, full real-model/artifact acceptance, a second consumer, valued-input
  implementation and S01–S04 remain open. No remote write was made by this
  local reconciliation.
