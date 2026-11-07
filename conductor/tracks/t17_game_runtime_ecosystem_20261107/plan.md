# T17 implementation plan — execution pending

Each leaf changes one behavior and touches at most five files. Paths are
repository-relative unless prefixed with a consumer name. New paths and test
targets below are explicitly **future**: create the test first, observe the
distinguishing failure, then implement the behavior. A nonexistent target or a
filtered Cargo run with zero matching tests is not a pass. If a leaf needs more
files or another behavior, split it into a linked leaf before implementation.

`local` means routine implementation, diff review, and focused checks.
`specialist` adds independent agent review at the named numerical or public
contract boundary. Neither label adds a repeated human approval gate. Before a
phase closes, record exact command results and relevant CI once; rerun broader
checks only for an identified risk or required repository gate. Provider pin
changes require their own qualified migration leaf, not a hidden extra edit.

## Phase A — package boundary

### [ ] T17.01 — expose a versioned generic game/result contract

- Behavior: validate the declared semantic and result schema version, rejecting
  unsupported versions explicitly while preserving UOGTO identifiers.
- Depends on: T02's existing bounded implementation; no new provider pin.
- Execution: specialist, public contract and UOGTO semantics.
- Files (4): `crates/uogto-game-core/src/lib.rs`,
  `crates/uogto-game-core/tests/runtime_contract.rs` (future),
  `docs/architecture/game-runtime-contract-v1.md` (future),
  `fixtures/conformance/game-runtime-contract-v1.json` (future).
- Check: `cargo test --locked -p uogto-game-core --test runtime_contract`
  (future target); include unknown-version and unsupported-representation cases.

### [ ] T17.02 — reject Kairos in the static package dependency closure

- Behavior: fail the boundary guard if either generic crate gains a direct or
  transitive Kairos dependency; permit it only in the optional adapter package.
- Depends on: T17.01.
- Execution: local.
- Files (3): `scripts/validate_extraction.py`, `tests/test_extraction.py`
  (future), `.github/workflows/ci.yml`.
- Checks: `python -m unittest discover -s tests -p 'test_extraction.py'`
  (future suite), `python scripts/validate_extraction.py`, and
  `cargo test --locked -p uogto-game-core -p uogto-game-solve` (existing packages).
  The guard must inspect Cargo's resolved dependency graph and reject a seeded
  transitive violation, not just search top-level manifest strings.

### [ ] T17.03 — consume the packaged crates outside this workspace

- Behavior: build a standalone consumer from local package artifacts without
  importing application code or relying on the provider source tree.
- Depends on: T17.02.
- Execution: local; preserve the agreed public contract.
- Files (5): `crates/uogto-game-core/Cargo.toml`,
  `crates/uogto-game-solve/Cargo.toml`, `Cargo.lock`,
  `scripts/validate_game_packages.py` (future),
  `tests/test_game_packages.py` (future).
- Checks: `cargo test --locked -p uogto-game-core -p uogto-game-solve`;
  `python scripts/validate_game_packages.py` (future helper). The helper must
  unpack the produced artifacts into a temporary standalone consumer, resolve
  their local artifact dependency explicitly, then run `cargo test --locked
  --manifest-path <temporary-consumer>/Cargo.toml`. Record artifact hashes; no
  registry publication or repository extraction is part of this leaf.

## Phase B — inherited numerical methods

### [ ] T17.04 — implement the declared four-stage replicator step (S01)

- Behavior: advance supported continuous replicator dynamics by the declared
  four-stage RK4 update, retaining the legacy Euler result under its own version.
- Depends on: T17.01; exact upstream API/caller inventory recorded first.
- Execution: specialist, numerical integration.
- Files (4): `crates/uogto-game-solve/src/lib.rs`,
  `crates/uogto-game-solve/src/replicator.rs` (future),
  `crates/uogto-game-solve/tests/replicator_rk4.rs` (future),
  `docs/validation/replicator-rk4.md` (future).
- Check: `cargo test --locked -p uogto-game-solve --test replicator_rk4`
  (future target). Use analytic logistic evolution and step-refinement order;
  include time-varying fitness, discontinuity handling, positivity/conservation,
  and a negative control that fails for Euler relabelled as RK4.

### [ ] T17.05 — return a qualified mixed-Nash result (S02)

