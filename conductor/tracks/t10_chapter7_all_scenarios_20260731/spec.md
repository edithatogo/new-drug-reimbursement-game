# Specification

## Overview

Implement a strict, source-mapped evaluation surface for all four economic
contexts in Pekarsky (2015), Chapter 7, while retaining the existing generalized
opportunity-set API as a separately labelled extension.

## Authoritative inputs

- Pekarsky (2015), Chapter 7, DOI `10.1007/978-3-319-08903-4`, especially
  equations 7.1-7.5 and Table 7.2 on printed pages 108-125 (PDF pages 118-135).
- Authorized local source PDF SHA-256
  `8455ad153cf5b6c1570bfc945108efe659904b3c8f89fdf7b74b88c9523c4848`;
  the PDF itself must not enter the repository.
- `CODEX_IMPLEMENTATION_PROMPT.md`, Workstream 1.
- `docs/research/source-conformance-audit.md`.

## Requirements

- Represent Scenario 1: efficient budget financed by expansion, with
  `beta_c = n`.
- Represent Scenario 2: efficient fixed budget financed by displacement, with
  `n = m` and `beta_c = d`.
- Represent Scenario 3: allocatively inefficient fixed budget, with
  `m > n`, `n <= d <= m`, and the equations 7.2-7.5 threshold.
- Represent Scenario 4's Chapter 7 summary model: technically inefficient fixed
  budget, with caller-supplied positive investment aICER `mu`, displacement
  `d`, contraction `m`, and
  `1 / beta_c^v = 1 / mu - 1 / m + 1 / d`.
- Compute scenario, reimbursement health effect, best-alternative health gain,
  NEBhR, health shadow price, EVCI, and the applicable budget shadow-price
  descriptors with finite, dimensionally consistent outputs.
- Reject missing, non-positive, non-finite, misordered, or scenario-incompatible
  parameters instead of silently changing scenarios.
- Keep the Scenario 4 summary model distinct from deriving `mu`; do not invent
  the investment-production model cited to Pekarsky (2012, Appendix 5).
- Maintain independent Python and Rust implementations using a shared,
  versioned all-scenario fixture.
- Expose a stable CLI/schema input contract and update source, status, and
  governance documentation without storing source pages or copied tables.

## Acceptance criteria

- Every Chapter 7 scenario row has a source location, units, assumptions,
  independent Python/Rust calculation, and fixture receipt.
- Scenario-specific invalid domains fail closed in both languages.
- Existing generalized APIs remain available and are not relabelled as strict
  source conformance.
- Full repository quality gate passes.
- Automated review finds no unresolved high-confidence in-scope defect.

## Non-functional constraints

- Standard-library Python only for the application core.
- No reimbursement vocabulary may enter the domain-neutral UOGTO/Kairos crates.
- Numerical comparisons must use documented scale-aware tolerances.
- Outputs are conditional model results, not empirical or policy validation.

## External gates

- Deriving or calibrating `mu` from investment primitives requires Pekarsky
  (2012, Appendix 5), parameter evidence, and renewed independent review.
- Human health-economist, HTA, and regulator-grade validation remain external.

## Out of scope

- Chapter 9 Game 2 and Chapter 10 Game 3.
- Empirical calibration, investment-program simulation, uncertainty, and VOI.
- Publication, release, or policy approval.
