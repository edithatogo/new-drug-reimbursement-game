# Paignia provider and reimbursement-consumer supplement

Date: 2026-11-08. Owner: existing T17 and issue #100. Status: the immutable native consumer is implemented and locally tested; package, scientific and complete real-model acceptance remain separately evidenced. Read [spec.md](spec.md) and [plan.md](plan.md). Preserve T17.01-T17.17 through the source transfer; this document neither creates replacement task IDs nor completes a scientific obligation.

## Actual provider and transfer

The maintainer has created [edithatogo/paignia](https://github.com/edithatogo/paignia). It is the authoritative reusable Rust game-library repository. This repository is the historical incubator and a reimbursement application/consumer. Repository creation does not require waiting for package qualification; package qualification and publication remain pending until their own receipts exist.

| Historical source | Receiving package/component | Acceptance boundary |
|---|---|---|
| `crates/uogto-game-core` | Paignia `paignia-core` | Typed domain-neutral game/result contract and versioned migration |
| `crates/uogto-game-solve` | Paignia `paignia-solve` | Each claimed algorithm has independent numerical evidence |
| T17.08 execution adapter | Optional `paignia-kairos` | Native dynamic execution, not a static prerequisite |
| Semantic mapping | Optional `paignia-uogto` | Versioned UOGTO conformance, not a second ontology engine |
| Tabular boundary | Optional `paignia-arrow` | Arrow/Polars semantics, not mandatory static-core dataframes |

The actual provider is `12b22ce7571b9c590405bf53c2c1c5862b49cd64`, recorded consistently in the application manifest, Cargo-generated lock, ecosystem lock and `extraction-manifest.json`. The local generic crate copies are removed. Do not globally rename historical commands or copy a second independently evolving solver. Renaming/transferring source is possible before qualification; it must not be described as qualification. Preserve licence/source history, fixtures, package identities of old releases and rollback evidence.

Provider T17.01-.08/.12-.17 belongs in Paignia. T17.09/.10 retain the two selected application-consumer owners; .11 retains reimbursement-specific valuation ownership. Keep the leaf IDs and their existing obligations. The receiving [Paignia PR #1](https://github.com/edithatogo/paignia/pull/1) proposes integration and scientific-contract refinements without taking over initial source transfer. [Paignia PR #2](https://github.com/edithatogo/paignia/pull/2) completed that source transfer; the two workstreams retain their owners.

## Responsibility and independent readiness

Paignia owns game representations, supported algorithms, behavioural-model mechanisms and diagnostics. This application owns institutions, payer/manufacturer/patient roles, empirical assumptions, payoff/valuation construction and clinical interpretation. Innovate owns innovation dynamics and observation models; Kairos owns execution time/state/resources/RNG; Voiage owns decision and information-value arithmetic; UOGTO owns semantics.

Static solving works without Kairos, Voiage, Python, pandas or xarray. Independent Gambit/OpenSpiel references remain isolated test oracles. Minimal solver/core, supported static methods and optional dynamics qualify independently. Preserve S01-S04 obligations and unsupported states; unfinished general CFR or dynamic replay does not block a smaller verified perfect-information/pure-Nash release. The two-real-application rule gates scoped package/consumer acceptance, not creation of the already existing provider repository.

## PN aliases amend existing leaves, not a second status ledger

Execute one behaviour within the owning T17 file budget. Record the exact target after source reconciliation, a meaningful failing assertion, minimal implementation, passing nonzero tests, review and receipt. New test paths below are proposed until created. Stop on missing source fields, ambiguous information structure or unqualified algorithms; do not invent assumptions to close a task.

### PN01 — identity/provenance mapping (T17.01/.03)

Use Paignia's actual `extraction-manifest.json` and transfer map, plus the application's existing extraction guard. If a separate package map remains needed, use `docs/architecture/paignia-package-map.json` and a focused `tests/test_paignia_package_map.py`, not a duplicate source inventory.

Acceptance assertions: repository is `edithatogo/paignia`; the source manifest records `standalone_repository_created=true` from the actual GitHub record; published/qualified remains false absent its evidence; incubator paths and source commits remain historical provenance. Unsupported future adapters are not inferred to exist. Run the existing guard and the created test with a genuine negative control. Do not assert repository_created=false merely because a package is unqualified.

### PN02 — immutable application dependency switch (T17.09 and provider .03)

The transfer owner moves/renames source; the application owner consumes its exact candidate. Freeze affected manifest/import/lock paths in a bounded leaf and retain last-qualified rollback. A temporary qualified Git/artifact dependency is not package-index publication.

Write the external-consumer test first: with the provider checkout unavailable, run a real reimbursement case against the produced package, preserve declared semantics, reject unsupported games and expose solver/version identity. Test before/after results against an independent reference, not merely each other. Record package hash, lock, feature closure and nonzero test count; preserve legitimate corrected-result differences rather than forcing parity with a flawed seed. The immutable Git consumer switch is implemented at the revision above. Complete external-artifact/real-model acceptance remains open; the existing synthetic native fixture alone does not satisfy it.

### PN03 — one algorithm owner and honest result (T17.01/.04-.07)

Extend the existing ownership guard with duplicated-owner and missing-S01-S04 negative cases. The provider result must retain game class, information structure, solution concept, algorithm/version, status, tolerance, residuals where defined, selection rule and completeness. One equilibrium found is not an exhaustive catalogue. Unsupported/nonconverged is not economic zero. Noisy choice, inertia or learning is not automatically a Nash prediction; solver restart frequencies are not behavioural probabilities.

Preserve named RK4, mixed-Nash, actual correlated-incentive/objective and information-set CFR requirements per advertised method. Test application response to an unsupported concept and incomplete catalogue before accepting a provider result. Moving code does not close its numerical leaf.

### PN04 — scoped consumers/release (T17.09/.10/.12)

In Paignia T17.12, create/extend the planned `tests/test_game_consumer_evidence.py` to reject duplicated application IDs, source-tree-only imports, mismatched artifacts and toy-only consumers. Require two distinct real applications using the same qualified artefacts. Reimbursement plus Innovate may be first; retain CareOps's existing optional consumer work without making it an extra blanket gate. A Voiage schema wrapper alone is not another application.

Test standalone minimal/default/advertised-extra dependency closures including build/transitive features. Static consumers must remain eligible without Kairos/Voiage; a claimed dynamic capability without qualified adapter evidence fails. Retain every unresolved obligation outside the released scope. Namespace availability, provenance, licences/security, ABI/schema compatibility, package contents and rollback remain publication checks; do not fabricate their receipts.

## Consumer-specific information and observation tests

Reuse T17.14/.15/.17 and existing strategic pilot work in [PR #103](https://github.com/edithatogo/new-drug-reimbursement-game/pull/103).

A manufacturer policy sees only declared public signals and its own permitted information, not a payer's private threshold or another firm's hidden cost. Two worlds with equal lawful observations and legal actions yield equal inputs/actions under matched policy randomness; seed a private-field/action-mask leak and require rejection. Offline solution access to the full mathematical game is distinct from live policy access. Changing solver exploration must not perturb paired exogenous simulation draws under the declared coupling.

Label information recipient, timing, disclosure, commitments, observation model and equilibrium selection. Conventional EVPI/EVSI, research net benefit, strategic information value and social information value are distinct. Application welfare assumptions and transfer-versus-resource accounting stay explicit. Reuse Voiage SI01-SI04 and its signed-social contract; do not implement a second evaluator here. Preserve signed reference results without clipping. Averages of separately solved fully observed hidden-state games cannot substitute for an information-consistent policy/game.

Preserve parameter/model/equilibrium/measurement/simulation-replicate identities. The finite consumer noise fixture uses one parameter state with replicates A=[-1,1], B=[1,-1]: conditional means and parameter EVPI are 0, while incorrectly treating replicates as parameter draws gives 1. Voiage owns the arithmetic; this application must provide truthful identities and valuation. Report Monte Carlo precision and inner/outer budgets rather than disguising numerical noise as learnable uncertainty.

Medicines scripts, quantities, spending and treated stock remain different source measures. Supply-interval/coding/coverage changes are observation-process candidates, not automatic adoption/abandonment effects. Effective and known-at dates support lawful historical forecasts. Innovate owns generic utilisation/innovation methods; Atlas owns source/terminology qualification; this application owns payer/manufacturer/eligibility and economic assumptions. Do not infer missing indication, patient count or private use from aggregate PBS records.

## Coordination and limits

Central policy: repository-standards PR #120 `docs/paignia-library-boundary.md` and `docs/scientific-result-contracts.md`. Innovate PR #570 retains its 52 packets and broad innovation/hype-impact purpose. Kairos Track 114/PR #381 retains execution acceptance; Voiage PR #1287/#1288 and issue #1286 retain outcome, information and VOP promotion. Preserve concurrent source-transfer work and reconcile its files before implementation.

Every implementation receipt binds exact source/artifact/feature closure, commands/nonzero test counts, assumptions, numerical tolerances and reviews. All plans remain separate from actual runtime/scientific acceptance. This reconciliation preserves the concurrent scientific requirements while retaining the implemented immutable consumer switch. It changes no solver, economic function, native fixture or provider revision and supplies no scientific or full release acceptance. Native sources/manifests/locks are byte-identical to locally tested candidate `1b83a7cf9d18fe966dee1f4cd1aa8969872824ce`; the new guard and plan reconciliation have their own Python and documentation checks.


## Current implementation and where the remaining work executes

The source guard and seven positive/negative tests check the actual immutable
provider, absent local cores (including alternate workspace paths), mutable
branches, lock drift and patch overrides.
Rust 1.75 formatting, Clippy, 14 existing application tests and the synthetic
native game test passed; Python discovery passed 148 tests. These checkpoints
remain distinct from the richer result/observation/information contracts above.
No missing provider field or unimplemented algorithm is inferred to exist.

Only application T17.09 and T17.11 are active here. The provider's fourteen
leaves remain in [Paignia T17](https://github.com/edithatogo/paignia/tree/main/conductor/tracks/t17_game_runtime_ecosystem_20261107),
and T17.10 remains with the second application. PN01–PN04 amend those same IDs;
they create no separate completion ledger.

| Requirement retained from the concurrent refinement | Implementation / acceptance owner |
|---|---|
| Game class, information structure, solution concept, algorithm/version, status, tolerance, residuals, selection and catalogue completeness | Paignia T17.01 and the applicable numerical leaf; application T17.09 rejects unsupported/incomplete results. |
| Corrected algorithm results, independent references and unsupported-versus-zero behavior | Paignia T17.04–T17.07 plus application acceptance; preserve legitimate correction differences instead of enforcing a flawed legacy output. |
| Lawful player observations, private-field/action-mask leaks, matched policy randomness and solver/exogenous stream isolation | Paignia T17.14/.15/.17 and selected application/PR #103 cases; conditional on claiming that information or dynamic profile. |
| Distinct information-value concepts, recipient/timing/disclosure/commitments and signed welfare accounting | Application T17.11 / PR #103 supply semantics and valuation; Voiage SI01–SI04 and its signed-social contract own arithmetic. |
| Parameter/model/equilibrium/measurement/replicate identity and the A=[−1,1], B=[1,−1] noise counterexample | Application T17.11 preserves input identities; Voiage owns the 0-versus-1 arithmetic oracle and precision/budget contract. |
| Medicines measures, coverage/coding/supply intervals, effective/known-at dates and absent indication/private-use fields | Existing application strategic pilot PR #103, Innovate observation methods and Atlas source/terminology qualification; no generic Paignia economic model. |
| Isolated minimal/default/advertised-extra closures, two real applications and artifact/publication receipts | Paignia T17.02/.03/.12 and each consumer's receipt; source creation and toy fixtures do not discharge them. |

The [local plan](plan.md) breaks the application acceptance work into bounded
future slices. Static perfect-information release eligibility does not acquire
blanket Voiage, hidden-information or native-dynamics prerequisites: require
only the scientific and semantic contracts of the capabilities actually claimed.
