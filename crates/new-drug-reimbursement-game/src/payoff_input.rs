//! Application-owned admission of valued payoffs for the static game.

use std::collections::BTreeMap;
use std::fmt;

use paignia_core::{
    GameSpecification, Node, NodeId, PlayerId, ResultIdentityRecord, STATIC_GAME_PROFILE_V1,
};
use paignia_solve::{
    backward_induction_result, BackwardInductionResult, ResultSolveError, SolverConfig,
};

use crate::paignia_acceptance::{accept, AcceptanceError, ResultUse};

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct PayoffBasis {
    pub unit: String,
    pub perspective: String,
}

#[derive(Clone, Debug, PartialEq)]
pub struct ValuedPayoff {
    pub amount: f64,
    pub basis: PayoffBasis,
    pub valuation_revision: String,
}

pub type TerminalValuations = BTreeMap<NodeId, BTreeMap<PlayerId, ValuedPayoff>>;

#[derive(Debug)]
pub struct ValuedSolution {
    pub policy: BackwardInductionResult,
    pub valuations: TerminalValuations,
}

#[derive(Debug)]
pub enum PayoffInputError {
    NoPlayerBasis,
    InvalidPlayerBasis { player: PlayerId },
    UnknownTerminal { node: NodeId },
    RawPayoffs { node: NodeId },
    PlayerPayoffSet { node: NodeId },
    UnitMismatch { node: NodeId, player: PlayerId },
    PerspectiveMismatch { node: NodeId, player: PlayerId },
    InvalidValue { node: NodeId, player: PlayerId },
    Solver(ResultSolveError),
    ResultAcceptance(AcceptanceError),
}

impl fmt::Display for PayoffInputError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::NoPlayerBasis => write!(formatter, "the game needs a payoff basis"),
            Self::InvalidPlayerBasis { player } => {
                write!(
                    formatter,
                    "missing or invalid payoff basis for {:?}",
                    player.0
                )
            }
            Self::UnknownTerminal { node } => {
                write!(
                    formatter,
                    "valuations reference a nonterminal node {:?}",
                    node.0
                )
            }
            Self::RawPayoffs { node } => {
                write!(formatter, "unvalued payoffs supplied at {:?}", node.0)
            }
            Self::PlayerPayoffSet { node } => {
                write!(
                    formatter,
                    "incomplete or undeclared player payoffs at {:?}",
                    node.0
                )
            }
            Self::UnitMismatch { node, player } => {
                write!(
                    formatter,
                    "payoff unit mismatch for {:?} at {:?}",
                    player.0, node.0
                )
            }
            Self::PerspectiveMismatch { node, player } => write!(
                formatter,
                "payoff perspective mismatch for {:?} at {:?}",
                player.0, node.0
            ),
            Self::InvalidValue { node, player } => write!(
                formatter,
                "non-finite payoff or missing valuation revision for {:?} at {:?}",
                player.0, node.0
            ),
            Self::Solver(error) => error.fmt(formatter),
            Self::ResultAcceptance(error) => error.fmt(formatter),
        }
    }
}

impl std::error::Error for PayoffInputError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Solver(error) => Some(error),
            Self::ResultAcceptance(error) => Some(error),
            _ => None,
        }
    }
}

pub(crate) fn declared_label(label: &str) -> bool {
    !label.is_empty() && label.trim() == label
}

/// Solve a valued static game and return the inputs with their valuation revisions.
///
/// The versioned specification supplies decisions, chance nodes and empty
/// terminal payoff maps. The caller supplies the matching result identities.
/// The application supplies one exact unit and perspective for each player.
/// Every terminal needs one explicit valued payoff per declared player.
///
/// # Errors
///
/// Returns an application admission error for missing, incompatible or
/// non-finite payoffs before calling Paignia. Returns the native error for
/// rejected graph structure or solver failure.
pub fn solve_valued_game(
    mut specification: GameSpecification,
    identities: ResultIdentityRecord,
    basis: &BTreeMap<PlayerId, PayoffBasis>,
    valuations: TerminalValuations,
) -> Result<ValuedSolution, PayoffInputError> {
    if basis.is_empty() {
        return Err(PayoffInputError::NoPlayerBasis);
    }
    for (player, expected) in basis {
        if !declared_label(&expected.unit) || !declared_label(&expected.perspective) {
            return Err(PayoffInputError::InvalidPlayerBasis {
                player: player.clone(),
            });
        }
    }
    for node in valuations.keys() {
        if !matches!(
            specification.game.nodes.get(node),
            Some(Node::Terminal { .. })
        ) {
            return Err(PayoffInputError::UnknownTerminal { node: node.clone() });
        }
    }
    for (node, declaration) in &mut specification.game.nodes {
        match declaration {
            Node::Decision { player, .. } if !basis.contains_key(player) => {
                return Err(PayoffInputError::InvalidPlayerBasis {
                    player: player.clone(),
                });
            }
            Node::Terminal { payoffs } => {
                if !payoffs.is_empty() {
                    return Err(PayoffInputError::RawPayoffs { node: node.clone() });
                }
                let values = valuations
                    .get(node)
                    .filter(|values| values.keys().eq(basis.keys()))
                    .ok_or_else(|| PayoffInputError::PlayerPayoffSet { node: node.clone() })?;
                for (player, value) in values {
                    let expected = &basis[player];
                    if value.basis.unit != expected.unit {
                        return Err(PayoffInputError::UnitMismatch {
                            node: node.clone(),
                            player: player.clone(),
                        });
                    }
                    if value.basis.perspective != expected.perspective {
                        return Err(PayoffInputError::PerspectiveMismatch {
                            node: node.clone(),
                            player: player.clone(),
                        });
                    }
                    if !value.amount.is_finite() || !declared_label(&value.valuation_revision) {
                        return Err(PayoffInputError::InvalidValue {
                            node: node.clone(),
                            player: player.clone(),
                        });
                    }
                    payoffs.insert(player.clone(), value.amount);
                }
            }
            _ => {}
        }
    }
    let requested_identities = identities.clone();
    let policy = backward_induction_result(
        &specification,
        STATIC_GAME_PROFILE_V1,
        identities,
        SolverConfig::default(),
    )
    .map_err(PayoffInputError::Solver)?;
    accept(
        &policy.envelope,
        &specification,
        &requested_identities,
        ResultUse::ContingentPolicy,
    )
    .map_err(PayoffInputError::ResultAcceptance)?;
    Ok(ValuedSolution { policy, valuations })
}
