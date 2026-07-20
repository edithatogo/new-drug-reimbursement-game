# Codex implementation brief

## Mission

Develop this repository into two interoperable products while keeping their
boundaries explicit:

1. **New Drug Reimbursement Game application** — an auditable implementation of
   Pekarsky's PEA and strategic games, extended with post-2015 methods and
   empirical evidence.
2. **General game-theory runtime** — a UOGTO-native Rust capability above
   Kairos, suitable for extraction into its own repository and reuse across
   domains.

## Invariants

- No source book or copied content.
- No runtime use of Nashpy, Gambit/pygambit, OpenSpiel, BCEA, heemod, or dampack.
- No third-party Hugging Face model or dataset IDs.
- No duplication of Voiage VOI algorithms or Kairos scheduling/DES/ABM.
- No reimbursement vocabulary in domain-neutral Rust crates.
- No silent interpretation of `mu`, threshold, displacement, confidential
  price, or future innovation.
- Every equation, parameter, evidence record, game assumption, solver result,
  and trace has provenance and a version.

## Workstream 1 — verify the mathematical foundation

1. Re-derive IPER, `Delta E_R`, NEBhR, EVCI, and all `beta_c` contexts from
   Pekarsky Chapters 6–8.
2. Create a signed derivation note with dimensions and assumptions.
3. Add property tests:
   - NEBhR is zero at `f = beta_c`;
   - sign changes correctly around the threshold;
   - `n = m` gives `beta_c = d` for the fixed efficient case;
   - `d = m` gives `beta_c = n` for optimal displacement;
   - monotonicity and unit-rescaling invariants;
   - invalid and non-identifiable contexts fail closed.
4. Locate and verify the exact Chapter 7 technical-efficiency formulation.
   Preserve alternative named interpretations until source and expert review
   resolves them.
5. Add an independent implementation in Rust and cross-language fixtures.

## Workstream 2 — general Rust game runtime

Extend `uogto-game-core` and `uogto-game-solve` without domain leakage:

- canonical IDs and versioned game specification;
- players, roles, actions, strategies, states, transitions, terminal outcomes;
- chance nodes, information sets, beliefs, signals, rules, and observations;
- scalar/vector payoffs, utility functions, perspectives, and constraints;
- validation errors with machine-readable paths;
- canonical serialization and JSON-LD/UOGTO mapping;
- backward induction and subgame-perfect result objects;
- pure-strategy normal-form best response and Nash enumeration;
- solver traits, diagnostics, tie policies, tolerances, and reproducibility;
- repeated and stochastic game specifications;
- bargaining/mechanism interfaces;
- execution traces.

Design a compiler from supported game specifications to Kairos events and ECS
state. Do not write another scheduler or RNG. Pin and use the released Kairos
contract when available. Add conformance fixtures and deterministic trace tests.

Prepare extraction into a dedicated Rust repository. The extraction must not
require moving application files or reimbursement ontology terms.

## Workstream 3 — UOGTO

Use the pinned UOGTO revision in `ecosystem.lock.toml`.

1. Validate the application extension against UOGTO core and the HTA applied
   pack.
2. Expand the proposal for price, net price, confidential rebate, displacement,
   financing, reallocation, contract, evidence development, implementation,
   R&D, capital market, jurisdiction, perspective, and equity concepts.
3. Add SHACL constraints, JSON-LD contexts, examples for Games 1–3, and
   competency questions.
4. Map executable elements to UOGTO execution bindings and Kairos traces.
5. Produce an upstream-ready patch/PR branch plan; do not fork ontology core
   semantics in the application.

## Workstream 4 — application games

### Game 1

Reconstruct the continuous-price extensive-form game with explicit assumptions,
production cost, demand/quantity, tie policy, threshold observability, and
alternative strategies. Prove equivalence between the analytic corner solution
and the Rust solver for discretized approximations. Add variants for hidden
threshold, bargaining, net-price rebates, and contract enforcement.

### Game 2

Implement the firm–institution–capital-market game with:

- do nothing, lobby, or borrow;
- R&D cost, interest, success/failure, and information structure;
- public versus private parameters;
- complete strategy definitions and payoffs;
- backward induction or the appropriate equilibrium concept;
- source-mapped assumptions and independent tests.

