# Kairos maintainer acceptance and narrow-extraction request (not sent)

This is an unsent request template for the Kairos maintainer. It is designed
to close the released-contract and extraction gates without requesting source
redistribution or a broader API guarantee.

## Recipient and purpose

**Recipient:** Kairos maintainer/owner responsible for the pinned revision
`fae901558f07b7b717a676adbafbe2cdc78dea1c`.

Please confirm whether the pinned revision may be treated as an accepted
research-only adapter contract by this downstream repository, and whether a
narrow, derived DTO extraction is permitted for local validation and a
research-only release.

## Requested maintainer receipt

Please provide an attributable response containing:

- maintainer identity and role;
- exact Kairos revision or release tag (and whether it is immutable);
- contract artifact/path and version;
- accepted DTO fields, types, units, and schema version;
- compatibility guarantees and explicitly excluded guarantees;
- permitted transformations (if any) and whether source code is transformed;
- permitted destinations (local tests, downstream repository, release archive,
  or other named destination);
- source licence and attribution requirements;
- whether redistribution of source, payloads, or generated DTOs is allowed;
- expiration/review date, if any; and
- explicit disposition: `accepted_research_only`, `accepted_broader`,
  `declined`, or `not_authorized`.

The response may point to a signed release/contract document. A repository
owner's downstream approval alone is not a Kairos maintainer acceptance.

## Narrow extraction boundary

Until a replacement receipt exists, request authorization only for the
following derived, domain-neutral DTO surface:

1. deterministic execution request/response metadata required by the pinned
   adapter tests;
2. trace/event records needed to reproduce those tests;
3. schema/version identifiers and field-level units; and
4. checksums or provenance identifiers for the exact input and output bundle.

Do **not** request scheduler, RNG, discrete-event, agent-based, or application
domain implementation details; confidential data; unredacted source; or
payload redistribution. The downstream repository must continue to avoid
reimplementing Kairos internals and must keep reimbursement vocabulary outside
the runtime crate.

## Receipt and verification protocol

On receipt, preserve the exact response or linked artifact, URI, MIME type,
retrieval date, byte count, SHA-256, licence/terms, and permitted-use text.
Record the reviewed downstream revision and Kairos revision together. Run the
relevant-subagent panel for contract mapping, provenance/licensing, runtime
reproducibility, and security; record each receipt and any disagreement.

Promotion requires all of the following:

- maintainer acceptance at the exact immutable revision;
- explicit extraction fields and transformations;
- named destinations and redistribution terms;
- attribution requirements satisfied;
- panel receipts bound to the same revisions and digest; and
- a separate downstream research-only release authorization.

## Contingencies

- **No maintainer response:** retain the current candidate-only disposition;
  do not call the adapter a released contract.
- **Acceptance without extraction permission:** allow local compatibility tests
  only; keep extracted payloads private and do not publish them.
- **Permission limited to a release/tag:** re-pin to that immutable tag and
  rerun all checks; do not silently retain the current SHA.
- **Unclear source terms:** stop extraction and request clarification; no
  derived artefact is promoted.
- **Schema mismatch or incompatible revision:** preserve the old candidate
  receipt, open a new compatibility review, and keep the gate pending.
- **Owner declines:** record a negative receipt and retain the isolated,
  candidate-only adapter.

This template is preparation only. No message has been sent and no Kairos
gate is closed by this document.
