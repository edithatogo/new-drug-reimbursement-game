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
