//! Domain-neutral finite extensive-form game types.
//!
//! The crate deliberately contains no health, reimbursement, drug, QALY, or
//! HTA concepts. It is the extraction seed for a Rust game-theory runtime above
//! Kairos and aligned with UOGTO.

use std::collections::{BTreeMap, BTreeSet};
use std::fmt;

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct PlayerId(pub String);

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct NodeId(pub String);

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct ActionId(pub String);

pub type PayoffVector = BTreeMap<PlayerId, f64>;

#[derive(Clone, Debug, PartialEq)]
pub struct ActionEdge {
    pub action: ActionId,
    pub target: NodeId,
}

#[derive(Clone, Debug, PartialEq)]
pub struct ChanceEdge {
    pub probability: f64,
    pub target: NodeId,
}

#[derive(Clone, Debug, PartialEq)]
pub enum Node {
    Decision {
        player: PlayerId,
        edges: Vec<ActionEdge>,
    },
    Chance {
        edges: Vec<ChanceEdge>,
    },
    Terminal {
        payoffs: PayoffVector,
    },
}

#[derive(Clone, Debug, PartialEq)]
pub struct Game {
    pub root: NodeId,
    pub nodes: BTreeMap<NodeId, Node>,
}

pub const GAME_SPEC_SCHEMA_VERSION: &str = "1.0.0";

#[derive(Clone, Debug, PartialEq)]
pub struct GameSpecification {
    pub schema_version: String,
    pub id: String,
    pub game: Game,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum ValidationError {
    EmptyIdentifier { path: String },
    UnsupportedSchemaVersion { path: String, value: String },
    MissingRoot(NodeId),
    MissingTarget { from: NodeId, target: NodeId },
    EmptyDecision(NodeId),
    DuplicateAction { node: NodeId, action: ActionId },
    EmptyChance(NodeId),
    InvalidProbability(NodeId),
    ProbabilityMass(NodeId),
    InvalidPayoff { node: NodeId, player: PlayerId },
    Cycle(NodeId),
    UnreachableNode(NodeId),
}

impl fmt::Display for ValidationError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{self:?}")
    }
}

impl std::error::Error for ValidationError {}

impl ValidationError {
    #[must_use]
    pub fn code(&self) -> &'static str {
        match self {
            Self::EmptyIdentifier { .. } => "empty_identifier",
            Self::UnsupportedSchemaVersion { .. } => "unsupported_schema_version",
            Self::MissingRoot(_) => "missing_root",
            Self::MissingTarget { .. } => "missing_target",
            Self::EmptyDecision(_) => "empty_decision",
            Self::DuplicateAction { .. } => "duplicate_action",
            Self::EmptyChance(_) => "empty_chance",
            Self::InvalidProbability(_) => "invalid_probability",
            Self::ProbabilityMass(_) => "probability_mass",
            Self::InvalidPayoff { .. } => "invalid_payoff",
            Self::Cycle(_) => "cycle",
            Self::UnreachableNode(_) => "unreachable_node",
        }
    }

    #[must_use]
    pub fn path(&self) -> String {
        match self {
            Self::EmptyIdentifier { path } | Self::UnsupportedSchemaVersion { path, .. } => {
                path.clone()
            }
            Self::MissingTarget { from, target } => {
                format!("game.nodes.{}.target.{}", from.0, target.0)
            }
            Self::MissingRoot(node)
            | Self::EmptyDecision(node)
            | Self::DuplicateAction { node, .. }
            | Self::EmptyChance(node)
            | Self::InvalidProbability(node)
            | Self::ProbabilityMass(node)
            | Self::InvalidPayoff { node, .. }
            | Self::Cycle(node)
            | Self::UnreachableNode(node) => format!("game.nodes.{}", node.0),
        }
    }
}

