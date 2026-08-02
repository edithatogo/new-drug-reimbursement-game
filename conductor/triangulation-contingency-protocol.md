# Evidence triangulation and contingency protocol

This protocol is the reusable Conductor execution contract for T13--T16 and
any future governed evidence track. It supplements
`evidence-sourcing-policy.md` and `evidence-acquisition-programme.md`; those
documents remain authoritative where wording differs.

## Orchestrator sequence

For each worklist field or claim, the orchestrator must create a bounded row
with an owner, intended use, freshness window, and stop condition. It then:

1. queries the ranked authority hierarchy (official API/release, official
   archive/publication scheme, accountable committee/procurement record,
   bounded public-record request, then a negative/deferred receipt);
2. records one immutable receipt per acquisition attempt, including URL/query,
   revision, retrieval time, status, media type, byte length, SHA-256, locator,
   rights, transformations, and disposition;
3. groups receipts by the underlying accountable record, not by URL, and marks
   mirrors as availability redundancy rather than independent corroboration;
4. compares programme/decision identity, dates, population, intervention,
   comparator, units, price year, definitions, and uncertainty;
5. emits a field-level outcome and preserves every supporting, negative, or
   conflicting receipt before proceeding to the next row.

The orchestrator may delegate acquisition, provenance, methods, and
reproducibility checks to separate subagents. A consensus receipt must list
the exact target commit/packet digest, role receipts, disagreements, and
quorum. A panel recommendation never substitutes for an accountable owner,
custodian, licensing, or release authorization.

## Decision matrix and contingencies

| Outcome | Autonomous action | Safe disposition | Retry trigger |
| --- | --- | --- | --- |
| Two independent authoritative records agree | Hash and cross-reference both; select the higher-ranked canonical record | `candidate_for_promotion` pending owner gate | Any source revision or context change |
| One accountable owner record only | Preserve the receipt and missing-corroborator reason | `single_source_authority`; promotion only with explicit owner acceptance | New independent record or owner acceptance |
| Conflicting values, identity, or dates | Preserve all receipts and exact differences; never average or silently select | `deferred_conflict`; synthetic/metadata-only fallback | Authoritative resolution or superseding revision |
| Incomplete, redacted, or not-held | Mark each missing field and constrain unaffected roles | `not_identifiable`; do not infer zero or substitute a proxy | Complete attributable record |
| Inaccessible, mutable, or rate-limited | Retry boundedly via official API/archive and capture each attempt; reject unhashable bytes | `deferred_inaccessible` unless a stable official mirror is verified | Endpoint recovery or stable mirror |
| Restricted, paid, confidential, or unclear terms | Retain metadata only; do not authenticate, transfer, or store payload | `restricted_pending_terms`; synthetic/public-only fallback | Named permission, terms adjudication, and destination approval |
| No evidence after documented ladder | Seal the negative search receipt with scope and dates | `not_found`; retain research-only operation | New publication, archive, or owner response |

## Options and recommendation

The recommended route is **same-programme owner packet plus independent
official context**, because it maximizes authority, reproducibility, rights, and
field completeness. A **hybrid** (official context plus approved-derived
parameters) is acceptable when the owner explicitly accepts residual gaps.
**Public reconstruction** is research-only and cannot establish confidential
prices, displacement, or missing uncertainty. **Synthetic fallback** is always
available for conformance and demonstration, but disables empirical, payer,
HTA, regulatory, and calibrated claims.

For inaccessible, conflicting, or restricted evidence, the orchestrator must
choose the matrix disposition rather than inventing a value. Genuine stop
conditions are credentials, new terms, confidential/raw data, external
submission/contact, intended-use change, and accountable promotion approval.

## Refresh and invalidation

Invalidate dependent receipts, panel reviews, and derived outputs when source
bytes/hash, publisher, revision, terms, programme/decision context, units,
transformations, uncertainty, code/model, destination, audience, or reviewed
commit changes. Retain historical receipts append-only, reacquire the affected
row, rerun the panel, and bind the new consensus and approvals to the final
commit before promotion or release.
