//! Backward induction for finite, acyclic, perfect-information games.

use std::collections::BTreeMap;
use std::fmt;

use uogto_game_core::{ActionId, Game, Node, NodeId, PayoffVector, PlayerId, ValidationError};

#[derive(Clone, Debug, PartialEq)]
pub struct Solution {
    pub expected_payoffs: PayoffVector,
    pub choices: BTreeMap<NodeId, ActionId>,
}

#[derive(Clone, Debug, PartialEq)]
pub enum SolveError {
    InvalidGame(ValidationError),
    MissingNode(NodeId),
}

impl fmt::Display for SolveError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{self:?}")
    }
}

impl std::error::Error for SolveError {}

/// Solve a validated finite, acyclic, perfect-information game.
///
/// # Errors
///
/// Returns [`SolveError::InvalidGame`] when the game violates the supported
/// contract, or [`SolveError::MissingNode`] when traversal cannot resolve a
/// referenced node.
pub fn backward_induction(game: &Game) -> Result<Solution, SolveError> {
    game.validate().map_err(SolveError::InvalidGame)?;
    let mut choices = BTreeMap::new();
    let payoffs = solve_node(game, &game.root, &mut choices)?;
    Ok(Solution {
        expected_payoffs: payoffs,
        choices,
    })
}

fn solve_node(
    game: &Game,
    node_id: &NodeId,
    choices: &mut BTreeMap<NodeId, ActionId>,
) -> Result<PayoffVector, SolveError> {
    let node = game
        .nodes
        .get(node_id)
        .ok_or_else(|| SolveError::MissingNode(node_id.clone()))?;
    match node {
        Node::Terminal { payoffs } => Ok(payoffs.clone()),
        Node::Chance { edges } => {
            let mut expected = PayoffVector::new();
            for edge in edges {
                let child = solve_node(game, &edge.target, choices)?;
                for (player, payoff) in child {
                    *expected.entry(player).or_insert(0.0) += edge.probability * payoff;
                }
            }
            Ok(expected)
        }
        Node::Decision { player, edges } => {
            let mut best: Option<(f64, ActionId, PayoffVector)> = None;
            for edge in edges {
                let child = solve_node(game, &edge.target, choices)?;
                let utility = payoff_for(&child, player);
                let replace = match &best {
                    None => true,
                    Some((best_utility, best_action, _)) => {
                        utility > *best_utility + 1e-12
                            || ((utility - *best_utility).abs() <= 1e-12
                                && edge.action < *best_action)
                    }
                };
                if replace {
                    best = Some((utility, edge.action.clone(), child));
                }
            }
            let (_, action, payoffs) = best.expect("validated decision has an action");
            choices.insert(node_id.clone(), action);
            Ok(payoffs)
        }
    }
}

fn payoff_for(payoffs: &PayoffVector, player: &PlayerId) -> f64 {
    payoffs.get(player).copied().unwrap_or(0.0)
}

#[cfg(test)]
mod tests {
    use std::collections::BTreeMap;

    use super::*;
    use uogto_game_core::{ActionEdge, Game, Node};

    #[test]
    fn chooses_controlling_players_best_action() {
        let player = PlayerId("institution".into());
        let root = NodeId("root".into());
        let accept = NodeId("accept".into());
        let reject = NodeId("reject".into());
        let mut nodes = BTreeMap::new();
        nodes.insert(
            root.clone(),
            Node::Decision {
                player: player.clone(),
                edges: vec![
                    ActionEdge {
                        action: ActionId("reimburse".into()),
                        target: accept.clone(),
                    },
                    ActionEdge {
                        action: ActionId("reject".into()),
                        target: reject.clone(),
                    },
                ],
            },
        );
        nodes.insert(
            accept,
            Node::Terminal {
                payoffs: BTreeMap::from([(player.clone(), 1.0)]),
            },
        );
        nodes.insert(
            reject,
            Node::Terminal {
                payoffs: BTreeMap::from([(player.clone(), 0.0)]),
            },
        );
        let solution = backward_induction(&Game {
            root: root.clone(),
            nodes,
        })
        .unwrap();
        assert_eq!(solution.choices[&root], ActionId("reimburse".into()));
    }
}
