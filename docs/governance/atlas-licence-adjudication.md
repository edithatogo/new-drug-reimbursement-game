# Reimbursement Atlas licence adjudication

## Adjudication packet

| Field | Value |
|---|---|
| Atlas repository | `https://github.com/edithatogo/reimbursement-atlas` |
| Atlas revision | `5b0c2fe3e1b7d2d6c3c1975cf1a162f2787c67aa` |
| Software licence | Apache-2.0 for project-owned code and documentation |
| Derived licence ledger | `data/derived/licence_review/summary.json` and `data/licence_review/decisions.jsonl` |
| Artefacts reviewed | 229 |
| Approved | 229 |
| Pending in owner-approved ledger | 0 |
| NHS Payment Scheme queue rows | Pending `public_reuse_review` |
| Approval scope | Derived candidate fields within the documented grouped scope |
| Reviewer | Repository owner / `edithatogo` |

The ledger records checksum-bound owner decisions and requires attribution and
the applicable provider terms to remain attached to each derived artefact.

## Hugging Face destination check

The pinned Atlas publication check reports `pass` with zero mismatches:

- dataset `edithatogo/reimbursement-atlas`: observed licence `other`, matching
  the source-specific data boundary;
- Space `edithatogo/reimbursement-atlas`: observed licence `apache-2.0` and
  static SDK, matching the publication contract.

## Boundary

This adjudication reconciles the owner-approved grouped scope for existing
derived Atlas outputs. It does not close the NHS-context source-term gate while
the NHS Payment Scheme queue rows remain `public_reuse_review` pending. It does
not permit raw source payloads, restricted descriptors, credentials,
confidential values, unsupported coverage/net-price claims, or promotion of
candidate evidence into calibrated reimbursement results. Atlas evidence
approval and independent health-economics review remain separate gates.
