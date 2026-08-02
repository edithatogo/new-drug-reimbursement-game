# Evidence acquisition programme

This programme coordinates the remaining evidence work across T13–T16. It is
dependency ordered and fail closed: public discovery is autonomous, but access
to restricted values, acceptance of terms, external submission, and promotion
remain explicit authorization boundaries.

## Dependency sequence

1. Reconcile the Conductor registry, gate register, and immutable-source state.
2. Acquire one attributable NHS TA1121 decision/displacement packet.
3. Build an approved-derived Atlas packet at an immutable revision for the same
   programme and price-year context.
4. Freeze the repository commit, packet hashes, parameter mapping, conversions,
   and uncertainty representation.
5. Run equation/unit/provenance validation and the four-role subagent panel.
6. Obtain packet-specific health-economist approval and constrain any output to
   its authorized audience.
7. Expand into regulatory, raw-data, or confidential-data workflows only when
   a named purpose requires them and every applicable authorization exists.

## Authoritative-source hierarchy

1. Signed or attributable NHS commissioner/custodian decision records and
   Atlas owner-approved immutable derived exports.
2. Immutable owner-controlled releases and exact-revision contract artifacts.
3. Official NICE, DHSC, NHS, MHRA, ICO, NCSC, ONS, legislation, catalogue, and
   API material.
4. Official committee, formulary, procurement, finance, and archive records.
5. DOI-bound primary research for method triangulation only.
6. Secondary sources for discovery only; never for promotion.

## Machine acquisition contract

For every eligible public source, record the requested and final URI, publisher,
title, retrieval time, HTTP status, MIME type, content length, ETag,
Last-Modified value, SHA-256, authority rank, field/claim locators, rights,
disposition, contingency, and refresh trigger. Store only receipts unless the
source and destination terms expressly permit payload retention.

Public acquisition must actively query official sites, APIs, release manifests,
archives, committee indexes, and public catalogues. A search-result snippet is
a lead, not evidence. Every material claim needs either two independent official
sources or an explicit authority-specific label.

## Triangulation and fallback decision rules

The orchestrator applies these rules field-by-field; a packet is not promoted
because its aggregate score is high:

| Evidence state | Required action | Permitted disposition |
| --- | --- | --- |
| Two independent authoritative records agree on value, role, units, and date | Preserve both receipts and the cross-check table; prefer the higher-ranked owner record for the canonical value | Candidate for promotion after owner approval |
| One accountable owner record exists and no independent corroborator is published | Preserve the owner receipt, label the field `single_source_authority`, and record the missing corroborator | Promotion only when the accountable owner explicitly accepts the residual risk |
| Sources disagree on value, programme identity, or date | Preserve each immutable receipt and the exact disagreement; never average or silently choose | `deferred_conflict` until owner disposition |
| A source is incomplete, redacted, or not-held | Record field-level absence and the search/response receipt; use only unaffected fields | `not_identifiable` for the affected role; synthetic fallback remains enabled |
| Source is inaccessible, rate-limited, or mutable | Retry through the publisher API/archive and capture attempts; reject unhashable bytes | `deferred_inaccessible` unless a stable official mirror is verified |
| Terms or provenance are unclear | Retain metadata only and stop redistribution/derived promotion | `restricted_pending_terms` |

Independence means a distinct accountable publisher and acquisition path, not
two URLs that mirror the same PDF. Corroborators must be compared on the exact
programme/decision ID, intervention and comparator, price year, service line,
and unit basis. A contextual source may corroborate identity or timing but
cannot corroborate a confidential price, displacement value, or Atlas-derived
parameter. Negative receipts are first-class outputs and must include the
queries, date range, endpoints searched, HTTP outcomes, and the next fallback;
they must never be converted into an inferred zero.

### Contingency ladder

For each unresolved role, execute in order: (1) official API or release
manifest; (2) official archive/publication-scheme mirror; (3) accountable
committee, formulary, procurement, or finance record; (4) a bounded public-record
request to the accountable custodian; (5) explicit negative/deferred receipt.
The orchestrator may execute steps 1–3 autonomously and prepare step 4, but
submission, credentials, confidential access, source-term acceptance, and
promotion remain human/external stop conditions. If a later source supersedes
an earlier one, retain both receipts, mark the earlier receipt invalidated, and
recompute every dependent hash and panel receipt.

## NHS packet worklist

The minimum packet identifies payer/commissioner, budget boundary, service line,
provider, decision date, price year, intervention, comparator, displaced
programme, stable programme/decision ID, baseline cost and unit, horizon, and an
accountable owner confirming the displacement role. Search NHS England,
South Yorkshire ICB, committee-paper repositories, publication schemes,
formularies, procurement/finance records, Royal Free NAC, and the Midlands
Amyloidosis Service. Provider records are routing evidence unless they own the
decision.

If no public record supplies the fields, preserve the search receipts and route
one bounded public-record/FOI request to the accountable body. Do not request
patient-level data or confidential net prices. A not-held, refused, or redacted
response is a valid negative receipt.

## Atlas packet worklist

Poll immutable Atlas releases and approved-derived exports. Require packet ID,
exact commit/tag, byte hash, creation date, NHS context, Chapter 7 roles `n`,
`m`, `d`, `mu`, `phi`, annual programme effect and horizon, units, price-year
conversion, transformations, marginal/joint uncertainty, source hashes, rights,
and owner disposition. Reject terminology-only, foreign-schedule, mutable,
cross-programme, incomplete, or unapproved material.

## Calibration and panel worklist

Freeze the exact source and repository revisions before validation. Test role
alignment, units, price year, discounting, uncertainty/covariance, Scenario 4
programme identity, stale-receipt rejection, and promotion authorization.
Cross-reference every equation, assumption, heuristic, and parameter against
the source book and authoritative methods.

The review panel has four roles: economics/equations, NHS
context/displacement, Atlas provenance/licensing, and runtime/reproducibility.
Each receipt records the exact packet and commit, conflicts, checks, findings,
limitations, and disposition; the orchestrator records receipt hashes, quorum,
disagreements, and consensus. Panel review informs but does not replace an
accountable owner authorization.

## Optional downstream evidence

- **T14:** sponsor, intended purpose, jurisdiction, submission route,
  classification, claims matrix, validation plan, and exact-candidate
  authorization. Without these, remain a research-to-regulatory gap assessment.
- **T15:** exact raw source/fields, custodian permission, lawful basis, terms,
  controlled environment, operators, retention/deletion, transformations, and
  destination. Prefer Atlas-derived-only or public aggregate data.
- **T16:** confidential owner, contract/NDA, field schedule, purpose, operators,
  environment, disclosure rules, destination, output authorization, and deletion
  receipt. Prefer aggregate/redacted outputs; missing authority means no use.

## Contingencies

- Inaccessible: try the official API/archive and record the failure.
- Conflicting: preserve all sources, apply the stricter rule, and defer the
  affected field for owner disposition.
- Incomplete: enable only complete scenario-role sets; otherwise return
  `not_identifiable`.
- Restricted: record metadata only and stop before authentication, acceptance,
  transfer, or storage.
- Unclear rights: keep derived output private and prohibit redistribution.
- No evidence: retain synthetic/methodology-only operation and a negative receipt.

## Refresh and invalidation

Invalidate dependent receipts when the programme, decision date, price year,
Atlas revision, source bytes or terms, transformations, units, uncertainty,
code/model, sponsor, purpose, operator, environment, audience, destination, or
repository commit changes. Reacquire sources, rerun the panel, and bind all
approvals to the final commit before promotion or release.
