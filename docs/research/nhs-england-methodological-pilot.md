# NHS England methodological evidence pilot

## Result

This pilot cross-references public NHS/DHSC opportunity-cost evidence and NICE
methods guidance against every parameter required by the four Chapter 7
scenarios. It is evidence triage, not an empirical calibration. The executable
receipt is `docs/generated/nhs-england-pilot-readiness.json`; it always sets
`approved_calibration_permitted` to `false`.

| Scenario | Source requirement | Pilot result | Why |
|---|---|---|---|
| 1, expandable efficient | `n` in equation 7.1 | `candidate_only` | National/historical candidates exist, but their price basis, uncertainty, decision-context fit, Atlas approval, and health-economist approval are absent. |
| 2, fixed efficient | `n = m` and actual displacement `d` | `not_identifiable` | The sources do not identify the displaced programme or establish economic efficiency in one aligned decision context. |
| 3, allocative inefficiency | `m > n` and `n <= d <= m` in equations 7.2-7.5 | `not_identifiable` | `d` is absent. Different estimates cannot be cherry-picked across periods and budget scopes to manufacture the ordering. |
| 4, technical investment | Aligned decision-context `m` and `d`; same-investment-programme `mu`, `phi`, annual effect, horizon, and discounting; Appendix 5 identity | `not_identifiable` | No programme-specific investment evidence or numeric horizon exists. Discount guidance alone cannot identify `phi`; the case-specific identity `phi * annual_effect = incremental_cost / mu` remains unchecked. |

The Chapter 7 equation locations and implemented identities are documented in
`docs/research/dimensional-derivation-ledger.md` and
`docs/research/source-conformance-audit.md`. Pekarsky (2015), Chapter 7, is the
model authority; public NHS sources are considered only as parameter
candidates.

## Reviewed sources

Source binaries and copied tables are deliberately excluded from Git.
Checksums below identify the exact local review snapshots; CI validates the
committed dossier and receipt, not the absent source binaries.

| Source | Reviewed claim | Snapshot SHA-256 |
|---|---|---|
| [DHSC 2026 statutory-scheme consultation-stage impact assessment](https://assets.publishing.service.gov.uk/media/6989d4b14cff1c70a3b6e4fd/consultation-stage-impact-assessment-proposed-2026-changes-to-statutory-scheme-for-branded-medicines-pricing.pdf), Annex C, PDF pp. 22-23; discount calculation on PDF pp. 11-12 and 14 | GBP 15,000/QALY is a pragmatic simplifying marginal-health-opportunity-cost assumption informed by a reported GBP 12,981 estimate. It is not a firm estimate, prediction, commitment, or NICE threshold. The example discounts QALYs at 1.5%. | `da2f3bb1ae21e65cd0aac668f1e21f35e5c1685c69aa6f76f0048e9eea90c60e` |
| [CHE Research Summary 9](https://www.york.ac.uk/media/che/documents/papers/researchsummaries/Summary%209.pdf), July 2023 | Marginal NHS cost per QALY is likely below GBP 15,000 and varies by geography and programme. The qualitative result supports caution; it is not entered as a new numeric candidate. | `4b1814572e363dcb2e722a4fb43b1a6e04ef5c6b278bc6f6130fdf375fdaad02` |
| [Martin, Claxton, Lomas, and Longo (2023)](https://eprints.whiterose.ac.uk/id/eprint/197618/), reporting the [2014/15 study](https://doi.org/10.1007/s40258-022-00723-2) | Approximately GBP 7,000/QALY for locally commissioned NHS services in 2014/15; the related paper also demonstrates material scope heterogeneity. | White Rose repository PDF: `2eea0d4ac30aa2175fa0496a0c95e9294b9fd1499c84c8b52c32f9a36d6988b4` |
| [NICE economic-evaluation manual](https://www.nice.org.uk/process/pmg36/chapter/economic-evaluation-2/), sections 4.2 and 4.5 | Use a horizon long enough to capture important differences; the standard reference case discounts costs and health effects at 3.5% annually. | `20b1111fc52b846dcb1e3ce4c705af4592472bbc13369f7d74ac2fb578de40b5` |

The DHSC 1.5% and NICE 3.5% rates are distinct candidates with different
methodological scopes. Neither is silently selected. Publication year,
observation period, and monetary price year are also distinct: the reviewed
passages do not establish the monetary price years of GBP 15,000, GBP 12,981,
or approximately GBP 7,000, so every candidate records `price_year: null` and
no inflation adjustment.

## Mapping controls

The candidate dossier is intentionally separate from the approved Atlas
packet. Each candidate records its source, exact location, scope, study period,
price-year knowledge, transformation, assumptions, limitations, uncertainty,
possible roles, optional programme identity, and optional reviewed alignment
identity.

- GBP 15,000, GBP 12,981, and approximately GBP 7,000 are considered only for
  `n` and `m`; none identifies actual displacement `d`.
- A record may span both `n` and `m`, but no other mixed-role record is allowed.
- Distinct records may satisfy a multi-parameter constraint only when an
  explicit non-null alignment identifier says their scopes and transformations
  were reviewed together.
- Scenario 4 requires one alignment identity across the decision context. A
  non-null programme identity must match across `mu`, `phi`, annual effect,
  horizon, and discount evidence; `m` and `d` remain distinct economic roles.
  The cost/effect identity is still checked later against the decision case.
- Nonnumeric guidance is allowed only for the horizon. It remains visible in
  provenance while the role stays `not_identifiable`.
- `supported` is part of the shared readiness vocabulary but is unreachable
  from a candidate-only dossier. Only the separate approved Atlas path can
  supply approved model evidence.

The parser is authoritative for constraints that JSON Schema cannot express,
including unique candidate identifiers and context-derived units.

## Reproduction

```bash
python -m reimbursement_game.cli pilot-readiness fixtures/evidence/nhs-england-methodological-candidates-v1.json
python -m unittest discover -s tests -p 'test_pilot_readiness.py'
```

Promotion remains externally gated on a specific NHS payer/service line and
displaced programme, a reviewed transformation/alignment, Reimbursement Atlas
approval, and independent health-economic approval.

The decision form for those remaining gates is
`docs/governance/nhs-pilot-external-gate-intake.md`.
