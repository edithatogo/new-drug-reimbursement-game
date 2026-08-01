# Upstream acquisition receipt — 2026-08-01

Codex inspected the pinned local Atlas and Kairos checkouts at the revisions in
`ecosystem.lock.toml`.

## Atlas

No public Atlas record matching TA1121, acoramidis, tafamidis, ATTR-CM, or the
required NHS programme roles was found. The existing Atlas licence validation
therefore remains valid for its reviewed sources, but it does not create an
NHS-specific approved-derived packet. The Atlas gate remains pending.

The authoritative GitHub surface exposes release `v0.1.0` at commit
`5b0c2fe3e1b7d2d6c3c1975cf1a162f2787c67aa`, matching the pinned checkout. This
confirms revision identity, not NHS parameter approval.

## Kairos

The pinned Kairos checkout has no release tags and its release manifest marks
the current train as `r2-dry-run` with production publishing disabled. The
repository contains compatibility and packaging documentation, but no released
DTO/API contract or maintainer acceptance receipt bound to this integration.
Local workspace tests remain useful compatibility evidence only. The Kairos
contract gate remains pending and the adapter must remain isolated.

The authoritative `edithatogo/Kairos` GitHub surface has no releases and no
tags, confirming that no released contract artifact is available at this check.

These are completed acquisition checks, not failures: the absence of a matching
artifact is recorded explicitly so no gate is closed by inference.
