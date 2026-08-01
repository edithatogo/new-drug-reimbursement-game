# Specification

Add explicit, research-only extensions identified in the post-2015 synthesis:
distributional equity, managed entry, adaptive evidence policies, and
portfolio/global spillovers.

## Requirements

- Represent subgroup health outcomes and equity weights without collapsing them
  into an unlabelled scalar.
- Represent managed-entry price/rebate, monitoring, clawback, renegotiation,
  and termination terms as explicit state and deterministic settlement.
- Represent an adaptive evidence policy over observed states and a bounded
  information value supplied by Voiage; do not reimplement VOI algorithms.
- Represent portfolio innovation and global spillovers with explicit payer
  shares and provenance-labelled assumptions.
- Reject invalid/non-finite inputs and label all outputs as extensions, not
  source-equation or empirical claims.

## Acceptance criteria

- Deterministic tests cover each extension and fail-closed validation.
- Documentation maps every extension to the synthesis and ownership boundary.
- Full repository quality gates pass.
