# Maximal public-data acquisition plan

## Objective

Discover and inventory every publicly accessible source that can inform the
TA1121/acoramidis reimbursement context, regardless of whether reuse rights are
already clear. Public accessibility authorizes discovery and metadata capture;
it does not by itself authorize payload retention, redistribution, calibration,
or claim promotion.

## Source hierarchy

1. **Primary decision authorities:** NICE TA1121 guidance, committee materials,
   resource-impact documents, NHS England commissioning/payment publications,
   ICB and trust decision records, formularies, traffic-light decisions, and
   publication-scheme or FOI disclosure records.
2. **Primary administrative aggregates:** NHSBSA finalised/provisional SCMD,
   PCA, dm+d/SNOMED resources, ODS organisation identifiers, NHS England open
   data and statistical collections, OpenPrescribing-derived public aggregates.
3. **Primary regulatory and clinical records:** MHRA, EMA, ClinicalTrials.gov,
   ISRCTN, EU CTIS where public, trial registries, product characteristics,
   safety communications, and regulatory assessment reports.
4. **Primary commercial/public records:** manufacturer public price notices,
   annual reports, investor disclosures, Contracts Finder, Find a Tender,
   procurement notices, public framework agreements, and public commercial
   framework documents. Confidential rebates must never be inferred.
5. **Scholarly and grey literature:** PubMed, Europe PMC, Crossref, DOI landing
   pages, institutional repositories, preprints, health-economic publications,
   conference abstracts, charity/patient-group reports, and university outputs.
6. **Archives and redundancy:** UK Government Web Archive, National Archives,
   official site mirrors, cached publication indexes, replacement URLs, and
   independently published official local records. Search snippets are leads,
   not evidence.

## Programmatic acquisition routes

For each source family, agents must first enumerate official records through
documented APIs, feeds, sitemaps, or bounded site search:

- NICE guidance pages, downloadable resources, and published document metadata.
- NHSBSA CKAN `package_search`, `package_show`, datastore APIs, and streamed CSV
  downloads for SCMD/PCA.
- NHS organisation sites through sitemaps, document-library indexes,
  publication-scheme pages, committee minutes, and formulary search.
- ODS/dm+d/SNOMED identifiers to resolve medicines, organisations, and stable
  programme/service identifiers where publicly available.
- PubMed/Europe PMC/Crossref APIs and registry APIs using TA1121, acoramidis,
  tafamidis, ATTR-CM, amyloidosis, reimbursement, displacement, budget impact,
  implementation, and commissioning synonyms.
- Contracts Finder and Find a Tender APIs/search exports for attributable public
  procurement records.
- UK Government Web Archive/National Archives discovery for removed official
  records, retaining archive provenance separately from the original publisher.

Every request must use bounded timeouts, redirects, retries, byte limits, and a
stable user agent. Prefer metadata-only requests before payload acquisition.

## Receipt requirements

Create one immutable receipt per attempted source containing:

- canonical source ID, publisher, authority rank, requested/final URL;
- query terms or API parameters and retrieval timestamp;
- HTTP status, MIME type, ETag/Last-Modified when available, byte length, and
  SHA-256 for directly retrieved bytes;
- source revision/effective date and stable identifiers;
- exact factual fields supported and unsupported;
- licence/terms URL, terms status, payload-retention decision, permitted use,
  destination, and required attribution;
- transformation manifest, uncertainty/missingness status, and downstream
  artifacts that depend on the receipt;
- negative/deferred reason and retry condition when unavailable, incomplete,
  conflicting, superseded, restricted, or unhashable.

Do not commit raw payloads. Stream and hash them where lawful and technically
possible; retain only receipts and approved-derived fields.

## Rights separation

Classify each record independently:

- `reuse_confirmed`: terms permit the intended derived/contextual use;
- `citation_only`: public access supports citation and metadata, but payload or
  derived reuse is not confirmed;
- `terms_ambiguous`: inventory only; require adjudication before use;
- `restricted`: record metadata and stop before payload acquisition;
- `prohibited`: record a negative receipt and exclude the source.

