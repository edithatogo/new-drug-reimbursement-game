# Implementation plan

## Phase 1 - Evidence contract

- [ ] Add failing tests and a strict JSON schema for versioned parameter
  evidence records and packets.
- [ ] Implement immutable evidence-record and packet parsing with fail-closed
  provenance, approval, marginality, unit, context, and uncertainty checks.
- [ ] Automated review and focused validation checkpoint.

## Phase 2 - Scenario calibration

- [ ] Add failing tests for Scenario 1-4 evidence-role assembly and calibration
  receipts.
- [ ] Implement compatible-record selection, scenario input assembly, and
  deterministic provenance receipts without duplicating Chapter 7 equations.
- [ ] Automated review and focused validation checkpoint.

## Phase 3 - Atlas and Voiage boundaries

- [ ] Strengthen the Atlas derived-export adapter to parse the governed packet
  contract and reject raw, unapproved, or incompatible records.
- [ ] Prepare aligned parameter and strategy-value samples for the pinned
  Voiage `ParameterSet`/`ValueArray` API, with no local VOI algorithm.
- [ ] Add a synthetic non-empirical fixture, CLI validation, examples, and
  boundary documentation.
- [ ] Automated review and ecosystem integration checkpoint.

## Phase 4 - Completion

- [ ] Run the full repository quality gate, record commit-bound evidence, and
  reconcile Conductor registry, status, run log, and external gates.
