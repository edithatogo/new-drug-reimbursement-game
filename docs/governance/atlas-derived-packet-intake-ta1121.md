# Atlas-derived packet intake: TA1121

The companion JSON is the completed intake and mapping-boundary packet for the
TA1121 candidate context. It binds the work to Reimbursement Atlas commit
`5b0c2fe3e1b7d2d6c3c1975cf1a162f2787c67aa` and records the public-source
provenance, reviewed-source boundary, validation state, and missing inputs.

This is intentionally **not** an executable approved-derived Chapter 7 packet:
the Atlas checkout contains no programme-aligned NHS records for displacement,
`d`, `mu`, `phi`, annual programme effect, horizon, or discounting. The packet
therefore remains `pending_accountable_review` and cannot enter calibration.

Promotion requires an immutable Atlas export with source checksums, documented
transformations, uncertainty, licence disposition, a local displacement
record, and named human health-economist approval. Raw payloads and restricted
descriptors are excluded by design.
