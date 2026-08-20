# External blocker execution register

This register is the active handoff for the remaining non-repository gates.
Statuses are intentionally conservative: a local test or owner intention does
not substitute for an authoritative external receipt.

| Gate | Current status | Recommended next action | Closure evidence |
|---|---|---|---|
| Specific NHS displacement context | closed as owner-authorized deferral | Preserve the prohibition on inferring displacement; reopen only if an attributable local record supplies the displaced programme, stable programme ID, and baseline unit | `conductor/tracks/t13_empirical_calibration_20260802/nhs-displacement-deferred-closure-2026-08-03.json` |
| Atlas-derived NHS records | candidate approved at an obsolete target; current-head promotion invalidated | Requalify exact packet bytes, digest, sources, transformations, terms, destination, and target commit before any promotion | `atlas-owner-approval-receipt-2026-08-03.json` records the packet approval and failed target binding; no empirical promotion is permitted |
| Kairos public contract boundary | satisfied with conditions | Preserve the accepted pinned boundary and refresh if the revision changes | `kairos-maintainer-acceptance-receipt-2026-08-02.json`; native DTO/release promotion remains separately deferred |
| Extraction approval | satisfied for the bounded historical research-only surface; current-head release requalification required | Preserve source-specific restrictions and revalidate the exact release commit before publishing another release | `research-only-extraction-owner-authorization-2026-08-01.md`; broader, calibrated, raw, confidential, payer, policy, HTA, or regulatory release remains prohibited |

Repository-owned work is complete for the current slice: the TA1121 public
candidate, Atlas intake packet, method decision, health-economist receipt,
UOGTO acceptance, and fail-closed tests are committed. The synthetic Chapter 7
packet remains available for conformance tests only and is never promoted as
NHS evidence.

Atlas `v0.1.1` has an immutable negative disposition: terminology exists, but
no Atlas-issued TA1121 `n/m/d` packet is present. A repository-derived candidate
was subsequently owner-approved for research-only contextual use, but its exact
target binding is obsolete. The next retry must requalify the approved candidate
against the intended commit or use a newer immutable Atlas-issued packet.

When any receipt arrives, bind it to the current commit and exact source hash,
update only its matching Conductor gate, regenerate readiness outputs, and run
the full validation suite before considering promotion.
