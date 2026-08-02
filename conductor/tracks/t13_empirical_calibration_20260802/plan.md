# T13 plan

## Phase 0 — autonomous evidence acquisition

- [x] Build the ranked machine-readable source inventory and parameter-to-source worklist from `sourcing.md`. (`c5c826a`)
- [x] Programmatically retrieve, hash, receipt, and triangulate all eligible public NHS, NICE, DHSC, Atlas, and primary-method sources. (`c5c826a`)
- [x] Emit distinct negative/deferred receipts for unavailable, inaccessible, conflicting, incomplete, or restricted evidence. (`c5c826a`)
- [x] Record options, recommendation, rationale, fallback, stop condition, freshness, and invalidation triggers for every unresolved role. (`c5c826a`)
- [x] Review checkpoint: validate receipt structures, rights, redundant-source independence, and source-to-claim coverage with the standard library because optional `jsonschema` is not installed. (`c5c826a`)

## Phase 1 — authorization and packet freeze

- [~] Record the exact NHS context, Atlas packet, source terms, and owner approvals, sourcing all public components before requesting external action. Public components are complete; authoritative displacement and approved Atlas packet remain external.
- [ ] Freeze the repository commit, packet digest, parameter-role mapping, and price-year conversions.
- [ ] Review checkpoint: verify every external gate and fail closed on missing evidence.

## Phase 2 — calibration validation

- [ ] Add failing tests for packet alignment, uncertainty, discounting, and promotion controls.
- [ ] Implement any missing deterministic validation and receipt generation.
- [ ] Run cross-language, property, provenance, and packaging checks.
- [ ] Review checkpoint: reconcile equations, assumptions, heuristics, and parameters with authoritative sources.

## Phase 3 — constrained output

- [ ] Generate calibrated research-only outputs and limitation metadata.
- [ ] Obtain exact-target economics and reproducibility role receipts.
- [ ] Regenerate readiness and release receipts.
- [ ] Completion checkpoint: run full repository and Conductor validation.
- [ ] Completion checkpoint: reacquire or revalidate every receipt invalidated by the final commit or release freeze.
