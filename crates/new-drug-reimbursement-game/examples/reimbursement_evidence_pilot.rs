//! Synthetic evidence-contingent reimbursement at a precommitted price.
//!
//! The payer's health-opportunity-cost calculation uses Pekarsky (2015),
//! Chapter 7 equations 7.2–7.5, DOI 10.1007/978-3-319-08903-4.
//! The fixed offer, prior and evidence mechanism are synthetic.

use std::collections::BTreeMap;

use new_drug_reimbursement_game::payoff_input::{
    solve_valued_game, PayoffBasis, ValuedPayoff, ValuedSolution,
};
use new_drug_reimbursement_game::{
    fixed_budget_shadow_price, net_economic_benefit_health, OpportunitySet,
};
use paignia_core::{
    ActionEdge, ActionId, CatalogueClaim, ChanceEdge, Game, GameInstanceId, GameSpecification,
    GameSpecificationId, Node, NodeId, PlayerId, ResultAlgorithm, ResultGameClass,
    ResultIdentityRecord, ResultInformationStructure, ResultSelectionRule, ResultSolutionConcept,
    ResultStatus, SolverRunId, GAME_SPEC_SCHEMA_VERSION, RESULT_IDENTITY_SCHEMA_VERSION,
};

const SPECIFICATION: &str = "urn:ndrg:si04:synthetic-committed-offer-v1";
const INSTANCE: &str = "urn:ndrg:si04:synthetic-two-state-instance";
const RUN: &str = "urn:ndrg:si04:valued-policy-run";
const PROVIDER_REVISION: &str = "a04a19da06cc50e310a172574ed66f62000b891a";
const UNIT: &str = "synthetic-common-monetary-unit";
const PRICE: f64 = 5.0;
const PRODUCTION_COST: f64 = 2.0;
const PROBABILITY: f64 = 0.5;

struct EvidenceState {
    world: &'static str,
    observation: &'static str,
    health_gain: f64,
}

const EVIDENCE: [EvidenceState; 2] = [
    EvidenceState {
        world: "favourable",
        observation: "clinical_positive",
        health_gain: 9.0,
    },
    EvidenceState {
        world: "adverse",
        observation: "clinical_negative",
        health_gain: 1.0,
    },
];

fn node(id: &str) -> NodeId {
    NodeId(id.into())
}

fn accepted_terminal(state: &EvidenceState) -> NodeId {
    node(&format!("{}_accepted", state.world))
}

fn terminal() -> Node {
    Node::Terminal {
        payoffs: BTreeMap::new(),
    }
}

