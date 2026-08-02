# T16 plan

## Phase 0 — autonomous public control-evidence acquisition

- [x] Build the ranked public standards, policy, contract-template, aggregate-report, and disclosure-control worklist from `sourcing.md`. (`8c3a849`)
- [x] Programmatically retrieve, hash, receipt, and triangulate eligible public control evidence without sourcing confidential values. (`8c3a849`)
- [x] Emit negative/deferred dispositions for inaccessible, conflicting, incomplete, restricted, or declined owner/control evidence. (`8c3a849`)
- [x] Record aggregate-only, secure-enclave, local-no-export, and no-use options with recommendation, rationale, contingency, and stop conditions. (`8c3a849`)
- [x] Review checkpoint: validate receipt schemas, authority, independence, classification, threat model, and disclosure boundaries. (`8c3a849`, `246c3d3`)

## Phase 1 — classification and authority

- [ ] Select confidential-data use only when aggregate/redacted, approved-derived, and local no-export alternatives cannot satisfy the named purpose.
- [ ] Bind the complete field schedule, owner, contract, purpose, operators, environment, audience, destination, disclosure rule, and deletion obligation before value access.
- [~] Source public control evidence first, then inventory confidential fields, owners, contracts, purposes, destinations, and disclosure risks without accessing values. Public controls are complete; an exact owner field schedule remains external.
- [ ] Approve the controlled environment, operators, access, retention, revocation, and incident plan.
- [ ] Review checkpoint: verify authorization before any confidential value is accessed.

## Phase 2 — controls and validation

- [x] Add synthetic tests for reconstruction, aggregation, export, and public-surface leakage; no restricted execution path is enabled. (`246c3d3`)
- [ ] Implement isolated computation, redaction, aggregation, and audience-labelled outputs.
- [ ] Run threat-model, privacy, legal, security, and disclosure-control reviews.
- [ ] Review checkpoint: validate deletion, revocation, and incident exercises.

## Phase 3 — restricted disposition

- [ ] Obtain per-destination disclosure authorization.
- [ ] Generate only permitted restricted outputs and negative/public receipts.
- [ ] Completion checkpoint: prove public repository and releases contain no confidential data.
- [ ] Completion checkpoint: reauthorize and refresh receipts at the exact restricted-output commit and destination.
