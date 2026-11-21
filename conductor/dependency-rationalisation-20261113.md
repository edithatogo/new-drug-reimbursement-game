# Rust dependency rationalisation — new-drug-reimbursement-game (2026-11-13)

## Repository-specific decisions

- Verified: small Rust workspace declares custom game-domain crates and MSRV 1.75; do not automatically adopt heavyweight runtime, Polars or neural dependencies.
- Align finite-game semantics and numerical proof oracles with Paignia/UOGTO; avoid duplicating Paignia's graph validation and game-solver types until shared contracts are accepted.
- Evaluate typed errors with Thiserror and separate Serde game interchange DTOs; retain domain-specific reimbursement rules outside generic Paignia and Kairos crates.
- Add Proptest for budget/payoff bounds, game action permutations, rational choice/tie stability and solver non-regression; Criterion for bounded equilibrium computation.
- Do not introduce Tokio, Reqwest, SQLx, Ratatui or PyO3 without concrete integration boundary and retained deterministic trace; upstream Kairos/ Paignia handoffs require exact pin compatibility.

## Evidence and implementation gates

- Status: **planned / scope registered**; no runtime substitution or CI/benchmark success is asserted by this file.
- Reconcile existing Conductor tracks before new work; preserve domain-specific APIs, schema versions, privacy and public CLI behaviour.
- Write failing contract tests before code changes, then run native targeted/full tests, fmt/clippy and relevant integration/supply-chain checks at exact SHA.
- Use Cargo feature/duplicate inventories plus security, licence and MSRV assessments, and fixed-fixture performance baselines before adoption.
- Record adopt / retain / reject / defer decisions and rollback; only close after verified evidence.
