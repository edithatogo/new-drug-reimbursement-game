# Chapter 8 finite reimbursement offers

`chapter8_finite::solve_finite_game1` evaluates a finite menu for the existing
fixed-budget Game 1. The manufacturer chooses an incremental price per health
unit from the menu. The institution observes the offer and accepts or rejects.
The parties share the parameters. Rejection gives both parties zero incremental
payoff. With zero incremental manufacturing cost, acceptance gives the
manufacturer `price × health effect` in currency and the institution the
application's net economic benefit in health (NEBh).

The adapter uses the same input domain as `solve_pekarsky_game1`, including
`n ≤ d ≤ m`, `n < m`, and no additional reallocation strategy. It rejects
an empty menu, duplicate prices and nonpositive or nonfinite valuations where
the source model requires positive finite values. It retains signed NEBh.
The application declares each player's unit and perspective and records the
valuation revision. Paignia's backward induction selects a completed policy.
The provider resolves payoffs within its configured tolerance by action ID.
`accept` sorts before `reject`, so the institution accepts at indifference.
Offer IDs sort by the positive binary64 price, so an all-rejected menu
selects its lowest offer. The application retains the admitted result and
provenance through its [valued-payoff port](payoff-input-contract.md).

## Independent expected result

The [source conformance audit](../research/source-conformance-audit.md) records
Pekarsky (2015), Chapter 8, equation 8.2, printed p. 150, and its assumptions
(DOI `10.1007/978-3-319-08903-4`). For an accepted price `p` and positive
health gain `H`, that fixed-budget model gives
`NEBh = H[1 − p(1/d + 1/n − 1/m)]`. The largest individually rational
price is therefore `1/(1/d + 1/n − 1/m)`. Since firm rent rises with `p`,
the equilibrium selects the highest acceptable price in the finite menu,
subject to the documented numerical tolerance.

The maintained [Chapter 8 example](../../examples/cases/chapter8_example.json)
uses synthetic inputs with `n = 20,000`, `m = 60,000`, `d = 40,000` and
`H = 10`. The reciprocal threshold is `7/120,000`. A menu containing the
threshold gives price `120,000/7`, rent `1,200,000/7` and NEBh zero. With
offers `12,000`, `22,000` and `16,000`, the selected offer is `16,000` with
rent `160,000` and NEBh `2/3`. A menu of prices above the threshold gives
zero rent and zero NEBh through rejection. The test uses absolute tolerances
of `1e-9` for price, `1e-8` for currency payoffs and `1e-12` for health payoffs.
It also requires rejection of invalid menus and a nonzero alternative
reallocation productivity outside Game 1.

The case qualifies the application model on synthetic parameters under the
declared finite perfect-information profile. The closed-form solver remains
available for the continuous threshold. Clinical inputs, private information,
simulation and empirical uptake are outside this case's scope.