### Game 3

Implement the multi-period current/future-drug game with:

- development and manufacturing choices;
- first- and second-drug prices;
- clinical and manufacturing innovation;
- lifecycle/patent/competition states;
- premium, rebate, and public-investment contract variants;
- uncertainty and global spillover extensions.

Keep domain models in the application crate/package and generic mechanics in the
Rust runtime.

## Workstream 5 — Voiage

Voiage owns VOI. Build an adapter and shared fixtures rather than algorithms.

- transform reimbursement outcomes into strategy net-benefit arrays;
- preserve health-unit versus monetary-unit perspectives;
- pass parameter samples with UOGTO IDs and evidence revisions;
- compute EVPI/EVPPI/EVSI/ENBS, portfolio/sequential/structural VOI, value of
  perspective, equity and implementation-adjusted methods where supported;
- add diagnostics and round-trip fixtures;
- propose missing generic capabilities upstream to Voiage;
- reconcile Voiage licence metadata before distribution.

## Workstream 6 — Kairos

- finalize the game-event vocabulary and state components;
- build a native adapter against pinned released crates/bindings;
- represent negotiations, evidence arrival, R&D, capacity, implementation, and
  payment/contract events;
- use deterministic random streams and trace IDs;
- add replay fixtures and performance benchmarks;
- keep Kairos domain-neutral.

## Workstream 7 — Reimbursement Atlas and Hugging Face

Only use owner-controlled assets.

- consume approved derived exports from `edithatogo/reimbursement-atlas`;
- add a PEA parameter-candidate schema and derived view upstream;
- preserve source checksums, licences, transformations, reviewer decisions, and
  uncertainty;
- never copy restricted/raw source payloads into this repository;
- publish only to `edithatogo/*` after explicit approval;
- reconcile Hugging Face dataset licence metadata before automation;
- fail closed when a record is not approved, marginality is unclear, or the
  budget boundary is incompatible.

## Workstream 8 — post-2015 research programme

Verify the bibliography using primary/official sources, then implement or scope:

- empirical marginal productivity/opportunity-cost calibration;
- distributional CEA and equity-sensitive payoff profiles;
- managed entry agreements and coverage with evidence development;
- indication/subgroup/lifecycle pricing;
- repeated games, incomplete information, confidential rebates, lobbying,
  appeals, reputation, and international reference pricing;
- affordability, capacity, implementation, and political constraints;
- global R&D spillovers and multi-payer public-goods problems;
- causal displacement and identifiability;
- model uncertainty and robust decisions.

For every extension record the research question, estimand, equilibrium concept,
data requirement, identification assumptions, and validation plan.

## Workstream 9 — governance and quality

- update `ecosystem.lock.toml` only through reviewed pin changes;
- add ADRs for every dependency;
- SBOM, licence audit, provenance manifest, signed releases, and reproducible
  builds;
- strict Rust/Python lint, typing, unit/property/mutation/conformance tests;
- independent mathematical implementation and benchmark cases;
- model-risk, security, privacy, and human-review gates;
- generated docs and stable schemas;
- no claim of policy readiness without external review evidence.

## Acceptance criteria

Before completing a milestone:

```bash
python scripts/validate_scope.py
python -m unittest discover -s tests -p 'test_*.py'
python -m compileall -q src scripts tests
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
```

Also verify:

- every HF ID begins `edithatogo/`;
- no prohibited capability package is a runtime dependency;
- no book binary or copied source asset is present;
- domain-neutral crates pass a vocabulary-boundary test;
- UOGTO/JSON-LD/SHACL fixtures validate;
- Voiage and Kairos integration tests use pinned owner-controlled revisions;
- built artifacts install and execute from a clean environment.

## Required final report

Report:

- commits and files changed;
- exact ecosystem revisions and licence decisions;
- equations and games implemented, with source locations;
- external and independent validation performed;
- exact test/lint/type/coverage/build results;
- upstream proposals/PRs prepared;
- unresolved assumptions, discrepancies, and evidence gaps;
- work requiring health-economics, ontology, legal, governance, or security
  review.
