# Pekarsky foundation and clean-room implementation map

Source: B. A. K. Pekarsky, *The New Drug Reimbursement Game* (2015), Springer,
DOI 10.1007/978-3-319-08903-4.

## Concepts implemented

| Book concept | Source location | Implementation |
|---|---|---|
| Reimbursement comprises adoption and financing | Chapter 6, Table 6.1 | `ReimbursementInputs`, `evaluate_reimbursement` |
| IPER distinguishes negotiable price from an exogenous cost | Chapters 6–8 | `incremental_price_effectiveness_ratio` |
| Health shadow price `beta_c` | Chapters 6–7 | `health_shadow_price` |
| Expansion `n`, contraction `m`, displacement `d` | Chapters 7 and glossary | `OpportunitySet` |
| Net economic benefit in health units | Chapter 7, equations 7.2–7.5 | `evaluate_reimbursement` |
| Economic value of clinical innovation | Chapter 6 | `economic_value_clinical_innovation` result |
| Firm chooses the highest reimbursable price under the exact Game 1 assumptions | Chapter 8, equation 8.2, printed p. 150/PDF p. 160 | `solve_pekarsky_game1` |
| Public-threshold game with other contexts or non-zero IMER | Repository extension, not equation 8.2 | `solve_revealed_threshold_game` |
| R&D financing game | Chapter 9 | specification backlog; not claimed complete |
| Three-period premium game | Chapter 10 | specification backlog; not claimed complete |

## Generalized formulation

For fixed-budget reimbursement, let:

- `1/d` be health lost per currency unit through the actual displacement;
- `g*` be health gained per currency unit by the best alternative strategy.

The health shadow price is the IPER making reimbursement and the best
alternative equal:

```text
1 / beta_c = 1 / d + g*
```

When the only alternative is reallocation from programme `m` to programme `n`,
`g* = 1/n - 1/m`, reproducing the Chapter 7 expression. Technical-efficiency,
equity, implementation, contract, or future-health strategies can be included
as explicitly defined alternatives rather than smuggled into an ambiguous
symbol.

## Copyright boundary

No source pages, figures, tables, or substantial prose are included. Notation
and equations are attributed. Examples and test values are synthetic.

The independent dimensional derivation, executable evidence, and pending review
gates are recorded in
[`dimensional-derivation-ledger.md`](./dimensional-derivation-ledger.md).
The exhaustive equation, parameter, assumption, and heuristic disposition is in
[`source-conformance-audit.md`](./source-conformance-audit.md).
