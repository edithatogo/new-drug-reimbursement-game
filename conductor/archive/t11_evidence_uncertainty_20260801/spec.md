# Specification

## Overview

Implement a governed, versioned evidence and uncertainty boundary for the four
Chapter 7 scenarios. The application must consume approved, derived parameter
records from Reimbursement Atlas, preserve model-role interpretations and
provenance, assemble scenario inputs only from compatible records, and prepare
aligned samples for Voiage without implementing VOI algorithms.

## Authoritative inputs

- `CODEX_IMPLEMENTATION_PROMPT.md`, Workstreams 5, 7, 8, and 9.
- `docs/research/parameter-evidence.md` and
  `docs/governance/model-risk.md`.
- `ecosystem.lock.toml` Reimbursement Atlas revision
  `c73d34dacae2f907a0eac399da8e6f43ce8d00ca`.
- `ecosystem.lock.toml` Voiage revision
  `6141cc49a9ad41161756677840d6a61b25fd386a`.
- `schemas/pekarsky-chapter7-scenario.schema.json` and
  `src/reimbursement_game/chapter7.py`.

## Requirements

- Define a strict version-1 parameter-evidence record for the roles `n`, `d`,
  `m`, `mu`, `phi`, `annual_program_health_effect`, `horizon`, and
  `discount_rate`.
- Require jurisdiction, payer, budget boundary, service line, price year,
  decision date, implementation horizon, units, programme identity, evidence
  method, marginality, causal assumptions, uncertainty representation, source
  URI and checksum, transformation, reviewer, approval state, evidence
  revision, and scale limits.
- Accept only approved, derived Atlas records with supported units, finite
  values, finite aligned samples, valid checksums, and explicit marginality.
- Fail closed when scenario-required records are missing, duplicated,
  context-incompatible, unit-incompatible, unapproved, or empirically
  mislabelled.
- Assemble Scenario 1-4 inputs from compatible evidence records while keeping
  incremental cost and health effect as explicit decision-case inputs.
- Preserve the exact evidence-record IDs and revisions in a deterministic
  calibration receipt.
- Prepare aligned parameter samples and health-net-benefit strategy samples for
  Voiage's pinned `ParameterSet` and `ValueArray` boundary. Do not calculate
  EVPI, EVPPI, EVSI, ENBS, or generate probability samples in this repository.
- Provide a schema, synthetic approved-derived fixture, CLI validation path,
  tests, and documentation. Synthetic data must be conspicuously labelled as
  non-empirical and unusable for policy decisions.

## Acceptance criteria

- The JSON schema rejects incomplete, unapproved, raw, or ambiguous evidence
  records.
- Python tests cover every role, all four scenario assemblies, context/unit
  mismatch, sample alignment, provenance preservation, and Voiage boundary
  construction.
- The existing strict Chapter 7 evaluator consumes assembled inputs without a
  parallel economic implementation.
- The application never imports Atlas acquisition code and never implements a
  VOI algorithm or random-distribution sampler.
- Full repository quality gates pass.

## Non-functional constraints

- Standard-library Python only in the application core; optional NumPy/Voiage
  imports remain isolated inside the Voiage adapter.
- No raw or restricted source payloads, book content, credentials, or
  machine-local paths may be committed.
- Numeric comparisons and sample alignment must be deterministic and fail
  closed.
- Outputs are technical calibration receipts, not empirical validation,
  reimbursement recommendations, or regulator-grade evidence.

## External gates

- Reimbursement Atlas must approve and publish real derived parameter records.
- A health economist must review every real calibration packet and its causal
  assumptions.
- Voiage licence metadata must be reconciled before distribution.
- A real jurisdiction, payer, and programme must be selected before an
  empirical reference calibration is attempted.

## Out of scope

- Acquiring, scraping, licensing, or reviewing raw evidence.
- Inventing or estimating empirical values for any jurisdiction.
- Random sampling, correlation fitting, causal estimation, or VOI algorithms.
- Publishing a dataset, release, HTA submission, or policy recommendation.
