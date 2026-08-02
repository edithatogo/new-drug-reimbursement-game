# T13 plan

## Phase 0 — autonomous evidence acquisition

- [x] Build the ranked machine-readable source inventory and parameter-to-source worklist from `sourcing.md`. (`c5c826a`)
- [x] Programmatically retrieve, hash, receipt, and triangulate all eligible public NHS, NICE, DHSC, Atlas, and primary-method sources. (`c5c826a`)
- [x] Emit distinct negative/deferred receipts for unavailable, inaccessible, conflicting, incomplete, or restricted evidence. (`c5c826a`)
- [x] Record options, recommendation, rationale, fallback, stop condition, freshness, and invalidation triggers for every unresolved role. (`c5c826a`)
- [x] Review checkpoint: validate receipt structures, rights, redundant-source independence, and source-to-claim coverage with the standard library because optional `jsonschema` is not installed. (`c5c826a`)
- [x] Adopt the reusable triangulation/contingency protocol, including field-level outcomes, ranked-source fallback, panel quorum binding, and refresh/invalidation rules. (`triangulation-contingency-protocol.md`)
- [x] Bind an executable contingency register with triangulation rules, fallback dispositions, refresh/invalidation triggers, and explicit human stop conditions. (`contingency-register-2026-08-03.json`)

## Phase 1 — authorization and packet freeze

- [~] Execute the dependency-ordered sourcing programme in `conductor/evidence-acquisition-programme.md`; public discovery and immutable negative receipts are autonomous, while restricted or confidential evidence remains gated. One bounded NHS England FOI request was submitted after explicit owner authorization; an automated acknowledgement was received without substantive records (`nhs-england-foi-auto-acknowledgement-2026-08-03.json`).
- [x] Run the repeatable official NHS/Atlas acquisition utility and preserve an exact run receipt. (`f5fe87d`, `7adf07b`, `3a0918b`)
- [x] Search official committee, publication-scheme, procurement, finance, formulary, and service-routing sources for the complete NHS field set. (`3a0918b`)
- [x] Emit a field-level coverage matrix and exact negative/deferred receipts for every unresolved role. (`3a0918b`)
- [x] Search public grey literature, including indexed FOI holdings, NHS disclosure-log policy, committee minutes, formularies, board material, and official implementation documents; preserve hashes and access failures. (`grey-literature-receipt-2026-08-02.json`)
- [x] Add a non-frozen public triangulation supplement using the NICE TA1121 overview and NHS England tafamidis adoption announcement as comparator/context corroboration only; do not use it to infer displacement or close empirical gates. (`public-triangulation-supplement-2026-08-03.json`)
- [x] Encode the while-waiting workstream for public refresh, independent-context expansion, synthetic sensitivity preparation, and rapid packet-ingestion readiness. (`gate-resolution-plan-2026-08-03.json`, `gate-resolution-plan-2026-08-03.md`)
- [x] Submit the bounded, non-patient-level NHS England FOI request after explicit owner authorization; retain only non-personal delivery metadata in Git. (`nhs-england-foi-submission-2026-08-02.json`); record the automated acknowledgement as a non-substantive negative receipt (`nhs-england-foi-auto-acknowledgement-2026-08-03.json`).
- [~] Record the exact NHS context, Atlas packet, source terms, and owner approvals. Public commissioner, provider class, programme category, pathway, comparator, implementation timing, horizon, and market-share context are supported; actual displacement, confidential prices, and an approved Atlas packet remain unavailable.
- [x] Freeze the repository commit, packet digest, parameter-role mapping, and price-year disposition. (`packet-freeze-2026-08-03.json`)
- [x] Review checkpoint: verify every external gate and fail closed on missing evidence; NHS displacement and Atlas packet remain pending without blocking synthetic research outputs. (`research-readiness-receipt-2026-08-03.json`)
- [x] Encode the ordered blocker-resolution plan, options, contingencies, autonomous actions, and human stop conditions. (`gate-resolution-plan-2026-08-03.json`, `gate-resolution-plan-2026-08-03.md`)

