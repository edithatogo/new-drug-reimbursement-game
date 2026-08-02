# T15 evidence sourcing playbook

## Ranked sources

1. Data custodian/controller terms, signed permissions, data dictionaries, and access decisions.
2. Official public API/catalogue metadata, schemas, provenance, and licence records.
3. Atlas-controlled ingestion/export contracts and approved derived views.
4. Official legal/privacy/security guidance applicable to the source and jurisdiction.
5. Secondary catalogues for discovery only.

## Autonomous acquisition

- Discover public datasets and APIs, retrieve public metadata, schemas, data
  dictionaries, sample definitions, licence text, terms, update schedules, and
  aggregate documentation.
- Hash and receipt every public metadata artifact; classify proposed fields and
  map them to purpose, minimization, transformation, retention, and destination.
- Test ingestion with synthetic or explicitly public non-sensitive fixtures and
  validate that only permitted derived records cross the Atlas boundary.
- Do not retrieve raw payloads merely because an endpoint is technically reachable.

## Options

1. **Recommended — metadata-first, Atlas-derived-only pipeline.** Minimizes exposure and preserves provenance ownership.
2. **Controlled raw ingestion.** Only after custodian, legal/privacy, security,
   storage, operator, retention, and extraction gates pass.
3. **Aggregate/public-data-only.** Use when individual/raw access is unnecessary or unavailable.
4. **No-use fallback.** Record a negative receipt and retain synthetic validation.

## Contingencies and stops

- Inaccessible metadata: use the official catalogue/archive and record failure.
- Conflicting dictionaries/terms: bind to the custodian's effective version and defer unresolved fields.
- Incomplete documentation: do not infer field meaning or lawful purpose.
- Restricted source: stop before authentication, application acceptance,
  download, transfer, or storage; request the required authority as one grouped decision.

## Refresh

Refresh metadata and terms before access, at every ingestion/release freeze, and
when the dataset version, schema, controller, purpose, lawful basis, storage,
operator, transformation, destination, retention, or repository commit changes.
