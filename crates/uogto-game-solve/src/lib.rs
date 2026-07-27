//! Backward induction for finite, acyclic, perfect-information games.

use std::collections::BTreeMap;
use std::fmt;

use uogto_game_core::{ActionId, Game, Node, NodeId, PayoffVector, PlayerId, ValidationError};

pub const DEFAULT_SOLVER_TOLERANCE: f64 = 1e-12;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum TiePolicy {
    LexicographicAction,
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct SolverConfig {
    pub tolerance: f64,
    pub tie_policy: TiePolicy,
}

impl Default for SolverConfig {
    fn default() -> Self {
        Self {
            tolerance: DEFAULT_SOLVER_TOLERANCE,
            tie_policy: TiePolicy::LexicographicAction,
        }
    }
}

#[derive(Clone, Debug, Default, Eq, PartialEq)]
pub struct SolverDiagnostics {
    pub visited_nodes: usize,
    pub resolved_ties: usize,
}

#[derive(Clone, Debug, PartialEq)]
pub struct Solution {
    pub expected_payoffs: PayoffVector,
    pub choices: BTreeMap<NodeId, ActionId>,
    pub tolerance: f64,
    pub tie_policy: TiePolicy,
    pub diagnostics: SolverDiagnostics,
}

#[derive(Clone, Debug, PartialEq)]
pub enum SolveError {
    InvalidGame(ValidationError),
    InvalidTolerance(f64),
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
    backward_induction_with_config(game, SolverConfig::default())
}

/// Solve with an explicit numeric tolerance and deterministic tie policy.
///
/// # Errors
///
/// Returns [`SolveError::InvalidTolerance`] when the tolerance is not finite
/// or is negative, in addition to the errors documented by
/// [`backward_induction`].
pub fn backward_induction_with_config(
    game: &Game,
    config: SolverConfig,
) -> Result<Solution, SolveError> {
    if !config.tolerance.is_finite() || config.tolerance < 0.0 {
        return Err(SolveError::InvalidTolerance(config.tolerance));
    }
    game.validate().map_err(SolveError::InvalidGame)?;
    let mut choices = BTreeMap::new();
    let mut diagnostics = SolverDiagnostics::default();
    let payoffs = solve_node(game, &game.root, config, &mut choices, &mut diagnostics)?;
    Ok(Solution {
        expected_payoffs: payoffs,
        choices,
        tolerance: config.tolerance,
        tie_policy: config.tie_policy,
        diagnostics,
    })
}

fn solve_node(
    game: &Game,
    node_id: &NodeId,
    config: SolverConfig,
    choices: &mut BTreeMap<NodeId, ActionId>,
    diagnostics: &mut SolverDiagnostics,
) -> Result<PayoffVector, SolveError> {
    diagnostics.visited_nodes += 1;
    let node = game
        .nodes
        .get(node_id)
        .ok_or_else(|| SolveError::MissingNode(node_id.clone()))?;
    match node {
        Node::Terminal { payoffs } => Ok(payoffs.clone()),
        Node::Chance { edges } => {
            let mut expected = PayoffVector::new();
            for edge in edges {
                let child = solve_node(game, &edge.target, config, choices, diagnostics)?;
                for (player, payoff) in child {
                    *expected.entry(player).or_insert(0.0) += edge.probability * payoff;
                }
            }
            Ok(expected)
        }
        Node::Decision { player, edges } => {
            let mut best: Option<(f64, ActionId, PayoffVector)> = None;
            for edge in edges {
                let child = solve_node(game, &edge.target, config, choices, diagnostics)?;
                let utility = payoff_for(&child, player);
                let replace = match &best {
                    None => true,
                    Some((best_utility, best_action, _)) => {
                        if (utility - *best_utility).abs() <= config.tolerance {
                            diagnostics.resolved_ties += 1;
                            match config.tie_policy {
                                TiePolicy::LexicographicAction => edge.action < *best_action,
                            }
                        } else {
                            utility > *best_utility
                        }
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
        assert_eq!(
            solution.tolerance.to_bits(),
            DEFAULT_SOLVER_TOLERANCE.to_bits()
        );
        assert_eq!(solution.tie_policy, TiePolicy::LexicographicAction);
        assert_eq!(solution.diagnostics.visited_nodes, 3);
        assert_eq!(solution.diagnostics.resolved_ties, 0);
    }

    #[test]
    fn resolves_ties_lexicographically_with_explicit_tolerance() {
        let player = PlayerId("player".into());
        let root = NodeId("root".into());
        let first = NodeId("first".into());
        let second = NodeId("second".into());
        let nodes = BTreeMap::from([
            (
                root.clone(),
                Node::Decision {
                    player: player.clone(),
                    edges: vec![
                        ActionEdge {
                            action: ActionId("zeta".into()),
                            target: first,
                        },
                        ActionEdge {
                            action: ActionId("alpha".into()),
                            target: second,
                        },
                    ],
                },
            ),
            (
                NodeId("first".into()),
                Node::Terminal {
                    payoffs: BTreeMap::from([(player.clone(), 1.0)]),
                },
            ),
            (
                NodeId("second".into()),
                Node::Terminal {
                    payoffs: BTreeMap::from([(player, 1.000_001)]),
                },
            ),
        ]);
        let solution = backward_induction_with_config(
            &Game {
                root: root.clone(),
                nodes,
            },
            SolverConfig {
                tolerance: 0.001,
                tie_policy: TiePolicy::LexicographicAction,
            },
        )
        .unwrap();

        assert_eq!(solution.choices[&root], ActionId("alpha".into()));
        assert_eq!(solution.diagnostics.resolved_ties, 1);
    }

    #[test]
    fn rejects_invalid_tolerances() {
        let game = Game {
            root: NodeId("missing".into()),
            nodes: BTreeMap::new(),
        };
        for tolerance in [f64::NAN, f64::INFINITY, -f64::EPSILON] {
            assert!(matches!(
                backward_induction_with_config(
                    &game,
                    SolverConfig {
                        tolerance,
                        ..SolverConfig::default()
                    }
                ),
                Err(SolveError::InvalidTolerance(value))
                    if value.to_bits() == tolerance.to_bits()
            ));
        }
    }
}
