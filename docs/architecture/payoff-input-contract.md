# Valued payoffs at the Paignia boundary

`payoff_input::solve_valued_game` takes a versioned finite static game
specification, its result identities, the application's exact payoff unit
and perspective for each player, and the valued payoffs for every terminal.
The graph declares empty payoff maps.
Each terminal valuation carries a signed finite amount, the unit and
perspective, and the revision of the valuation input.

The application binds units and perspectives to its selected case before
solving. For example, a firm's payoff can be measured in a named currency
and price year while the funding institution's payoff is measured in net
health units. Values match the declared basis exactly. A case with explicit
zero payoff records the zero and its provenance.

The port rejects missing or undeclared players, nonterminal valuation targets,
raw embedded payoffs, incompatible bases, non-finite amounts and blank
valuation revisions. It calls Paignia's `backward_induction_result` at the qualified
`bd880dd` revision using the static perfect-information profile. The result
retains the provider's versioned envelope and the original valuations. The valuation
revision is the caller's reference to its evidence and assumptions. The
application remains responsible for resolving that reference.

The finite offer example exercises this path with the existing application
health-benefit calculation and a synthetic valuation revision. Its analytical
oracle checks the threshold offer and both players' payoffs. The native
contract fixture uses distinct revision references to check per-payoff
provenance. The real-model
artifact receipt and the Voiage metric and identity contracts retain their
own acceptance criteria.

```sh
cargo test --locked -p new-drug-reimbursement-game --test payoff_input_contract --test paignia_static_game
```
