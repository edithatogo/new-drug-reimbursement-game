# Release-readiness evidence register

This register separates repository validation from approvals that must be
supplied by an independent reviewer or an upstream component owner. Empty
entries are intentionally open; no approval is inferred from a passing test.

| Gate | Required evidence | Current state | Owner/action |
|---|---|---|---|
| Chapter 7 interpretation | Exact source location, dimensional derivation, and independent economics review | Pending | Obtain reviewer statement and attach it to T01 |
| UOGTO ontology | Validation against the pinned UOGTO revision and upstream disposition | Pending | Request upstream ontology review |
| Kairos execution | Pinned API compatibility and upstream execution/trace review | Pending | Request Kairos owner review |
| Extraction boundary | Approval that the game runtime can be extracted without application leakage | Pending | Record extraction reviewer and evidence |
| Licences and provenance | Licence reconciliation for every dependency and derived artifact | Pending | Complete licence/source adjudication |
| Release | Maintainer release decision after all preceding gates close | Pending | Maintainer decision |

## Evidence acceptance

Each gate closes only with an artifact path, reviewer or owner identity,
revision/hash, date, and an explicit disposition. CI output proves automated
validation only; it does not close independent review, legal, provenance, or
upstream-approval gates.
