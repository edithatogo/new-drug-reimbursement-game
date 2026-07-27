# Specification

## Overview

Independently implement and cross-check the price-effectiveness identities used
by the application, while preserving explicit economic interpretations and
failing closed when a context is incomplete or non-identifiable.

## Authoritative inputs

- `CODEX_IMPLEMENTATION_PROMPT.md`, Workstream 1.
- `AGENTS.md` and `DEPENDENCY_MIGRATION_PLAN.md`.
- Pekarsky (2015), Chapters 6-8, DOI `10.1007/978-3-319-08903-4`.
- `ecosystem.lock.toml`; Voiage pin
  `6141cc49a9ad41161756677840d6a61b25fd386a` remains authoritative for VOI.

## Requirements

- Cover IPER, reimbursement population health effect, NEBhR, EVCI, and each
  named shadow-price context with units and assumptions.
- Prove threshold-zero, sign, `n = m`, `d = m`, monotonicity, and currency-unit
  rescaling invariants in independently written Python and Rust code.
- Use shared fixtures to detect cross-language drift.
- Preserve named Chapter 7 technical-efficiency alternatives until the exact
  source interpretation and expert review resolve them.
- Reject non-finite, non-positive, missing, and non-identifiable inputs.

## Acceptance criteria

- Full Python and Rust gates pass.
- Shared fixtures give equivalent Python and Rust results within declared
  tolerances.
- Every implemented identity has a source location, units, and assumptions.
- Repository completion does not assert independent health-economics approval.

## External gates

- Exact Chapter 7 technical-efficiency source verification.
- Independent health-economics review of derivations and dimensional analysis.

## Out of scope

- Empirical calibration and regulator-grade validation.
- Implementing VOI algorithms owned by Voiage.
