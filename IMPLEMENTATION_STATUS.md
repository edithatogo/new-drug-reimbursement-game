# Implementation status

## Complete in this handoff

- Ecosystem-first architecture and pin file.
- Clean-room PEA kernel with source notes and invariant tests.
- Strict Python/Rust implementations of all four Chapter 7 economic scenarios,
  plus an explicit generalized opportunity-set abstraction.
- Analytic revealed-threshold reimbursement equilibrium.
- Domain-neutral Rust extensive-form types, validation, and backward induction.
- Python conformance oracle implementing the same finite perfect-information
  contract.
- UOGTO reimbursement extension proposal, JSON-LD example, and SHACL proposal.
- Voiage, Kairos, Reimbursement Atlas, and UOGTO application adapters.
- Strict approved-derived parameter packets, all-scenario calibration receipts,
  aligned uncertainty validation, and pinned-compatible Voiage schema handoff.
- Candidate-only NHS England source mapping with deterministic role and
  all-scenario readiness receipts; this does not constitute empirical
  calibration or approval.
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
- Scenario 4 implements the source Appendix 5 identities with caller-supplied,
  provenance-bound `mu`, `phi`, and annual programme health effect. The
  software does not empirically estimate those parameters.
- Reimbursement Atlas integration reads reviewed local derived exports; the new
  parameter adapter accepts only the strict version-1 approved-derived packet
  and does not fetch raw data or claim evidence readiness.
- Voiage integration is optional and has not been vendored. The application
  prepares pinned `ValueArray`/`ParameterSet` inputs but retains no VOI
  algorithm or sampler.

## Workstation implementation milestones

- T01 now has cross-language threshold, sign, special-case, unit-rescaling, and
  invalid-input invariants in Python and Rust (`0e6e968`).
- T02 now rejects empty identifiers, duplicate actions, non-finite payoffs, and
  unreachable nodes with structured Rust validation errors (`9717125`).
- These checks harden the seed implementation. Authorized-source verification
  now covers all four Chapter 7 scenarios, including the 2012 Appendix 5
  investment derivation; regulator-grade domain review remains out of scope.

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
