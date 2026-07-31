# Pinned UOGTO and Kairos runtime contracts

This note records the read-only contract inspection used for the first
domain-neutral game-runtime milestone. It is tied to the immutable revisions in
`ecosystem.lock.toml`; it does not claim compatibility with either repository's
moving default branch.

## UOGTO

- Repository: `https://github.com/edithatogo/UOGTO`
- Revision: `849386068399a764ad5304cc8a0ffe53094b091c`
- Reused surfaces:
  - `jsonld/core.context.jsonld`, `jsonld/extensions.context.jsonld`, and
    `jsonld/packs.context.jsonld` define the context composition boundary.
  - `ontologies/extensions/kg-execution-bindings.ttl` defines declarative
    execution bindings.
  - `shapes/core.shacl.ttl`, `shapes/execution.shacl.ttl`, and
    `shapes/game-types.shacl.ttl` are the validation authorities.
  - `examples/extensive-form-game.ttl`,
    `examples/normal-form-game.jsonld`, and
    `examples/stochastic-markov-game.jsonld` are the relevant conformance
    examples.
- Application terms remain in the reimbursement applied pack. The Rust crates
  consume canonical identifiers and do not redefine UOGTO ontology terms.

## Kairos

- Repository: `https://github.com/edithatogo/kairos`
- Revision: `fae901558f07b7b717a676adbafbe2cdc78dea1c`
- Released Rust surfaces inspected:
  - `kairo-ecs-types`: `SimTime`, `EventKind::Custom`, `ScheduleRequest`,
    `DispatchedEvent`, `StepOutcome`, and versioned DTO wrappers.
  - `kairo-ecs-core`: deterministic `Scheduler`, `SchedulerFacade`, and
    `RecordingScheduler`.
  - `kairo-ecs-state`: generational entities and component stores.
  - `kairo-ecs-rng`: authoritative random-stream capability.
- The game runtime may compile a validated execution plan into
  `ScheduleRequest` values and map dispatched events back to trace records. It
  must not own time advancement, priority ordering, event IDs, ECS allocation,
  random streams, DES, or ABM.

## Current compatibility boundary

The first runtime milestone intentionally keeps the Kairos adapter as a
versioned proposal rather than adding a source or path dependency. The pinned
Kairos event kind is a numeric custom code, so stable allocation of game event
codes and the DTO representation require upstream agreement. Until that
contract is released, native compilation is an external compatibility gate and
unsupported execution semantics must fail explicitly.
