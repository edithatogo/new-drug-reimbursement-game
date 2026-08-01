# Specification

Integrate the application’s governed uncertainty samples with the pinned
`edithatogo/voiage` decision-analysis capability without duplicating VOI
algorithms or silently promoting empirical evidence.

## Requirements

- Validate aligned net-benefit and parameter samples before optional imports.
- Construct Voiage `ValueArray` and `ParameterSet` objects at the pinned API
  boundary; EVPI/EVPPI/EVSI/ENBS remain Voiage-owned.
- Emit a deterministic, hash-bound handoff receipt containing strategy names,
  sample count, parameter roles, perspective, health unit, and evidence
  revision.
- Preserve fail-closed behavior for ragged, non-finite, unaligned, unsigned,
  or non-health bundles and for unavailable optional dependencies.
- Document the pin, ownership boundary, synthetic fixture restriction, and
  reproducibility contract.

## Acceptance criteria

- Focused adapter tests cover valid schema construction, receipt determinism,
  malformed matrices, and unavailable runtime behavior.
- The handoff receipt is stable for identical inputs and changes when evidence
  revision or values change.
- Full repository quality gates pass.

## Out of scope

- Reimplementing any VOI method.
- Fitting distributions, sampling, or empirical calibration in this package.
- Treating a technical handoff receipt as policy or reimbursement approval.
