# Quality-frontier disposition

This record closes the repository-owned part of the quality-frontier audit for
the current one-workflow, solo-maintainer project.

## Implemented and continuously replayed

- **Property-style checks:** `tests/test_quality_frontier.py` runs 128 seeded
  cases (`random.Random(20260801)`) and checks positivity, binding-alternative
  selection, threshold identity, and monotone reimbursement decisions.
- **Contract checks:** the same suite checks the fixed-budget input contract;
  the existing conformance fixture checks the cross-language economics schema.
- **Deterministic replay:** the seed, case count, and expected decision vector
  are committed and run by the required Python CI job.

## Explicitly deferred or not applicable

- **Mutation testing (MT):** no mutation runner is included in the pinned,
  dependency-free CI environment. A future maintainer may add a pinned,
  scheduled mutation lane with a recorded score.
- **DST (differential/system testing):** there is no independent production
  implementation to compare against. Rust/Python conformance fixtures are the
  applicable differential boundary; external comparison remains out of scope
  until an approved upstream contract exists.
- **Input mutation/fuzzing:** unbounded fuzzing is not warranted for this pure,
  numeric API in the fast PR lane. The seeded boundary sweep is the bounded
  replacement; a scheduled fuzz lane can be added when release scope expands.

These are evidence-backed scope decisions, not claims that deferred techniques
were run. Hosted CI remains authoritative for committed checks.
