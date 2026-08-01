# External blocker execution register

This register is the active handoff for the remaining non-repository gates.
Statuses are intentionally conservative: a local test or owner intention does
not substitute for an authoritative external receipt.

| Gate | Current status | Recommended next action | Closure evidence |
|---|---|---|---|
| Specific NHS displacement context | pending | Obtain one ICB/commissioner decision record for TA1121, including the actual displaced programme and baseline unit cost | Signed context packet with payer, service line, decision date, price year, displaced programme, stable ID, and accountable owner |
| Atlas-derived NHS records | pending | Request an approved-derived export at an immutable Atlas revision | Packet ID/revision, `n,m,d` records, optional Scenario 4 records, provenance, transformations, uncertainty, licences, and Atlas approval |
| Kairos contract | pending | Request released DTO/API contract or upstream maintainer acceptance for the pinned revision | Exact revision, contract artefact, exact-head CI/trace receipt, maintainer disposition |
| Extraction approval | pending | Obtain extraction/publication-owner decision for each source and destination | Source-term adjudication, extraction scope, release surface, owner, date, and restrictions |

Repository-owned work is complete for the current slice: the TA1121 public
candidate, Atlas intake packet, method decision, health-economist receipt,
UOGTO acceptance, and fail-closed tests are committed. The synthetic Chapter 7
packet remains available for conformance tests only and is never promoted as
NHS evidence.

When any receipt arrives, bind it to the current commit and exact source hash,
update only its matching Conductor gate, regenerate readiness outputs, and run
the full validation suite before considering promotion.