- Behavior: solve the explicitly supported game class with the named mixed-Nash
  algorithm, returning explicit unsupported/nonconverged statuses elsewhere.
- Depends on: T17.01; exact upstream API/caller inventory recorded first.
- Execution: specialist, equilibrium algorithms.
- Files (5): `crates/uogto-game-solve/src/lib.rs`,
  `crates/uogto-game-solve/src/mixed_nash.rs` (future),
  `crates/uogto-game-solve/tests/mixed_nash.rs` (future),
  `fixtures/conformance/mixed-nash-v1.json` (future),
  `docs/validation/mixed-nash.md` (future).
- Check: `cargo test --locked -p uogto-game-solve --test mixed_nash`
  (future target). Freeze independent fixtures and residual tolerances for
  dominance, matching pennies, coordination, degeneracy, multiple equilibria,
  and rectangular games. Include the upstream dominant-action counterexample.
  Account explicitly for support-enumeration and Lemke–Howson promises; an
  unimplemented algorithm stays unsupported, never silently substituted.

### [ ] T17.06 — solve the declared correlated-equilibrium program (S03)

- Behavior: return a distribution satisfying the actual incentive constraints
  and declared objective, with solver status and residuals.
- Depends on: T17.01; qualified solver-backend decision before dependency work.
- Execution: specialist, optimization and equilibrium constraints.
- Files (5): `crates/uogto-game-solve/src/lib.rs`,
  `crates/uogto-game-solve/src/correlated_equilibrium.rs` (future),
  `crates/uogto-game-solve/tests/correlated_equilibrium.rs` (future),
  `fixtures/conformance/correlated-equilibrium-v1.json` (future),
  `docs/validation/correlated-equilibrium.md` (future).
- Check: `cargo test --locked -p uogto-game-solve --test correlated_equilibrium`
  (future target). Compare feasibility, incentive residuals, and objective with
  independent solutions, including a case distinguishing a correlated optimum
  from a product distribution. Evaluate existing Clarabel capability before
  custom optimization; any dependency/lock change gets a separate bounded leaf.

### [ ] T17.07 — train CFR/CFR+ on a supported information-set graph (S04)

- Behavior: update a policy on general supported information sets using the
  declared CFR variant rather than a hard-coded Kuhn-game implementation.
- Depends on: T17.01; exact upstream API/caller inventory recorded first.
- Execution: specialist, extensive-game semantics and regret minimization.
- Files (5): `crates/uogto-game-solve/src/lib.rs`,
  `crates/uogto-game-solve/src/cfr.rs` (future),
  `crates/uogto-game-solve/tests/cfr_information_sets.rs` (future),
  `fixtures/conformance/cfr-reference-v1.json` (future),
  `docs/validation/cfr.md` (future).
- Check: `cargo test --locked -p uogto-game-solve --test cfr_information_sets`
  (future target). Validate legal actions, chance weighting, imperfect-recall
  rejection, and Kuhn/Leduc value and exploitability against pinned independent
  references across iteration counts. Keep game-specific helpers separate.

## Phase C — optional execution and real consumers

### [ ] T17.08 — execute a supported game trace through the Rust Kairos adapter

- Behavior: translate the supported game execution plan into actual native
  Kairos events with stable UOGTO/game trace identity and deterministic replay.
- Depends on: T17.01–T17.03 and accepted Kairos provider contracts under the
  deferred scientific-consumer track; pin qualification remains separate.
- Execution: specialist, public execution contract.
- Files (5): `Cargo.toml`, `Cargo.lock`,
  `crates/uogto-game-kairos/Cargo.toml` (future),
  `crates/uogto-game-kairos/src/lib.rs` (future),
  `crates/uogto-game-kairos/tests/native_replay.rs` (future).
- Check: `cargo test --locked -p uogto-game-kairos --test native_replay`
  (future package/target). Prove native dispatch, deterministic event order, and
  explicit unsupported operations. The adapter depends on game core and Kairos;
  static solving remains independent and must still pass T17.02.

### [ ] T17.09 — run one CareOps game through the shared package contract

- Behavior: execute an actual CareOps application game using the qualified
  packages, retaining the game's players, payoff construction, and policy in
  CareOps rather than copying a generic solver into that repository.
