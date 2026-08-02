# Evidence sourcing policy for T13-T16

This policy is mandatory for the restricted-scope tracks. The reusable
execution matrix is in `conductor/triangulation-contingency-protocol.md`.
Agents must actively
acquire eligible public evidence; drafting a request is not completion when an
official public source can be retrieved safely. Acquisition never expands
permission to access restricted, raw, personal, confidential, paid, or
credential-gated material.

## Ranked source hierarchy

1. **Primary authority:** the responsible public body, data custodian, contract
   owner, regulator, standards body, or original signed decision record.
2. **Owner-controlled immutable system:** pinned Atlas, UOGTO, Kairos, Voiage,
   or `edithatogo/*` release/export with maintainer and licence receipts.
3. **Official implementation guidance:** government, NHS, NICE, MHRA, ICO, or
   equivalent jurisdiction-specific manuals, APIs, registers, and archives.
4. **Primary research:** DOI-bound peer-reviewed articles, institutional
   repositories, and appendices used to validate methods rather than grant
   operational authority.
5. **Secondary discovery sources:** indexes, search engines, summaries, and
   mirrors. These may locate evidence but cannot independently close a gate.

Lower-ranked sources never override a conflicting higher-ranked source. A
single primary authority may establish a fact within its remit; otherwise a
material fact requires two independent sources, including at least one from
levels 1-3.

## Programmatic acquisition contract

For each worklist row, the agent must:

1. search official domains, catalogues, APIs, repositories, registers, and
   archives before using general web search;
2. retrieve the exact bytes or immutable API response using a documented URL,
   query, revision, and request timestamp;
3. respect authentication, robots, rate limits, licence terms, and API terms;
4. record HTTP/API status, media type, content length, ETag/Last-Modified when
   present, and SHA-256 of the original bytes;
5. record publisher, title, publication/effective date, page/table/field
   locator, retrieval method, transformations, units, uncertainty, licence,
   permitted destination, and reviewer disposition;
6. store only permitted evidence in Git; keep prohibited bytes outside the
   repository and commit a redacted metadata or negative receipt instead;
7. bind every derived record and decision to the source receipt, exact packet
   revision, repository commit, and transformation/code revision.

Receipts must conform to `conductor/source-receipt-schema.json`. Retrieval logs
must never contain credentials, cookies, tokens, confidential query values, or
restricted payload excerpts.

## Triangulation and conflict rules

- Maintain a source-to-claim matrix and identify duplicate sources that merely
  republish the same underlying record.
- Prefer independent provenance chains; mirrors of the same document count as
  redundancy for availability, not independent corroboration.
- Compare identifiers, dates, jurisdictions, populations, programme scope,
  units, price years, definitions, revisions, and uncertainty.
- Preserve all conflicting receipts. Do not average, merge, or select a value
  silently. Defer promotion until an authoritative resolution is recorded.
- Cross-check every equation, assumption, heuristic, parameter, and
  transformation against its named source and executable validation.

## Options and decisions

Every phase decision must record at least:

- the recommended option and why it best satisfies authority, rights,
  reproducibility, minimization, and intended use;
- viable alternatives and their costs, limitations, and promotion effects;
- a fail-closed fallback, normally synthetic, metadata-only, aggregate-only, or
  no-use;
- the accountable decision owner when the choice changes external scope.

## Negative and deferred receipts

An unsuccessful or prohibited acquisition is evidence. Record the query,
sources attempted, dates, statuses, missing fields, restriction, responsible
gate, retry condition, and safe fallback. `not_found`, `inaccessible`,
`conflicting`, `incomplete`, `restricted`, and `declined` are distinct states.
No negative receipt proves non-existence beyond the documented search scope.

## Autonomous actions and stop conditions

Agents may autonomously search, retrieve, hash, classify, triangulate, and
analyse public, freely accessible evidence; inspect owner-controlled local
repositories; run validation; author receipts; and implement fail-closed code
and synthetic fixtures.

Agents must stop before accepting new terms, authenticating with unavailable
credentials, paying, bypassing access controls, accessing raw personal or
confidential material, transferring restricted bytes, contacting external
people, filing/submitting, publishing, or changing the intended legal or
regulatory use. They must present the exact blocker, options, recommendation,
rationale, and safe contingency.

## Refresh and invalidation

A receipt is invalidated when its bytes, hash, revision, terms, publisher,
schema, transformation, target programme/context, destination, or reviewed
repository commit changes. Re-run acquisition and dependent reviews when an
ETag/Last-Modified value changes, a source is superseded, or the track's
freshness window expires. Refresh at every release or submission freeze even if
the nominal URL is unchanged. Downstream artifacts must name the superseding
receipt; historical receipts remain append-only.

## Additional controls

- Use bounded retry/backoff and cache immutable public bytes by digest.
- Record data classification before storage and processing.
- Maintain lineage from source to transformation to derived record to output.
- Score evidence for authority, completeness, recency, independence, rights,
  and reproducibility; a score never overrides a mandatory gate.
- Require a redaction/leakage check before commits, logs, CI, issues, or release.
- Make source inventories machine-readable and validate receipt hashes in CI.
