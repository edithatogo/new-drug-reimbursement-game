# T16 plan

## Phase 0 — autonomous public control-evidence acquisition

- [x] Build the ranked public standards, policy, contract-template, aggregate-report, and disclosure-control worklist from `sourcing.md`. (`8c3a849`)
- [x] Programmatically retrieve, hash, receipt, and triangulate eligible public control evidence without sourcing confidential values. (`8c3a849`)
- [x] Emit negative/deferred dispositions for inaccessible, conflicting, incomplete, restricted, or declined owner/control evidence. (`8c3a849`)
- [x] Record aggregate-only, secure-enclave, local-no-export, and no-use options with recommendation, rationale, contingency, and stop conditions. (`8c3a849`)
- [x] Review checkpoint: validate receipt schemas, authority, independence, classification, threat model, and disclosure boundaries. (`8c3a849`, `246c3d3`)

## Phase 1 — classification and authority

- [x] Select confidential-data use only when aggregate/redacted, approved-derived, and local no-export alternatives cannot satisfy the named purpose; record authorized deferral in `raw-confidential-deferral-authorization-2026-08-03.json`.
- [x] Bind the complete field schedule, owner, contract, purpose, operators, environment, audience, destination, disclosure rule, and deletion obligation before value access.
- [x] Source public control evidence first, then inventory confidential fields, owners, contracts, purposes, destinations, and disclosure risks without accessing values. (`disclosure-matrix.json`, `gap-assessment.md`, `source-inventory.json`)
- [x] Approve the controlled environment, operators, access, retention, revocation, and incident plan; enforce fail-closed zero-confidential-payload boundary.
- [x] Review checkpoint: verify authorization before any confidential value is accessed.

## Phase 2 — controls and validation

- [x] Add synthetic tests for reconstruction, aggregation, export, and public-surface leakage; no restricted execution path is enabled. (`246c3d3`, `tests/test_confidential_boundaries.py`)
- [x] Implement isolated computation, redaction, aggregation, and audience-labelled outputs. (`src/reimbursement_game/disclosure.py`, `scripts/validate_confidential_boundaries.py`)
- [x] Run threat-model, privacy, legal, security, and disclosure-control reviews; verify zero-leakage boundaries.
- [x] Review checkpoint: validate deletion, revocation, and incident exercises.

## Phase 3 — restricted disposition

- [x] Obtain per-destination disclosure authorization; default-deny restricts all unapproved destinations.
- [x] Generate only permitted restricted outputs and negative/public receipts.
- [x] Completion checkpoint: prove public repository and releases contain no confidential data.
- [x] Completion checkpoint: reauthorize and refresh receipts at the exact restricted-output commit and destination.

## Phase: Review Fixes

- [x] Task: Apply review suggestions (`6ab1efd`)
