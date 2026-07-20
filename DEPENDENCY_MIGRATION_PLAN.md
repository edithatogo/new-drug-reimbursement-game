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
| General finite-game representation and solvers | Rust incubator crates in this repo | A dedicated Rust game-theory repository above Kairos (working name only) | Crates extracted without importing reimbursement-domain types |
| Evidence ingestion/provenance | Local reviewed-export reader | `edithatogo/reimbursement-atlas` | Atlas publishes a stable PEA-derived-view contract |
| Python game solver | Minimal conformance oracle | Rust game runtime binding | Python solver removed from production path; retained only as oracle fixture |
| Numerical arrays | Python lists in core; NumPy only inside Voiage | Voiage/Rust backend | No direct NumPy dependency in application core |
| RDF validation | Static TTL/JSON-LD plus lightweight checks | UOGTO build/SHACL toolchain | Application ontology passes upstream UOGTO validation in CI |

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
