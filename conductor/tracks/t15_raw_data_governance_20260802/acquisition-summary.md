# T15 autonomous metadata acquisition summary — 2026-08-02

The metadata-first acquisition pass retrieved and hashed NHS England gateway
terms, NHSBSA prescription-data catalogue metadata, ICO data-protection
principles, the pinned Atlas source-licence ledger and evidence schema, and the
public Hugging Face dataset metadata. No dataset payload was downloaded.

The recommended route remains Atlas-derived-only. NHS gateway content is OGL
3.0, but linked datasets need exact terms. Atlas source records retain
source-specific restrictions. The Hugging Face dataset is public and ungated
but declares `license:other`, so automated payload consumption remains deferred.

The safe fallback is public metadata, aggregate documentation, synthetic
fixtures, and negative receipts. Raw access requires the named custodian,
legal/privacy basis, controlled environment, operator, retention, and extraction
authorizations.
