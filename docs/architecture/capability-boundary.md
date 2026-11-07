# Capability boundary

## Application layer

The application owns only reimbursement-domain concepts:

- clinical innovation and incremental cost;
- IPER and the health shadow price;
- adoption, financing, displacement, reallocation, and contracts;
- reimbursement-specific players, actions, evidence mappings, and reports.

## General game capability

The external **Paignia** `paignia-core` and `paignia-solve` packages are the
reusable Rust game boundary. They are immutable Git dependencies of this
application, with no local generic implementation. Their supported subset
is finite game validation, backward induction, chance-node expectations, and
pure Nash enumeration. The broader capability remit and pending roadmap cover:

- players, roles, states, actions, strategies, information sets, beliefs;
- normal/extensive/stochastic/repeated game representations;
- payoff and preference representations;
- validation and canonical serialization;
- solver interfaces and equilibrium-result objects;
- solver diagnostics and selected policies, with optional native execution;
- UOGTO semantic identifiers and conformance.

It must contain no drug, reimbursement, QALY, HTA, payer, or manufacturer
semantics.

Specific games, payoff construction, and domain policy stay in CareOps,
Innovate, or the reimbursement application. HEOR valuation is a distinct
capability supplying valued inputs under explicit units, perspectives, and
assumptions; it is not owned by the generic solver or Kairos. Voiage retains VOI.

## Kairos boundary

Kairos owns deterministic scheduling, time, events, ECS state, random streams,
DES, and ABM. Static game representation and solving have no Kairos dependency,
direct or transitive. An optional adapter depends on game core and Kairos and
compiles supported game execution into native events; neither provider depends
on the adapter. The adapter does not reimplement scheduling or use a non-Rust
simulation fallback.

`Solution.trace` currently records solver analysis of alternative branches.
The adapter projects only the selected policy and declared chance outcomes into
a new causal execution trace. Live policies receive their permitted observation
and legal actions, not the full solver graph or opponent-private state. Game
specification, instance, session and trace identities remain distinct from the
adapter's full generational Kairos entity/event handles.

Static expectation-based solving consumes no simulation random draws. Future
stochastic solvers accept an explicit random source/configuration; native
execution uses separately identified Kairos streams. Solver budget changes must
not advance unrelated simulation streams. Resume support must restore qualified
policy, native state and RNG state together, or reject that capability.

Paignia is the implementation home. This application's
[T17](../../conductor/tracks/t17_game_runtime_ecosystem_20261107/index.md) owns
only .09 consumer acceptance and .11 valued-input contracts; the other stable
IDs forward to Paignia or the second application. The provider retains S01 RK4,
S02 mixed Nash, S03 CE and S04 CFR/CFR+ as open scientific obligations. Moving
source never validates those methods or permits a duplicate corrected solver.

Two real static consumers can qualify the same bounded artifacts without
waiting for an optional adapter or every future algorithm. The local finite
application test is useful native integration evidence, not full release/model
acceptance. Registry publication, independent artifacts and second-consumer
acceptance remain distinct. See [the source transfer history](paignia-transfer-map.md).

## UOGTO boundary

UOGTO is declarative and semantic. The Rust runtime validates and executes a
supported subset and emits traces that preserve UOGTO identifiers. Domain
extensions remain separate applied packs.

## Voiage boundary

The application constructs strategy-specific net-benefit or health-benefit
samples. Voiage computes VOI. The application does not contain EVPI/EVPPI/EVSI
algorithms.

## Evidence boundary

Reimbursement Atlas owns source acquisition, provenance, licensing, mapping,
and human review. This application consumes reviewed derived records and adds
model-specific parameter interpretations with their own provenance.
