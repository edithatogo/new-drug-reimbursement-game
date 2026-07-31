# Source-conformance audit

Status: complete code-and-source cross-check for the implemented Chapters 6–8
surface. The audit is bound to the authorized 2015 Pekarsky PDF with SHA-256
`8455ad153cf5b6c1570bfc945108efe659904b3c8f89fdf7b74b88c9523c4848`.
Printed-page and PDF-page references are both recorded because they differ by
ten pages in the reviewed file.

Scenario 4 is additionally bound to the University of Adelaide repository copy
of Pekarsky's 2012 dissertation, Appendix 5, PDF pages 231–234, SHA-256
`10b727b52872483ac60f3958c9e4dd2c6fba2d1e875b1fac5cd9d52469341723`.
Repository record:
`https://digital.library.adelaide.edu.au/items/df22f408-5195-4b7c-83bb-cd03e707e55b`.

## Equation and parameter matrix

| Item | Source | Repository disposition | Executable evidence |
|---|---|---|---|
| `f = Delta C_P / Delta E_P` (IPER) | Ch. 6, printed pp. 95–98/PDF pp. 105–108 | Exact for positive finite inputs | `incremental_price_effectiveness_ratio`; Python tests |
| Expandable threshold `beta_c = n` (7.1) | printed p. 110/PDF p. 120 | Exact when expansion is the sole alternative | `test_expandable_context_reduces_to_n` |
| Fixed efficient threshold `beta_c = d` | printed p. 114/PDF p. 124 | Exact when `n = m` | Python/Rust special-case tests |
| `Delta E_R = Delta E_P - Delta C_P/d` | Ch. 7 | Exact fixed-budget reimbursement effect | Python/Rust NEBh tests |
| `Delta E_T = Delta C_P(1/n - 1/m)` | printed p. 116/PDF p. 126 | Exact when `m > n`; generalized kernel clips non-positive gain | Python/Rust identity tests |
| NEBhR (7.2) | printed p. 116/PDF p. 126 | Exact in strict Scenario 3 domain | shared economics fixture |
| `1/beta_c = 1/d + 1/n - 1/m` | printed p. 116/PDF p. 126 | Exact in strict Scenario 3 domain | Python/Rust threshold tests |
| EVCI `= beta_c Delta E_P` | printed p. 117/PDF p. 127 | Exact | evaluation result and sign tests |
| inequalities (7.3), (7.4), (7.5) | printed pp. 118–119/PDF pp. 128–129 | Algebraically equivalent and directly tested | `test_equations_7_3_and_7_4_are_equivalent` |
| Reallocation gain (8.1) | printed p. 148/PDF p. 158 | Same strict formula as Chapter 7 | exact Game 1 validator and fixture |
| equilibrium `f* = (1/d + 1/n - 1/m)^-1` (8.2) | printed p. 150/PDF p. 160 | Exact only through `solve_pekarsky_game1` | Python/Rust Game 1 fixture |
| firm rent `pi = f* Delta E_P` | printed p. 151/PDF p. 161 | Exact Game 1 assumes incremental IMER zero | Python/Rust Game 1 fixture |
| institution NEBhR at equilibrium | printed pp. 151–152/PDF pp. 161–162 | Zero subject to floating-point error | Python/Rust Game 1 fixture |
| Scenario 4 `phi Delta E_G = Delta C_P/mu` | 2012 Appendix 5, p. 233 | Exact for caller-supplied, provenance-bound inputs | Python/Rust all-scenario fixture |
| Scenario 4 `beta_c^v = (1/d + 1/mu - 1/m)^-1` | 2012 Appendix 5, pp. 233–234; 2015 Table 7.2 | Exact within the source assumptions | Python/Rust all-scenario fixture |

`Delta C_P` is incremental currency cost; `Delta E_P`, `Delta E_D`, and
`Delta E_A` are health effects; `f`, `n`, `m`, `d`, and `beta_c` are
currency/health; productivity terms are health/currency. `incremental_imer` in
the generalized solver is an incremental manufacturing cost-effectiveness
ratio, not an unscaled manufacturing cost.

## Assumption disposition

Strict Chapter 7 validation distinguishes required adoption from economic
preference and enforces each scenario's source domain. Exact Game 1 validation
enforces positive fixed health effect, fixed budget,
positive `n`, `m`, and `d`, `m > n`, `n <= d <= m`, no additional alternative,
and zero incremental IMER. The source additionally assumes:

- one monopolistic/patent-holding firm and one reimbursing institution;
- a clinically superior drug for a homogeneous target group, adopted for all
  eligible patients with fixed and certain health effect;
- reimbursement means adoption plus financing through displacement;
- only non-patented services are displaced; actual displacement is exogenous,
  non-optimal, continuous/divisible, and uses a constant certain aICER;
- expansion/contraction opportunities are feasible, locally linear over the
  relevant `Delta C_P`, known with certainty, and reallocation is costless;
- the current allocation is inefficient and reallocation is not already
  institutionalized;
- the firm knows the public threshold, all terminal nodes are reachable, the
  institution reimburses on indifference, and the firm does not lobby above
  the threshold; and
- the game does not infer a relationship between today's price and future
  innovation.

Those institutional and empirical assumptions cannot be proven from numeric
inputs. Exact solver output is therefore conditional model evidence, not an
empirical, policy, HTA, legal, or regulator-grade conclusion.

Scenario 4 additionally assumes a fixed budget in every period, a Year 1
investment financed by optimal contraction, restoration of the contracted
programme after Year 1, no subsequent net budget effect, known future effects,
`phi > 1`, `mu > 0`, and a positive net present health gain. The evaluator
requires the source identity `phi * Delta E_G = Delta C_P / mu`; it does not
estimate or validate the empirical discounting process behind those inputs.

## Heuristics and generalized extensions

The reusable economics kernel deliberately extends the source by clipping
non-positive reallocation productivity to zero, selecting the maximum among
named alternative strategies, accepting wider parameter domains, and applying
a scale-aware floating-point decision tolerance. The generalized Chapter 8
solver additionally permits a non-zero IMER and other financing contexts.
None of those outputs may be labelled exact Game 1 or exact Scenario 3
conformance without first satisfying the strict source domain.

The equilibrium command uses the strict Game 1 solver. Its input
`incremental_cost` remains relevant to the evaluation command but is ignored
by equilibrium because Game 1 endogenizes `f*` and therefore
`Delta C_P = f* Delta E_P`.

## Source discrepancies

The apparent `n = m` typo on printed page 115/PDF page 125 and the
`Delta E_P`/`Delta C_P` dimensional typo on printed page 109/PDF page 119 are
recorded and adjudicated in the dimensional ledger. No source scans or source
prose are stored in the repository.
