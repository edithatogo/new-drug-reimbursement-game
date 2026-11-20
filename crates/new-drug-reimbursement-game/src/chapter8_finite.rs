//! The application-owned finite offer menu for Pekarsky Chapter 8 Game 1.

use std::{collections::BTreeMap, fmt};

use paignia_core::{
    ActionEdge, ActionId, Game, GameSpecification, Node, NodeId, PlayerId, ResultIdentityRecord,
    GAME_SPEC_SCHEMA_VERSION,
};

use crate::payoff_input::{
    solve_valued_game, PayoffBasis, PayoffInputError, TerminalValuations, ValuedPayoff,
    ValuedSolution,
};
use crate::{
    net_economic_benefit_health, valid_game1_domain, Chapter8Game1Equilibrium, OpportunitySet,
};

const ACCEPT: &str = "accept";
const REJECT: &str = "reject";

/// Fixed-budget Game 1 inputs and the finite menu of currency-per-health offers.
#[derive(Clone, Copy, Debug)]
pub struct Chapter8FiniteInputs<'a> {
    pub incremental_health_effect: f64,
    pub opportunities: OpportunitySet,
    pub offers: &'a [f64],
    pub currency_unit: &'a str,
    pub health_unit: &'a str,
    pub valuation_revision: &'a str,
}

#[derive(Debug)]
pub struct Chapter8FiniteOutcome {
    pub equilibrium: Chapter8Game1Equilibrium,
    pub reimbursed: bool,
    pub valued: ValuedSolution,
}

#[derive(Debug)]
pub enum Chapter8FiniteError {
    OutsideSourceModel,
    InvalidOfferMenu,
    InvalidOfferValuation { index: usize },
    PayoffInput(PayoffInputError),
    MissingApplicationOutcome,
}

impl fmt::Display for Chapter8FiniteError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::OutsideSourceModel => {
                formatter.write_str("inputs are outside fixed-budget Chapter 8 Game 1")
            }
            Self::InvalidOfferMenu => {
                formatter.write_str("offer menu must contain distinct positive finite prices")
            }
            Self::InvalidOfferValuation { index } => write!(
                formatter,
                "offer at index {index} has an unsupported payoff"
            ),
            Self::PayoffInput(error) => error.fmt(formatter),
            Self::MissingApplicationOutcome => {
                formatter.write_str("the policy lacks the expected application outcome")
            }
        }
    }
}

impl std::error::Error for Chapter8FiniteError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::PayoffInput(error) => Some(error),
            _ => None,
        }
    }
}

/// Solve the finite restriction of Pekarsky (2015) Chapter 8 Game 1 through
/// Paignia. This uses zero incremental manufacturing cost, public parameters
/// and the application's net economic benefit in health for each offer.
///
/// # Errors
/// Returns an error for unsupported source-model inputs, invalid offers or
/// payoffs, provider admission failure, or missing application result fields.
pub fn solve_finite_game1(
    inputs: Chapter8FiniteInputs<'_>,
    identities: ResultIdentityRecord,
) -> Result<Chapter8FiniteOutcome, Chapter8FiniteError> {
    if !valid_game1_domain(inputs.incremental_health_effect, inputs.opportunities) {
        return Err(Chapter8FiniteError::OutsideSourceModel);
    }
    if inputs.offers.is_empty() {
        return Err(Chapter8FiniteError::InvalidOfferMenu);
    }
    let firm = PlayerId("firm".into());
    let institution = PlayerId("institution".into());
    let basis = BTreeMap::from([
        (
            firm.clone(),
            PayoffBasis {
                unit: inputs.currency_unit.into(),
                perspective: "manufacturing-firm".into(),
            },
        ),
        (
            institution.clone(),
            PayoffBasis {
                unit: inputs.health_unit.into(),
                perspective: "funding-institution".into(),
            },
        ),
    ]);
    let FiniteOfferGraph {
        game,
        valuations,
        offers,
    } = build_offer_graph(inputs, &firm, &institution, &basis)?;
    let root = game.root.clone();
    let specification = GameSpecification {
        schema_version: GAME_SPEC_SCHEMA_VERSION.into(),
        id: identities.specification_id.0.clone(),
        game,
    };
    let valued = solve_valued_game(specification, identities, &basis, valuations)
        .map_err(Chapter8FiniteError::PayoffInput)?;
    let missing = || Chapter8FiniteError::MissingApplicationOutcome;
    let policy = valued
        .policy
        .envelope
        .solutions
        .first()
        .ok_or_else(missing)?;
    let (price, response) = policy
        .choices
        .get(&root)
        .and_then(|offer| offers.get(offer))
        .ok_or_else(missing)?;
    let reimbursed = match policy.choices.get(response).map(|action| action.0.as_str()) {
        Some(ACCEPT) => true,
        Some(REJECT) => false,
        _ => return Err(missing()),
    };
    let expected = &policy.expected_payoffs;
    let equilibrium = Chapter8Game1Equilibrium {
        offered_iper: *price,
        firm_economic_rent: *expected.get(&firm).ok_or_else(missing)?,
        institution_nebh: *expected.get(&institution).ok_or_else(missing)?,
    };
    Ok(Chapter8FiniteOutcome {
        equilibrium,
        reimbursed,
        valued,
    })
}

