# Kairos contract and extraction checklist

This is a least-privilege handoff for the candidate Kairos adapter. It
documents what this repository can verify locally and what an upstream
maintainer or extraction owner must still authorize. It does not assert that a
released Kairos contract or extraction permission exists.

## Pinned contract identity

- Repository: `https://github.com/edithatogo/kairos`
- Pinned revision: `fae901558f07b7b717a676adbafbe2cdc78dea1c`
- Contract status at this revision: candidate-only; no release tag or
  maintainer acceptance receipt is currently recorded.
- Downstream adapter schema:
  `https://github.com/edithatogo/kairos/conformance/game-events/v0`

Any replacement revision, tag, or schema requires a new compatibility and
owner receipt. The downstream owner acceptance at the pinned revision is not
upstream maintainer acceptance.

## DTO and field boundary

The proposed handoff contains only the following domain-neutral values:

- event `sequence` (zero-based integer);
- event `time` (finite, non-negative number, non-decreasing);
- event `kind` (non-empty string); and
- JSON-serializable event `payload` with string keys.

The corresponding upstream surfaces under review are `ScheduleRequest`,
`DispatchedEvent`, `StepOutcome`, `SimTime`, and versioned DTO wrappers. The
repository must not allocate event codes, advance time, assign priorities or
IDs, own ECS/RNG state, or reimplement DES/ABM scheduling. Unsupported
semantics must fail explicitly.

## Allowed transformations and destinations

- [ ] Normalize event ordering and validate time/payload constraints as
  implemented by `KairosScenarioExporter`.
- [ ] Compute a SHA-256 trace receipt over canonical JSON; record the digest
  and event count.
- [ ] Send only the domain-neutral event envelope to a maintainer-approved
  Kairos contract endpoint or a local conformance fixture.
- [ ] Store schema, trace digest, and validation logs in this repository's
  research-only evidence surface.
- [ ] Exclude raw NHS/Atlas payloads, patient or confidential data,
  undisclosed prices, and Kairos source from the repository and public
  destinations.

No external transfer, publication, or redistribution is authorized until an
extraction owner records permitted sources, fields, transformations,
destination, attribution, and terms.

## Required external receipts

### Kairos maintainer/contract owner

- [ ] Exact revision or release tag and contract version.
- [ ] DTO/schema artifact and stable event-kind allocation.
- [ ] Exact-head CI or compatibility trace for the proposed envelope.
- [ ] Explicit native-integration disposition and scope.
- [ ] Maintainer identity, date, and receipt digest.

### Extraction, legal, and release owner

- [ ] Allowed source repositories/artifacts and fields.
- [ ] Permitted transformations and derived fields.
- [ ] Approved destinations and retention period.
- [ ] Attribution, licence, and redistribution terms per source.
- [ ] Restricted/raw material disposition.
- [ ] Research-only release authorization and owner identity/date.

## Current disposition and fallback

As of 2026-08-02, local compatibility and trace-receipt tests are available,
but released-contract, extraction, and publication gates remain pending. Keep
the adapter isolated and describe it as local compatibility only. If the
receipts cannot be obtained, publish only software, methodology, synthetic
fixtures, and permitted derived-only artifacts.