impl GameSpecification {
    /// Validate specification metadata and the embedded game graph.
    ///
    /// # Errors
    ///
    /// Returns a structured [`ValidationError`] for unsupported schema
    /// versions, empty canonical identifiers, or invalid game semantics.
    pub fn validate(&self) -> Result<(), ValidationError> {
        if self.schema_version != GAME_SPEC_SCHEMA_VERSION {
            return Err(ValidationError::UnsupportedSchemaVersion {
                path: "schema_version".into(),
                value: self.schema_version.clone(),
            });
        }
        Game::ensure_identifier("id", &self.id)?;
        self.game.validate()
    }
}

impl Game {
    /// # Errors
    ///
    /// Returns a [`ValidationError`] when the game graph references a missing
    /// node, contains a cycle, or otherwise violates the supported finite-game
    /// contract.
    pub fn validate(&self) -> Result<(), ValidationError> {
        Self::ensure_identifier("root", &self.root.0)?;
        if !self.nodes.contains_key(&self.root) {
            return Err(ValidationError::MissingRoot(self.root.clone()));
        }
        for (node_id, node) in &self.nodes {
            Self::ensure_identifier("nodes", &node_id.0)?;
            match node {
                Node::Decision { player, edges } => {
                    Self::ensure_identifier("decision.player", &player.0)?;
                    if edges.is_empty() {
                        return Err(ValidationError::EmptyDecision(node_id.clone()));
                    }
                    let mut actions = BTreeSet::new();
                    for edge in edges {
                        Self::ensure_identifier("decision.action", &edge.action.0)?;
                        if !actions.insert(edge.action.clone()) {
                            return Err(ValidationError::DuplicateAction {
                                node: node_id.clone(),
                                action: edge.action.clone(),
                            });
                        }
                        self.ensure_target(node_id, &edge.target)?;
                    }
                }
                Node::Chance { edges } => {
                    if edges.is_empty() {
                        return Err(ValidationError::EmptyChance(node_id.clone()));
                    }
                    let mut total = 0.0;
                    for edge in edges {
                        if !edge.probability.is_finite() || edge.probability < 0.0 {
                            return Err(ValidationError::InvalidProbability(node_id.clone()));
                        }
                        total += edge.probability;
                        self.ensure_target(node_id, &edge.target)?;
                    }
                    if (total - 1.0).abs() > 1e-9 {
                        return Err(ValidationError::ProbabilityMass(node_id.clone()));
                    }
                }
                Node::Terminal { payoffs } => {
                    for (player, value) in payoffs {
                        Self::ensure_identifier("terminal.player", &player.0)?;
                        if !value.is_finite() {
                            return Err(ValidationError::InvalidPayoff {
                                node: node_id.clone(),
                                player: player.clone(),
                            });
                        }
                    }
                }
            }
        }
        let mut visiting = BTreeSet::new();
        let mut visited = BTreeSet::new();
        self.depth_first(&self.root, &mut visiting, &mut visited)?;
        if let Some(unreachable) = self
            .nodes
            .keys()
            .find(|node_id| !visited.contains(*node_id))
        {
            return Err(ValidationError::UnreachableNode(unreachable.clone()));
        }
        Ok(())
    }

    fn ensure_identifier(path: &str, value: &str) -> Result<(), ValidationError> {
        if value.trim().is_empty() {
            Err(ValidationError::EmptyIdentifier {
                path: path.to_owned(),
            })
        } else {
            Ok(())
        }
    }

    fn ensure_target(&self, from: &NodeId, target: &NodeId) -> Result<(), ValidationError> {
        if self.nodes.contains_key(target) {
            Ok(())
        } else {
            Err(ValidationError::MissingTarget {
                from: from.clone(),
                target: target.clone(),
            })
        }
    }

