# Post-2015 synthesis: improvements and unresolved gaps

This document turns the 2015 framework into a research programme. It is a
methodological synthesis, not a claim that every cited development has been
fully integrated. Bibliographic metadata must be reverified before publication.

## 1. Empirical health opportunity cost

Subsequent work has expanded empirical estimation of marginal health-system
productivity and opportunity-cost thresholds across England, Australia, the
United States, and lower- and middle-income countries. This directly addresses
Pekarsky's concern that `n`, `d`, `m`, and related quantities lacked evidence.
The remaining bridge is not merely a single threshold estimate: the application
needs jurisdiction-, year-, budget-, service-line-, and displacement-specific
posterior distributions with transparent causal assumptions.

**Build implication:** Reimbursement Atlas should expose reviewed candidate
records and provenance; the application should maintain parameter-role
interpretations; Voiage should value further research on them.

## 2. Distributional and equity-sensitive evaluation

Distributional cost-effectiveness analysis formalized health-inequality impacts
and equity trade-offs. Population-health maximization can therefore be one
perspective among several rather than the only institutional utility.

**Build implication:** UOGTO payoff profiles need perspective, population group,
equity weight, and distributional outcome semantics. The game runtime must
support vector-valued outcomes and explicit utility functions rather than
silently collapsing them.

## 3. Value of information and adaptive evidence

VOI good-practice methods, EVSI methods, adaptive designs, sequential VOI,
portfolio VOI, and structural uncertainty have matured. Voiage already develops
many of these capabilities.

**Build implication:** reimbursement decisions become policies over evidence
states, not one-off deterministic comparisons. Games 2 and 3 should use Voiage
outputs and Kairos event time rather than a bespoke uncertainty engine.

## 4. Managed entry agreements and contracts

Outcomes-based agreements, price-volume agreements, rebates, coverage with
evidence development, and other managed-entry arrangements provide richer
responses than accept/reject at a list price. Confidential net prices also make
observed list-price games empirically incomplete.

**Build implication:** add contract, observability, auditability, enforcement,
clawback, renegotiation, and termination objects to the application extension;
keep generic mechanism and contract semantics in UOGTO/general runtime.

## 5. Indication, subgroup, and lifecycle pricing

A single drug may have heterogeneous value by indication, subgroup, line of
therapy, sequence, combination, and time. Patent expiry, competition, learning,
and manufacturing changes make price and surplus dynamic.

**Build implication:** model a portfolio of linked games sharing firm capacity,
R&D state, evidence, and price constraints. Use repeated/stochastic games and
Kairos timelines.

## 6. Strategic information and bargaining

The 2015 games deliberately simplify information. Real reimbursement features
private R&D costs, confidential discounts, uncertain demand, non-public
reservation values, lobbying, appeals, international reference pricing, and
multi-jurisdiction spillovers.

**Build implication:** implement information sets, beliefs, signals, bargaining
protocols, commitment, reputation, and incomplete-information equilibrium
interfaces in the general Rust library, with UOGTO mappings.

## 7. Affordability, implementation, and capacity

Cost effectiveness does not guarantee affordability, deliverability, or timely
implementation. Budget impact, workforce, diagnostics, supply constraints,
service substitution, and political costs can alter feasible strategies.

**Build implication:** compile implementation pathways to Kairos DES/ABM models.
Health opportunity cost becomes state- and capacity-dependent.

## 8. Innovation incentives and global spillovers

The relationship between local price and future innovation is uncertain,
delayed, portfolio-mediated, and distributed across jurisdictions. A static
premium is not automatically the right instrument.

**Build implication:** represent R&D investment, success probabilities, capital
markets, knowledge spillovers, global payer interactions, and contracts as a
multi-period model. Voiage should quantify the value of reducing key structural
uncertainties.

## 9. Identification and causal displacement

The programme actually displaced is often hidden. Marginal productivity
estimates do not by themselves identify the causal chain from a reimbursement
decision to lost health.

**Build implication:** evidence records must distinguish observed displacement,
modelled displacement, budget-holder reports, and inferred marginal effects.

## 10. Reproducible semantics

The original framework is mathematically rich but not machine-readable. UOGTO,
SHACL, canonical schemas, deterministic traces, and conformance fixtures can
make assumptions inspectable and reusable.

**Build implication:** every result should identify the game specification,
parameter revision, solver revision, evidence revisions, perspective, and trace.

See `REFERENCES.md` and `docs/research/model-extension-map.md`.
