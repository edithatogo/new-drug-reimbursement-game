# Quality gates

The baseline gate is:

```bash
python scripts/validate_scope.py
python -m unittest discover -s tests -p 'test_*.py'
python -m compileall -q src scripts tests
python scripts/discover_ecosystem.py --offline-fixture-mode
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
```

Integration gates additionally require all pinned components in
`ecosystem.lock.toml` to resolve through:

```bash
python scripts/discover_ecosystem.py --check
```

A local path manifest is evidence for a workstation only and must never be
committed.