fn solve_pilot_game() -> ValuedSolution {
    let institution = PlayerId("institution".into());
    let firm = PlayerId("firm".into());
    let basis = BTreeMap::from([
        (
            institution.clone(),
            PayoffBasis {
                unit: UNIT.into(),
                perspective: "funding-institution".into(),
            },
        ),
        (
            firm.clone(),
            PayoffBasis {
                unit: UNIT.into(),
                perspective: "manufacturing-firm".into(),
            },
        ),
    ]);
    let valued = |player: &PlayerId, amount| ValuedPayoff {
        amount,
        basis: basis[player].clone(),
        valuation_revision: SPECIFICATION.into(),
    };
    let payoff = |net_benefit, profit| {
        BTreeMap::from([
            (institution.clone(), valued(&institution, net_benefit)),
            (firm.clone(), valued(&firm, profit)),
        ])
    };
    let opportunities = OpportunitySet {
        expansion_icer: None,
        contraction_icer: None,
        displacement_icer: Some(1.0),
        additional_best_productivity: 0.0,
    };
    let shadow_price = fixed_budget_shadow_price(opportunities).expect("synthetic shadow price");
    let root = node("disclosed_evidence");
    let withhold = node("withheld");
    let mut nodes = BTreeMap::from([(withhold.clone(), terminal())]);
    let mut valuations = BTreeMap::from([(withhold.clone(), payoff(0.0, 0.0))]);
    let mut evidence_edges = Vec::new();

    for state in &EVIDENCE {
        let decision = node(state.world);
        let accepted = accepted_terminal(state);
        let health = net_economic_benefit_health(PRICE, state.health_gain, opportunities)
            .expect("synthetic health net benefit");
        nodes.insert(accepted.clone(), terminal());
        valuations.insert(
            accepted.clone(),
            payoff(health * shadow_price, PRICE - PRODUCTION_COST),
        );
        nodes.insert(
            decision.clone(),
            Node::Decision {
                player: institution.clone(),
                edges: vec![
                    ActionEdge {
                        action: ActionId("reimburse".into()),
                        target: accepted,
                    },
                    ActionEdge {
                        action: ActionId("withhold".into()),
                        target: withhold.clone(),
                    },
                ],
            },
        );
        evidence_edges.push(ChanceEdge {
            probability: PROBABILITY,
            target: decision,
        });
    }
    nodes.insert(
        root.clone(),
        Node::Chance {
            edges: evidence_edges,
        },
    );
    solve_valued_game(
        GameSpecification {
            schema_version: GAME_SPEC_SCHEMA_VERSION.into(),
            id: SPECIFICATION.into(),
            game: Game { root, nodes },
        },
        ResultIdentityRecord {
            schema_version: RESULT_IDENTITY_SCHEMA_VERSION.into(),
            specification_id: GameSpecificationId(SPECIFICATION.into()),
            game_instance_id: GameInstanceId(INSTANCE.into()),
            solver_run_id: SolverRunId(RUN.into()),
            session_id: None,
            policy_artifact_id: None,
            solver_trace_id: None,
        },
        &basis,
        valuations,
    )
    .expect("qualify the application valued-payoff policy")
}

fn main() {
    let result = solve_pilot_game();
    let native = &result.policy.envelope;
    assert_eq!(native.status, ResultStatus::Completed);
    assert_eq!(native.catalogue, CatalogueClaim::OneFound);
    assert_eq!(native.game_class, ResultGameClass::FiniteAcyclicExtensive);
    assert_eq!(
        native.information_structure,
        ResultInformationStructure::PerfectInformation
    );
    assert_eq!(
        native.solution_concept,
        ResultSolutionConcept::ToleranceAwareBackwardInductionPolicy
    );
    assert_eq!(
        native.algorithm.algorithm,
        ResultAlgorithm::BackwardInduction
    );
    assert_eq!(
        native.selection_rule,
        ResultSelectionRule::InputOrderPairwiseToleranceThenLexicographic
    );
    assert_eq!(native.solutions.len(), 1);

    // The first row binds the producer run. Subsequent rows report the two
    // observation-conditioned choices and the original valued offer payoffs.
    println!(
        "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{PROVIDER_REVISION}",
        native.schema_version,
        native.semantic_profile,
        native.algorithm.version,
        native.identities.specification_id.0,
        native.identities.game_instance_id.0,
        native.identities.solver_run_id.0,
        native.tolerance,
    );
    for state in &EVIDENCE {
        let values = &result.valuations[&accepted_terminal(state)];
        let decision = &native.solutions[0].choices[&node(state.world)];
        println!(
            "{}\t{}\t{PROBABILITY}\t{}\t{}\t{}",
            state.world,
            state.observation,
            values[&PlayerId("institution".into())].amount,
            values[&PlayerId("firm".into())].amount,
            decision.0,
        );
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn conditional_offer_matches_the_independent_ledger() {
        let result = solve_pilot_game();
        let solution = &result.policy.envelope.solutions[0];
        // At price 5 the payer receives 9 - 5 or 1 - 5. The firm receives 5 - 2
        // only when the payer reimburses. Each state has probability one half.
        assert_eq!(solution.choices[&node("favourable")].0, "reimburse");
        assert_eq!(solution.choices[&node("adverse")].0, "withhold");
        assert_eq!(
            solution.expected_payoffs[&PlayerId("institution".into())].to_bits(),
            2.0_f64.to_bits()
        );
        assert_eq!(
            solution.expected_payoffs[&PlayerId("firm".into())].to_bits(),
            1.5_f64.to_bits()
        );
    }
}
