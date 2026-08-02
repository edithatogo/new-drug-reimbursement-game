# Atlas packet closure checklist

This checklist is the fail-closed handoff for an approved-derived TA1121
packet. It is an intake and verification aid; checking an item does not grant
Atlas, NHS, licensing, or release approval.

## Immutable identity

- [ ] Atlas repository URL and exact 40-character commit SHA are recorded.
- [ ] The lockfile revision and resolved checkout revision are identical, or
  the difference is explained by an owner-signed reconciliation receipt.
- [ ] Packet ID, export version, creation date, and byte-level SHA-256 are
  recorded.
- [ ] Every source artifact has a URI, publisher, date/version, MIME type,
  byte count, SHA-256, and retrieval receipt.

## Programme-aligned contents

- [ ] The packet names the NHS payer, service line, decision date, price year,
  intervention, comparator, displaced programme, stable programme ID, and
  accountable owner.
- [ ] Required Chapter 7 roles (`n`, `m`, `d`, `mu`, `phi`, annual programme
  health effect, and horizon) are present or explicitly marked unavailable.
- [ ] Baseline units, currency, time horizon, and discounting convention are
  explicit and dimensionally compatible with the repository schema.
- [ ] Scenario 4 is disabled unless one specific investment programme and its
  effects are identified by the authoritative packet.

## Provenance, transformations, and terms

- [ ] Each derived field maps to one or more source records and includes the
  transformation, unit conversion, and uncertainty treatment.
- [ ] Atlas licence/source terms identify permitted extraction, derivation,
  destination, and publication scope.
- [ ] Raw or restricted payloads are excluded from this repository unless a
  separate written authorization permits them.
- [ ] An Atlas owner/reviewer records disposition, identity, date, exact
  revision, and packet digest. General licence-ledger validation is not a
  substitute for packet approval.

## Panel and release binding

- [ ] Four role receipts are complete: economics/methods, NHS context and
  displacement, Atlas provenance/licensing, and runtime/reproducibility.
- [ ] Each receipt records reviewer identity/model, independence/conflicts,
  reviewed commit and packet paths, source revisions/hashes, checks,
  findings, disposition, limitations, timestamp, and attestation.
- [ ] The orchestrator records receipt hashes, quorum, disagreements,
  abstentions, unresolved gates, final disposition, exact commit, and packet
  digest.
- [ ] The repository readiness and full validation suites pass at the bound
  revisions before any scenario is promoted.
- [ ] Research-only release authorization is separate from calibrated,
  regulatory, or HTA claims authorization.

## Current disposition

As of 2026-08-02, immutable Atlas release `v0.1.1` has been reconciled and
receipted. It contains terminology-only acoramidis/tafamidis material but no
programme-aligned TA1121 `n/m/d` packet, NHS displacement/baseline, aligned
uncertainty, or approval receipt. The release is not promotable; synthetic and
methodology-only paths remain the safe fallback. Retry only against a newer
immutable release or a separately attached approved-derived packet.
