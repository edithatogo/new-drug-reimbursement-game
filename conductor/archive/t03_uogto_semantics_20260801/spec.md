# Specification

## Overview

Define the application-owned reimbursement extension and its execution
boundary to UOGTO and Kairos without forking upstream ontology or scheduler
semantics.

## Requirements

- Pin and document the authoritative UOGTO revision and applied-pack boundary.
- Represent reimbursement concepts as application extension terms while
  preserving UOGTO identifiers, context composition, and validation authority.
- Export a valid, finite JSON-LD game instance with stable case identifiers,
  players, governance rules, and economic values.
- Map executable elements to the runtime's domain-neutral execution boundary;
  generic scheduling, time, event ordering, ECS state, and randomness remain
  upstream Kairos responsibilities.
- Record an upstream-ready proposal surface and reviewable patch plan without
  copying or redefining UOGTO core semantics in this repository.

## Acceptance criteria

- The pinned UOGTO/Kairos contract note and capability-boundary documentation
  are internally consistent with the adapters and Rust runtime.
- Focused adapter and runtime tests pass, including rejection of non-finite
  economic values.
- The UOGTO exporter emits stable JSON-LD identifiers and canonical context
  terms for a representative case.
- No upstream source files, ontology core terms, or scheduler implementation
  are forked into the application.
- Evidence records identify the exact revision, validation commands, and
  resulting commits.

## Out of scope

- Changing UOGTO ontology core semantics.
- Adding a Kairos source/path dependency before its upstream event contract is
  released.
- Empirical reimbursement calibration or external evidence approval.
