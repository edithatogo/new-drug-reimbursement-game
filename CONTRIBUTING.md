# Contributing

Open or link a capability issue in the authoritative ecosystem repository before
adding shared functionality here. Application changes require source notes,
assumption declarations, tests, and model-risk updates. General game changes
must remain domain-neutral and include UOGTO conformance fixtures.

## Maintainer workflow

This is a solo-maintainer repository. Automated CI is the required review gate;
an additional human approval or team review is not required. Keep pull requests
small, explain the evidence and model assumptions, and do not commit private
reimbursement data or credentials. Before requesting review, run:

```bash
python scripts/run_quality_gate.py
```

Dependency updates are managed by Renovate. Do not add Dependabot configuration
or silently broaden the pinned ecosystem scope.

## Game capability intake

UOGTO owns game-theoretic semantics and Paignia owns reusable game
representations and solvers. Every newly identified, added or materially changed
game must have linked records under both upstream contracts:

- [UOGTO semantic coverage and extension intake](https://github.com/edithatogo/UOGTO/blob/main/docs/contracts/downstream-game-intake.md).
- [Paignia generic capability and fixture intake](https://github.com/edithatogo/paignia/blob/main/docs/integrations/downstream-game-intake.md).

Use the same intake key in both records and link them from the local plan or
pull request. Identify the originating source path and immutable revision,
players, actions, information, timing, payoff meaning and requested solution.
Record the semantic and implementation dispositions separately:

| Upstream | Allowed dispositions |
| --- | --- |
| UOGTO | `reuse_existing`, `extension_required`, `unsupported`, `mapping_review_pending` |
| Paignia | `reuse_existing`, `extension_required`, `unsupported`, `domain_only`, `assessment_pending` |

For `reuse_existing`, add or refine the UOGTO mapping/example with full term
IRIs and link the supported Paignia API/profile, its limits and fixture evidence.
For `extension_required`, link the upstream proposal, a minimal synthetic example
and independently expected results. `unsupported` records the missing requirement
and its effect on claims or execution. Paignia's `domain_only` records why the
change needs no generic implementation. Pending assessments need a reason,
owner and next action; they do not establish semantic or executable support.

Inspect existing upstream work before proposing another term, solver or fixture.
An unchanged game with new parameters can reuse its intake key and add an
application example. Data, assumptions, payoff construction and calibration
remain here; Paignia receives only reusable representations, algorithms and
conformance fixtures. Preserve source revision, licence and attribution for
any transferred example or implementation.

On adoption, record the exact UOGTO revision/profile and full IRIs, Paignia
revision or artifact hash, fixture identity, and focused semantic/native/consumer
checks actually run, including independent expected results and invalid or
unsupported cases. Ontology conformance and numerical verification are separate.
A record or dependency pin alone does not complete a migration.

Existing local or pedagogical implementations may remain while migration is
assessed, with their scope and limitations labelled. New game changes still
require intake. This policy does not replace algorithms, change model assumptions
or promote heuristic outputs to verified equilibria.
