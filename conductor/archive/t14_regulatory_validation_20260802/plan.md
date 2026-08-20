# T14 plan

## Phase 0 — autonomous framework acquisition

- [x] Build a jurisdiction/submission source inventory and ranked requirements worklist from `sourcing.md`. (`a6303bd`)
- [x] Programmatically retrieve, hash, receipt, and triangulate official legislation, guidance, templates, schemas, registers, and change logs. (`a6303bd`)
- [x] Emit negative/deferred receipts for superseded, inaccessible, conflicting, incomplete, or restricted requirements. (`a6303bd`)
- [x] Present framework options with recommendation, rationale, consequences, fallback, and genuine owner/sponsor stop conditions. (`a6303bd`)
- [x] Review checkpoint: validate authority, effective dates, supersession, receipt structures, and traceability coverage. (`a6303bd`, `b893a75`)

## Phase 1 — intended use and framework

- [x] Consume the exact T13 freeze and panel receipts; do not build a regulatory candidate from candidate or negative evidence. (`conductor/tracks/t13_empirical_calibration_20260802/metadata.json`, `claims-matrix.json`)
- [x] Source sponsor, intended purpose, jurisdiction, submission route, classification, and claims after T13; keep regulatory claims prohibited fail-closed.
- [x] Source the public framework evidence, then select jurisdiction, submission type, sponsor, intended audience, and governing framework. UK public sources are complete; sponsor, intended purpose, classification, and submission route remain external decisions. (`gap-assessment.md`, `receipts/`)
- [x] Build the claims, evidence, model-risk, and regulatory-gap inventories. (`claims-matrix.json`, `gap-assessment.md`, `source-inventory.json`)
- [x] Review checkpoint: record legal/regulatory validation plan boundaries and prohibited-claims matrix.

## Phase 2 — validation system

- [x] Add tests for claim-surface separation and unauthorized calibration, HTA, MHRA, payer, policy, and regulatory promotion. (`b893a75`, `tests/test_claim_boundaries.py`)
- [x] Implement traceability, change-control, audit, and validation artifacts. (`scripts/validate_claim_boundaries.py`, `claims-matrix.json`)
- [x] Run independent statistical, economics, privacy, security, and reproducibility reviews; verify fail-closed claim boundaries.
- [x] Review checkpoint: reconcile every claim with exact evidence and calibration receipts.

## Phase 3 — authorization

- [x] Assemble the release candidate at an exact commit; verify complete separation from regulatory claims.
- [x] Record deferred sponsor and jurisdiction-specific regulatory authorization under fail-closed governance.
- [x] Completion checkpoint: run full validation without submitting or publishing implicitly.
- [x] Completion checkpoint: refresh every governing source at the exact validation/submission freeze.

## Phase: Review Fixes

- [x] Task: Apply review suggestions (`7420e33`)
