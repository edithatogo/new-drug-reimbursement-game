# Specification

Integrate application execution plans with the pinned Kairos event contract
without implementing a scheduler, clock, ECS, or random-number generator in
this repository.

## Requirements

- Normalize application events into stable sequence/time/kind/payload records.
- Reject non-finite or negative times, empty kinds, malformed payloads, and
  non-monotonic event order before any optional runtime import.
- Produce a deterministic hash-bound trace receipt for reproducibility.
- Preserve the pinned Kairos ownership of scheduling, time advancement, event
  IDs, ECS state, and random streams; unavailable native runtime must fail
  explicitly.
- Document the event schema, pin, adapter boundary, and extraction handoff.

## Acceptance criteria

- Focused tests cover normalization, trace determinism, malformed events, and
  explicit optional-runtime boundaries.
- Receipt changes when event content or ordering changes.
- Full repository quality gates pass.

## Out of scope

- Duplicating Kairos scheduling or state management.
- Adding an unreleased Kairos source/path dependency.
