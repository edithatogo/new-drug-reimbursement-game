//! Application admission of a static Paignia result for a declared use.

use std::fmt;

use paignia_core::{
    GameSpecification, ResultEnvelope, ResultEnvelopeError, ResultIdentityRecord, ResultStatus,
};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ResultUse {
    ContingentPolicy,
    ExhaustiveCatalogue,
}

#[derive(Debug, Eq, PartialEq)]
pub enum AcceptanceError {
    InvalidEnvelope(ResultEnvelopeError),
    IdentityMismatch,
    Incomplete {
        status: ResultStatus,
        detail: Option<String>,
    },
    ExhaustiveCatalogueUnavailable,
}

impl fmt::Display for AcceptanceError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::InvalidEnvelope(error) => error.fmt(formatter),
            Self::IdentityMismatch => write!(
                formatter,
                "result differs from the requested identity binding"
            ),
            Self::Incomplete { status, detail } => {
                write!(formatter, "Paignia reported {status:?}")?;
                if let Some(detail) = detail {
                    write!(formatter, " ({detail})")?;
                }
                Ok(())
            }
            Self::ExhaustiveCatalogueUnavailable => {
                write!(
                    formatter,
                    "an exhaustive catalogue is unavailable for this result"
                )
            }
        }
    }
}

impl std::error::Error for AcceptanceError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::InvalidEnvelope(error) => Some(error),
            _ => None,
        }
    }
}

/// Admit the exact completed result for the requested application use.
///
/// # Errors
/// Returns a typed failure for invalid or foreign result envelopes, incomplete
/// outcomes, or a claim of exhaustive enumeration for the static policy.
pub fn accept(
    envelope: &ResultEnvelope,
    specification: &GameSpecification,
    expected: &ResultIdentityRecord,
    requested_use: ResultUse,
) -> Result<(), AcceptanceError> {
    envelope
        .validate_against(specification, &expected.game_instance_id)
        .map_err(AcceptanceError::InvalidEnvelope)?;
    if &envelope.identities != expected {
        return Err(AcceptanceError::IdentityMismatch);
    }
    if envelope.status != ResultStatus::Completed {
        return Err(AcceptanceError::Incomplete {
            status: envelope.status,
            detail: envelope.status_detail.clone(),
        });
    }
    if requested_use == ResultUse::ExhaustiveCatalogue {
        return Err(AcceptanceError::ExhaustiveCatalogueUnavailable);
    }
    Ok(())
}
