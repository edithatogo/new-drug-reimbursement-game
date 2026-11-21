//! Application declarations for a valued comparison evaluated by Voiage.

pub mod replicates;

use std::collections::{BTreeMap, BTreeSet};
use std::fmt;

use paignia_core::PlayerId;

use crate::payoff_input::{declared_label, PayoffBasis, ValuedPayoff};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum InformationMetric {
    Evpi,
    Evsi,
    ResearchNetBenefit,
    StrategicInformationValue,
    SocialInformationValue,
}

impl InformationMetric {
    /// The application contract label for this estimand.
    #[must_use]
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Evpi => "evpi",
            Self::Evsi => "evsi",
            Self::ResearchNetBenefit => "research_net_benefit",
            Self::StrategicInformationValue => "strategic_information_value",
            Self::SocialInformationValue => "social_information_value",
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum PolicySelection<'a> {
    Fixed {
        policy: &'a str,
    },
    Centralized {
        objective: &'a str,
        tie_rule: &'a str,
    },
    DeclaredResponse {
        model: &'a str,
        policy: &'a str,
    },
    /// References an equilibrium receipt admitted at the provider boundary.
    RecomputedFiniteNash {
        policy: &'a str,
        selection_rule: &'a str,
        receipt_revision: &'a str,
    },
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct InformationContext<'a> {
    pub design_id: &'a str,
    pub comparator_design_id: &'a str,
    pub recipients: &'a [PlayerId],
    pub timing: &'a str,
    pub disclosure: &'a str,
    pub commitment: Option<&'a str>,
    pub observation_model: &'a str,
    pub selection: PolicySelection<'a>,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum WelfareLedgerStage {
    PreTransfer,
    PostTransfer,
}

/// Declared cardinally comparable utilities and the ledger used to weight them.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct WelfareAssumptions<'a> {
    pub weights: &'a BTreeMap<PlayerId, f64>,
    pub ledger_stage: WelfareLedgerStage,
    pub rationale: &'a str,
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Transfer<'a> {
    pub payer: &'a PlayerId,
    pub recipient: &'a PlayerId,
    pub value: &'a ValuedPayoff,
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct ResourceCost<'a> {
    pub actor: &'a PlayerId,
    pub category: &'a str,
    pub value: &'a ValuedPayoff,
}

/// The application-owned meaning and valuation basis of a provider request.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct VoiageInput<'a> {
    pub metric: InformationMetric,
    pub basis: &'a PayoffBasis,
    pub target_actor: Option<&'a PlayerId>,
    pub context: InformationContext<'a>,
    pub valuation_revision: &'a str,
    pub welfare: Option<WelfareAssumptions<'a>>,
    pub transfers: &'a [Transfer<'a>],
    pub costs: &'a [ResourceCost<'a>],
}

/// One value projected from the provider result with its comparison labels.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct VoiageValue<'a> {
    pub metric: InformationMetric,
    pub design_id: &'a str,
    pub comparator_design_id: &'a str,
    pub target_actor: Option<&'a PlayerId>,
    pub value: &'a ValuedPayoff,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum InputError {
    InvalidDeclaration(&'static str),
    SameDesignAndComparator,
    InvalidRecipients,
    ActorRequired,
    WelfareRequired,
    SocialActorTarget,
    InvalidWelfare,
    InvalidTransfer,
    InvalidCost,
    MetricMismatch,
    ComparisonMismatch,
    ActorMismatch,
    BasisMismatch,
    ValuationRevisionMismatch,
    NonFiniteValue,
}

impl fmt::Display for InputError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        let message = match self {
            Self::InvalidDeclaration(field) => {
                return write!(formatter, "missing or invalid {field}");
            }
            Self::SameDesignAndComparator => "the design and comparator must be distinct",
            Self::InvalidRecipients => "recipients need distinct declared identities",
            Self::ActorRequired => "strategic information value needs a target actor",
            Self::WelfareRequired => "social information value needs declared welfare weights",
            Self::SocialActorTarget => "social information value uses the declared welfare group",
            Self::InvalidWelfare => {
                "welfare needs a rationale, finite nonnegative weights and a positive weight"
            }
            Self::InvalidTransfer => {
                "transfers need distinct actors and a valued nonnegative amount"
            }
            Self::InvalidCost => "costs need an actor, category and valued nonnegative amount",
            Self::MetricMismatch => "the reported information metric differs from the declaration",
            Self::ComparisonMismatch => {
                "the reported design comparison differs from the declaration"
            }
            Self::ActorMismatch => "the reported actor differs from the declaration",
            Self::BasisMismatch => "the payoff unit or perspective differs from the declaration",
            Self::ValuationRevisionMismatch => {
                "the valuation revision differs from the declaration"
            }
            Self::NonFiniteValue => "the reported information value must be finite",
        };
        formatter.write_str(message)
    }
}

impl std::error::Error for InputError {}

