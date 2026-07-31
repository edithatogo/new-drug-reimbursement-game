# Build, schema, extraction, and release controls

## Deterministic inputs

- Python build backends are exact pins in `pyproject.toml`.
- Rust dependency resolution is committed in `Cargo.lock`.
- Ecosystem integrations are full commit SHAs in `ecosystem.lock.toml`.
- `docs/generated/governance-inventory.json` is regenerated only with
  `python scripts/governance_inventory.py --write`; CI uses `--check`.
- `SOURCE_DATE_EPOCH` is the current commit timestamp for release builds.

`scripts/validate_packaging.py` builds the wheel and source distribution twice
in isolated environments, normalizes source-archive metadata, requires
byte-identical SHA-256 results, installs the wheel without dependencies in a
new virtual environment, and imports the installed package. Passing this check
is build evidence, not release authorization.

## Schema policy

- Every persisted schema has an explicit `schema_version`.
- Additive optional fields may retain the current major version.
- Removing fields, changing meanings, or changing default interpretation
  requires a major schema version.
- Unknown or unsupported versions fail closed.
- UOGTO identifiers, evidence revisions, solver tolerance, tie policy, and
  trace ordering must survive serialization.
- Generated artifacts are checked for exact drift in CI.

## Extraction policy

`extraction-manifest.json` is the authoritative initial crate set.
`scripts/validate_extraction.py` verifies that the domain-neutral crates exist,
have only the declared internal dependency edge, and contain no application
vocabulary. Extraction copies complete Git history or a reviewable subtree; it
does not authorize publishing a new repository.

## Release gates

A candidate can be assembled only after local and hosted gates pass. Publishing
or signing it additionally requires:

1. reconciled Voiage and Hugging Face licence metadata;
2. independent health-economics and ontology review;
3. security, legal, privacy, and reproducibility approval;
4. extraction approval if the Rust crates are released separately;
5. an explicit release authorization.

Absent evidence leaves the corresponding gate pending. A successful build,
test run, draft pull request, or candidate archive is never reported as a
release.
