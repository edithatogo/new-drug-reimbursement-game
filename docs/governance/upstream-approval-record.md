# Upstream approval record

On 2026-07-31 the repository owner explicitly approved the pinned UOGTO and
Kairos upstream integration scope for this handoff. The approval authorizes
proceeding with the repository's declared adapter contracts and extraction
packet; it does not alter the pinned revisions or imply that upstream APIs have
accepted a pull request.

Evidence remains the pinned contracts, local validation, and the review packet
in `docs/governance/release-readiness-evidence.md`.

## Owner confirmation — 2026-08-01

The repository owner reaffirmed approval to proceed with the pinned UOGTO and
Kairos adapter scope and the planned extraction packet. This confirmation is
authorization from the component owner, not evidence that UOGTO or Kairos has
accepted an upstream change, that a released contract is available, or that
the extraction boundary has received its separate transfer approval. Those
receipts remain open where required by T02 and T09.

## Pin-resolution check — 2026-08-01

The former UOGTO pin `849386068399a764ad5304cc8a0ffe53094b091c` was no longer
advertised by the authoritative remote. The owner-approved replacement pin is
the current public UOGTO `main` revision
`ac5b8e86c4a3547d008e83ba4cfcbb5f3ba95f25`. The Kairos pin remains
`fae901558f07b7b717a676adbafbe2cdc78dea1c`. This resolves pin discovery, but
released-contract acceptance, hosted check evidence, and extraction receipts
remain separate gates.
