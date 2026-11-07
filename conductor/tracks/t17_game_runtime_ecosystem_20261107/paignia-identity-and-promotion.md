# Paignia provider and reimbursement-consumer supplement

Date: 2026-11-08. Owner: existing T17 and issue #100. Status: planning; implementation/package/consumer acceptance remains separately evidenced. Read [spec.md](spec.md) and [plan.md](plan.md). Preserve T17.01-T17.17 through the source transfer; this document neither creates replacement task IDs nor completes a scientific obligation.

## Actual provider and transfer

The maintainer has created [edithatogo/paignia](https://github.com/edithatogo/paignia). It is the authoritative reusable Rust game-library repository. This repository is the historical incubator and a reimbursement application/consumer. Repository creation does not require waiting for package qualification; package qualification and publication remain pending until their own receipts exist.

| Historical source | Receiving package/component | Acceptance boundary |
|---|---|---|
| `crates/uogto-game-core` | Paignia `paignia-core` | Typed domain-neutral game/result contract and versioned migration |
| `crates/uogto-game-solve` | Paignia `paignia-solve` | Each claimed algorithm has independent numerical evidence |
| T17.08 execution adapter | Optional `paignia-kairos` | Native dynamic execution, not a static prerequisite |
| Semantic mapping | Optional `paignia-uogto` | Versioned UOGTO conformance, not a second ontology engine |
| Tabular boundary | Optional `paignia-arrow` | Arrow/Polars semantics, not mandatory static-core dataframes |

Resolve the current source-transfer PR, exact manifest and immutable Paignia revision before changing dependencies. Do not globally rename historical commands or copy a second independently evolving solver. Renaming/transferring source is possible before qualification; it must not be described as qualification. Preserve licence/source history, fixtures, package identities of old releases and rollback evidence.

Provider T17.01-.08/.12-.17 belongs in Paignia. T17.09/.10 retain the two selected application-consumer owners; .11 retains reimbursement-specific valuation ownership. Keep the leaf IDs and their existing obligations. The receiving [Paignia PR #1](https://github.com/edithatogo/paignia/pull/1) supplies integration and scientific-contract refinements without taking over initial source transfer.

## Responsibility and independent readiness

Paignia owns game representations, supported algorithms, behavioural-model mechanisms and diagnostics. This application owns institutions, payer/manufacturer/patient roles, empirical assumptions, payoff/valuation construction and clinical interpretation. Innovate owns innovation dynamics and observation models; Kairos owns execution time/state/resources/RNG; Voiage owns decision and information-value arithmetic; UOGTO owns semantics.

Static solving works without Kairos, Voiage, Python, pandas or xarray. Independent Gambit/OpenSpiel references remain isolated test oracles. Minimal solver/core, supported static methods and optional dynamics qualify independently. Preserve S01-S04 obligations and unsupported states; unfinished general CFR or dynamic replay does not block a smaller verified perfect-information/pure-Nash release. The two-real-application rule gates scoped package/consumer acceptance, not creation of the already existing provider repository.

## PN aliases amend existing leaves, not a second status ledger

Execute one behaviour within the owning T17 file budget. Record the exact target after source reconciliation, a meaningful failing assertion, minimal implementation, passing nonzero tests, review and receipt. New test paths below are proposed until created. Stop on missing source fields, ambiguous information structure or unqualified algorithms; do not invent assumptions to close a task.

### PN01 — identity/provenance mapping (T17.01/.03)

Use Paignia's actual `extraction-manifest.json` and transfer map, plus the application's existing extraction guard. If a separate package map remains needed, use `docs/architecture/paignia-package-map.json` and a focused `tests/test_paignia_package_map.py`, not a duplicate source inventory.

Acceptance assertions: repository is `edithatogo/paignia`; repository_created is true from the actual GitHub record; published/qualified remains false absent its evidence; incubator paths and source commits remain historical provenance. Unsupported future adapters are not inferred to exist. Run the existing guard and the created test with a genuine negative control. Do not assert repository_created=false merely because a package is unqualified.

### PN02 — immutable application dependency switch (T17.09 and provider .03)

The transfer owner moves/renames source; the application owner consumes its exact candidate. Freeze affected manifest/import/lock paths in a bounded leaf and retain last-qualified rollback. A temporary qualified Git/artifact dependency is not package-index publication.

Write the external-consumer test first: with the provider checkout unavailable, run a real reimbursement case against the produced package, preserve declared semantics, reject unsupported games and expose solver/version identity. Test before/after results against an independent reference, not merely each other. Record package hash, lock, feature closure and nonzero test count; preserve legitimate corrected-result differences rather than forcing parity with a flawed seed. No provider pin is changed by this planning update.

### PN03 — one algorithm owner and honest result (T17.01/.04-.07)

Extend the existing ownership guard with duplicated-owner and missing-S01-S04 negative cases. The provider result must retain game class, information structure, solution concept, algorithm/version, status, tolerance, residuals where defined, selection rule and completeness. One equilibrium found is not an exhaustive catalogue. Unsupported/nonconverged is not economic zero. Noisy choice, inertia or learning is not automatically a Nash prediction; solver restart frequencies are not behavioural probabilities.

Preserve named RK4, mixed-Nash, actual correlated-incentive/objective and information-set CFR requirements per advertised method. Test application response to an unsupported concept and incomplete catalogue before accepting a provider result. Moving code does not close its numerical leaf.

### PN04 — scoped consumers/release (T17.09/.10/.12)

Extend existing `tests/test_game_consumer_evidence.py` to reject duplicated application IDs, source-tree-only imports, mismatched artifacts and toy-only consumers. Require two distinct real applications using the same qualified artefacts. Reimbursement plus Innovate may be first; retain CareOps's existing optional consumer work without making it an extra blanket gate. A Voiage schema wrapper alone is not another application.

Test standalone minimal/default/advertised-extra dependency closures including build/transitive features. Static consumers must remain eligible without Kairos/Voiage; a claimed dynamic capability without qualified adapter evidence fails. Retain every unresolved obligation outside the released scope. Namespace availability, provenance, licences/security, ABI/schema compatibility, package contents and rollback remain publication checks; do not fabricate their receipts.

## Consumer-specific information and observation tests

Reuse T17.14/.15/.17 and existing strategic pilot work in [PR #103](https://github.com/edithatogo/new-drug-reimbursement-game/pull/103).

A manufacturer policy sees only declared public signals and its own permitted information, not a payer's private threshold or another firm's hidden cost. Two worlds with equal lawful observations and legal actions yield equal inputs/actions under matched policy randomness; seed a private-field/action-mask leak and require rejection. Offline solution access to the full mathematical game is distinct from live policy access. Changing solver exploration must not perturb paired exogenous simulation draws under the declared coupling.

Label information recipient, timing, disclosure, commitments, observation model and equilibrium selection. Conventional EVPI/EVSI, research net benefit, strategic information value and social information value are distinct. Application welfare assumptions and transfer-versus-resource accounting stay explicit. Reuse Voiage SI01-SI04 and its signed-social contract; do not implement a second evaluator here. Preserve signed reference results without clipping. Averages of separately solved fully observed hidden-state games cannot substitute for an information-consistent policy/game.

Preserve parameter/model/equilibrium/measurement/simulation-replicate identities. The finite consumer noise fixture uses one parameter state with replicates A=[-1,1], B=[1,-1]: conditional means and parameter EVPI are0, while incorrectly treating replicates as parameter draws gives1. Voiage owns the arithmetic; this application must provide truthful identities and valuation. Report Monte Carlo precision and inner/outer budgets rather than disguising numerical noise as learnable uncertainty.

Medicines scripts, quantities, spending and treated stock remain different source measures. Supply-interval/coding/coverage changes are observation-process candidates, not automatic adoption/abandonment effects. Effective and known-at dates support lawful historical forecasts. Innovate owns generic utilisation/innovation methods; Atlas owns source/terminology qualification; this application owns payer/manufacturer/eligibility and economic assumptions. Do not infer missing indication, patient count or private use from aggregate PBS records.

## Coordination and limits

Central policy: repository-standards PR #120 `docs/paignia-library-boundary.md` and `docs/scientific-result-contracts.md`. Innovate PR #570 retains its 52 packets and broad innovation/hype-impact purpose. Kairos Track114/PR381 retains execution acceptance; Voiage PR1287/1288 and issue1286 retain outcome, information and VOP promotion. Preserve concurrent source-transfer work and reconcile its files before implementation.

Every implementation receipt binds exact source/artifact/feature closure, commands/nonzero test counts, assumptions, numerical tolerances and reviews. All plans remain separate from actual runtime/scientific acceptance. This edit performs no package rename, source transfer, dependency switch, publication or merge.
