# Implementation status

## Complete in this handoff

- Ecosystem-first architecture and pin file.
- Clean-room PEA kernel with source notes and invariant tests.
- Explicit opportunity-set abstraction for alternative strategies.
- Analytic revealed-threshold reimbursement equilibrium.
- Domain-neutral Rust extensive-form types, validation, and backward induction.
- Python conformance oracle implementing the same finite perfect-information
  contract.
- UOGTO reimbursement extension proposal, JSON-LD example, and SHACL proposal.
- Voiage, Kairos, Reimbursement Atlas, and UOGTO application adapters.
- `edithatogo`-only Hugging Face manifest and scope validator.
- Post-2015 synthesis, gap map, model-risk register, and upstream proposal
  packets.
- Detailed and covering Codex prompts.

## Partial / experimental

- The Chapter 8 model implements a declared assumption set, including a public
  threshold, fixed target quantity, no bargaining below the threshold, and a
  single institution. It is not a universal pricing model.
- The Rust game runtime supports finite, acyclic, perfect-information games and
  expected-payoff chance nodes. Imperfect information, mixed strategies,
  repeated games, mechanism design, learning, and equilibrium refinements are
  roadmap items.
- Technical-efficiency opportunities are represented as explicit alternative
  strategy productivity. No undocumented equation for `mu` is asserted.
- Reimbursement Atlas integration reads reviewed local derived exports; it does
  not fetch raw data or claim evidence readiness.
- Voiage integration is optional and has not been vendored.

## Not complete

- Full formal reconstructions of the Chapter 9 and Chapter 10 games.
- Empirical calibration of `n`, `d`, `m`, or technical-efficiency opportunities.
- Native Rust/Python FFI and released Kairos integration.
- Upstream PRs to UOGTO, Voiage, Kairos, or Reimbursement Atlas.
- Regulator-grade validation, legal review, or deployment approval.

## v0.4.0 handoff and activation

Implemented:

- Git-bundle-first workstation restoration preserving the original commit history;
- an internal activation prompt that creates or safely wires the GitHub remote,
  resolves pinned ecosystem clones, validates CI, and starts implementation;
- standard-library ecosystem clone discovery with fail-closed pin checks;
- repository-local Conductor tracks and baseline Python/Rust CI.

Workstation activation is complete: the private GitHub repository is wired,
all four ecosystem pins are available in clean ignored cache clones, `main` and
the implementation branch are pushed, local and hosted baselines are green,
Conductor T00 is complete, and issues #3-#11 track T01-T09.

No release, publication, regulator-grade validation, licence reconciliation, or
external domain approval is implied.
