# Dimensional derivation and assumption ledger

Status: independently derived implementation note; external health-economics
review pending.

Primary conceptual source: Pekarsky (2015), Chapters 6-8, especially Chapter 7
equations 7.2-7.5 and the Chapter 8 Game 1 solution. DOI
`10.1007/978-3-319-08903-4`.

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

The exact mapping of any source technical-efficiency parameter to `g*` remains
unresolved. Code must use a named `AlternativeStrategy` with units and
provenance instead of silently assigning a formula to that parameter.

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

## Pending review gates

- Verify the exact Chapter 7 technical-efficiency formulation against an
  authorized source and record the precise location.
- Obtain independent dimensional and economic review.
- Do not treat passing tests as policy, HTA, or regulator-grade validation.