    fn depth_first(
        &self,
        node_id: &NodeId,
        visiting: &mut BTreeSet<NodeId>,
        visited: &mut BTreeSet<NodeId>,
    ) -> Result<(), ValidationError> {
        if visited.contains(node_id) {
            return Ok(());
        }
        if !visiting.insert(node_id.clone()) {
            return Err(ValidationError::Cycle(node_id.clone()));
        }
        let node = self.nodes.get(node_id).expect("validated node existence");
        match node {
            Node::Decision { edges, .. } => {
                for edge in edges {
                    self.depth_first(&edge.target, visiting, visited)?;
                }
            }
            Node::Chance { edges } => {
                for edge in edges {
                    self.depth_first(&edge.target, visiting, visited)?;
                }
            }
            Node::Terminal { .. } => {}
        }
        visiting.remove(node_id);
        visited.insert(node_id.clone());
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rejects_cycles() {
        let root = NodeId("root".into());
        let mut nodes = BTreeMap::new();
        nodes.insert(
            root.clone(),
            Node::Decision {
                player: PlayerId("p".into()),
                edges: vec![ActionEdge {
                    action: ActionId("again".into()),
                    target: root.clone(),
                }],
            },
        );
        let game = Game { root, nodes };
        assert!(matches!(game.validate(), Err(ValidationError::Cycle(_))));
    }

    #[test]
    fn rejects_duplicate_actions_at_a_decision_node() {
        let root = NodeId("root".into());
        let terminal = NodeId("terminal".into());
        let action = ActionId("same".into());
        let game = Game {
            root: root.clone(),
            nodes: BTreeMap::from([
                (
                    root.clone(),
                    Node::Decision {
                        player: PlayerId("player".into()),
                        edges: vec![
                            ActionEdge {
                                action: action.clone(),
                                target: terminal.clone(),
                            },
                            ActionEdge {
                                action: action.clone(),
                                target: terminal.clone(),
                            },
                        ],
                    },
                ),
                (
                    terminal,
                    Node::Terminal {
                        payoffs: BTreeMap::new(),
                    },
                ),
            ]),
        };
        assert_eq!(
            game.validate(),
            Err(ValidationError::DuplicateAction { node: root, action })
        );
    }

    #[test]
    fn rejects_unreachable_nodes_and_non_finite_payoffs() {
        let root = NodeId("root".into());
        let unreachable = NodeId("unreachable".into());
        let player = PlayerId("player".into());
        let invalid_payoff = Game {
            root: root.clone(),
            nodes: BTreeMap::from([(
                root.clone(),
                Node::Terminal {
                    payoffs: BTreeMap::from([(player.clone(), f64::NAN)]),
                },
            )]),
        };
        assert_eq!(
            invalid_payoff.validate(),
            Err(ValidationError::InvalidPayoff {
                node: root.clone(),
                player,
            })
        );

        let unreachable_game = Game {
            root: root.clone(),
            nodes: BTreeMap::from([
                (
                    root,
                    Node::Terminal {
                        payoffs: BTreeMap::new(),
                    },
                ),
                (
                    unreachable.clone(),
                    Node::Terminal {
                        payoffs: BTreeMap::new(),
                    },
                ),
            ]),
        };
        assert_eq!(
            unreachable_game.validate(),
            Err(ValidationError::UnreachableNode(unreachable))
        );
    }

    #[test]
    fn specification_metadata_is_versioned_and_errors_have_paths() {
        let root = NodeId("terminal".into());
        let game = Game {
            root: root.clone(),
            nodes: BTreeMap::from([(
                root,
                Node::Terminal {
                    payoffs: BTreeMap::new(),
                },
            )]),
        };
        let valid = GameSpecification {
            schema_version: GAME_SPEC_SCHEMA_VERSION.into(),
            id: "urn:uogto:game:fixture".into(),
            game: game.clone(),
        };
        assert_eq!(valid.validate(), Ok(()));

        let invalid = GameSpecification {
            schema_version: "2.0.0".into(),
            id: valid.id,
            game,
        };
        let error = invalid.validate().unwrap_err();
        assert_eq!(error.code(), "unsupported_schema_version");
        assert_eq!(error.path(), "schema_version");
    }
}
