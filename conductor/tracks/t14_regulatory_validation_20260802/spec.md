# T14 regulatory and HTA validation boundary

## Overview

Define the evidence, quality-system, validation, human accountability, and claim
controls required before any regulator-facing, HTA, policy, or payer-facing use.
Creation of this track is not regulatory authorization.

## Requirements

1. Maintain a claims inventory that maps every claim to evidence, model version,
   validation, owner, jurisdiction, and intended audience.
2. Define the applicable regulatory/HTA quality framework and document gaps.
3. Require validated empirical calibration from T13 before assessing empirical
   claims.
4. Establish independent human review, change control, auditability, incident
   handling, and post-release monitoring requirements.
5. Prevent research-only outputs from being represented as regulator-ready.

## Acceptance criteria

- Applicable jurisdiction, submission type, accountable sponsor, and quality
  framework are explicitly approved.
- Validation protocol, claims matrix, risk assessment, and traceability matrix
  are complete and independently reviewed.
- Every external gate passes at the exact submission commit and artifact hashes.
- Regulatory/HTA release remains disabled until explicit authorization.

## External gates

- T13 calibrated evidence completed for the intended use.
- Named sponsor and accountable regulatory/HTA owner.
- Independent human statistical, health-economic, legal, privacy, and security review.
- Jurisdiction-specific submission and release authorization.

## Non-functional constraints

- Research and regulatory release surfaces remain physically and semantically distinct.
- All claims are versioned, reproducible, attributable, and reversible.

## Out of scope

- Filing, submission, payer communication, or deployment without a separate,
  explicit external authorization.

## Authoritative inputs

- `docs/governance/model-risk.md`
- `docs/governance/research-only-release-authorization.md`
- `docs/releases/v0.4.0-research-only.md`
- T13 completed evidence when available.
