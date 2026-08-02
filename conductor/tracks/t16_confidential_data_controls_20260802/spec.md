# T16 confidential and commercially sensitive data controls

## Overview

Define a separate controlled path for confidential prices, rebates, contracts,
commercial assumptions, and other sensitive non-public data. No confidential
data is authorized for this repository by creating this track.

## Requirements

1. Classify each proposed field and establish owner, contract, purpose,
   permitted computation, disclosure audience, retention, and destruction rules.
2. Use isolated secrets/data stores, least-privilege access, encryption, audit
   logs, and redacted or aggregate outputs.
3. Prevent reconstruction, inference, logging, telemetry, fixtures, or publication
   of confidential values.
4. Separate confidential analyses from public research outputs and regulatory
   claims unless each destination is explicitly authorized.
5. Provide breach, revocation, key rotation, deletion, and disclosure-review procedures.
6. Follow `sourcing.md` and the shared evidence-sourcing policy: agents must
   autonomously acquire public standards, policies, redacted templates, and
   aggregate evidence, but may not acquire confidential values without exact
   owner, contract, environment, operator, purpose, and destination approvals.

## Acceptance criteria

- Data owner, legal, privacy, security, and intended-destination approvals are
  recorded for every confidential source and field.
- Threat model, disclosure controls, aggregation thresholds, access tests,
  deletion receipts, and incident procedures pass review.
- Public artifacts contain no confidential or reconstructable values.
- Every output is labelled with its permitted audience and disclosure status.

## External gates

- Confidential-data owner permission and binding contract/NDA terms.
- Legal, privacy, security, and information-governance approval.
- Approved operators, controlled environment, and release/disclosure authorization.

## Non-functional constraints

- Default deny, least privilege, encryption, audited access, minimization, and revocation.

## Out of scope

- Storing confidential values in Git, public CI, issues, logs, fixtures, model
  outputs, or public release artifacts.

## Authoritative inputs

- `docs/governance/model-risk.md`
- `docs/governance/release-packet/security-privacy-scope-receipt-2026-08-02.json`
- T15 controlled-data environment and receipts when applicable.
- `conductor/evidence-sourcing-policy.md`
- `conductor/source-receipt-schema.json`
- `conductor/tracks/t16_confidential_data_controls_20260802/sourcing.md`
