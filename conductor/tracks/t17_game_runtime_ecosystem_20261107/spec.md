# T17 specification — reusable Rust game capability

## Problem and observed baseline

At repository revision `ab4ce37a905a8cf9bb54d1ad905de4b0f34b7165`,
`uogto-game-core` has no dependencies and `uogto-game-solve` depends only on
`uogto-game-core`. The crates already provide finite game validation, backward
induction, chance-node expectations, and pure Nash enumeration. Those facts do
not establish mixed Nash, general correlated equilibrium, CFR/CFR+, or a
qualified continuous replicator method.

The refinement at `90602b93db7352bfb307bac7852db211cf94af1e` confirms that
`GameSpecification` is versioned, IDs are strings, and `Solution.trace` records
solver analysis. The application manifest declares core/solve dependencies, but
its Rust library and executable do not call them; declarations are not consumer
qualification. The receiving work remains
[issue 100](https://github.com/edithatogo/new-drug-reimbursement-game/issues/100)
and this track, coordinated with
[Innovate PR 570, G01–G04](https://github.com/edithatogo/innovate/pull/570).
No additional coordinator or library repository is introduced.

The existing capability should become reusable through package contracts before
any repository extraction. Earlier descriptions of a library "above Kairos"
mean optional simulation integration, not a mandatory dependency for static
solving. CareOps, Innovate and the reimbursement application are candidate
consumers; naming one here does not qualify it.

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

Keep representation independent of `ComponentStore`, simulation clocks and
generational runtime handles. Normal-form, perfect-information and future
information-set profiles must state their own supported capabilities. The
receiving core currently has no information-set representation; ontology labels
do not add that execution capability. Keep specification, instantiated model,
session, policy artifact and trace IDs distinct and preserve UOGTO namespaces.

The proposed [Kairos extraction map](https://github.com/edithatogo/kairos/blob/acd00bdc30b745d9c3fbc38d1352785128f44567/conductor/contracts/game-extraction-map.md)
(`K01.games`) in [PR 382](https://github.com/edithatogo/kairos/pull/382) records
these source differences for T17.01 and T17.13. Its file is
`conductor/contracts/game-extraction-map.md`; the proposal does not qualify an API.

| Boundary | Required versioned decision |
|---|---|
| String game IDs versus numeric players and generational entity handles | Explicit namespace and reversible mapping; reject duplicates, unknown IDs and stale generations. Array position or a truncated handle is not semantic identity. |
| Zero-probability chance edges accepted here but rejected by Kairos constructors | Declare probability domain, mass tolerance and zero-edge treatment; reject invalid/non-finite values without silently changing a game. |
| Absent player payoff treated as zero here but rejected by Kairos | Declare complete payoff vectors or an intentional sparse-zero profile. Accidental omissions must not acquire a new interpretation during conversion. |
| Tolerance/lexicographic ties here versus first traversed maximum in Kairos | Version tie/equilibrium selection and test reordered inputs; conversion must preserve the declared decision rule. |
| Solver result and backend diagnostics | Own a stable result envelope with algorithm/version, class, status, residual and tolerance; keep backend-specific diagnostics optional. Unsupported and nonconverged are not equilibrium results. |

Simulation is opt-in through a separate adapter package, provisionally named
`uogto-game-kairos`. That name and its Cargo commands below describe a future
target; the package does not exist at the observed baseline. The adapter does
not make static solvers depend on Kairos through a default feature.

The proposed [Kairos execution port](https://github.com/edithatogo/kairos/blob/acd00bdc30b745d9c3fbc38d1352785128f44567/conductor/contracts/game-execution-port.md)
(`K01.port`, `conductor/contracts/game-execution-port.md`) is the adapter
contract input, not an accepted native adapter. `Solution.trace` contains postorder
visits to hypothetical alternatives, including unchosen and chance branches.
It remains a solver diagnostic. The adapter executes only a selected policy and
declared chance process, producing a new causal trace with native event identity,
time and committed effects. Expected solver payoffs are distinct from realized
outcomes and subsequent economic valuation.

A live policy receives only its lawful observation: player/information-set ID,
observation revision, permitted information and legal actions. Offline solving
may inspect the full mathematical game; that does not authorize exposing hidden
state to an acting policy. Unknown information structures, simultaneous-action
semantics and unsupported lifecycle operations fail explicitly. Same-tick order,
stale/duplicate commands, cancellation and zero-time limits use the qualified
Kairos port; the adapter adds no second scheduler. Numerical `dt` is not a
simulation tick until the profile defines units and conversion.

Deterministic expectation-based solvers need no RNG. Future stochastic solvers
take an explicit RNG source/configuration without importing Kairos. Native
execution obtains separate purpose/identity streams from Kairos; changing a
solver's iteration budget must not advance exogenous simulation streams. Record
algorithm, seed/stream policy and versions, plus the comparison's declared
coupling across strategies/draws. Checkpoint/resume supports only qualified
policy/native state and RNG combinations; unsupported resume fails explicitly.

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

T17.04–T17.07 own the corrected reusable implementations. Kairos Track 110 keeps
the source-side regression and transfer/retirement record; do not implement a
second permanent corrected solver there. A bounded static release may exclude
these pending methods, with explicit unsupported status and replacement plans.
Their exclusion never closes S01–S04 or permits importing old approximations as
qualified implementations. Reuse the existing Clarabel backend where qualified;
its numerical acceptance and dependency decision remain explicit.

## Acceptance and sequencing

Package contracts and independent consumption come first. T17.01–T17.03 qualify
the selected static profile; T17.09–T17.10 qualify two real application cases;
T17.12 checks those receipts. Select two distinct real applications; reimbursement
plus Innovate is an eligible pair after qualification, and CareOps is another
candidate. Both may be static-only. Require only the algorithms/features each advertised
case actually uses, not every pending method or the optional Kairos adapter.
Record exact revisions, artifact hashes, capability/profile versions, commands,
fixtures and results outside the provider checkout. Two toy fixtures or two
wrappers in this repository do not count. This can establish eligibility for a
bounded library and a separate repository-extraction decision; it does not
publish packages or create a repository. Full T17 closure still requires its
remaining obligations or explicit supported/withdrawn completion decisions.

T17.02 checks resolved normal/build dependencies for every supported static
feature profile. T17.03 builds unpacked artifacts with the provider checkout
unavailable. This must expose Kairos's current external `include!` generated
component file and repository-relative ontology fixtures if those features are
transferred. Include/generate the required supported data inside its owning
package, or explicitly exclude that feature. Resolve the declared compiler
profiles (Kairos 1.99, this workspace 1.75) through actual builds; declarations
alone are not compatibility evidence. Keep optimization backends and optional
semantic/serialization tooling out of the minimal representation closure.

The existing deferred scientific-consumer track still controls provider/pin
qualification. Static package work can proceed independently; native adapter
qualification waits for `K01.port` and the accepted Kairos contract. T17.13–T17.16
cover conversion, permitted observations, RNG isolation and replay; T17.17 adds
the currently missing independent information-set representation. Only the
capabilities actually claimed make those receipts mandatory; a bounded
perfect-information static release does not wait for that representation.
Consumer valuation checks remain consumer-owned; T17.11 is the reimbursement
application's valued-input port, not a blanket gate on other static consumers.
Preserve old consumer pins and output versions until their replacements pass
consumer-specific tests.
Rollback restores the last qualified package/adapter version, never a parallel
scheduler or a silent Python/JavaScript solver fallback.

Routine leaves need a scoped diff review and focused tests. Numerical methods
and public contract changes need an independent specialist agent review of the
mathematics or interface, fixes, and relevant CI. This is a solo-maintainer
workflow; repeated human approval is not a routine implementation gate. Genuine
unresolved economic interpretations remain explicit alternatives.

## Scope of this planning change

Refine the existing T17 package/adapter boundary and preserve scientific obligations.
No source relocation, runtime dependency, pin, release, repository creation, or
consumer qualification occurs in this change. T00–T16 and their limitations
remain historical records. All seventeen implementation leaves remain pending.
