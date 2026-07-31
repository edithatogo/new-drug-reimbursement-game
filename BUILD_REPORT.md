# Build and validation report

- Handoff version: `0.4.0`
- Environment date: `2026-07-27`
- Critical portable checks passed: **yes**

## Scope and clean-room validation

```text
scope validation passed
```

## Python unit tests

```text
24 tests passed
```

The test suite includes the PEA/economic invariants, Chapter-8-style game,
adapters, reference game, copyright/ecosystem scope, bundle activation contract,
version synchronization, Conductor mapping, and ecosystem-clone discovery.

## Python compilation

```text
python -m compileall -q src scripts tests
passed
```

## Ecosystem discovery contract

```text
python scripts/discover_ecosystem.py --offline-fixture-mode
offline ecosystem contract validation passed (4 components; clones not asserted)
```

The offline gate validates the lock file, owner scope, full revisions, and remote
normalization. It deliberately does not claim that workstation clones exist.
Clone resolution is performed by the activation prompt on the user's machine.

## Rust, Ruff, and MyPy

The 2026-07-27 workstation activation used Python 3.14.6, Ruff 0.16.0, mypy
2.3.0, Cargo 1.96.1, and Rust 1.96.1. Ruff passed, mypy checked 12 source files
without issues, and Rust formatting, Clippy with warnings denied, three unit
tests, and all doc-test targets passed.

GitHub Actions run `30254455585` independently passed the `python` and `rust`
jobs on `main`.

## Git and distribution checks

The final handoff process separately verifies:

- repository integrity with `git fsck --full`;
- a Git bundle containing `main` and annotated tag `v0.4.0`;
- bundle restoration into a clean checkout;
- source-ZIP tree identity against the tagged Git tree;
- SHA-256 integrity for the bundle, source ZIP, covering prompt, and bootstrap
  helper;
- absence of book binaries, credentials, nested Git repositories, and absolute
  workstation paths in committed files.
