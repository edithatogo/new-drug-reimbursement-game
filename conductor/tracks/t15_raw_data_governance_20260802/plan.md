# T15 plan

## Phase 0 — autonomous metadata and rights discovery

- [ ] Build the ranked public dataset/API metadata inventory and classification worklist from `sourcing.md`.
- [ ] Programmatically retrieve, hash, receipt, and triangulate public catalogues, schemas, dictionaries, licences, terms, and aggregate documentation.
- [ ] Emit negative/deferred receipts for inaccessible, conflicting, incomplete, restricted, or declined sources without retrieving prohibited raw payloads.
- [ ] Record recommended acquisition mode, alternatives, rationale, minimization, fallback, retry condition, and exact authorization stop.
- [ ] Review checkpoint: validate receipt schemas, authority, rights, classification, lineage, storage boundary, and leakage controls.

## Phase 1 — authority and environment

- [ ] Source all public metadata first, then identify each source, custodian, purpose, classification, terms, and legal/privacy basis.
- [ ] Approve controlled storage, access roles, retention, deletion, and incident procedures.
- [ ] Review checkpoint: verify no acquisition begins before every applicable gate passes.

## Phase 2 — controlled derivation

- [ ] Add tests for repository leakage, prohibited fields, credentials, and fail-closed export.
- [ ] Implement or configure isolated ingestion and Atlas-derived-record handoff.
- [ ] Validate hashes, transformations, lineage, minimization, and deletion receipts.
- [ ] Review checkpoint: privacy, security, licensing, and reproducibility review.

## Phase 3 — disposition

- [ ] Authorize only permitted derived outputs and destinations.
- [ ] Archive access, extraction, deletion, and negative receipts.
- [ ] Completion checkpoint: verify the repository and release artifacts contain no raw data.
- [ ] Completion checkpoint: refresh source terms and invalidate dependent receipts at the exact ingestion/release commit.
