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
| General finite-game representation and solvers | Immutable `paignia-core` / `paignia-solve` Git dependencies | `edithatogo/paignia`, independent of Kairos for static solving | Native consumer execution plus provider artifact and two-real-consumer release acceptance; S01–S04 retain independent completion |
| Evidence ingestion/provenance | Local reviewed-export reader | `edithatogo/reimbursement-atlas` | Atlas publishes a stable PEA-derived-view contract |
| Python game solver | Minimal conformance oracle | Rust game runtime binding | Python solver removed from production path; retained only as oracle fixture |
| Numerical arrays | Python lists in core; NumPy only inside Voiage | Voiage/Rust backend | No direct NumPy dependency in application core |
| RDF validation | Static TTL/JSON-LD plus lightweight checks | UOGTO build/SHACL toolchain | Application ontology passes upstream UOGTO validation in CI |

## Paignia dependency and provider handoff

Paignia now owns generic Rust game representation and solvers. This application
retains its game/payoff model and consumes the actual immutable provider
revision recorded in Cargo, its lockfile and `extraction-manifest.json`. The
source guard rejects local generic crate copies, path overrides, mutable refs
and lock drift. Other provider pins retain their prior qualification scope.

The original [T17](conductor/tracks/t17_game_runtime_ecosystem_20261107/index.md)
now keeps application leaves .09 and .11. Paignia owns the fourteen provider
leaves; .10 belongs to the second application. The stable IDs and PN aliases
are retained as handoffs rather than duplicate active solver work.

Static solving has no Kairos dependency. The optional Paignia adapter depends
on the game library and qualified Rust Kairos APIs. UOGTO owns canonical
semantics, HEOR owns valuation contracts and Voiage owns VOI. Application games
and assumptions remain outside generic solvers and the simulation kernel.

The user-selected repository exists. Two real consumers of the same qualified
artifacts remain the bounded package-release gate; repository creation and
source transfer supply no scientific or release evidence. A source-level Git
consumer test does not discharge T17.03 or the full real-model receipt. S01 RK4,
S02 mixed Nash, S03 CE and S04 CFR/CFR+ remain open with Paignia and the Kairos
source-side register. Historical T00–T16 receipts retain their original scope.

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
