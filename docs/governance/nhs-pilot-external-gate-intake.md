# NHS pilot external-gate intake

This intake is the boundary between the completed methodological pilot and any
real Chapter 7 calibration. It does not approve evidence, select a displaced
programme, or authorize a reimbursement decision. The current readiness receipt
therefore remains candidate-only until every required field below has an
accountable source and reviewer.

For an owner-facing request form with receipt and hash requirements, use the
[external-gate request template](./external-gate-request-template.md).

## Recommended decision

Authorize one narrowly defined NHS decision context and an orchestrated panel
of relevant subagents. The minimum panel includes health economics/methods,
NHS context/displacement, Atlas provenance/licensing, and
reproducibility/runtime roles. Keep DHSC's 1.5% QALY discount convention and
NICE's 3.5% reference-case convention as explicit sensitivity cases until the
panel consensus and any required owner sign-off select the applicable method.
Ask Reimbursement Atlas to produce the approved-derived packet for that same
context.

## Decision choices

### Context

- **Methodological-only:** retain the current public-source dossier. This is
  immediately executable but cannot identify `d`, Scenario 3 ordering, or
  Scenario 4 programme inputs.
- **One real NHS context (recommended):** select one payer/service line,
  decision date, intervention/comparator, and actual displaced programme. This
  is the smallest scope that can unblock Scenarios 2-4.
- **Synthetic stress test:** create a fully specified fictional context for
  software testing only. It must remain explicitly non-empirical and cannot
  satisfy the external gates.

### Evidence route

- **Atlas-approved derived records (recommended):** Atlas owns acquisition,
  licensing, transformations, uncertainty, and approval; this repository
  consumes only the resulting packet.
- **Candidate dossier:** useful for exploratory mapping, but it cannot enter
  calibration or support a policy conclusion.
- **Raw local sources:** not permitted under the evidence-calibration contract.

### Review

- **Four-role subagent panel (recommended):** economics/methods, NHS context,
  Atlas/provenance, and reproducibility/runtime, with an orchestrator and
  consensus receipt.
- **Lean three-role panel:** economics, evidence/licensing, and runtime; use
  only for research implementation when NHS-context review is not in scope.
- **Panel plus named human economist:** strongest route for empirical
  promotion; human sign-off remains separate from the panel consensus.

## Required context record

Provide these values before requesting promotion:

| Field | Required decision |
|---|---|
| `jurisdiction` | England region or national scope |
| `payer` | NHS England, ICB, or other accountable commissioner |
| `budget_boundary` | Funding pool that actually bears the decision |
| `service_line` | Specific programme/service line |
| `decision_date` | Date of the reimbursement decision |
| `price_year` | Monetary basis after reviewed transformation |
| `intervention` / `comparator` | Decision technology and comparator |
| `displaced_programme` | Programme and mechanism supplying actual `d` |
| `programme_id` | Stable identity for Scenario 4 investment evidence |
| `reviewer` | Panel ID, role receipts, orchestrator, and any required human sign-off |
| `discounting_method` | DHSC 1.5%, NICE 3.5%, or justified alternative |

## Promotion acceptance criteria

Promotion may be considered only when:

1. Atlas supplies an approved-derived packet covering the selected context;
2. `d` is tied to the actual displaced programme rather than a generic average;
3. `n`, `m`, and `d` share a reviewed decision-context alignment;
4. Scenario 4's `mu`, `phi`, annual effect, horizon, and discounting share one
   investment-programme identity;
5. uncertainty samples, transformations, and price-year treatment are
   reviewed and recorded; and
6. the panel publishes role receipts and consensus; any required human reviewer
   separately signs the role mapping and resulting calibration receipt.

Until then, the canonical status remains Scenario 1 `candidate_only`, Scenarios
2-4 `not_identifiable`, and `approved_calibration_permitted: false`.
