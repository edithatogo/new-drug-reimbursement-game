# Paignia dependency and application boundary

The generic Rust implementation now lives in
[edithatogo/paignia](https://github.com/edithatogo/paignia). This repository has
one Rust workspace member, the reimbursement application. Its `paignia-core`
and `paignia-solve` dependencies use the same exact Git revision, declared in
Cargo, `Cargo.lock`, `ecosystem.lock.toml` and `extraction-manifest.json`.
Local generic cores, mutable refs and dependency patch overrides are rejected.

The application owns its game, health-economic valuation, institutions and
empirical assumptions. `paignia_static_game` builds a finite offer/response graph
using existing valuation and executes the actual native provider. Its analytic
result is useful integration evidence; complete economic-model and package
release acceptance remain open.

## Provider responsibilities

Paignia owns versioned representation/results, supported algorithms and solver
diagnostics. The current bounded native seed has no Kairos dependency. An
optional Paignia adapter will consume qualified Kairos time/events/state/RNG and
preserve causal execution separately from solver analysis. UOGTO owns canonical
semantics/IRIs/SHACL; Paignia implements only a declared executable subset.
HEOR valuation and Voiage VOI remain separate capabilities.

The [canonical provider T17](https://github.com/edithatogo/paignia/tree/main/conductor/tracks/t17_game_runtime_ecosystem_20261107)
retains fourteen provider leaves including inherited S01–S04 and independent
artifact qualification. Application T17.09 and T17.11 stay here; T17.10 stays
with the distinct second consumer. This ownership handoff preserves all original
IDs without parallel implementations or competing completion claims.

## Qualification

- Source/native dependency execution proves the tested integration case at an
  exact revision; it is not registry publication or empirical validity.
- Provider extracted-source smoke tests are not a substitute for release
  artifacts and two real application receipts against the same supported profile.
- Static cases do not wait for the optional adapter or unrelated advanced
  methods. Each advertised method/feature still requires its own controls.
- Legacy Python game solving remains an independent reference oracle, never a
  fallback core behind a native execution claim.

See [the application T17 plan](../../conductor/tracks/t17_game_runtime_ecosystem_20261107/plan.md),
[the capability boundary](capability-boundary.md), and
[the source transfer history](paignia-transfer-map.md).
