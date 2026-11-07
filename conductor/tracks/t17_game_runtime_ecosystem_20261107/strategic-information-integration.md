# T17 strategic-information provider and reimbursement pilot

Date: 8 November 2026. Status: roadmap accepted for incorporation; all numerical,
package, application and scientific qualification remains pending. This supplements
T17 and issue #100; it creates no new coordinator, package or repository.

## Boundary and sequencing

The generic Rust packages own supported game representations, solving and result
diagnostics. Voiage owns VOI. UOGTO owns semantics; Kairos is optional for native
dynamic execution. The reimbursement application owns payoff construction,
health-economic valuation, evidence interpretation and disclosure/contract terms.
Keep domain economics out of game-core/solve and never duplicate VOI formulas here.

Preserve the current bounded static qualification: T17.01–03, two real application
cases under T17.09–10, and T17.12. Reimbursement plus Innovate is an eligible pair
after actual qualification; CareOps is another candidate, not a mandatory blocker.
Both cases may be static and must use the same qualified package artifacts outside
the provider checkout. A Voiage wrapper or two toy cases is not a second real consumer.
Advanced methods, dynamic execution and strategic VOI are required only for claims
that use them. Their exclusion does not close S01–S04 or the full T17 programme.
No provider pin or independent extraction decision changes in this addendum.

## Pending work within existing leaves

- [ ] T17.01/result contracts: distinguish unsupported representation, no equilibrium
  in the searched class, nonconvergence, selected equilibrium and catalogue coverage.
  Export algorithm/version, tolerances, residuals and explicit selection semantics.
  Do not infer probabilities from repeated solver restarts or label a pure catalogue
  as exhaustive over mixed equilibria. Keep backend-specific diagnostics optional.
- [ ] T17.13–14 and T17.17: map specification, instance, policy, player, session and
  trace identities without conflating analyst draws with player observations. Live
  policies receive only permitted observations/legal actions. Incomplete-information
  profiles require accepted representation and solving semantics, not just labels.
- [ ] T17.15–16: isolate solver RNG from exogenous simulation RNG; distinguish solver
  traversal from selected-policy/chance execution; qualify policy/native/RNG replay
  together. Cache/warm-start evidence binds information regime, solution concept,
  selection rule, valuation and tolerance so search order cannot silently select value.
- [ ] T17.04–07: retain inherited RK4, mixed-Nash, CE and CFR scientific obligations.
  Test only claims actually supported by the candidate. Normal-form mixed Nash does
  not establish Bayesian games; general CE does not establish Bayes correlated equilibrium.
- [ ] T17.11: extend the application-owned valued-input port for an optional Voiage
  signed-information consumer. Preserve actor values, perspective, weights, units,
  time, transfers and paired-world provenance. Solver failure is not value zero.

## Reimbursement pilot, separate from generic package acceptance

First reproduce a tiny exact static game. Then construct a bounded synthetic
research/pricing or evidence-contingent-contract case. The application declares
who learns what and when, commitment/pricing assumptions and feasible choices.
Compare fixed responses, recomputed responses, research-only and disclosure-only
regimes. Acquisition and disclosure are different interventions.

Use Voiage's qualified methods for information value; preserve negative actor or
social differences rather than clipping them. Social aggregation requires declared
cardinal comparability and weights; transfers are not automatically resource costs.
Research-cost and ENBS claims require the accepted Voiage study contracts. Empirical
calibration stays gated on reviewed Atlas-derived inputs and domain review; synthetic
fixtures are not reimbursement advice or independent empirical validation.

## Acceptance and execution

Use the shared SI-V01–SI-V08 cases in the linked Voiage plan: single-player VOI
reduction, matching pennies, multiple equilibria, lawful observations, signed values,
invalid-provider diagnostics, existing solver suites and an installed consumer.
The provider owns solver correctness; Voiage owns value arithmetic. Keep external
Gambit/OpenSpiel comparisons isolated with licences and pinned versions, never runtime
imports. Hub identifiers remain edithatogo/* and publication needs separate authority.

Before a runtime slice, freeze exact public types and test names, add a failing
witness, implement minimally, run focused tests and retain exact artifacts/review.
Run AGENTS.md's full required checks for the final implementation; this planning
entry is not a claim that Cargo, native, Python or consumer tests have passed.
Existing task statuses, historical receipts and unsupported dispositions remain intact.

## Coordinated Voiage plan

See the [shared SI01–SI04 plan and SI-V01–SI-V08 cases](https://github.com/edithatogo/voiage/blob/c414752a228e7af5d689d9d5876f8f7372c42447/conductor/tracks/scientific_ecosystem_alignment_20261029/strategic-information-integration.md).
That source commit is a planning proposal, not a dependency pin or an acceptance receipt.
