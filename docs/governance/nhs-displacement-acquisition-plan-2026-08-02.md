# NHS displacement-packet acquisition plan (not sent)

This plan operationalises the approved acquisition route for one authoritative,
non-patient-level TA1121 decision context. It is preparation only: no request
is sent by this repository and no candidate source is promoted automatically.

## Recommended sequence

1. **Route to the accountable commissioner first.** Start with NHS England
   specialised commissioning or the medicines-optimisation committee that
   owns the South Yorkshire TA1121 decision. Use the South Yorkshire IMOC
   minutes only to identify the likely decision owner; they do not establish
   displacement.
2. **Use service providers for routing, not attribution.** Contact the Royal
   Free National Amyloidosis Centre and University Hospitals Birmingham /
   Midlands Amyloidosis Service only to identify the commissioning record or
   confirm that they do not hold it.
3. **Use a formal public-record/FOI route if the owner is unresolved.** Request
   a releasable decision paper, minute, or budget implementation extract from
   the named NHS body. Do not request patient-level data or confidential net
   prices.
4. **Freeze and receipt any response.** Preserve the exact bytes, URI or
   correspondence identifier, sender/owner, date, MIME type, byte count,
   SHA-256, terms, and permitted use. Classify the response as `authoritative`,
   `supporting_only`, `candidate_only`, or `negative`.
5. **Run the relevant-subagent panel.** Map each field to the source, check
   equations/units and uncertainty, and record the reviewed revision, packet
   digest, disagreements, and per-role receipts. The panel cannot substitute
   for commissioner or custodian approval.
6. **Promote only after all gates bind.** Link the NHS receipt to the
   reconciled Atlas revision and approved-derived packet, then rerun readiness
   and full validation. Keep `d` and displacement-dependent scenarios
   disabled until this sequence succeeds.

## Minimum request payload

Request one bounded decision context containing:

- accountable payer/commissioner and budget boundary;
- service line/provider and stable programme or decision ID;
- decision date, price year, and relevant horizon;
- intervention and explicitly named comparator;
- actual displaced or reallocated programme and mechanism;
- baseline cost and health/currency unit used for the decision; and
- owner confirmation that this programme is the source for displacement
  parameter `d`.

Accept a redacted record only when the required fields and accountable owner
remain visible. A response stating that the information is not held, cannot
be disclosed, or does not identify displacement is a valid negative receipt,
not a promotion receipt.

## Recipient and escalation routing

| Stage | Recipient | Purpose | Fallback |
|---|---|---|---|
| 1 | NHS England specialised commissioner or named South Yorkshire decision owner | Authoritative decision and displacement record | Ask the ICB medicines-optimisation secretariat to identify the owner |
| 2 | South Yorkshire ICB medicines-optimisation / IMOC secretariat | Confirm payer, service line, decision ID, and record custodian | Treat response as routing or negative evidence if displacement is absent |
| 3 | Royal Free NAC and UHB Midlands amyloidosis service | Identify the commissioning record or confirm non-custody | Do not attribute their service materials as the payer decision |
| 4 | Formal NHS public-record/FOI channel | Obtain a releasable decision extract | Retain a negative receipt if no auditable record is released |

## Contingencies and closure rules

- If no local displacement record is available, retain the model in
  synthetic/methodology-only mode; do not infer `d` from a formulary or traffic
  light.
- If the specialised commissioner differs from South Yorkshire ICB, redirect
  the request and preserve the original routing receipt.
- If baseline cost is redacted but the programme identity and unit are explicit,
  leave `d` pending and consider only scenario-scoped, non-calibrated outputs.
- If sources conflict, preserve each receipt and defer promotion pending panel
  adjudication; never silently select one.
- If source terms or Atlas revision hashes do not reconcile, keep derived
  outputs private and stop promotion.
- If no accountable owner responds, record the failed route and leave the gate
  pending. Repository authorship is not owner approval.

## Authoritative artefact checklist

The eventual packet must include a signed or otherwise attributable owner
receipt, exact source hash, source-to-field mapping, transformation and unit
ledger, uncertainty description, licence/terms disposition, panel receipts,
and a digest-bound promotion decision. Until every item exists, the canonical
state remains `candidate_only` / `not_identifiable` and
`approved_calibration_permitted: false`.
