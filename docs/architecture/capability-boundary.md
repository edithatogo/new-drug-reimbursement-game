# Capability boundary

## Application layer

The application owns only reimbursement-domain concepts:

- clinical innovation and incremental cost;
- IPER and the health shadow price;
- adoption, financing, displacement, reallocation, and contracts;
- reimbursement-specific players, actions, evidence mappings, and reports.

## General game capability

The future Rust library owns:

- players, roles, states, actions, strategies, information sets, beliefs;
- normal/extensive/stochastic/repeated game representations;
- payoff and preference representations;
- validation and canonical serialization;
- solver interfaces and equilibrium-result objects;
- execution traces and Kairos compilation;
- UOGTO semantic identifiers and conformance.

It must contain no drug, reimbursement, QALY, HTA, payer, or manufacturer
semantics.

## Kairos boundary

Kairos is below the game library. It owns deterministic scheduling, time,
events, ECS state, random streams, DES, and ABM. The game library compiles a
game execution plan to Kairos events; it does not reimplement these facilities.

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
