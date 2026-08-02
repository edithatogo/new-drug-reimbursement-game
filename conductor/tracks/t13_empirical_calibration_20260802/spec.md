# T13 empirical calibration and calibrated research outputs

## Overview

Establish a fail-closed path from approved-derived evidence to reproducible,
research-only empirical calibration. This track does not authorize calibration;
it defines and implements the controls required once the external evidence and
owner approvals are complete.

## Requirements

1. Consume only immutable, Atlas-approved derived packets aligned to one NHS
   decision context and stable programme identifiers.
2. Bind every parameter, transformation, uncertainty model, discounting choice,
   reviewer disposition, and result to exact revisions and hashes.
3. Require accountable health-economist approval and current panel receipts.
4. Fail closed on missing roles, cross-programme values, ambiguous marginality,
   incompatible price years, or unapproved records.
5. Keep calibrated outputs separate from regulatory, HTA, policy, and payer
   claims.
6. Follow `sourcing.md` and the shared evidence-sourcing policy: agents must
   actively acquire eligible official public evidence, emit schema-valid
   positive or negative receipts, triangulate material claims, and stop only at
   the documented external boundaries.

## Acceptance criteria

- A schema-valid approved-derived packet and deterministic calibration receipt
  exist for every activated scenario.
- Python and Rust conformance, uncertainty, provenance, and reproducibility
  checks pass against the exact packet and commit.
- Release metadata labels outputs `calibrated_research_only` and records all
  limitations.
- Every external gate below is passing and hash-bound before empirical output is
  enabled.

## External gates

- Authoritative NHS displacement context and accountable owner receipt.
- Atlas-approved programme-aligned packet and source-term disposition.
- Health-economist method and calibration approval.
- Exact-target relevant-subagent panel consensus.
- Research-only calibrated-output release authorization.

## Non-functional constraints

- No raw, confidential, patient-level, or undisclosed commercial source data.
- Deterministic receipts and immutable evidence references.
- Existing ecosystem ownership boundaries remain authoritative.

## Out of scope

- Regulatory submissions, HTA claims, reimbursement recommendations, policy
  claims, and production decision support.

## Authoritative inputs

- `docs/architecture/evidence-calibration-contract.md`
- `docs/research/parameter-evidence.md`
- `docs/governance/health-economist-approval.md`
- `docs/governance/subagent-panel-consensus-2026-08-02.json`
- `ecosystem.lock.toml`
- `conductor/evidence-sourcing-policy.md`
- `conductor/source-receipt-schema.json`
- `conductor/tracks/t13_empirical_calibration_20260802/sourcing.md`
