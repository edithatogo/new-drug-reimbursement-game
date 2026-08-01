# Kairos contract and extraction authorization receipt

**Receipt ID:** `kairos-extraction-authorization-2026-08-01`
**Recorded:** 2026-08-01
**Repository:** <https://github.com/edithatogo/Kairos>
**Pinned revision:** `fae901558f07b7b717a676adbafbe2cdc78dea1c`

## Evidence inspected

The pinned checkout was verified at the exact revision above. The associated
qualification record (`kairos-upstream-qualification.json`) reports:

- no tags at the pinned revision;
- no GitHub release for the repository;
- release stage `r2-dry-run`;
- production publishing disabled;
- local compatibility and workspace-test evidence available;
- no maintainer acceptance receipt for a released DTO/API contract.

The local tests and compatibility documents establish only that the adapter is
locally usable at this pin. They are not evidence of upstream contract
acceptance, extraction permission, or redistribution rights.

## Disposition

| Gate | Disposition | Basis |
| --- | --- | --- |
| Kairos released-contract acceptance | **pending** | No release/tag or maintainer acceptance receipt was found. |
| Kairos extraction approval | **pending** | No extraction-owner authorization was found. |
| Extraction/publication authorization | **pending** | No receipt specifies permitted fields, transformations, destinations, attribution, or redistribution terms. |
| Local adapter compatibility | **candidate-only** | Pinned checkout and local tests are available, but cannot substitute for the three approvals above. |

## Allowed use until replacement receipt

The adapter may remain in the repository as an isolated, candidate-only
integration for local testing. It must not be represented as native Kairos
integration, a released upstream contract, or authorized extraction. No Kairos
payload should be published or redistributed from this receipt.

## Required replacement evidence

To close any pending gate, a replacement receipt must identify the approving
owner or maintainer, exact Kairos revision/tag, contract artifact or extracted
fields, permitted transformations and destinations, source terms, and an
explicit research-only or broader release disposition. Until then, the
Conductor gates remain pending and the release scope is limited to software and
methodology.
