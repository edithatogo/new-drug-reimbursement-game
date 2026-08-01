# Specification

## Overview

Make repository builds, dependency boundaries, provenance, and extraction
readiness mechanically reviewable while keeping release, legal, security, and
domain approvals as explicit external gates.

## Authoritative inputs

- `CODEX_IMPLEMENTATION_PROMPT.md`, Workstream 9.
- `ecosystem.lock.toml`, `docs/governance/model-risk.md`, and
  `docs/architecture/capability-boundary.md`.
- GitHub issue `#11`.

## Requirements

- Generate deterministic dependency and provenance inventories without
  resolving unpinned network content.
- Check declared licences and retain unresolved licence decisions as blocking
  findings rather than assumptions.
- Exercise install/build/test flows from a clean temporary environment.
- Enforce the Rust extraction vocabulary and dependency boundary.
- Document stable schema and release expectations.
- Preserve separate evidence for local validation, hosted CI, external review,
  and release authorization.

## Acceptance criteria

- The full Python, Rust, lint, type, scope, and Conductor gates pass.
- Generated governance artifacts are reproducible and checked for drift.
- No release or policy-readiness claim is made without external evidence.
- The domain-neutral crates can be packaged without application files.

## External gates

- Independent health-economics, ontology, security, legal, and
  reproducibility review.
- Voiage and Hugging Face licence reconciliation.
- Extraction repository and release authorization.
