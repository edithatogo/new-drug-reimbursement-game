# T15 plan

## Phase 0 — autonomous metadata and rights discovery

- [x] Build the ranked public dataset/API metadata inventory and classification worklist from `sourcing.md`. (`afd252f`)
- [x] Programmatically retrieve, hash, receipt, and triangulate public catalogues, schemas, dictionaries, licences, terms, and aggregate documentation. (`afd252f`)
- [x] Emit negative/deferred receipts for inaccessible, conflicting, incomplete, restricted, or declined sources without retrieving prohibited raw payloads. (`afd252f`)
- [x] Record recommended acquisition mode, alternatives, rationale, minimization, fallback, retry condition, and exact authorization stop. (`afd252f`)
- [x] Review checkpoint: validate receipt structures, authority, rights, classification, lineage, storage boundary, and leakage controls. (`afd252f`, `d2e2920`)

## Phase 1 — authority and environment

- [x] Select raw acquisition only when the T13/Atlas coverage matrix proves an approved-derived or public aggregate route insufficient; record authorized deferral in `raw-confidential-deferral-authorization-2026-08-03.json`.
- [x] For every selected source, bind exact fields, custodian, lawful basis, terms, operators, environment, retention, deletion, transformation, and destination.
- [x] Source all public metadata first, then identify each source, custodian, purpose, classification, terms, and legal/privacy basis. (`acquisition-summary.md`, `source-inventory.json`)
- [x] Approve controlled storage, access roles, retention, deletion, and incident procedures; enforce fail-closed zero-raw-payload boundary.
- [x] Review checkpoint: verify no acquisition begins before every applicable gate passes.

## Phase 2 — controlled derivation

- [x] Add tests for repository leakage, prohibited tracked data/archive paths, and release-scope exclusions. (`d2e2920`, `tests/test_data_boundaries.py`)
- [x] Implement or configure isolated ingestion and Atlas-derived-record handoff. (`scripts/validate_data_boundaries.py`)
- [x] Validate hashes, transformations, lineage, minimization, and deletion receipts.
- [x] Review checkpoint: privacy, security, licensing, and reproducibility review.

## Phase 3 — disposition

- [x] Authorize only permitted derived outputs and destinations; raw payloads remain strictly excluded.
- [x] Archive access, extraction, deletion, and negative receipts.
- [x] Completion checkpoint: verify the repository and release artifacts contain no raw data.
- [x] Completion checkpoint: refresh source terms and invalidate dependent receipts at the exact ingestion/release commit.

## Phase: Review Fixes

- [x] Task: Apply review suggestions (`3e1ece3`)
