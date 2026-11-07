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

The receiving handoff is [issue 100](https://github.com/edithatogo/new-drug-reimbursement-game/issues/100),
coordinated with [Innovate PR 570, G01–G04](https://github.com/edithatogo/innovate/pull/570).
Kairos `K01.games` supplies `conductor/contracts/game-extraction-map.md`;
`K01.port` supplies `conductor/contracts/game-execution-port.md`. Their contracts
are proposed in [Kairos PR 382](https://github.com/edithatogo/kairos/pull/382);
they are inputs, not evidence that this package or adapter already exists.

Dependency lines control execution; phase headings group related work. The
bounded static path is T17.01–T17.03, two selected real consumer cases in
T17.09–T17.10, then T17.12. It does not require the optional native adapter or
all future numerical methods. Additional capabilities require their own named
receipts. All leaves remain pending; partial qualification does not close T17.

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
  Freeze the supported representation independently of ECS, plus specification,
  instance, session, policy and trace identity. Declare chance-zero/mass rules,
  complete versus intentional sparse-zero payoffs, tolerance and tie selection.
  Include the observed string/generational-ID and semantic conversion negatives
  from the source map. A stable result names algorithm/version, supported class,
  status and residuals; backend diagnostics are optional. Solver diagnostic
  traces and realized causal traces are different record types. Core references
  no Kairos state, clock or simulation RNG; unknown information structures reject.

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
  transitive violation, not just search top-level manifest strings. Inspect
  normal/build dependencies under the supported default, minimal and optional
  feature profiles; include a violation hidden behind an optional feature or
  build dependency. Keep optimization in solver/backend scope and avoid making
  semantic tooling, serialization or native integration mandatory in game core.

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
  their local artifact dependency explicitly, run `cargo generate-lockfile
  --manifest-path <temporary-consumer>/Cargo.toml`, then run `cargo test --locked
  --manifest-path <temporary-consumer>/Cargo.toml`. Make the provider checkout
  unavailable and exercise every advertised feature profile with nonzero tests.
  Include transferred generated sources/fixtures inside their package, or mark
  that feature unsupported: Kairos's current external `include!` and ontology
  fixture paths must not survive accidentally. Qualify the selected compiler
  profile against the declared MSRV rather than assuming Kairos's 1.99 and this
  workspace's 1.75 declarations are interchangeable. Record artifact hashes;
  no publication or repository extraction is part of this leaf.

## Phase B — inherited numerical methods

These leaves own the corrected generic implementations, coordinated with Kairos
Track 110's source regressions and transfer/retirement decisions. Do not maintain
two corrected solver implementations. A bounded release may leave S01–S04
pending and explicitly unsupported; any advertised method must complete its own
oracle and result contract. Exclusion is not scientific completion.

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
- Depends on: T17.01 and T17.17; exact upstream API/caller inventory recorded first.
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

## Phase C — optional execution and representation gaps

### [ ] T17.08 — execute a supported game trace through the Rust Kairos adapter

- Behavior: translate the supported game execution plan into actual native
  Kairos events for one selected policy/chance path.
- Depends on: T17.01–T17.03, T17.14 and accepted `K01.port`/Kairos provider
  contracts under the deferred scientific-consumer track; pin qualification
  remains separate. This is not a static package prerequisite.
- Execution: specialist, public execution contract.
- Files (5): `Cargo.toml`, `Cargo.lock`,
  `crates/uogto-game-kairos/Cargo.toml` (future),
  `crates/uogto-game-kairos/src/lib.rs` (future),
  `crates/uogto-game-kairos/tests/native_replay.rs` (future).
- Check: `cargo test --locked -p uogto-game-kairos --test native_replay`
  (future package/target). A tiny two-action/one-chance case dispatches only the
  chosen causal path. `Solution.trace` includes postorder hypothetical branches:
  preserving it for diagnostics must never schedule those alternatives or treat
  expected payoffs as sampled outcomes. Repeated execution with declared inputs
  gives the same native event order. Use the frozen observation/identity/time
  contract; reject unsupported simultaneous, stale, duplicate, cancellation or
  delayed-effect operations before mutation until separately implemented. Bound
  zero-time loops explicitly. This leaf does not qualify all lifecycle features,
  stochastic stream isolation or checkpoint resume. The adapter depends on game
  core and Kairos; static solving stays independent and still passes T17.02.

### [ ] T17.13 — reject semantically lossy Kairos/game conversions

- Behavior: convert the supported game/runtime representation without silently
  losing identity or changing the declared game semantics.
- Depends on: T17.01 and T17.08; the source map supplies the exact legacy surface.
- Execution: specialist, public conversion and compatibility contract.
- Files (4): `crates/uogto-game-kairos/src/lib.rs`,
  `crates/uogto-game-kairos/src/conversion.rs` (future),
  `crates/uogto-game-kairos/tests/semantic_conversion.rs` (future),
  `docs/architecture/game-semantic-conversion-v1.md` (future).
- Check: `cargo test --locked -p uogto-game-kairos --test semantic_conversion`
  (future target). Preserve specification/instance/session/trace namespaces and
  full generational entity/event handles; reject collisions, unknown identities
  and stale generations. Round-trip the supported profile and reject unmapped
  chance-zero, payoff-completeness or tie-selection semantics. Never silently
  discard information sets. A deliberate semantic change requires a new profile
  and consumer decision. Only consumers using this conversion require its receipt.

### [ ] T17.14 — expose only the declared player observation to a live policy

- Behavior: construct a policy input containing only the player's permitted
  information and legal actions for the selected executable profile.
- Depends on: T17.01; T17.17 additionally applies when information sets are claimed.
- Execution: specialist, game information and public policy contract.
- Files (4): `crates/uogto-game-core/src/lib.rs`,
  `crates/uogto-game-core/src/observation.rs` (future),
  `crates/uogto-game-core/tests/policy_observation.rs` (future),
  `docs/architecture/policy-observation-v1.md` (future).
- Check: `cargo test --locked -p uogto-game-core --test policy_observation`
  (future target). Two hidden states with the same lawful observation yield the
  same policy input/legal-action set; opponent-private values and full-world
  references cannot leak through it. Bind session, player/information-set and
  observation revision, rejecting unsupported information structures explicitly.
  Offline solvers may inspect the mathematical game without granting that access
  to an acting policy. A static solver with no live policy API need not wait here.

### [ ] T17.15 — isolate solver exploration from simulation random streams

- Behavior: keep exogenous simulation draws invariant when solver exploration
  or its iteration budget changes under the declared coupling policy.
- Depends on: T17.08 and T17.13 for stable runtime identity mapping.
- Execution: specialist, RNG and comparison semantics.
- Files (4): `crates/uogto-game-kairos/src/lib.rs`,
  `crates/uogto-game-kairos/src/randomness.rs` (future),
  `crates/uogto-game-kairos/tests/rng_isolation.rs` (future),
  `docs/validation/game-rng-isolation.md` (future).
- Check: `cargo test --locked -p uogto-game-kairos --test rng_isolation`
  (future target). Use native purpose/identity streams and record algorithm,
  stream/distribution versions and the intended strategy/draw coupling. Changed
  solver budgets, reordered construction and policy branches preserve declared
  exogenous draws; intentionally independent streams remain distinct. The
  RNG-isolation regression must consume both exploration and exogenous streams
  using an explicit exploratory or stochastic fixture, so it distinguishes
  stream isolation from a fixture that draws nothing. Static
  expectation-based solving draws nothing. A future stochastic static solver
  receives an explicit RNG/configuration without a Kairos dependency; it must
  not borrow a simulation-global stream. A shared seed alone is not this oracle.

### [ ] T17.16 — restore qualified policy and native state for causal replay

- Behavior: resume the supported game execution from one checkpoint with the
  same subsequent causal events and outcomes as uninterrupted execution.
- Depends on: T17.08 and T17.15.
- Execution: specialist, state ownership and replay.
- Files (4): `crates/uogto-game-kairos/src/lib.rs`,
  `crates/uogto-game-kairos/src/checkpoint.rs` (future),
  `crates/uogto-game-kairos/tests/policy_resume.rs` (future),
  `docs/validation/game-policy-resume.md` (future).
- Check: `cargo test --locked -p uogto-game-kairos --test policy_resume`
  (future target). Restore live policy state, identity mapping, native state and
  qualified RNG checkpoints together; a sibling branch remains isolated. Keep
  frozen offline training provenance distinct from live replay state. Reject
  incompatible versions or unsupported mutable policy state before resuming;
  matching a solver's diagnostic trace alone does not establish replay.

### [ ] T17.17 — validate an ECS-independent information-set representation

- Behavior: validate the declared finite information-set graph without importing
  Kairos storage or treating ontology labels as implemented semantics.
- Depends on: T17.01 and the UOGTO executable-profile contract.
- Execution: specialist, extensive-game representation.
- Files (4): `crates/uogto-game-core/src/lib.rs`,
  `crates/uogto-game-core/src/information_sets.rs` (future),
  `crates/uogto-game-core/tests/information_sets.rs` (future),
  `docs/architecture/game-information-contract-v1.md` (future).
- Check: `cargo test --locked -p uogto-game-core --test information_sets`
  (future target). Check player/namespace ownership, consistent legal actions
  within each information set and the declared recall/observation rules. Reject
  unsupported imperfect recall and invalid memberships. The current `Game` has
  no information-set representation; retain its bounded perfect-information
  profile while this extension is pending. CFR acceptance follows in T17.07.

## Phase D — real application consumers

### [ ] T17.09 — qualify a first real static application game

- Behavior: execute one real application game against the qualified static
  artifacts, retaining its model/payoffs/policy in the application.
- Depends on: T17.03; consumer-local track and API inventory. Require a numerical
  leaf only for a method actually used by the case, not all T17.04–T17.07.
- Execution: local against the agreed contracts; a changed public contract
  returns to the relevant specialist leaf.
- Files (at most 5, future consumer scope): selected application's game adapter,
  focused integration test, dependency manifest, lockfile and acceptance receipt.
  Resolve exact paths in its owning track before claiming. The reimbursement
  application or CareOps is a candidate; existing manifest declarations without
  executed generic game calls do not qualify either.
- Check: consumer-local Cargo test target must be declared after that inventory;
  this track asserts no existing consumer integration target. The receipt must
  contain the actual `cargo test --locked -p <resolved-package> --test
  <resolved-target>` command and nonzero test count, package hashes, model case,
  independent reference outputs and the supported capability/profile. Execute
  the real model outside the provider checkout using T17.03's artifacts. Static
  qualification needs no Kairos receipt; a native claim additionally needs
  T17.08 and the conversion/RNG/resume leaves its selected features use. Valuation
  units/perspective checks belong to this consumer, not a blanket dependency on
  the reimbursement port T17.11. This is a future acceptance gate.

### [ ] T17.10 — qualify a second distinct real static application game

- Behavior: execute a second actual application's game using the same static
  artifacts, retaining its domain model and payoff construction locally.
- Depends on: T17.03; consumer-local track and API inventory. Only the selected
  method/features add their numerical or native acceptance prerequisites.
- Execution: local against the agreed contracts.
- Files (at most 5, future consumer scope): selected application's game adapter,
  focused integration test, dependency manifest, lockfile and acceptance receipt.
  Resolve exact paths in its owning track before claiming. Innovate's G01–G04
  programme is a candidate and retains its owner; this leaf does not take over
  PR 570. The two consumer leaves can proceed independently.
- Check: declare the consumer-local Cargo target after inventory; record the
  actual `cargo test --locked -p <resolved-package> --test <resolved-target>`
  command, nonzero test count, artifact hashes, application case, and independent
  expected result. Require a distinct real application identity from T17.09,
  not another wrapper around the same case. Reimbursement plus Innovate is an
  eligible pair once both execute their models; CareOps is not mandatory for
  that pair. A static case needs no dynamic adapter or unrelated numerical
  method. Apply T17.09's capability-specific receipt rules. This is a future
  target, not evidence of a present integration.

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

## Phase E — bounded evidence and extraction eligibility

### [ ] T17.12 — require two real consumers for repository-extraction eligibility

- Behavior: report extraction as ineligible until two distinct real consumer
  receipts identify the same qualified static artifacts and passing profile.
- Depends on: T17.03, T17.09 and T17.10. Numerical/native receipts apply only to
  the supported capabilities claimed by the artifacts and consumer cases.
- Execution: local evidence validation; reuse the numerical/public-contract
  reviews already recorded instead of requesting repeated human approval.
- Files (4): `scripts/validate_game_consumer_evidence.py` (future),
  `tests/test_game_consumer_evidence.py` (future),
  `docs/validation/game-consumers.json` (future), `extraction-manifest.json`.
- Checks: `python -m unittest discover -s tests -p
  'test_game_consumer_evidence.py'` (future suite), `python
  scripts/validate_game_consumer_evidence.py` (future guard), and
  `cargo test --locked -p uogto-game-core -p uogto-game-solve`.
  Reject duplicated application identities, mismatched artifacts/profiles,
  toy-only cases, absent/failed receipts and advertised capabilities without
  their method evidence. Accept two real static consumers, including the
  reimbursement application plus Innovate, without requiring optional Kairos
  integration, T17.11 or every future algorithm. Record S01–S04 individually as
  supported with evidence, explicitly unsupported/pending, or withdrawn with a
  replacement decision; omission is not allowed. Pending excluded methods keep
  their owners and completion tasks open. This bounded eligibility report does
  not close the whole track, create a repository, publish packages or change
  pins. Full track closure still requires its remaining obligations and quality
  gates; the first useful static package does not wait for that broader closure.

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
