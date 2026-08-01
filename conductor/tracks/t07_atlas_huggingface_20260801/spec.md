# Specification

Integrate approved-derived Reimbursement Atlas packets and the owner-scoped
`edithatogo/` Hugging Face publication surface without copying raw or
restricted source data.

## Requirements

- Produce a content-addressed receipt for a validated Atlas packet, preserving
  packet ID/revision, record count, source licences, and approval state.
- Validate Hugging Face repository IDs, publication kind, licence metadata, and
  source-term boundary before any publication handoff.
- Reject third-party IDs, raw-source publication, missing revisions, and
  licence mismatches.
- Keep Atlas acquisition, provenance, transformations, and human approval
  authoritative; this repository only consumes approved-derived packets.

## Acceptance criteria

- Focused tests cover Atlas receipt determinism and Hugging Face contract
  validation/rejection paths.
- Documentation records the exact owner namespace and source-specific licence
  distinction.
- Full repository quality gates pass.

## Out of scope

- Uploading to Hugging Face or changing Atlas records.
- Promoting candidate or unapproved evidence.
