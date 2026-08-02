# Kairos contract and extraction checklist

This is a least-privilege handoff for the candidate Kairos adapter. It
documents what this repository can verify locally and what an upstream
maintainer or extraction owner must still authorize. It distinguishes the
accepted public-contract boundary from native integration and restricted-data
permissions that do not yet exist.

## Pinned contract identity

- Repository: `https://github.com/edithatogo/kairos`
- Pinned revision: `fae901558f07b7b717a676adbafbe2cdc78dea1c`
- Contract status at this revision: the maintainer accepts the versioned public
  contract boundary for research-only and synthetic conformance work; there is
  no release tag or native adapter compatibility acceptance.
- Downstream adapter schema:
  `https://github.com/edithatogo/kairos/conformance/game-events/v0`

Any replacement revision, tag, or schema requires a new compatibility and
owner receipt. The bounded maintainer disposition is recorded in
`kairos-maintainer-acceptance-receipt-2026-08-02.json`.

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

- [x] Normalize event ordering and validate time/payload constraints as
  implemented by `KairosScenarioExporter`.
- [x] Compute a SHA-256 trace receipt over canonical JSON; record the digest
  and event count.
- [x] Send only the domain-neutral event envelope to a maintainer-approved
  Kairos contract endpoint or a local conformance fixture.
- [x] Store schema, trace digest, and validation logs in this repository's
  research-only evidence surface.
- [x] Exclude raw NHS/Atlas payloads, patient or confidential data,
  undisclosed prices, and Kairos source from the repository and public
  destinations.

Only the hashed public contract documents, synthetic fixtures, and associated
metadata are authorized for this public repository. Raw, restricted, or
confidential transfer remains prohibited.

## Required external receipts

### Kairos maintainer/contract owner

- [x] Exact revision and versioned public contract documents.
- [~] DTO/schema artifact identified; native downstream mapping and stable event-kind allocation remain unapproved.
- [~] Exact-revision core/cross-platform checks pass; fuzz-smoke and native-envelope compatibility remain unresolved.
- [x] Explicit disposition: public/synthetic contract work accepted; native promotion deferred.
- [x] Maintainer identity, date, scope, source hashes, and refresh rule.

### Extraction, legal, and release owner

- [ ] Allowed source repositories/artifacts and fields.
- [ ] Permitted transformations and derived fields.
- [ ] Approved destinations and retention period.
- [ ] Attribution, licence, and redistribution terms per source.
- [ ] Restricted/raw material disposition.
- [ ] Research-only release authorization and owner identity/date.

## Current disposition and fallback

As of 2026-08-02, public contract-metadata extraction and synthetic conformance
are maintainer-authorized. Native DTO mapping, exact-head green compatibility,
a registry release, and any raw/confidential extraction remain pending. Keep
the adapter isolated and describe it as local compatibility only.
