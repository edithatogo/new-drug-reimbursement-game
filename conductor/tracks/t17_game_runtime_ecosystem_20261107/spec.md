# T17 specification — reusable Rust game capability

## Problem and observed baseline

At repository revision `ab4ce37a905a8cf9bb54d1ad905de4b0f34b7165`,
`uogto-game-core` has no dependencies and `uogto-game-solve` depends only on
`uogto-game-core`. The crates already provide finite game validation, backward
induction, chance-node expectations, and pure Nash enumeration. Those facts do
not establish mixed Nash, general correlated equilibrium, CFR/CFR+, or a
qualified continuous replicator method.

The existing capability should become reusable through package contracts before
any repository extraction. Earlier descriptions of a library "above Kairos"
mean optional simulation integration, not a mandatory dependency for static
solving. CareOps and Innovate are intended consumers; neither counts as a
qualified consumer merely because this track names it.

## Ownership and dependency direction

| Owner/package | Responsibility | Dependency boundary |
|---|---|---|
| `uogto-game-core` | Domain-neutral game specifications, identifiers, validation, and result contracts | No Kairos or application dependency |
| `uogto-game-solve` | Supported generic Rust solving algorithms and diagnostics | Depends on game core; static solvers have no Kairos dependency, including transitive dependencies |
| Optional game-to-Kairos adapter | Compile supported game execution into native simulation events and preserve trace identity | Depends on game core and Kairos; neither provider depends on this adapter |
| UOGTO | Game semantics and semantic conformance | Runtime implements a declared subset; no local semantic fork |
| CareOps, Innovate, reimbursement application | Specific games, player interpretations, payoff construction, and domain policy | Consume the generic library; do not place their models in Kairos or generic crates |
| HEOR valuation capability | Health-economic valuation under declared units, perspectives, and assumptions | Supplies valued inputs; distinct from equilibrium solving and simulation |
| Voiage | Value-of-information methods | Receives decision/uncertainty inputs; no duplicate VOI implementation here |

Kairos retains scheduling, simulation time, events, ECS, RNG, DES, and ABM. A
game solver must not acquire a scheduler to solve a static payoff table. A
simulation adapter must execute the Rust core and report unavailable or
unsupported operations explicitly; no host-language engine fallback.

## Public contracts

The versioned game/result contract records supported representations, UOGTO
identifiers, payoff ordering, finite-value requirements, algorithm/version,
tolerance, tie policy, termination status, and numerical diagnostics. Unsupported
representations are distinguishable from a proved absence of an equilibrium or
failure to converge. Domain units and valuation provenance belong to consumer
input contracts; they must not introduce health or reimbursement concepts into
the generic crates.

Simulation is opt-in through a separate adapter package, provisionally named
`uogto-game-kairos`. That name and its Cargo commands below describe a future
target; the package does not exist at the observed baseline. The adapter does
not make static solvers depend on Kairos through a default feature.

## Inherited scientific obligations

The [Kairos scientific completion register](https://github.com/edithatogo/kairos/blob/main/conductor/scientific-completion.md)
and [Track 110](https://github.com/edithatogo/kairos/blob/main/conductor/tracks/110-scientific-method-completion/index.md)
remain authoritative for the inherited obligations. These links coordinate
work; they do not update `ecosystem.lock.toml` or qualify its old pin.

| ID | Completion obligation retained by T17 | Plan leaf |
|---|---|---|
| S01 RK4/replicator | Named legacy Euler baseline; real four-stage RK4 or an explicitly versioned/renamed supported Euler API; time-varying callbacks; analytic logistic replicator, step refinement, event discontinuities, positivity, conservation. Clipping alone does not prove accuracy. | T17.04 |
| S02 mixed Nash | Actual supported mixed-Nash/support-enumeration/Lemke–Howson algorithms or explicit unsupported boundaries; dominance, matching pennies, coordination, degeneracy, multiple equilibria, rectangular games; best-response residual/exploitability and the strictly dominant-action counterexample. | T17.05 |
| S03 correlated equilibrium | Actual incentive constraints and a qualified LP/conic solve; feasibility, incentive residual, and objective comparison. A product of Nash marginals is not a general CE solver. | T17.06 |
| S04 CFR/CFR+ | Supported information-set graphs, chance transitions, legal actions, imperfect-recall rejection; separate Kuhn helpers; independently checked Kuhn/Leduc values, exploitability, and iteration scaling. | T17.07 |

Relocating code never closes these obligations. Each method ends with an
accurate supported implementation and independent evidence, or an explicit
unsupported/withdrawn API plus a documented replacement decision. Keep original
Kairos IDs, owner history, callers, negative results, and output-version effects
in the evidence. Core arithmetic tests and a copied implementation used as an
oracle are insufficient. Pin reference versions, licenses, fixture hashes, and
acceptance tolerances before measuring. Gambit/OpenSpiel comparisons, where
used, run in isolated research jobs and never become runtime dependencies.

## Acceptance and sequencing

Package contracts and independent consumption come first. An independent
repository becomes eligible for a separate extraction decision only after two
distinct real consumers execute their own application cases using the same
versioned package artifacts, outside the provider source checkout. The intended
pair is CareOps and Innovate. Record exact revisions, artifact hashes, commands,
fixtures, and results; two toy fixtures or two wrappers in this repository do
not count. Evidence establishes eligibility, not automatic repository creation.

The existing deferred scientific-consumer track still controls provider/pin
qualification. Static package work can proceed independently; native adapter
qualification waits for the accepted Kairos contract. Preserve old consumer
pins and output versions until their replacements pass consumer-specific tests.
Rollback restores the last qualified package/adapter version, never a parallel
scheduler or a silent Python/JavaScript solver fallback.

Routine leaves need a scoped diff review and focused tests. Numerical methods
and public contract changes need an independent specialist agent review of the
mathematics or interface, fixes, and relevant CI. This is a solo-maintainer
workflow; repeated human approval is not a routine implementation gate. Genuine
unresolved economic interpretations remain explicit alternatives.

## Scope of this planning change

Create and register T17, clarify ownership, and preserve scientific obligations.
No source relocation, runtime dependency, pin, release, repository creation, or
consumer qualification occurs in this change. T00–T16 and their limitations
remain historical records. All twelve implementation leaves start pending.
