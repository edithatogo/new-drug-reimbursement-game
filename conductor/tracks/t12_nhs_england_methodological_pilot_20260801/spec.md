# Specification

## Overview

Build a fail-closed NHS England methodological evidence pilot for Chapter 7.
The pilot captures official and primary-source parameter candidates, evaluates
their semantic fitness for every evidence role, and produces scenario readiness
receipts. It must not convert candidate evidence into an approved calibration.

## Authoritative inputs

- DHSC, *Consultation stage impact assessment: proposed 2026 changes to the
  statutory scheme for branded medicines pricing*, Annex C, PDF pp. 22-23,
  SHA-256 `da2f3bb1ae21e65cd0aac668f1e21f35e5c1685c69aa6f76f0048e9eea90c60e`.
- Centre for Health Economics, University of York, *Research Summary 9:
  Estimating the health effects of changes in health care expenditure* (July
  2023), SHA-256
  `4b1814572e363dcb2e722a4fb43b1a6e04ef5c6b278bc6f6130fdf375fdaad02`.
- Martin, Claxton, Lomas, and Longo (2023), DOI
  `10.1016/j.healthpol.2023.104800`; White Rose repository PDF SHA-256
  `2eea0d4ac30aa2175fa0496a0c95e9294b9fd1499c84c8b52c32f9a36d6988b4`,
  reporting the 2014/15 result from Martin et al. (2022), DOI
  `10.1007/s40258-022-00723-2`.
- NICE, *Technology appraisal and highly specialised technologies guidance:
  the manual*, sections 4.2 and 4.5.
- `schemas/parameter-evidence-packet-v1.schema.json`,
  `src/reimbursement_game/evidence.py`, and
  `docs/architecture/evidence-calibration-contract.md`.

## Requirements

- Define a candidate-dossier schema separate from the approved Atlas packet.
- Record source URL, checksum or DOI metadata, exact location, jurisdiction,
  budget boundary, price year, unit, estimand, candidate roles, uncertainty,
  transformations, assumptions, and mapping limitations.
- Represent GBP 15,000/QALY, GBP 12,981/QALY, approximately GBP 7,000/QALY for
  2014/15 locally commissioned services, DHSC's 1.5% QALY discount rate, and
  NICE's 3.5% reference-case discount rate without conflating their scopes or
  price years.
- Treat GBP 15,000/QALY as a pragmatic policy proxy, not a firm prediction or
  the NICE decision threshold.
- Assess every Chapter 7 role and scenario as `supported`, `candidate_only`,
  `not_identifiable`, or `incompatible`, with explicit reasons.
- Refuse approved-packet conversion while records remain candidate,
  uncertainty is unspecified, displacement is unidentified, or review is
  absent.
- Add a CLI readiness command, tests, source-review documentation, and a
  deterministic readiness receipt.

## Acceptance criteria

- Checksums, pages, values, dates, and scopes are checked without committing
  source binaries.
- Tests prove the candidate dossier cannot enter the approved calibration path.
- Missing `d`, Scenario 3 ordering, and Scenario 4 programme evidence are not
  inferred.
- The readiness receipt deterministically matches its source dossier.
- Full repository quality gates pass.

## Non-functional constraints

- Standard-library Python only.
- No source PDF, copied table, long excerpt, raw NHS record, or restricted data
  may enter Git.
- Different price years or budget scopes remain distinct without a reviewed
  transformation.
- Outputs are methodological triage, not HTA, policy, or regulator conclusions.

## External gates

- Reimbursement Atlas must approve any promoted derived records.
- A health economist must approve role mappings, transformations, and
  uncertainty.
- A specific NHS payer/service line and displaced programme must be selected
  before Scenario 2-4 calibration.

## Out of scope

- Patient-level or confidential NHS data.
- Unreviewed inflation of historical estimates.
- Fitting uncertainty distributions or causal models.
- Promoting candidates or running a real reimbursement decision.