impl InformationContext<'_> {
    fn validate(&self) -> Result<(), InputError> {
        require_labels(&[
            ("design ID", self.design_id),
            ("comparator design ID", self.comparator_design_id),
            ("information timing", self.timing),
            ("disclosure rule", self.disclosure),
            ("observation model", self.observation_model),
        ])?;
        if self.design_id == self.comparator_design_id {
            return Err(InputError::SameDesignAndComparator);
        }
        if let Some(commitment) = self.commitment {
            require_labels(&[("commitment", commitment)])?;
        }
        let mut recipients = BTreeSet::new();
        for recipient in self.recipients {
            if !declared_label(&recipient.0) || !recipients.insert(recipient) {
                return Err(InputError::InvalidRecipients);
            }
        }
        match self.selection {
            PolicySelection::Fixed { policy } => require_labels(&[("fixed policy", policy)]),
            PolicySelection::Centralized {
                objective,
                tie_rule,
            } => require_labels(&[
                ("policy objective", objective),
                ("policy tie rule", tie_rule),
            ]),
            PolicySelection::DeclaredResponse { model, policy } => {
                require_labels(&[("response model", model), ("response policy", policy)])
            }
            PolicySelection::RecomputedFiniteNash {
                policy,
                selection_rule,
                receipt_revision,
            } => require_labels(&[
                ("selected equilibrium policy", policy),
                ("equilibrium selection rule", selection_rule),
                ("equilibrium receipt revision", receipt_revision),
            ]),
        }
    }
}

impl VoiageInput<'_> {
    /// Validate the application declaration before requesting a provider value.
    ///
    /// # Errors
    ///
    /// Returns an error for ambiguous information use, missing welfare or actor
    /// declarations, invalid accounting or missing valuation provenance.
    pub fn validate(&self) -> Result<(), InputError> {
        self.context.validate()?;
        require_labels(&[
            ("payoff unit", &self.basis.unit),
            ("payoff perspective", &self.basis.perspective),
            ("valuation revision", self.valuation_revision),
        ])?;
        if let Some(actor) = self.target_actor {
            require_labels(&[("target actor", &actor.0)])?;
        }
        match self.metric {
            InformationMetric::StrategicInformationValue if self.target_actor.is_none() => {
                return Err(InputError::ActorRequired);
            }
            InformationMetric::SocialInformationValue if self.welfare.is_none() => {
                return Err(InputError::WelfareRequired);
            }
            InformationMetric::SocialInformationValue if self.target_actor.is_some() => {
                return Err(InputError::SocialActorTarget);
            }
            _ => {}
        }
        if let Some(welfare) = self.welfare {
            if !declared_label(welfare.rationale)
                || !welfare.weights.values().any(|weight| *weight > 0.0)
                || welfare.weights.iter().any(|(actor, weight)| {
                    !declared_label(&actor.0) || !weight.is_finite() || *weight < 0.0
                })
            {
                return Err(InputError::InvalidWelfare);
            }
        }
        for transfer in self.transfers {
            if transfer.payer == transfer.recipient
                || !declared_label(&transfer.payer.0)
                || !declared_label(&transfer.recipient.0)
                || !nonnegative_valuation(transfer.value)
            {
                return Err(InputError::InvalidTransfer);
            }
        }
        for cost in self.costs {
            if !declared_label(&cost.actor.0)
                || !declared_label(cost.category)
                || !nonnegative_valuation(cost.value)
            {
                return Err(InputError::InvalidCost);
            }
        }
        Ok(())
    }

    /// Bind an already qualified provider value to the exact requested
    /// estimand, comparison, actor and valuation basis, retaining its sign.
    ///
    /// # Errors
    ///
    /// Returns an error for an invalid request, a mismatched report, or a
    /// non-finite amount.
    pub fn accept_value<'a>(
        &self,
        report: &VoiageValue<'a>,
    ) -> Result<&'a ValuedPayoff, InputError> {
        self.validate()?;
        if report.metric != self.metric {
            return Err(InputError::MetricMismatch);
        }
        if report.design_id != self.context.design_id
            || report.comparator_design_id != self.context.comparator_design_id
        {
            return Err(InputError::ComparisonMismatch);
        }
        if report.target_actor != self.target_actor {
            return Err(InputError::ActorMismatch);
        }
        if &report.value.basis != self.basis {
            return Err(InputError::BasisMismatch);
        }
        if report.value.valuation_revision != self.valuation_revision {
            return Err(InputError::ValuationRevisionMismatch);
        }
        if !report.value.amount.is_finite() {
            return Err(InputError::NonFiniteValue);
        }
        Ok(report.value)
    }
}

fn require_labels(fields: &[(&'static str, &str)]) -> Result<(), InputError> {
    for &(field, value) in fields {
        if !declared_label(value) {
            return Err(InputError::InvalidDeclaration(field));
        }
    }
    Ok(())
}

fn nonnegative_valuation(value: &ValuedPayoff) -> bool {
    value.amount.is_finite()
        && value.amount >= 0.0
        && declared_label(&value.basis.unit)
        && declared_label(&value.basis.perspective)
        && declared_label(&value.valuation_revision)
}
