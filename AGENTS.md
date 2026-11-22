# Agent instructions

Read these files before editing:

1. `README.md`
2. `CODEX_REPOSITORY_ACTIVATION_PROMPT.md` when activating a restored checkout
3. `DEPENDENCY_MIGRATION_PLAN.md`
4. `ecosystem.lock.toml`
5. `docs/architecture/capability-boundary.md`
6. `CODEX_IMPLEMENTATION_PROMPT.md`

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
  belongs in the Rust packages maintained in `edithatogo/paignia`, consumed here
  at an immutable revision. Do not recreate a local generic solver or package
  override. Generic source must not mention drugs, QALYs, reimbursement, HTA,
  or manufacturers; application games and valuation remain here.
- The Python game solver is a conformance oracle, not the future product.
- Never silently choose among ambiguous economic interpretations. Represent
  named alternatives and provenance.
- Mark experimental models honestly.

## Game capability intake

Every newly identified, added or materially changed game follows the
[contributor intake rule](CONTRIBUTING.md#game-capability-intake) and the linked
[UOGTO semantic contract](https://github.com/edithatogo/UOGTO/blob/main/docs/contracts/downstream-game-intake.md)
and [Paignia implementation contract](https://github.com/edithatogo/paignia/blob/main/docs/integrations/downstream-game-intake.md).
Record UOGTO's `reuse_existing`, `extension_required`, `unsupported` or
`mapping_review_pending` disposition separately from Paignia's `reuse_existing`,
`extension_required`, `unsupported`, `domain_only` or `assessment_pending`.
Reuse the same intake key in all three repositories. Payer/manufacturer rules,
valuation, empirical evidence and payoff construction remain here. Adoption
needs exact accepted provider revisions and the actual semantic/native/consumer
checks; intake does not close T17 release or valued-input acceptance gates.

## Required checks

```bash
python scripts/validate_scope.py
python -m unittest discover -s tests -p 'test_*.py'
python -m compileall -q src scripts tests
python scripts/discover_ecosystem.py --offline-fixture-mode
ty check src
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
```

Before opening or updating a pull request, also run `basedpyright`.
