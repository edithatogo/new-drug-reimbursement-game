# Paignia identity and promotion supplement

Date: 2026-11-08. Owner: existing T17, coordinated with issue #100. Status: planning; all implementation and publication gates remain open. Read [the specification](spec.md) and [the implementation plan](plan.md) first. This supplement names the capability and clarifies handoffs; it does not replace the twelve T17 leaves or their scientific obligations.

## Decision

The reusable game-theory library's working name is **Paignia**. The intended standalone slug is `paignia`; no new repository or registry namespace is claimed. The capability remains incubated here until T17.12 and the publication checks below pass.

Planned package mapping:

| Existing package/path | Planned name | Qualification |
|---|---|---|
| `crates/uogto-game-core` | `paignia-core` | Typed domain-neutral game/strategy/information/result contract. |
| `crates/uogto-game-solve` | `paignia-solve` | Independently verified algorithms and explicit unsupported status. |
| T17.08 optional adapter | `paignia-kairos` | Native Kairos event execution; not a static-solver dependency. |
| UOGTO adapter | `paignia-uogto` | Accepted versioned semantics, not an independent ontology fork. |
| Tabular adapter | `paignia-arrow` | Optional Arrow/Polars contract, separate from minimal solver dependencies. |

Do not rename packages, imports, test commands or old evidence in this documentation change. Test existing `uogto-game-*` IDs until the bounded rename leaf is implemented. Paignia is the target name, not proof that a distributable library already exists.

## Boundary and consumers

Paignia owns reusable game representation, equilibria, strategic learning and diagnostics. The reimbursement application retains institutions, case assumptions, evidence calibration, payoff construction and clinical interpretation. Innovate owns innovation-specific launch/entry/competition games and fitting; CareOps owns its service-operation games. Voiage owns decision uncertainty and VOI after an explicit utility/perspective mapping. UOGTO owns semantic identifiers and conformance. Kairos owns execution time/state/resources/RNG/replay through an optional adapter.

Static solving must build and run without Kairos, Python, pandas or xarray. No generic solver is copied into Innovate or CareOps. Do not introduce Nashpy/Gambit/OpenSpiel as runtime dependencies; permitted independent references remain isolated validation tools. Preserve T17's explicit dependency-decision policy for maintained numerical components.

## Executable supplementary leaves

### [ ] PN01 — identity and compatibility ledger

Scope: T17.01/T17.03; specialist public-contract review once. Future files (at most five): `docs/architecture/paignia-package-map.json`, `tests/test_paignia_package_map.py`, `scripts/validate_extraction.py`, `extraction-manifest.json`, and this supplement.

- [ ] Write `test_paignia_identity_does_not_claim_publication`: assert display name Paignia; legacy package IDs retain source paths; `repository_created` and `packages_published` are false until receipts exist.
- [ ] Run `python -m unittest discover -s tests -p 'test_paignia_package_map.py'`; require a real failing assertion, not a missing test/zero-test run.
- [ ] Implement the identity/alias ledger, recording namespace availability as unknown until checked at publication.
- [ ] Rerun the test and existing extraction guard; commit the bounded identity change separately from runtime migration.

### [ ] PN02 — safe package rename, only after packaging acceptance

Depends on T17.03 and PN01. Before implementation, freeze the actual affected manifest/import/lock paths in a leaf with at most five files; split per crate if needed. Never change an old receipt's package name.

- [ ] Add an installed-package test proving that the same supported input produces the same versioned result before and after the proposed rename, and that documented unsupported cases still fail.
- [ ] Record the failing consumer case; implement one crate's versioned naming/compatibility migration, retaining a release note and last-qualified rollback revision.
- [ ] Run that crate's actual tests with nonzero counts plus a clean external consumer of the produced package artifact. Record hashes and exact dependency closure.
- [ ] Only then repeat for the solver/adapters. No registry publishing is part of this leaf.

### [ ] PN03 — source/algorithm ownership reconciliation

Depends on T17.01 and the current Kairos caller inventory. Future receipt `docs/validation/paignia-source-ownership.json`; extend the existing extraction checks rather than create a second checker.

- [ ] Write rejection cases for duplicated algorithm ownership and missing inherited S01-S04 dispositions.
- [ ] Record source paths/licences/callers for `uogto-game-*` and Kairos game modules. Preserve or explicitly replace every accepted public promise.
- [ ] Link RK4, mixed-Nash, correlated-equilibrium and CFR acceptance to T17.04-T17.07. Moving or renaming code cannot close these leaves.
- [ ] Require residuals/exploitability where defined, selection assumptions and unsupported/nonconverged statuses in consumer receipts.

### [ ] PN04 — extraction/publication readiness

Depends on T17.12, PN01-PN03 and existing release gates.

- [ ] Extend `tests/test_game_consumer_evidence.py` to reject duplicate application IDs, source-tree-only imports, mismatched artifact hashes and toy-only consumers.
- [ ] Require two distinct real consumer receipts for the same artifacts. Prioritise the reimbursement application and Innovate; retain the existing CareOps acceptance leaf rather than treating a synthetic harness as that application.
- [ ] Check intended repository and package namespaces immediately before creating/publishing; record licence/provenance, security, API/schema/ABI compatibility, reproducible artifacts and rollback.
- [ ] Keep extraction eligibility separate from namespace reservation, repository creation and public release. Do not fabricate those receipts.

## Validation and hardening

Retain analytic backward induction, dominance, matching-pennies, coordination/multiple-equilibrium, correlated-incentive and imperfect-information tests from T17. Include invalid/NaN payoffs, label permutations, illegal actions, inconsistent information sets, resource limits and convergence failures. A zero-test filtered Cargo command never passes a gate.

Every completed leaf records source SHA, package hashes, resolved dependencies, seed, commands/nonzero test counts, numerical tolerances and review findings. Broader tests run for required repository gates and identified risk; no new repeated human approval loop is introduced.

## Coordination

Central policy: repository-standards PR #120, `docs/paignia-library-boundary.md` (proposed until merged). Innovate PR #570 retains the innovation/hype/medicines programme. Kairos issue #336 retains native provider qualification. Voiage issue #1286 owns decision-input and VOP promotion. Existing T17 remains the extraction authority; this supplement is not a new competing implementation track.
