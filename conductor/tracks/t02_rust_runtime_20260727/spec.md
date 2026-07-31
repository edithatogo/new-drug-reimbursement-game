# Specification

## Overview

Develop the domain-neutral Rust extraction seed into a validated, reproducible
finite-game runtime aligned with pinned UOGTO semantics and designed to compile
execution plans to Kairos without duplicating scheduling or random streams.

## Authoritative inputs

- `CODEX_IMPLEMENTATION_PROMPT.md`, Workstream 2.
- `docs/architecture/capability-boundary.md` and
  `docs/architecture/rust-game-runtime.md`.
- UOGTO pin `849386068399a764ad5304cc8a0ffe53094b091c`.
- Kairos pin `fae901558f07b7b717a676adbafbe2cdc78dea1c`.

## Requirements

- Provide canonical non-empty identifiers and versioned game specifications.
- Validate players, actions, nodes, transitions, chance mass, finite payoffs,
  reachability, information structures, and supported execution semantics with
  machine-readable paths.
- Implement deterministic backward induction, explicit tie policy, expected
  chance payoffs, diagnostics, and reproducible traces.
- Add pure-strategy normal-form best-response and Nash enumeration before mixed
  or repeated-game algorithms.
- Keep all reimbursement, drug, QALY, HTA, payer, and manufacturer vocabulary
  outside domain-neutral crates.
- Define Kairos compilation contracts only from the pinned released API.

## Acceptance criteria

- Rust formatting, Clippy, tests, vocabulary boundary, and conformance fixtures pass.
- Unsupported semantics fail explicitly rather than being silently approximated.
- Extraction does not require moving application-domain files.
- Kairos and UOGTO integration points cite their pinned revisions.

## External gates

- Upstream UOGTO ontology review.
- Released Kairos contract compatibility and extraction-repository approval.

## Out of scope

- A second scheduler, RNG, DES, or ABM implementation.
- Application-domain reimbursement semantics.
