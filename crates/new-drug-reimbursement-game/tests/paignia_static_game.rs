//! A finite application game using Paignia, with synthetic, analytic payoffs.
//!
//! Source concepts: Pekarsky (2015), Chapter 7 equations 7.2–7.5 and
//! Chapter 8 equation 8.2, DOI 10.1007/978-3-319-08903-4. This repository's
//! finite offer grid is an illustrative restriction, not the full economic model.

use std::collections::BTreeMap;

use new_drug_reimbursement_game::payoff_input::{solve_valued_game, PayoffBasis, ValuedPayoff};
use new_drug_reimbursement_game::{net_economic_benefit_health, OpportunitySet};
use paignia_core::{
    ActionEdge, ActionId, Game, GameInstanceId, GameSpecification, GameSpecificationId, Node,
    NodeId, PlayerId, ResultIdentityRecord, SolverRunId, RESULT_IDENTITY_SCHEMA_VERSION,
};

fn fixture_basis(firm: &PlayerId, institution: &PlayerId) -> BTreeMap<PlayerId, PayoffBasis> {
    BTreeMap::from([
        (
            firm.clone(),
            PayoffBasis {
                unit: "fixture-currency-unit".into(),
                perspective: "manufacturing-firm".into(),
            },
        ),
        (
            institution.clone(),
            PayoffBasis {
                unit: "fixture-net-health-unit".into(),
                perspective: "funding-institution".into(),
            },
        ),
    ])
}

fn fixture_specification(game: Game) -> (GameSpecification, ResultIdentityRecord) {
    let id = "urn:ndrg:test:finite-offers".to_string();
    (
        GameSpecification {
            schema_version: "1.0.0".into(),
            id: id.clone(),
            game,
        },
        ResultIdentityRecord {
            schema_version: RESULT_IDENTITY_SCHEMA_VERSION.into(),
            specification_id: GameSpecificationId(id),
            game_instance_id: GameInstanceId("urn:ndrg:test:finite-offers:instance".into()),
            solver_run_id: SolverRunId("urn:ndrg:test:finite-offers:solver-run".into()),
            session_id: None,
            policy_artifact_id: None,
            solver_trace_id: None,
        },
    )
}

#[test]
fn finite_offer_game_selects_the_highest_accepted_price() {
    // Fixed quantity/health gain, zero incremental manufacturing cost, public
    // threshold and acceptance at indifference. Each player's utilities retain
    // its own units; the solver compares only that player's alternatives.
    let opportunities = OpportunitySet {
        expansion_icer: Some(25_000.0),
        contraction_icer: Some(50_000.0),
        displacement_icer: Some(50_000.0),
        additional_best_productivity: 0.0,
    };
    let firm = PlayerId("firm".into());
    let institution = PlayerId("institution".into());
    let basis = fixture_basis(&firm, &institution);
    let valued = |player: &PlayerId, amount| ValuedPayoff {
        amount,
        basis: basis[player].clone(),
        valuation_revision: "finite-offer-acceptance-fixture-v1".into(),
    };
    let root = NodeId("firm_offer".into());
    let rejected = NodeId("rejected".into());
    let terminal = || Node::Terminal {
        payoffs: BTreeMap::new(),
    };
    let mut nodes = BTreeMap::from([(rejected.clone(), terminal())]);
    let mut valuations = BTreeMap::from([(
        rejected.clone(),
        BTreeMap::from([
            (firm.clone(), valued(&firm, 0.0)),
            (institution.clone(), valued(&institution, 0.0)),
        ]),
    )]);
    let mut offer_edges = Vec::new();

    let offers = [
        ("low", 20_000.0),
        ("threshold", 25_000.0),
        ("high", 30_000.0),
    ];
    for (label, price_per_health_unit) in offers {
        let response = NodeId(format!("response_{label}"));
        let accepted = NodeId(format!("accepted_{label}"));
        let total_cost = 4.0 * price_per_health_unit;
        let health_benefit = net_economic_benefit_health(total_cost, 4.0, opportunities)
            .expect("synthetic application inputs are valid");
        nodes.insert(accepted.clone(), terminal());
        valuations.insert(
            accepted.clone(),
            BTreeMap::from([
                (firm.clone(), valued(&firm, total_cost)),
                (institution.clone(), valued(&institution, health_benefit)),
            ]),
        );
        nodes.insert(
            response.clone(),
            Node::Decision {
                player: institution.clone(),
                edges: vec![
                    ActionEdge {
                        action: ActionId("accept".into()),
                        target: accepted,
                    },
                    ActionEdge {
                        action: ActionId("reject".into()),
                        target: rejected.clone(),
                    },
                ],
            },
        );
        offer_edges.push(ActionEdge {
            action: ActionId(label.into()),
            target: response,
        });
    }
    nodes.insert(
        root.clone(),
        Node::Decision {
            player: firm.clone(),
            edges: offer_edges,
        },
    );
    let (specification, identities) = fixture_specification(Game {
        root: root.clone(),
        nodes,
    });
    let result = solve_valued_game(specification, identities, &basis, valuations)
        .expect("finite valued application game is supported");
    assert_eq!(result.policy.envelope.solutions.len(), 1);
    let solution = &result.policy.envelope.solutions[0];

    // Independently: beta = 1 / (1/50000 + 1/25000 - 1/50000) = 25000.
    // Institution utilities are 0.8, 0, -0.8; accept wins the declared tie.
    // Firm revenues after those responses are 80000, 100000, 0.
    assert_eq!(solution.choices[&root], ActionId("threshold".into()));
    assert_eq!(
        solution.choices[&NodeId("response_threshold".into())],
        ActionId("accept".into())
    );
    assert_eq!(
        solution.choices[&NodeId("response_high".into())],
        ActionId("reject".into())
    );
    assert!((solution.expected_payoffs[&firm] - 100_000.0).abs() <= 1e-9);
    assert!(solution.expected_payoffs[&institution].abs() <= 1e-12);
}
