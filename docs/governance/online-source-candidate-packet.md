# Official online-source candidate packet

The machine-readable packet at
`fixtures/evidence/nhs-online-candidate-ta1121.json` records a reproducible
candidate NHS context assembled from official NICE and NHS England web sources.
It is deliberately marked `candidate_only` and cannot close the displacement,
Atlas-derived approval, independent-review, or calibrated-claims gates.

The NICE TA1121 record supplies a stable appraisal identifier, intervention,
comparator, and final recommendation date. The NHS England 2026/27 Payment
Scheme supplies the price-year context. Neither source identifies the locally
displaced programme, a local commissioner/service-line decision record, or an
approved net price. Those fields therefore remain unresolved rather than being
inferred from public text.

Retrieval dates and exact source locations are recorded in the JSON packet.
Any future promotion requires an approved-derived Atlas packet, transformation
ledger, uncertainty specification, and named health-economist sign-off.
