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

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum ValidationError {
    MissingRoot(NodeId),
    MissingTarget { from: NodeId, target: NodeId },
    EmptyDecision(NodeId),
    EmptyChance(NodeId),
    InvalidProbability(NodeId),
    ProbabilityMass(NodeId),
    Cycle(NodeId),
}

impl fmt::Display for ValidationError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{self:?}")
    }
}

impl std::error::Error for ValidationError {}

impl Game {
    pub fn validate(&self) -> Result<(), ValidationError> {
        if !self.nodes.contains_key(&self.root) {
            return Err(ValidationError::MissingRoot(self.root.clone()));
        }
        for (node_id, node) in &self.nodes {
            match node {
                Node::Decision { edges, .. } => {
                    if edges.is_empty() {
                        return Err(ValidationError::EmptyDecision(node_id.clone()));
                    }
                    for edge in edges {
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
                    if payoffs.values().any(|value| !value.is_finite()) {
                        return Err(ValidationError::InvalidProbability(node_id.clone()));
                    }
                }
            }
        }
        let mut visiting = BTreeSet::new();
        let mut visited = BTreeSet::new();
        self.depth_first(&self.root, &mut visiting, &mut visited)
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
}
