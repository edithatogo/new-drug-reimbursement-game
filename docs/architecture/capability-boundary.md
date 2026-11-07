# Capability boundary

## Application layer

The application owns only reimbursement-domain concepts:

- clinical innovation and incremental cost;
- IPER and the health shadow price;
- adoption, financing, displacement, reallocation, and contracts;
- reimbursement-specific players, actions, evidence mappings, and reports.

## General game capability

The existing `uogto-game-core` and `uogto-game-solve` crates are the package
boundary for the reusable Rust library outside Kairos. Their supported subset
is finite game validation, backward induction, chance-node expectations, and
pure Nash enumeration. The broader capability remit and pending roadmap cover:

- players, roles, states, actions, strategies, information sets, beliefs;
- normal/extensive/stochastic/repeated game representations;
- payoff and preference representations;
- validation and canonical serialization;
- solver interfaces and equilibrium-result objects;
- generic solver traces, with Kairos compilation in an optional adapter;
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

Reuse the packages here before considering another repository. An independent
repository is eligible for a separate extraction decision only after two real
consumers qualify the same package artifacts. A wrapper or toy fixture is not
a real consumer. [T17](../../conductor/tracks/t17_game_runtime_ecosystem_20261107/index.md)
records the pending work, including inherited Kairos S01 RK4, S02 mixed Nash,
S03 correlated equilibrium, and S04 CFR/CFR+ obligations. Moving code does not
validate those methods, and historical track completion does not discharge
them. This clarification changes no source, dependency pin, or runtime package.

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