No source may advance calibration merely because it is public, downloadable,
indexed by a search engine, or accessible through an archive.

## Triangulation and redundancy

- Require at least one national primary authority and one independent official
  local or administrative source for implementation-context claims.
- Require two independently published authoritative records for any field used
  beyond descriptive context.
- Treat mirrors, search snippets, copied tables, press summaries, and derived
  aggregators as leads unless their upstream primary record is verified.
- Prefer finalised over provisional administrative data; retain both when their
  divergence is analytically material.
- Record contradictions explicitly and defer the affected field rather than
  averaging, selecting silently, or imputing.
- Never use redundant contextual evidence to infer causal displacement,
  confidential price, baseline cost, or a missing programme identifier.

## Work packages

### WP1 — authority and committee corpus

Harvest NICE, NHS England, ICB, trust, specialist-centre, formulary, committee,
publication-scheme, and FOI disclosure records. Resolve removed documents using
official archive routes and hash all retrievable bytes.

### WP2 — secondary-care and prescribing aggregates

Enumerate finalised and provisional NHSBSA SCMD resources, resolve dm+d/SNOMED
identifiers, stream-filter relevant products without retaining payloads, and
compare SCMD coverage with PCA/OpenPrescribing. Record absence only as dataset
coverage, never clinical absence.

### WP3 — organisations and stable identifiers

Use ODS and public commissioning/service specifications to identify NHS England,
ICBs, trusts, specialist providers, programme categories, and stable public IDs.
Do not transform an organisation or budget-category identifier into a displaced
programme ID without an attributable decision record.

### WP4 — regulatory, clinical, and commercial context

Harvest regulatory decisions, public trial records, product documentation,
public list-price information, commercial-framework documents, procurement
notices, and public company disclosures. Keep net prices and rebates unknown
unless explicitly public and attributable.

### WP5 — literature and methods corpus

Harvest bibliographic metadata and openly accessible full text where terms allow.
Extract only source-mapped methods, assumptions, parameter definitions, and
uncertainty approaches. Do not copy substantial copyrighted text or figures.

### WP6 — rights adjudication and approved-derived projection

For every discovered source, record terms status and generate an approved-derived
projection only for permitted fields. Citation-only, ambiguous, restricted, and
prohibited sources remain in the discovery ledger but outside model inputs.

### WP7 — packet assembly and requalification

Build a candidate Atlas-compatible packet from approved-derived records; bind
source revisions, hashes, transformations, uncertainty, terms, destination, and
target commit. Re-run panel review, stale-source invalidation, T13 qualification,
and hosted CI. Keep empirical/calibrated promotion disabled unless the full Atlas
and NHS evidence contracts pass.

## Refresh and invalidation

- Refresh volatile indexes and provisional datasets monthly; refresh finalised
  datasets and decision documents when publisher metadata changes.
- Reacquire whenever URL, redirect, ETag, Last-Modified, byte hash, source
  revision, terms, transformation, packet digest, destination, or repository
  commit changes.
- Any material change invalidates downstream freeze, panel receipts, readiness,
  approval, and release bindings.
- Preserve superseded receipts; never rewrite prior evidence history.

## Autonomous actions

Agents may search, enumerate, retrieve public metadata, stream/hash lawful public
bytes, create receipts, resolve identifiers, triangulate context, generate
negative/deferred receipts, and run validation.

## Genuine stop conditions

Stop before credentials, paywalls, CAPTCHA circumvention, restricted payloads,
personal/confidential data, ambiguous reuse that affects retained/derived data,
external submissions, or any promotion to empirical/calibrated/payer/HTA/policy/
regulatory claims. These require the applicable owner, custodian, legal, or
release authorization.

## Completion criteria

- Every source family has an enumeration receipt and bounded acquisition result.
- Every attempted record has a hash receipt or explicit negative/deferred receipt.
- Rights classifications and attribution requirements are complete.
- Field coverage identifies supported, conflicting, missing, and prohibited data.
- Triangulation receipts distinguish context from causal/empirical evidence.
- Stale-source tests and packet requalification pass.
- Full local and hosted CI are green.
- Restricted claims remain disabled unless separately authorized.
