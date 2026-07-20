# Codex covering prompt — New Drug Reimbursement Game

Open the repository as the working directory and execute the detailed plan in
`CODEX_IMPLEMENTATION_PROMPT.md`.

Read first, in order:

1. `AGENTS.md`
2. `README.md`
3. `DEPENDENCY_MIGRATION_PLAN.md`
4. `ecosystem.lock.toml`
5. `docs/architecture/capability-boundary.md`
6. `docs/architecture/rust-game-runtime.md`
7. `CODEX_IMPLEMENTATION_PROMPT.md`
8. `IMPLEMENTATION_STATUS.md`

The owner has made these architectural decisions:

- Do not use other people's libraries for capabilities being developed in the
  `edithatogo` ecosystem.
- Voiage is authoritative for value of information.
- Kairos is the low-level Rust simulation/time/event/state engine.
- UOGTO is the game-theory ontology and semantic contract.
- Reimbursement Atlas is the reimbursement evidence/provenance layer.
- Hugging Face inputs and publication targets must be under `edithatogo/*`.
- The general game-theory capability must be abstracted from the new-drug
  reimbursement application and should mature into a Rust library above Kairos.
- Generic Python/Rust libraries are allowed only with an explicit ADR and a plan
  for stabilization, replacement, or migration into the ecosystem.
- Never add the source book, scans, figures, tables, or lengthy excerpts. Cite
  Pekarsky (2015), DOI 10.1007/978-3-319-08903-4, and the relevant chapter or
  equation.

Start by running `python scripts/run_quality_gate.py`. Preserve the clean-room
boundary and all working tests. Work in small, reviewable commits. Prioritize:

1. the domain-neutral Rust game runtime and UOGTO conformance;
2. upstream-compatible contracts with Kairos, Voiage, UOGTO, and Reimbursement
   Atlas;
3. complete, assumption-explicit reconstructions of Pekarsky Games 1–3;
4. post-2015 extensions: empirical opportunity cost, equity, managed entry,
   repeated/incomplete-information games, capacity, lifecycle pricing, and
   innovation spillovers;
5. evidence/VOI integration using only owner-controlled repositories and
   approved derived data.

Do not claim regulator-grade validity. In the final response report exact tests,
commits, pins, licences, mathematical checks, unresolved assumptions, and
upstream work still required.