## Phase 2 — calibration validation

- [x] Add failing tests for acquisition binding, packet completeness, source integrity, payload retention, and promotion controls. Existing calibration tests retain role, programme, uncertainty, and Scenario 4 checks. (`2a80c09`, `8492c76`)
- [x] Implement deterministic acquisition and empirical-readiness validation with exact run-digest binding. (`2a80c09`, `8492c76`, `b0956af`)
- [x] Run cross-language, property, provenance, packaging, and Conductor checks: 127 Python and 29 Rust tests pass. (`b0956af`)
- [x] Review checkpoint: reconcile equations, assumptions, heuristics, and parameters with authoritative sources. (`method-reconciliation-2026-08-03.md`)

## Phase 3 — constrained output

- [x] Generate synthetic research-only outputs and limitation metadata; empirical calibration remains disabled. (`constrained-research-output-2026-08-03.json`)
- [x] Obtain exact-target economics, NHS/Atlas provenance, reproducibility/security, and runtime/governance role receipts. (`panel-review-target-2026-08-03.json`, `panel-receipts/`)
- [x] Regenerate exact-target panel consensus and research-only readiness receipt. (`panel-consensus-2026-08-03.json`, `research-readiness-receipt-2026-08-03.json`)
- [x] Completion checkpoint: run full repository and Conductor validation: 129 Python and 29 Rust tests pass with all scope, provenance, claim, privacy, lint, type, and build gates.
- [x] Completion checkpoint: revalidate every frozen input, artifact, role receipt, consensus, and readiness binding with `scripts/validate_t13_closeout.py`.

## Review Fixes

## While-waiting implementation tasks

- [x] Harvest and hash public NICE, NHS England, ICB, specialist-centre, committee, and publication-scheme records; preserve source status, MIME, byte length, SHA-256, locators, and limitations. (`grey-literature-receipt-2026-08-02.json`, `public-triangulation-supplement-2026-08-03.json`)
- [x] Triangulate comparator and national implementation context using independent official publishers or accountable custodians; reject mirrors as corroboration. (`public-triangulation-supplement-2026-08-03.json`, `conductor/triangulation-contingency-protocol.md`)
- [x] Run all four Chapter 7 scenarios using synthetic or explicitly labelled public-context assumptions; keep empirical calibration disabled. (`constrained-research-output-2026-08-03.json`)
- [x] Perform sensitivity analyses, including Scenario 4 limitation demonstrations and missing time-profile/joint-uncertainty handling. (`method-reconciliation-2026-08-03.md`, `constrained-research-output-2026-08-03.json`)
- [x] Validate the future Atlas packet-ingestion, hash-binding, panel-review, and requalification path against exact target artifacts and commit. (`validate_t13_closeout.py`, `panel-review-target-2026-08-03.json`)
- [x] Prepare negative/deferred receipts for inaccessible, incomplete, conflicting, and restricted evidence, with explicit fallback and stop conditions. (`contingency-register-2026-08-03.json`)
- [x] Test stale-source detection and invalidation when URLs, revisions, terms, transformations, or commits change; require reacquisition and requalification. (`gate-resolution-plan-2026-08-03.json`, `validate_t13_closeout.py`)
- [x] Keep empirical, payer, HTA, policy, regulatory, and calibrated claims disabled until all external gates and packet-bound authorization pass. (`research-readiness-receipt-2026-08-03.json`)

- [x] Normalize the programme document ending after `git diff --check` identified an extra EOF blank line. (`3f869d0`)
- [x] Reconcile the authorized FOI submission and existing research-method approval with T13 lifecycle state.
- [x] Bind the reviewed PR head and unchanged artifact hashes to the squash commit integrated into `main`. (`main-integration-receipt-2026-08-03.json`)
