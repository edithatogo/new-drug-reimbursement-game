# Parameter draws and simulation replicates

The application declares a sampling plan for an identified producer run.
Each outer parameter draw has its own identity and a list of conditional
simulation replicates. The model, equilibrium and measurement coordinates
stay attached to each replicate. Equilibrium and measurement coordinates
can be absent when the producer omits those dimensions.

`voiage_input::replicates::DrawPlan::accept` matches the recorded outcomes
to the declared run and full coordinates. Each paired strategy outcome
shares one draw identity. The port requires complete, unique outcomes and
retains their recorded order. Replicate labels are scoped to their own
parameter draw.

The receipt reports the admitted outer count and the inner count for each
parameter draw. Exact enumeration and Monte Carlo precision are explicit.
A Monte Carlo standard error can be unknown or reported as a finite
nonnegative value, including zero.

The [synthetic fixture](../../fixtures/conformance/voiage-noise-identities-v1.json)
declares one parameter draw and two paired outcomes, `[-1, 1]` and `[1, -1]`.
Their conditional strategy values are `[0, 0]`. Installed Voiage reports
parameter EVPI of zero on those conditional values. Treating the replicates
as two parameter draws would report 1. The application rejects those
undeclared outer coordinates before the numerical handoff.

The application binds the original identities and valuation inputs.
Voiage retains ownership of numerical information value and its diagnostics.
