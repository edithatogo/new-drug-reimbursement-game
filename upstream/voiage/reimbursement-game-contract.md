# Voiage integration proposal

Add a fixture-backed adapter contract accepting:

- samples × strategies net-benefit arrays;
- optional parameter samples with semantic IDs;
- perspective IDs and population/time-horizon metadata;
- model and evidence revision provenance.

Return EVPI/EVPPI/EVSI/ENBS and diagnostics with the same provenance. The
reimbursement application should not add new VOI algorithms. Longer term, the
shared Rust schema should allow the future game runtime and Voiage Rust core to
exchange arrays and metadata without Python-specific coupling.
