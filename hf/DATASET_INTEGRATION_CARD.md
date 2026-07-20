# Proposed Reimbursement Atlas configuration: `new_drug_reimbursement_game`

This is a proposal for the owner-controlled dataset, not an upload.

Each row should be a derived, reviewed parameter candidate with:

- `record_id`
- `source_record_ids`
- `jurisdiction`
- `budget_boundary`
- `price_year`
- `currency`
- `health_unit`
- `parameter_role` (`n`, `d`, `m`, `alternative_productivity`)
- `point_estimate`
- `distribution_family` and `distribution_parameters`
- `marginal_or_average`
- `causal_status`
- `licence_status`
- `review_status`
- `reviewer`
- `source_checksums`
- `transformation_revision`

No raw restricted source text, confidential price, or unreviewed model output
should be published.
