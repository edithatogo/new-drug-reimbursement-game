# T15 plan

## Phase 0 — autonomous metadata and rights discovery

- [x] Build the ranked public dataset/API metadata inventory and classification worklist from `sourcing.md`. (`afd252f`)
- [x] Programmatically retrieve, hash, receipt, and triangulate public catalogues, schemas, dictionaries, licences, terms, and aggregate documentation. (`afd252f`)
- [x] Emit negative/deferred receipts for inaccessible, conflicting, incomplete, restricted, or declined sources without retrieving prohibited raw payloads. (`afd252f`)
- [x] Record recommended acquisition mode, alternatives, rationale, minimization, fallback, retry condition, and exact authorization stop. (`afd252f`)
- [x] Review checkpoint: validate receipt structures, authority, rights, classification, lineage, storage boundary, and leakage controls. (`afd252f`, `d2e2920`)

## Phase 1 — authority and environment

- [ ] Select raw acquisition only when the T13/Atlas coverage matrix proves an approved-derived or public aggregate route insufficient.
- [ ] For every selected source, bind exact fields, custodian, lawful basis, terms, operators, environment, retention, deletion, transformation, and destination.
- [~] Source all public metadata first, then identify each source, custodian, purpose, classification, terms, and legal/privacy basis. Public metadata is complete; source-specific lawful basis and custodian permission remain external.
- [ ] Approve controlled storage, access roles, retention, deletion, and incident procedures.
- [ ] Review checkpoint: verify no acquisition begins before every applicable gate passes.

## Phase 2 — controlled derivation

- [x] Add tests for repository leakage, prohibited tracked data/archive paths, and release-scope exclusions. (`d2e2920`)
- [ ] Implement or configure isolated ingestion and Atlas-derived-record handoff.
- [ ] Validate hashes, transformations, lineage, minimization, and deletion receipts.
- [ ] Review checkpoint: privacy, security, licensing, and reproducibility review.

## Phase 3 — disposition

- [ ] Authorize only permitted derived outputs and destinations.
- [ ] Archive access, extraction, deletion, and negative receipts.
- [ ] Completion checkpoint: verify the repository and release artifacts contain no raw data.
- [ ] Completion checkpoint: refresh source terms and invalidate dependent receipts at the exact ingestion/release commit.
