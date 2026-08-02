# T13 evidence sourcing playbook

## Ranked sources

1. Signed NHS payer/commissioner decision packet for the exact programme.
2. Atlas-approved derived export at an immutable revision with source-term and reviewer receipts.
3. NICE and DHSC official manuals, technology guidance, impact assessments, APIs, and archives.
4. Official NHS formulary/committee records and public procurement or finance records.
5. DOI-bound primary research for method triangulation only.

## Autonomous acquisition

- Query official NICE, GOV.UK/DHSC, NHS/ICB, and institutional repositories for
  the intervention, comparator, TA number, programme identifier, displacement,
  price year, discounting, horizon, and uncertainty.
- Retrieve and hash exact PDFs, HTML, JSON, CSV, and Atlas export bytes; capture
  page/table/field locators, API queries, response headers, and revisions.
- Build a source-to-parameter matrix for `n`, `m`, `d`, `mu`, `phi`, annual
  effect, horizon, discounting, transformations, and covariance.
- Triangulate public context independently from Atlas-derived values and run the
  equation, unit, programme-alignment, and uncertainty checks.

## Options

1. **Recommended — Atlas-approved same-programme packet plus official NHS context.**
   Strongest authority, rights, provenance, and reproducibility.
2. **Hybrid public context plus Atlas-derived parameters.** Use when the public
   decision packet is incomplete; empirical promotion remains conditional.
3. **Public reconstruction.** Candidate research only; cannot infer confidential
   net prices, displacement, `mu`, or `phi` without authoritative evidence.
4. **Synthetic fallback.** Preserve conformance testing with no empirical claim.

## Contingencies and stops

- Inaccessible source: check the official archive/API and record an inaccessible receipt.
- Conflicting sources: preserve both and defer the affected role to the responsible owner.
- Incomplete packet: promote only complete scenario-role sets; otherwise keep `not_identifiable`.
- Restricted source: record metadata only and stop before access or transfer.
- Stop for payer/Atlas approval, credentials, confidential values, or any change from research-only use.

## Refresh

Reacquire at every calibration/release freeze and whenever the programme,
decision date, price year, Atlas revision, source terms, transformation, or
repository commit changes.
