# Dimensional derivation and assumption ledger

Status: authorized-source verified and independently reviewed for the implemented
Scenario 3 reallocation model. Scenario 4 investment parameter `mu` remains
explicitly out of scope.

Primary conceptual source: Pekarsky (2015), Chapters 6-8, especially Chapter 7
equations 7.2-7.5 on printed pages 116, 118, and 119 (PDF pages 126, 128,
and 129), and the Chapter 8 Game 1 solution. DOI
`10.1007/978-3-319-08903-4`. The authorized PDF reviewed for this ledger has
SHA-256 `8455ad153cf5b6c1570bfc945108efe659904b3c8f89fdf7b74b88c9523c4848`.

This note records repository algebra without reproducing source prose or
claiming to resolve the outstanding Chapter 7 technical-efficiency
interpretation. Its review binding is the Git commit containing this file and
the executable tests cited below.

## Units

| Symbol | Meaning | Unit |
|---|---|---|
| `Delta C` | Incremental reimbursed cost | currency |
| `Delta E` | Incremental clinical health effect | health |
| `f` | Incremental price-effectiveness ratio | currency / health |
| `n` | Expansion ICER | currency / health |
| `m` | Contraction ICER | currency / health |
| `d` | Displacement ICER | currency / health |
| `g` | Alternative-strategy productivity | health / currency |
| `beta_c` | Health shadow price | currency / health |

Every finite ICER used as a denominator must be strictly positive. A fixed
budget requires `d`; an expandable context requires at least one positive
alternative productivity. Missing, non-finite, non-positive, or
non-identifiable contexts fail closed.

## IPER

For positive `Delta C` and `Delta E`:

```text
f = Delta C / Delta E
```

The units are currency per health unit. Price remains negotiable and is not
silently reinterpreted as an exogenous resource cost.

## Fixed-budget population health effect and NEBhR

Financing `Delta C` displaces `Delta C / d` health. Forgoing the best explicitly
named alternative with productivity `g*` costs `Delta C * g*` health. Therefore:

```text
NEBhR = Delta E - Delta C / d - Delta C * g*
```

No alternatives are summed implicitly. The caller must explicitly model a
combined strategy if multiple gains can jointly be realized.

## Shadow price and threshold identity

At the threshold, `NEBhR = 0` and `Delta C = beta_c * Delta E`. Substitution and
division by positive `Delta E` give:

```text
1 / beta_c = 1 / d + g*
beta_c = 1 / (1 / d + g*)
```

The denominator has units health per currency, so `beta_c` has units currency
per health.

For the explicitly named reallocation strategy:

```text
g_reallocation = max(0, 1 / n - 1 / m)
```

When the ordering supports a positive reallocation gain:

```text
1 / beta_c = 1 / d + 1 / n - 1 / m
```

Special cases:

- `n = m` implies `g_reallocation = 0`, so `beta_c = d`.
- `d = m` and `n < m` imply `1 / beta_c = 1 / n`, so `beta_c = n`.

Section 7.5 on printed page 117 (PDF page 127) defines `mu` for a distinct
Scenario 4 investment strategy that combines a current static-efficiency cost
with a future dynamic-efficiency gain and derives a separate `beta_c^v`. It is
not the Scenario 3 reallocation productivity `g*`. The implementation therefore
does not map `mu` to `g*`; it keeps investment opportunities as named,
provenanced alternatives and does not claim Scenario 4 conformance.

## EVCI and decision sign

The implemented economic value of clinical innovation is:

```text
EVCI = beta_c * Delta E
```

Its unit is currency. Since `Delta C = f * Delta E`, the binding-context
identity is:

```text
NEBhR = Delta E * (1 - f / beta_c)
```

Thus `f < beta_c` is positive, equality is zero, and `f > beta_c` is negative.

For the strict Scenario 3 domain, the book presents two equivalent
decompositions of that positive-benefit condition:

```text
Eq 7.3: (1/f - 1/d) > (1/n - 1/m)
Eq 7.4: (1/f - 1/n) > (1/d - 1/m)
Eq 7.5: f < beta_c
```

The first compares reimbursement net of displacement with reallocation; the
second rearranges the same terms. Their equivalence is tested directly.

## Source discrepancies and adjudication

- Scenario 3 prose on printed page 115 (PDF page 125) says `n = m`, but the
  same page requires a positive reallocation gain and equation 7.2 uses
  `1/n - 1/m`; printed page 119 (PDF page 129) explicitly requires `m > n`.
  The implementation follows the internally coherent `m > n` interpretation.
  This is an adjudication of an apparent source typo, not silent normalization.
- Printed page 109 (PDF page 119) refers once to expansion funded by
  `Delta E_P`; the surrounding dimensional algebra requires currency
  `Delta C_P`. The implementation uses `Delta C_P`.
- The source Scenario 3 domain also states `n <= d <= m`. The reusable
  opportunity-set kernel intentionally accepts wider domains, but exact
  Chapter 8 Game 1 validation enforces this ordering.

## Implementation policies and extensions

- `max(0, 1/n - 1/m)` treats a non-beneficial reallocation as unavailable in
  the generalized kernel. It is not the strict Scenario 3 domain condition.
- Choosing the most productive named `additional_alternatives` is a repository
  extension; the source equation does not define that maximization.
- The scale-aware floating-point tolerance around `f <= beta_c` is a numerical
  policy. Reimbursement on exact indifference follows Chapter 8, not Chapter
  7's required-adoption setup.
- Linearity, certainty, feasibility, and the institutional meaning of `n`,
  `m`, and `d` cannot be inferred from three numbers. Results are conditional
  on callers establishing those assumptions.

## Currency-unit rescaling

For a positive currency scale `s`, scale `Delta C`, `n`, `m`, and `d` by `s`.
Then `g' = g / s`, `beta_c' = s * beta_c`, and health-valued NEBhR is unchanged.
This guards against mixing dollars, cents, or other currency units.

## Executable evidence

- `tests/test_economics.py` independently exercises the Python identities.
- `crates/new-drug-reimbursement-game/src/lib.rs` independently implements and
  tests the Rust identities.
- The full repository gate runs both implementations, lint, typing, formatting,
  and clean-room scope checks.

## Review disposition

- Source fidelity passes for the implemented Scenario 3 reallocation model,
  including equations 7.2-7.5, `beta_c^alpha`, EVCI, and sign conditions.
- The independent technical panel receipt is recorded in
  `docs/governance/independent-review-panel.md`.
- Scenario 4 `mu`/`beta_c^v` remains excluded; implementing it would require
  the detailed Pekarsky (2012, Appendix 5) formulation and a new review.
- Passing source and implementation checks is not policy, HTA, legal, or
  regulator-grade approval.
