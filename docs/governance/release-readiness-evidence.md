# Release-readiness evidence register

This register separates repository validation from approvals that must be
supplied by an independent reviewer or an upstream component owner. Empty
entries are intentionally open; no approval is inferred from a passing test.

| Gate | Required evidence | Current state | Owner/action |
|---|---|---|---|
| Chapter 7 interpretation | Exact source location, dimensional derivation, and independent economics review | Source and executable conformance cover Scenarios 1–4; human health-economics review remains external | Preserve both source hashes/pages and empirical-parameter boundary |
| UOGTO ontology | Validation against the pinned UOGTO revision and upstream disposition | Owner approval recorded; upstream disposition pending | Run pinned SHACL validation when toolchain is available |
| Kairos execution | Pinned API compatibility and upstream execution/trace review | Owner approval recorded; native released integration pending | Adopt released DTO/code contract |
| Extraction boundary | Approval that the game runtime can be extracted without application leakage | Local checks and panel review pass; transfer approval pending | Record extraction owner authorization |
| Licences and provenance | Licence reconciliation for every dependency and derived artifact | Inventory packet complete; Voiage conflict is precisely recorded and adjudication remains pending | Resolve Voiage and source-specific terms; see `docs/governance/voiage-licence-adjudication.md` |
| Release | Maintainer release decision after all preceding gates close | Pending | Maintainer decision |

## Evidence acceptance

Each gate closes only with an artifact path, reviewer or owner identity,
revision/hash, date, and an explicit disposition. CI output proves automated
validation only; it does not close independent review, legal, provenance, or
upstream-approval gates.
