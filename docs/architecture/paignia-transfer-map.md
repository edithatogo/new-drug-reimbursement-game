# Paignia transfer history and current ownership

The generic Rust game seed has moved to
[edithatogo/paignia](https://github.com/edithatogo/paignia). This application now
consumes an exact provider revision and retains its economic model, game and
valuation. `extraction-manifest.json` records the current immutable provider and
historical source provenance; the package directories are absent here.

## Source record

| Snapshot | Revision / disposition |
|---|---|
| Incubator main after PR #102 | `f6c1c87b6b00875b33c1e19401c1de09481913ce`; original `uogto-game-core` / `uogto-game-solve` source. |
| Naming supplement PR #101 | `c7b2539b60ecb6457c75164c2a759730f5c1ec7c`; reconciled with all seventeen T17 leaves. |
| Prepared Paignia seed | `9ee388502bfe5f71d22b363dbb9c74f032a07ad4`; renamed native source, unchanged algorithms and source-level application test. |
| Paignia initial implementation | `12b22ce7571b9c590405bf53c2c1c5862b49cd64`, [PR #2](https://github.com/edithatogo/paignia/pull/2); reviewed tree `f438caa902e07a7ec5b7be3020c94d5b7e4868e8`. |

Paignia's [native CI](https://github.com/edithatogo/paignia/actions/runs/42420971781)
passed on stable and Rust 1.75. Its native provider suite and two-test
outside-workspace extracted-source smoke do not close registry-artifact or
real-application release qualification. The first smoke exposed an inherited
Cargo field-replacement bug; the corrected anchored mapping passed actual
native execution. No solver algorithm changed.

## Per-source disposition

| Source | Owner after transfer | Limits retained |
|---|---|---|
| `uogto-game-core` / `uogto-game-solve` seed | Paignia `paignia-core` / `paignia-solve` | Original Apache-2.0 attribution in provider root and crate notices; finite-game scope only. |
| Application Chapter 7/8 functions, economic fixtures and `paignia_static_game` | This application | Full economic assumptions, units and model qualification remain local; the synthetic case is not empirical evidence. |
| Kairos normal-form/Clarabel candidates and ECS-coupled game helpers | Kairos until selective Paignia/adapter handoff | No copy in this transfer; S01–S04 and source regressions remain open. |
| Kairos restricted ontology parser/codegen and legacy fixtures | Source retained pending explicit mapping/packaging work | Legacy `https://kairos.dev/ontology/game-theory#` is not canonical UOGTO; missing fixture provenance must be resolved. |
| UOGTO ontologies, IRIs, SHACL, semantic fixtures and reference inspection | UOGTO | Ontology/docs CC-BY-4.0; code MIT. No ontology or Python core is copied into Paignia. |

The detailed source audit and executable provider work now have one home in
[the Paignia transfer map](https://github.com/edithatogo/paignia/blob/main/docs/architecture/paignia-transfer-map.md).
It records the inspected Kairos `e76b97be2ea3712645933d903822ff6381c8883e`
and UOGTO `a5f90557c40f054255a1d6c2541fd76f07aa5090` snapshots; those audit
references do not upgrade this application's other provider pins.

## Ownership and acceptance

Provider T17.01–.08/.12–.17 belong to Paignia. This application retains .09/.11;
.10 belongs to the second real consumer. The old names/IDs and source commits
remain historical records, not parallel active implementations. The original
future repository-extraction gate now concerns bounded package-release
eligibility because the user chose the standalone home. Its artifact and
consumer requirements remain open.

Rollback uses a reviewed immutable provider revision or explicit ordinary
revert preserving history. No local compatibility solver or non-Rust fallback
is introduced. The application guard rejects a duplicate local core, mutable
reference, patch override or inconsistent Cargo/ecosystem lock.
