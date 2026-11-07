//! A finite application game using Paignia, with synthetic, analytic payoffs.
//!
//! Source concepts: Pekarsky (2015), Chapter 7 equations 7.2–7.5 and
//! Chapter 8 equation 8.2, DOI 10.1007/978-3-319-08903-4. This repository's
//! finite offer grid is an illustrative restriction, not the full economic model.

use std::collections::BTreeMap;

use new_drug_reimbursement_game::{net_economic_benefit_health, OpportunitySet};
use paignia_core::{ActionEdge, ActionId, Game, Node, NodeId, PlayerId};
use paignia_solve::backward_induction;

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
    let root = NodeId("firm_offer".into());
    let rejected = NodeId("rejected".into());
    let mut nodes = BTreeMap::from([(
        rejected.clone(),
        Node::Terminal {
            payoffs: BTreeMap::from([(firm.clone(), 0.0), (institution.clone(), 0.0)]),
        },
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
        nodes.insert(
            accepted.clone(),
            Node::Terminal {
                payoffs: BTreeMap::from([
                    (firm.clone(), total_cost),
                    (institution.clone(), health_benefit),
                ]),
            },
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
    let solution = backward_induction(&Game {
        root: root.clone(),
        nodes,
    })
    .expect("finite application game is supported");

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
