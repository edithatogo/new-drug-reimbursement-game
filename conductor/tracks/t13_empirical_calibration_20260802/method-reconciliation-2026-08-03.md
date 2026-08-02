# T13 method and assumption reconciliation

## Scope and disposition

This review binds the constrained T13 research output to the clean-room
derivations in `docs/research/source-conformance-audit.md`, the strict Python
and Rust conformance fixtures, the health-economist research-method approval,
and the public TA1121 evidence packet. It approves mathematical conformance and
synthetic research use only. It does not activate empirical calibration.

Primary conceptual source: Pekarsky, B. A. K. (2015), *The New Drug
Reimbursement Game*, Chapter 7, DOI
`10.1007/978-3-319-08903-4`. Scenario 4 is additionally checked against
Pekarsky's 2012 dissertation, Appendix 5, as already hash-bound in the source
conformance audit.

## Equation reconciliation

| Scenario | Implemented identity | Source location | Domain check | Disposition |
| --- | --- | --- | --- | --- |
| 1 | `beta_c = n` | 2015 equation 7.1, printed p. 110/PDF p. 120 | positive finite cost, effect, and `n` | exact within stated source domain |
| 2 | `beta_c = d` | 2015 Scenario 2, printed pp. 110–114/PDF pp. 120–124 | `n = m`; positive finite `d` | exact within stated source domain |
| 3 | `1/beta_c = 1/d + 1/n - 1/m` | 2015 equations 7.2–7.5, printed pp. 116–119/PDF pp. 126–129 | `m > n` and `n <= d <= m` | exact within stated source domain |
| 4 | `phi * DeltaE_G = DeltaC_P / mu`; `1/beta_c = 1/d + 1/mu - 1/m` | 2012 Appendix 5 pp. 231–234; 2015 Table 7.2 | `phi > 1`, `mu < m`, `d <= m`, one investment programme, positive net gain | exact identity; empirical values unavailable |

For all scenarios, `IPER = DeltaC_P / DeltaE_P`, `EVCI = beta_c * DeltaE_P`,
and the sign of net economic benefit in health units is checked by shared
Python/Rust fixtures. Currency and health-unit rescaling, threshold equality,
special cases, invalid domains, and non-identifiability fail-closed behavior
are covered by automated tests.

## Assumptions and heuristics

- Adoption is required inside the strict Chapter 7 comparison; the result is
  not an observed payer decision.
- `n`, `m`, `d`, and `mu` are marginal currency-per-health-unit roles. Average
  or merely incremental values cannot be substituted.
- Scenario 3 requires allocative inefficiency, not merely unequal programme
  averages.
- Scenario 4 treats `mu` as a source-backed exogenous marginal investment
  parameter. The application does not estimate it from public TA1121 context.
- NICE 3.5% is the provisional primary health-economic discount convention;
  DHSC 1.5% remains a sensitivity. Neither rate identifies `phi` without a
  programme-specific time profile.
- The synthetic conformance fixture uses 3.0%. This is not the approved primary
  method convention and cannot be promoted. Any empirical Scenario 4 packet
  must derive `phi` reproducibly from an approved time profile using 3.5% as
  primary and 1.5% as sensitivity.
- Synthetic uncertainty samples are aligned positionally for arithmetic
  conformance. Any empirical packet must supply joint-draw identifiers and
  dependence or covariance provenance; equal array length alone is
  insufficient evidence of a justified joint uncertainty model.
- The NICE TA1121 three-year resource-impact horizon and national market shares
  describe public treatment-substitution context. They do not identify an
  actual displaced programme or parameter `d`.
- No price-year conversion is permitted because programme-specific net prices
  and a displacement baseline are unavailable.

## Parameter disposition

| Role | T13 disposition |
| --- | --- |
| `n`, `m`, `d` | not identifiable from the approved public packet |
| `mu`, `phi`, annual programme effect | not identifiable; Scenario 4 remains synthetic sensitivity only |
| horizon | three-year NICE public context is supported; no same-programme Scenario 4 horizon is approved |
| discount rate | 3.5% primary method, 1.5% sensitivity; not an empirical parameter packet |
| intervention/comparators | acoramidis; tafamidis and vutrisiran supported as national context |
| commissioner/programme category | NHS England; PBC 10X supported as context, not displacement identity |

## Conclusion

The equations, dimensions, domains, parameter meanings, and method choices are
internally reconciled. The deterministic output may be labelled only
`synthetic_research_only`. Empirical promotion remains prohibited until an
immutable Atlas-approved same-programme packet and authoritative NHS
displacement context satisfy the T13 gates and trigger regeneration.
