# T17 application plan — Paignia consumer and valuation

The provider's fourteen implementation leaves now live in
[Paignia T17](https://github.com/edithatogo/paignia/tree/main/conductor/tracks/t17_game_runtime_ecosystem_20261107).
This repository owns only T17.09 and T17.11. The original seventeen IDs and PN
aliases remain in the handoff table below; historical evidence stays in Git.
Routine work uses focused checks and coherent review, with no repeated human
approval loop. No package-release or scientific method is completed by this move.

## Active application leaves

### [x] T17.09 — qualify the reimbursement application as a Paignia consumer

- Behavior: consume one immutable Paignia revision, construct the application
  game locally, and retain an independently checkable result.
- Dependency: the qualified Paignia T17.03 archives and the finite
  perfect-information static profile.
- Accepted source: the [Chapter 8 application case](../../../docs/architecture/paignia-chapter8-application.md)
  merged in [#114](https://github.com/edithatogo/new-drug-reimbursement-game/pull/114).
  The earlier `paignia_static_game` smoke remains a source-integration control.
- Bounded execution slices (each at most five files):
  1. Remove the four tracked files in the transferred core package; keep its
     source history and Paignia notices/provenance.
  2. Remove the four tracked files in the transferred solve package; no parallel
     compatibility implementation remains.
  3. Change `Cargo.toml`, the application manifest, `Cargo.lock`,
     `ecosystem.lock.toml` and the discovery inventory test (5 files) to the same
     actual immutable Paignia revision. Never fabricate a commit or use `main`.
  4. Update `extraction-manifest.json`, `scripts/validate_extraction.py` and
     `tests/test_paignia_dependency.py` to reject local cores, mutable refs,
     mismatched package revisions and lockfile drift.
  5. Run native workspace/application tests and record exact results in this
     plan/metadata. External packaged-artifact release acceptance is still open.
- Checks: `python scripts/validate_extraction.py`, `python -m unittest discover
  -s tests -p 'test_paignia_dependency.py'`, `cargo test --workspace --locked`,
  and `cargo test --locked -p new-drug-reimbursement-game --test paignia_static_game`.
  Require nonzero native tests and compare independent analytic outcomes.
- Qualification boundary: source-tree/git-revision execution is useful consumer
  evidence, not registry release, the second application receipt or S01–S04
  completion. Only numerical/native capabilities actually used add prerequisites.

#### T17.09.result — reject an unsupported or incomplete result

- Depends on: Paignia T17.01's actual result contract and the selected numerical
  method; missing fields return to that provider owner instead of being invented
  in this application. This is not a new generic result implementation here.
- Files (5): `crates/new-drug-reimbursement-game/src/lib.rs`,
  `crates/new-drug-reimbursement-game/src/payoff_input.rs`,
  `crates/new-drug-reimbursement-game/src/paignia_acceptance.rs`,
  `crates/new-drug-reimbursement-game/tests/paignia_result_contract.rs`, and
  `docs/architecture/paignia-result-acceptance.md`.
- Check: `cargo test --locked -p new-drug-reimbursement-game --test
  paignia_result_contract`. Reject unsupported/nonconverged results and
  incomplete catalogues for a requested exhaustive claim; neither means an
  economic zero or proof that no equilibrium exists. Preserve game class,
  information structure, solution concept, algorithm/version, tolerance,
  residuals where defined, selection and completeness. Noisy choice, inertia,
  learning and solver restart frequency must not silently become Nash predictions
  or behavioural probabilities. Independent references allow legitimate corrected
  results rather than forcing parity with a flawed historical seed.
- Candidate evidence: the valued-payoff path admits the exact solver identity
  and one completed policy. Five native contract tests distinguish structurally
  valid failed statuses, an exhaustive claim, a foreign solver run, missing
  choices and an unsupported algorithm version. The broader consumer receipt
  remains in T17.09.artifact.

#### Future slice T17.09.observation — enforce the case's lawful policy input

- Conditional on: a case claiming hidden information or live/dynamic policy;
  depend on Paignia T17.14/.17 and, for paired native streams, T17.15. Do not add
  these as blanket prerequisites for the existing static perfect-information case.
- Files (4): `crates/new-drug-reimbursement-game/src/lib.rs`,
  `crates/new-drug-reimbursement-game/src/policy_input.rs` (future),
  `crates/new-drug-reimbursement-game/tests/lawful_policy_input.rs` (future),
  `fixtures/conformance/paignia-lawful-observation-v1.json` (future).
- Check: `cargo test --locked -p new-drug-reimbursement-game --test
  lawful_policy_input` (future). Two worlds with equal lawful observations and
  legal actions yield equal inputs/actions under matched policy randomness.
  A payer's private threshold, another firm's private costs and private-derived
  action-mask leaks are negative controls. Offline full-game access grants no
  live-policy access. Solver exploration must preserve paired exogenous draws
  under the selected coupling. Separately solving fully observed hidden states
  and averaging their outcomes is not an information-consistent policy/game.

#### T17.09.artifact — accept a real case outside the provider checkout

- Depends on: provider T17.03's actual artifacts and the case-specific result
  contract. Use independent expected results, declared unsupported cases and
  solver/version identity; do not count the local synthetic fixture as the full
  real-model or second-application receipt.
- The application-owned [finite Chapter 8 model](../../../docs/architecture/paignia-chapter8-application.md)
  applies the existing fixed-budget valuation to each offer and uses the
  admitted Paignia policy to recover the reimbursement decision. Six tests check
  the independent equation 8.2 result, an off-threshold menu, rejection, invalid
  inputs, reciprocal overflow and near-tie order invariance. The model uses the
  maintained Chapter 8 example with explicitly synthetic inputs.
- The verifier stages the path dependencies and its resolved lock outside the
  checkout. The normal application uses its reviewed immutable Git pins.
- Check: `python -m unittest discover -s tests -p
  'test_paignia_consumer_artifact.py'` and `python
  scripts/validate_paignia_consumer.py`. Execute the real native case
  with provider checkout unavailable; bind artifact/hash/lock/feature closure,
  nonzero tests and declared profile. Reject duplicate application IDs,
  source-tree-only claims or mismatched artifacts. Paignia T17.02/.03/.12 own
  minimal/default/advertised-extra and build/transitive isolation plus the
  two-real-consumer release gate; no duplicate provider guard is created here.
- Accepted artifact evidence: [receipt](../../../docs/validation/paignia-consumer-receipt.json)
  and [execution log](../../../docs/validation/receipts/t17-reimbursement-chapter8.log).
  The model at `63a3801d378e04f59fec4124e67281f7cbba0b94` passed all six tests
  on Rust 1.75.0 against the qualified `bd880dd` archives. The same macOS policy
  denied source and Git cache reads and network access during resolution,
  compilation and tests. The log retains the resolved paths, feature sets and
  exact lock. It covers the declared synthetic case and static profile.

### [~] T17.11 — reject incompatible valued-payoff inputs at the application port

- Behavior: reject a payoff whose unit or perspective differs from the declared
  consumer contract before invoking Paignia; preserve valuation provenance.
- Depends on: Paignia T17.01 contract. HEOR valuation and Voiage VOI keep their
  own owners; no valuation algorithm moves into generic core or Kairos.
- Files (5): the application's `src/lib.rs` module binding, `src/payoff_input.rs`,
  `tests/payoff_input_contract.rs`, `tests/paignia_static_game.rs`, and
  [the payoff input contract](../../../docs/architecture/payoff-input-contract.md).
  The typed Rust fixture in `payoff_input_contract.rs` supplies the planned
  conformance cases with a distinct provenance revision for every payoff.
- Check: `cargo test --locked -p new-drug-reimbursement-game --test
  payoff_input_contract --test paignia_static_game`. The six port cases
  and the existing finite offer case pass against the versioned Paignia
  static contract at `bd880dd756d2ba56cc5f479bc078cea31b53c1d1`.
  The real artifact and extended Voiage receipts remain separate.

#### Future slice T17.11.metric — preserve the declared information-value meaning

- Depends on: the application's valuation contract and accepted Voiage SI01–SI04
  / signed-social inputs. This application supplies data/meaning; Voiage owns
  conventional EVPI/EVSI and information-value arithmetic. Do not add an evaluator.
- Files (4): `crates/new-drug-reimbursement-game/src/lib.rs`,
  `crates/new-drug-reimbursement-game/src/voiage_input.rs` (future),
  `crates/new-drug-reimbursement-game/tests/voiage_input_contract.rs` (future),
  `fixtures/conformance/voiage-input-contract-v1.json` (future).
- Check: `cargo test --locked -p new-drug-reimbursement-game --test
  voiage_input_contract` (future). Preserve recipient, timing, disclosure,
  commitments, observation model and equilibrium selection. Conventional
  EVPI/EVSI, research net benefit, strategic information value and social
  information value retain distinct labels. Preserve signed reference values,
  explicit welfare assumptions and transfer-versus-resource accounting; reject
  implicit clipping or incompatible metric/perspective substitution.

#### Future slice T17.11.identities — keep simulation noise out of parameter learning

- Depends on: the accepted input identity contract and T17.11.metric; Voiage
  supplies the independent arithmetic oracle and precision/budget contract.
- Files (4): `crates/new-drug-reimbursement-game/src/voiage_input.rs` (future),
  `crates/new-drug-reimbursement-game/tests/voiage_replicate_identity.rs` (future),
  `fixtures/conformance/voiage-noise-identities-v1.json` (future),
  `docs/architecture/voiage-input-identities.md` (future).
- Check: `cargo test --locked -p new-drug-reimbursement-game --test
  voiage_replicate_identity` (future). Preserve parameter, model, equilibrium,
  measurement and simulation-replicate identities. One parameter state with
  replicates A=[-1,1] and B=[1,-1] has conditional means and parameter EVPI 0;
  mislabelling replicates as parameter draws yields the invalid value 1. Reject
  that mislabelling and preserve the truthful valuation/identity input to
  Voiage. Report Monte Carlo precision and inner/outer budgets; do not implement
  a second VOI calculation or treat numerical noise as learnable uncertainty.

### Existing strategic-pilot observation handoff

[PR #103](https://github.com/edithatogo/new-drug-reimbursement-game/pull/103)
retains its application implementation owner. Its selected consumer cases must
keep medicines scripts, quantities, spending and treated stock distinct, and
consider supply intervals, coding and coverage changes as observation-process
candidates rather than automatic adoption/abandonment effects. Preserve
physical effective dates and known-at dates for lawful historical forecasts.
Innovate owns generic utilisation/innovation/observation methods; Atlas owns
source/terminology qualification; this application owns payer/manufacturer,
eligibility and economic assumptions. Missing indication, patient count and
private use must not be inferred from aggregate PBS records. Link those
case-specific receipts here when claimed; do not create a duplicate pilot track
or make the entire medicines programme gate the existing bounded static case.

## Stable ownership handoff

| Original IDs | Canonical owner | Status |
|---|---|---|
| T17.01, .02, .03 | Paignia | Generic contract, dependency isolation and artifact qualification remain open. |
| T17.04, .05, .06, .07 | Paignia; Kairos source-side register retained | S01 RK4, S02 mixed Nash, S03 CE and S04 CFR/CFR+ remain open. |
| T17.08 | Paignia | Optional Kairos adapter; independent of static solving. |
| T17.09 | This application | Active immutable consumer work above; release acceptance open. |
| T17.10 | Selected second consumer / Innovate G01–G04 | Its own real case and matching-artifact receipt; not a local duplicate task. |
| T17.11 | This application | Valued-payoff contract above. |
| T17.12 | Paignia | Two real consumer receipts for bounded package release eligibility. |
| T17.13, .14, .15, .16, .17 | Paignia | Conversion, lawful observation, RNG isolation, replay and information sets remain open. |

PN01 maps to provider T17.01/.03, PN02 to application T17.09 and provider
T17.03, PN03 to provider T17.01/.04–.07/.13 and PN04 to consumer
T17.09/.10 and provider T17.12. Repository creation occurred by user
direction; the original future-extraction gate now concerns bounded release
eligibility, without waiving artifact or consumer requirements. Rollback uses
an actually qualified immutable provider revision; source ownership stays with
Paignia. Restore historical code only through an explicit ordinary revert,
never silently as a second supported core.
