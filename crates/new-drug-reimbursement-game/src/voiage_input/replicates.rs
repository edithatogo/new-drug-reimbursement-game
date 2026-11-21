//! Bind reported simulation draws to the independently declared sampling plan.

use std::collections::{BTreeMap, BTreeSet};
use std::fmt;

use crate::payoff_input::declared_label;

/// Coordinates conditional on one parameter draw.
#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
pub struct InnerIdentity<'a> {
    pub model_id: &'a str,
    pub equilibrium_id: Option<&'a str>,
    pub measurement_id: Option<&'a str>,
    pub replicate_id: &'a str,
}

impl InnerIdentity<'_> {
    fn is_declared(&self) -> bool {
        [
            Some(self.model_id),
            self.equilibrium_id,
            self.measurement_id,
            Some(self.replicate_id),
        ]
        .into_iter()
        .flatten()
        .all(declared_label)
    }
}

/// One paired outcome draw. Its strategy rows share this identity.
#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
pub struct DrawIdentity<'a> {
    pub parameter_draw_id: &'a str,
    pub inner: InnerIdentity<'a>,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct DeclaredParameterDraw<'a> {
    pub id: &'a str,
    pub replicates: &'a [InnerIdentity<'a>],
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum SamplingPrecision {
    ExactEnumeration,
    MonteCarlo { standard_error: Option<f64> },
}

/// The parameter and replicate coordinates declared for the producer run.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct DrawPlan<'a> {
    pub producer_run_id: &'a str,
    pub parameter_draws: &'a [DeclaredParameterDraw<'a>],
    pub precision: SamplingPrecision,
}

/// Identities reported by the producer, in its original order.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct RecordedDraws<'a> {
    pub producer_run_id: &'a str,
    pub draws: &'a [DrawIdentity<'a>],
}

#[derive(Clone, Debug, PartialEq)]
pub struct DrawReceipt<'a> {
    pub recorded: RecordedDraws<'a>,
    pub inner_budgets: BTreeMap<&'a str, usize>,
    pub precision: SamplingPrecision,
}

impl DrawReceipt<'_> {
    /// Number of admitted parameter draws in the outer calculation.
    #[must_use]
    pub fn outer_budget(&self) -> usize {
        self.inner_budgets.len()
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum DrawIdentityError {
    RunMismatch,
    EmptyPlan,
    InvalidParameterDraw,
    DuplicateParameterDraw,
    EmptyReplicateSet,
    InvalidInnerIdentity,
    DuplicatePlannedReplicate,
    UnknownParameterDraw,
    UnplannedInnerIdentity,
    DuplicateOutcome,
    MissingOutcome,
    InvalidPrecision,
}

impl fmt::Display for DrawIdentityError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        let message = match self {
            Self::RunMismatch => "the recorded draws must match the declared producer run",
            Self::EmptyPlan => "the sampling plan needs at least one parameter draw",
            Self::InvalidParameterDraw => "the parameter draw identity is invalid",
            Self::DuplicateParameterDraw => "the sampling plan repeats a parameter draw identity",
            Self::EmptyReplicateSet => "each parameter draw needs at least one planned replicate",
            Self::InvalidInnerIdentity => "the conditional draw identity is invalid",
            Self::DuplicatePlannedReplicate => "the sampling plan repeats a conditional draw",
            Self::UnknownParameterDraw => "an outcome refers to an undeclared parameter draw",
            Self::UnplannedInnerIdentity => "an outcome has undeclared conditional coordinates",
            Self::DuplicateOutcome => "the producer repeated a paired outcome draw",
            Self::MissingOutcome => "one or more planned paired outcomes are missing",
            Self::InvalidPrecision => "a Monte Carlo standard error must be finite and nonnegative",
        };
        formatter.write_str(message)
    }
}

impl std::error::Error for DrawIdentityError {}

impl<'a> DrawPlan<'a> {
    /// Bind exactly one outcome to each planned conditional draw. The original
    /// order and separate precision declaration remain available to the caller.
    ///
    /// # Errors
    ///
    /// Returns an error for a foreign producer run, invalid declarations,
    /// unknown coordinates, repeated draws or incomplete outcomes.
    pub fn accept(
        &self,
        recorded: RecordedDraws<'a>,
    ) -> Result<DrawReceipt<'a>, DrawIdentityError> {
        if !declared_label(self.producer_run_id) || self.producer_run_id != recorded.producer_run_id
        {
            return Err(DrawIdentityError::RunMismatch);
        }
        if matches!(
            self.precision,
            SamplingPrecision::MonteCarlo { standard_error: Some(error) }
                if !error.is_finite() || error < 0.0
        ) {
            return Err(DrawIdentityError::InvalidPrecision);
        }
        if self.parameter_draws.is_empty() {
            return Err(DrawIdentityError::EmptyPlan);
        }

        let mut expected = BTreeSet::new();
        let mut inner_budgets = BTreeMap::new();
        for parameter in self.parameter_draws {
            if !declared_label(parameter.id) {
                return Err(DrawIdentityError::InvalidParameterDraw);
            }
            if parameter.replicates.is_empty() {
                return Err(DrawIdentityError::EmptyReplicateSet);
            }
            if inner_budgets
                .insert(parameter.id, parameter.replicates.len())
                .is_some()
            {
                return Err(DrawIdentityError::DuplicateParameterDraw);
            }
            for &inner in parameter.replicates {
                if !inner.is_declared() {
                    return Err(DrawIdentityError::InvalidInnerIdentity);
                }
                if !expected.insert(DrawIdentity {
                    parameter_draw_id: parameter.id,
                    inner,
                }) {
                    return Err(DrawIdentityError::DuplicatePlannedReplicate);
                }
            }
        }

        let mut seen = BTreeSet::new();
        for draw in recorded.draws {
            if !inner_budgets.contains_key(draw.parameter_draw_id) {
                return Err(DrawIdentityError::UnknownParameterDraw);
            }
            if !expected.contains(draw) {
                return Err(DrawIdentityError::UnplannedInnerIdentity);
            }
            if !seen.insert(draw) {
                return Err(DrawIdentityError::DuplicateOutcome);
            }
        }
        if seen.len() != expected.len() {
            return Err(DrawIdentityError::MissingOutcome);
        }
        Ok(DrawReceipt {
            recorded,
            inner_budgets,
            precision: self.precision,
        })
    }
}
