# Evidence strategy for n, d, m, and technical-efficiency alternatives

The book explicitly identifies the lack of empirical estimates as a central
problem. This repository treats each parameter as a role bound to a reviewed
evidence record, not as a universal scalar.

Required metadata:

- jurisdiction, payer, budget boundary, service line, and price year;
- decision date and implementation horizon;
- currency and health-outcome unit;
- programme identity and whether expansion/contraction was feasible;
- observed, elicited, modelled, or inferred status;
- causal assumptions and uncertainty distribution;
- source, checksum, transformation, reviewer, and approval state;
- whether the record represents average, incremental, or marginal productivity;
- displaced quantity and non-linearity/scale limits.

Reimbursement Atlas should own acquisition and provenance. This application
adds the semantic role—`n`, `d`, `m`, or an alternative strategy—and records the
model revision that used it. Voiage values additional evidence. No model output
may upgrade a candidate record to approved evidence automatically.

## Executable version-1 contract

The governed application boundary is implemented in
`schemas/parameter-evidence-packet-v1.schema.json` and
`reimbursement_game.evidence`. It requires approved, derived-only records and
enforces role-specific units and marginality. The supported roles are `n`,
`d`, `m`, `mu`, `phi`, annual programme health effect, horizon, and discount
rate.

`reimbursement_game.calibration` requires an explicit record ID for every role
needed by the selected scenario, rejects incompatible or unaligned draws, and
binds the resulting receipt to the case, packet, record revisions, and source
checksums. Scenario 4 additionally requires programme, horizon, and
discount-rate evidence to refer to one investment programme and validates the
Appendix 5 identities on every supplied draw.

The application accepts supplied deterministic, empirical-sample, or
posterior-sample representations. It does not fit distributions or generate
random samples. The aligned output is prepared for Voiage, which remains
authoritative for VOI.