struct FiniteOfferGraph {
    game: Game,
    valuations: TerminalValuations,
    offers: BTreeMap<ActionId, (f64, NodeId)>,
}

fn build_offer_graph(
    inputs: Chapter8FiniteInputs<'_>,
    firm: &PlayerId,
    institution: &PlayerId,
    basis: &BTreeMap<PlayerId, PayoffBasis>,
) -> Result<FiniteOfferGraph, Chapter8FiniteError> {
    let valued = |player: &PlayerId, amount| ValuedPayoff {
        amount,
        basis: basis[player].clone(),
        valuation_revision: inputs.valuation_revision.into(),
    };
    let payoffs = |revenue, health| {
        BTreeMap::from([
            (firm.clone(), valued(firm, revenue)),
            (institution.clone(), valued(institution, health)),
        ])
    };
    let terminal = || Node::Terminal {
        payoffs: BTreeMap::new(),
    };
    let rejected = NodeId("rejected".into());
    let mut nodes = BTreeMap::from([(rejected.clone(), terminal())]);
    let mut valuations = BTreeMap::from([(rejected.clone(), payoffs(0.0, 0.0))]);
    let mut offers = BTreeMap::new();
    let mut edges = Vec::with_capacity(inputs.offers.len());
    for (index, &price) in inputs.offers.iter().enumerate() {
        if !price.is_finite() || price <= 0.0 {
            return Err(Chapter8FiniteError::InvalidOfferMenu);
        }
        let price_id = format!("{:016x}", price.to_bits());
        let action = ActionId(format!("offer/{price_id}"));
        let response = NodeId(format!("response/{price_id}"));
        if offers
            .insert(action.clone(), (price, response.clone()))
            .is_some()
        {
            return Err(Chapter8FiniteError::InvalidOfferMenu);
        }
        let accepted = NodeId(format!("accepted/{price_id}"));
        let cost = price * inputs.incremental_health_effect;
        let health = net_economic_benefit_health(
            cost,
            inputs.incremental_health_effect,
            inputs.opportunities,
        )
        .ok_or(Chapter8FiniteError::InvalidOfferValuation { index })?;
        nodes.insert(accepted.clone(), terminal());
        valuations.insert(accepted.clone(), payoffs(cost, health));
        nodes.insert(
            response.clone(),
            Node::Decision {
                player: institution.clone(),
                edges: vec![
                    ActionEdge {
                        action: ActionId(ACCEPT.into()),
                        target: accepted,
                    },
                    ActionEdge {
                        action: ActionId(REJECT.into()),
                        target: rejected.clone(),
                    },
                ],
            },
        );
        edges.push(ActionEdge {
            action,
            target: response,
        });
    }
    let root = NodeId("firm-offer".into());
    nodes.insert(
        root.clone(),
        Node::Decision {
            player: firm.clone(),
            edges,
        },
    );
    Ok(FiniteOfferGraph {
        game: Game { root, nodes },
        valuations,
        offers,
    })
}
