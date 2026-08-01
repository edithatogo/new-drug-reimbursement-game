# UOGTO upstream proposal and patch plan

This document is the reviewable handoff for the reimbursement extension. It
does not copy UOGTO source or redefine its core semantics.

## Current application boundary

The application emits a JSON-LD `uogto:GameInstance` with the pinned UOGTO
context composition and stable instance identifiers. Reimbursement-specific
values use the `ndrg` applied-pack namespace. Core game identity, players, and
governing rules retain UOGTO identifiers. `UogtoExporter` rejects non-finite
economic values before serialization.

Executable plans remain domain-neutral. The Rust runtime preserves semantic
identifiers in traces and delegates scheduling, time advancement, event
ordering, ECS allocation, and random streams to the Kairos contract described
in [the pinned contract note](./pinned-runtime-contracts.md).

## Proposed upstream review surface

The upstream UOGTO proposal should be opened as a small, independently
reviewable patch containing:

1. the reimbursement applied-pack vocabulary for price, net price,
   confidential rebate, displacement, financing, reallocation, contract,
   evidence development, implementation, R&amp;D, capital market, jurisdiction,
   perspective, and equity;
2. JSON-LD context entries and SHACL shapes for those application terms;
3. competency questions and Games 1-3 examples demonstrating composition with
   UOGTO core; and
4. declarative execution-binding mappings that reference, rather than replace,
   the Kairos event contract.

The patch must be reviewed against UOGTO revision
`849386068399a764ad5304cc8a0ffe53094b091c`, include no scheduler or ontology
core fork, and preserve backwards compatibility for existing UOGTO examples.
Any changed identifier or binding requires a new pinned revision and a
follow-up compatibility receipt before this repository changes its lockfile.

## Disposition

The repository-side boundary is complete and testable. Upstream vocabulary,
SHACL, and execution-binding acceptance remain an upstream change-management
event; this track does not claim that a moving upstream branch is released.
