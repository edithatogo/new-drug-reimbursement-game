# Kairos game-execution adapter proposal

The general game runtime—not the reimbursement application—should compile game
transitions to Kairos events.

Minimum event vocabulary:

- `game.session.started`
- `game.action.selected`
- `game.chance.realized`
- `game.state.transitioned`
- `game.payoff.assigned`
- `game.session.completed`

Every event carries UOGTO identifiers, deterministic sequence/time, game and
session revisions, and a trace correlation ID. Kairos remains unaware of
reimbursement semantics.
