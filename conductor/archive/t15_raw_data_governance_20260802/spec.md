# T15 raw-data acquisition and governance

## Overview

Establish a segregated, least-privilege governance path for raw source data.
Raw data remains prohibited from this repository and its public release surface.

## Requirements

1. Define source, controller, lawful/contractual basis, purpose, minimization,
   retention, location, access roles, and permitted transformations before access.
2. Keep raw bytes outside the Git repository in an approved controlled environment.
3. Produce only provenance-preserving, licence-compliant derived records for Atlas.
4. Maintain deletion, incident, audit, and data-subject/privacy procedures where applicable.
5. Prevent raw payloads, credentials, identifiers, and restricted descriptors from
   entering commits, logs, fixtures, packages, or public artifacts.
6. Follow `sourcing.md` and the shared evidence-sourcing policy: agents must
   autonomously acquire public metadata, schemas, dictionaries, licences, and
   control evidence, while stopping before raw access until every applicable
   custodian, legal/privacy, security, storage, and operator gate passes.

## Acceptance criteria

- Data inventory, classification, DPIA/privacy assessment where required, source
  terms, access controls, retention, and deletion evidence are approved.
- A controlled ingestion pipeline produces hash-bound derived records without
  exporting prohibited fields.
- Secret, privacy, restricted-data, and repository-boundary tests pass.
- No raw data is committed to this repository.

## External gates

- Data-controller/custodian permission and exact source terms.
- Legal/privacy basis and security approval.
- Approved controlled storage and named operators.
- Atlas extraction and derived-publication authorization.

## Non-functional constraints

- Data minimization, encryption, least privilege, auditable access, and fail-closed export.

## Out of scope

- Public raw-data publication, patient-level data in Git, or bypassing Atlas provenance ownership.

## Authoritative inputs

- `docs/architecture/evidence-calibration-contract.md`
- `docs/governance/extraction-review.md`
- `docs/governance/research-only-extraction-owner-authorization-2026-08-01.md`
- `docs/governance/release-packet/security-privacy-scope-receipt-2026-08-02.json`
- `conductor/evidence-sourcing-policy.md`
- `conductor/source-receipt-schema.json`
- `conductor/tracks/t15_raw_data_governance_20260802/sourcing.md`
