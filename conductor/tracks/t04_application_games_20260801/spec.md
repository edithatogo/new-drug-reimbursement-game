# Specification

Implement the application-level Pekarsky games while preserving the strict
source models and explicit alternative assumptions.

## Requirements

- Game 1: continuous-price extensive form with production cost, quantity/effect,
  tie policy, threshold observability, and a discretised solver that can be
  compared with the analytic corner solution. Include hidden-threshold,
  bargaining, net-price rebate, and contract-enforcement variants.
- Game 2: firm/institution/capital-market choices (do nothing, lobby, borrow),
  R&amp;D cost, interest, success/failure, information structure, and complete
  payoffs with deterministic backward-induction choice.
- Game 3: multi-period current/future-drug development and manufacturing,
  first/second prices, clinical/manufacturing innovation, lifecycle and
  competition state, premium/rebate/public-investment contracts, uncertainty,
  and global spillover accounting.
- Every model must validate finite inputs, retain named assumptions, and expose
  provenance/version metadata. No silent equilibrium or parameter choices.
- Keep all application concepts in Python; generic game mechanics remain in
  the Rust/UOGTO runtime.

## Acceptance criteria

- Deterministic tests cover each game and every named variant.
- Game 1 grid results converge to the analytic threshold under explicit tie
  policy and identify hidden-threshold limits.
- Game 2 and Game 3 outputs include complete payoffs/state transitions and are
  reproducible for fixed inputs.
- Documentation maps equations/assumptions to Pekarsky locations and clearly
  labels extensions as non-source variants.
- Full repository quality gates pass.

## Out of scope

- Empirical NHS/Atlas calibration or regulatory claims.
- Reimplementation of Kairos scheduling, Voiage VOI, or UOGTO semantics.
