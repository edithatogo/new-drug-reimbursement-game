# Dependency and capability migration plan

## Governing rule

A dependency is not acceptable merely because it is convenient. For every
capability dependency, ask whether the capability belongs in the `edithatogo`
ecosystem. If it does, integrate the owned component or incubate the missing
module for extraction.

## Capability ledger

| Capability | Current implementation | Authoritative destination | Exit condition |
|---|---|---|---|
| VOI, EVPI, EVPPI, EVSI, ENBS | `VoiageAdapter`; no duplicate algorithms here | `edithatogo/voiage` and its Rust core | All application VOI calls pass Voiage conformance fixtures |
| Deterministic event time, queues, ECS, DES/ABM | Kairos scenario/event contract only | `edithatogo/kairos` | Native adapter consumes a released Kairos binding |
| Game semantics | UOGTO application extension | `edithatogo/UOGTO` | Reimbursement extension accepted or versioned as an official applied pack |
| General finite-game representation and solvers | `uogto-game-core` and `uogto-game-solve` in this repo | Reusable domain-neutral Rust packages outside Kairos; separate repository only after two real consumers qualify | Static dependency closure excludes Kairos; package artifacts consumed without application types; inherited scientific obligations retain independent evidence |
| Evidence ingestion/provenance | Local reviewed-export reader | `edithatogo/reimbursement-atlas` | Atlas publishes a stable PEA-derived-view contract |
| Python game solver | Minimal conformance oracle | Rust game runtime binding | Python solver removed from production path; retained only as oracle fixture |
| Numerical arrays | Python lists in core; NumPy only inside Voiage | Voiage/Rust backend | No direct NumPy dependency in application core |
| RDF validation | Static TTL/JSON-LD plus lightweight checks | UOGTO build/SHACL toolchain | Application ontology passes upstream UOGTO validation in CI |

## Game package boundary before repository extraction

[T17](conductor/tracks/t17_game_runtime_ecosystem_20261107/index.md) is pending
execution. It reuses the existing generic Rust crates; it does not create a new
repository, change pins, or claim a released package. Static solvers depend on
game core without Kairos. A separate optional execution adapter depends on game
core and qualified Rust Kairos APIs. CareOps, Innovate, and the reimbursement
application retain their specific games and payoffs; UOGTO supplies semantics,
HEOR valuation stays distinct, and Voiage owns VOI.

Two distinct real consumers must execute their own cases against the same
versioned package artifacts before independent repository extraction becomes
eligible for a separate decision. Preserve the existing deferred provider/pin
qualification track. Transferring the S01 RK4, S02 Nash, S03 CE, and S04 CFR
implementations or ownership never supplies their scientific validation.
Historical T00–T16 completion remains bounded by its original evidence.

## Explicitly excluded capability libraries

The runtime must not depend on Nashpy, Gambit/pygambit, OpenSpiel, BCEA,
heemod, or dampack. They may be named in historical design notes only. Any
future comparative validation must run in an isolated, non-runtime research
job, have a licence review, and produce only conformance results—not copied
implementation.

## Generic libraries

Generic serialization, FFI, testing, numerical, or web libraries can be used
when they do not replace an owned capability. Each addition requires an ADR
recording:

1. why the standard library is insufficient;
2. licence and supply-chain posture;
3. API boundary;
4. whether the dependency should later become an ecosystem module;
5. removal or stabilization criteria.
