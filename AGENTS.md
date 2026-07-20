# Agent instructions

Read these files before editing:

1. `README.md`
2. `DEPENDENCY_MIGRATION_PLAN.md`
3. `ecosystem.lock.toml`
4. `docs/architecture/capability-boundary.md`
5. `CODEX_IMPLEMENTATION_PROMPT.md`

## Non-negotiable constraints

- Do not add the source book, scans, copied figures, copied tables, or lengthy
  excerpts.
- Cite Pekarsky (2015), its chapter/equation location, and the DOI when an
  implementation depends on a book concept.
- Prefer `edithatogo` ecosystem components over third-party capability
  libraries.
- Do not add runtime dependencies on Nashpy, Gambit/pygambit, OpenSpiel, BCEA,
  heemod, or dampack.
- Hugging Face IDs must start with `edithatogo/`.
- Voiage owns VOI; Kairos owns simulation time/events/DES/ABM; UOGTO owns game
  semantics; Reimbursement Atlas owns reimbursement evidence/provenance.
- Keep application and general game capability separate. Domain-neutral code
  belongs in Rust crates and must not mention drugs, QALYs, reimbursement, HTA,
  or manufacturers.
- The Python game solver is a conformance oracle, not the future product.
- Never silently choose among ambiguous economic interpretations. Represent
  named alternatives and provenance.
- Mark experimental models honestly.

## Required checks

```bash
python scripts/validate_scope.py
python -m unittest discover -s tests -p 'test_*.py'
python -m compileall -q src scripts tests
cargo test --workspace
```
