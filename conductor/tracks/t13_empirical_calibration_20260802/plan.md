# T13 plan

## Phase 0 — autonomous evidence acquisition

- [x] Build the ranked machine-readable source inventory and parameter-to-source worklist from `sourcing.md`. (`c5c826a`)
- [x] Programmatically retrieve, hash, receipt, and triangulate all eligible public NHS, NICE, DHSC, Atlas, and primary-method sources. (`c5c826a`)
- [x] Emit distinct negative/deferred receipts for unavailable, inaccessible, conflicting, incomplete, or restricted evidence. (`c5c826a`)
- [x] Record options, recommendation, rationale, fallback, stop condition, freshness, and invalidation triggers for every unresolved role. (`c5c826a`)
- [x] Review checkpoint: validate receipt structures, rights, redundant-source independence, and source-to-claim coverage with the standard library because optional `jsonschema` is not installed. (`c5c826a`)

## Phase 1 — authorization and packet freeze

- [~] Execute the dependency-ordered sourcing programme in `conductor/evidence-acquisition-programme.md`; public discovery and immutable negative receipts are autonomous, while restricted or confidential evidence remains gated. No outbound requests are in scope.
- [x] Run the repeatable official NHS/Atlas acquisition utility and preserve an exact run receipt. (`f5fe87d`, `7adf07b`, `3a0918b`)
- [x] Search official committee, publication-scheme, procurement, finance, formulary, and service-routing sources for the complete NHS field set. (`3a0918b`)
- [x] Emit a field-level coverage matrix and exact negative/deferred receipts for every unresolved role. (`3a0918b`)
- [x] Search public grey literature, including indexed FOI holdings, NHS disclosure-log policy, committee minutes, formularies, board material, and official implementation documents; preserve hashes and access failures. (`grey-literature-receipt-2026-08-02.json`)
- [~] Record the exact NHS context, Atlas packet, source terms, and owner approvals. Public commissioner, provider class, programme category, pathway, comparator, implementation timing, horizon, and market-share context are supported; actual displacement, confidential prices, and an approved Atlas packet remain unavailable.
- [ ] Freeze the repository commit, packet digest, parameter-role mapping, and price-year conversions.
- [ ] Review checkpoint: verify every external gate and fail closed on missing evidence.

## Phase 2 — calibration validation

- [x] Add failing tests for acquisition binding, packet completeness, source integrity, payload retention, and promotion controls. Existing calibration tests retain role, programme, uncertainty, and Scenario 4 checks. (`2a80c09`, `8492c76`)
- [x] Implement deterministic acquisition and empirical-readiness validation with exact run-digest binding. (`2a80c09`, `8492c76`, `b0956af`)
- [x] Run cross-language, property, provenance, packaging, and Conductor checks: 127 Python and 29 Rust tests pass. (`b0956af`)
- [ ] Review checkpoint: reconcile equations, assumptions, heuristics, and parameters with authoritative sources.

## Phase 3 — constrained output

- [ ] Generate calibrated research-only outputs and limitation metadata.
- [ ] Obtain exact-target economics and reproducibility role receipts.
- [ ] Regenerate readiness and release receipts.
- [ ] Completion checkpoint: run full repository and Conductor validation.
- [ ] Completion checkpoint: reacquire or revalidate every receipt invalidated by the final commit or release freeze.

## Review Fixes

- [x] Normalize the programme document ending after `git diff --check` identified an extra EOF blank line. (`3f869d0`)