- Depends on: T17.03, T17.05, T17.08, T17.11; consumer-local track and API inventory.
- Execution: local against the agreed contracts; a changed public contract
  returns to the relevant specialist leaf.
- Files (at most 5, future consumer scope): `careops-sim` game adapter module,
  its focused integration test, dependency manifest, lockfile, and acceptance
  receipt. Resolve exact existing paths in its local track before claiming files.
- Check: consumer-local Cargo test target must be declared after that inventory;
  this track asserts no existing CareOps package/test name. The receipt must
  contain the actual `cargo test --locked -p <resolved-package> --test
  <resolved-target>` command and nonzero test count, package hashes, model case,
  reference outputs, and native replay evidence. This is a future acceptance gate.

### [ ] T17.10 — run one Innovate game through the shared package contract

- Behavior: execute an actual Innovate application game using the same package
  artifacts, retaining its domain model and payoff construction in Innovate.
- Depends on: T17.03, T17.05, T17.11; consumer-local track and API inventory.
- Execution: local against the agreed contracts.
- Files (at most 5, future consumer scope): Innovate game adapter module, its
  focused integration test, dependency manifest, lockfile, and acceptance receipt.
  Resolve exact existing paths in its local track before claiming files.
- Check: declare the consumer-local Cargo target after inventory; record the
  actual `cargo test --locked -p <resolved-package> --test <resolved-target>`
  command, nonzero test count, artifact hashes, application case, and independent
  expected result. This is a future target, not evidence of a present integration.

### [ ] T17.11 — reject incompatible valued-payoff inputs at the application port

- Behavior: reject a payoff input whose valuation unit or perspective differs
  from the consumer's declared contract before invoking the generic solver.
- Depends on: T17.01; preserve HEOR valuation and Voiage VOI ownership.
- Execution: specialist, public valuation/decision interface; do not silently
  resolve economic interpretations or insert valuation algorithms into game core.
- Files (4): `crates/new-drug-reimbursement-game/src/lib.rs`,
  `crates/new-drug-reimbursement-game/tests/payoff_input_contract.rs` (future),
  `docs/architecture/payoff-input-contract.md` (future),
  `fixtures/conformance/payoff-input-v1.json` (future).
- Check: `cargo test --locked -p new-drug-reimbursement-game --test
  payoff_input_contract` (future target). Matching declared units/perspectives
  pass through; incompatible inputs fail without an implicit conversion. Inputs
  retain valuation provenance; this does not qualify a HEOR or VOI method.

## Phase D — evidence and extraction eligibility

### [ ] T17.12 — require two real consumers for repository-extraction eligibility

- Behavior: report extraction as ineligible until two distinct real consumer
  receipts identify the same qualified package artifacts and passing cases.
- Depends on: T17.03–T17.11, including independent S01–S04 completion decisions.
- Execution: local evidence validation; reuse the numerical/public-contract
  reviews already recorded instead of requesting repeated human approval.
- Files (4): `scripts/validate_game_consumer_evidence.py` (future),
  `tests/test_game_consumer_evidence.py` (future),
  `docs/validation/game-consumers.json` (future), `extraction-manifest.json`.
- Checks: `python -m unittest discover -s tests -p
  'test_game_consumer_evidence.py'` (future suite), `python
  scripts/validate_game_consumer_evidence.py` (future guard), and
  `cargo test --locked -p uogto-game-core -p uogto-game-solve`.
  Reject duplicated consumer identities, mismatched artifacts, toy-only cases,
  and failed/absent receipts. Record all inherited scientific outcomes and
  relevant repository quality-gate results before track closure. Eligibility
  does not create a repository, publish packages, or alter pins automatically.

## Evidence and rollback

Each completed leaf records exact provider/consumer revisions, changed files,
commands, test counts, and review findings in its local evidence receipt. Failed
scientific controls remain visible. Mark a leaf complete only after its behavior
and acceptance evidence exist. A numerical implementation failure preserves an
explicit unsupported status and requires its supported replacement decision;
moving files or changing labels never supplies validation evidence.

Rollback uses a normal revert or the last qualified package/adapter revision,
retaining original algorithm/output versions for reproducibility. This planning
change creates no runtime artifact to roll back and authorizes no repository
extraction or pin update.
