use std::collections::BTreeMap;
use std::error::Error;

use new_drug_reimbursement_game::payoff_input::{PayoffBasis, ValuedPayoff};
use new_drug_reimbursement_game::voiage_input::{
    InformationContext, InformationMetric, InputError as VoiageInputError, PolicySelection,
    ResourceCost, Transfer, VoiageInput, VoiageValue, WelfareAssumptions, WelfareLedgerStage,
};
use paignia_core::PlayerId;

fn health_basis() -> PayoffBasis {
    PayoffBasis {
        unit: "net-QALY".into(),
        perspective: "funding-institution".into(),
    }
}

fn context(recipients: &[PlayerId]) -> InformationContext<'_> {
    InformationContext {
        design_id: "observe_then_decide",
        comparator_design_id: "withhold_signal",
        recipients,
        timing: "before_offer",
        disclosure: "recipient_only",
        commitment: Some("published_price_rule"),
        observation_model: "finite_clinical_signal_v1",
        selection: PolicySelection::DeclaredResponse {
            model: "offer_response_v1",
            policy: "disclosed_price_response",
        },
    }
}

fn input<'a>(basis: &'a PayoffBasis, recipients: &'a [PlayerId]) -> VoiageInput<'a> {
    VoiageInput {
        metric: InformationMetric::StrategicInformationValue,
        basis,
        target_actor: recipients.first(),
        context: context(recipients),
        valuation_revision: "valuations-v1",
        welfare: None,
        transfers: &[],
        costs: &[],
    }
}

fn report<'a>(input: &VoiageInput<'a>, payoff: &'a ValuedPayoff) -> VoiageValue<'a> {
    VoiageValue {
        metric: input.metric,
        design_id: input.context.design_id,
        comparator_design_id: input.context.comparator_design_id,
        target_actor: input.target_actor,
        value: payoff,
    }
}

#[test]
fn five_information_estimands_retain_their_distinct_labels() {
    assert_eq!(
        [
            InformationMetric::Evpi,
            InformationMetric::Evsi,
            InformationMetric::ResearchNetBenefit,
            InformationMetric::StrategicInformationValue,
            InformationMetric::SocialInformationValue,
        ]
        .map(InformationMetric::as_str),
        [
            "evpi",
            "evsi",
            "research_net_benefit",
            "strategic_information_value",
            "social_information_value",
        ]
    );
}

#[test]
fn signed_actor_value_retains_the_declared_information_use() -> Result<(), Box<dyn Error>> {
    let institution = PlayerId("institution".into());
    let recipients = [institution];
    let basis = PayoffBasis {
        unit: "cardinal-welfare-unit".into(),
        ..health_basis()
    };
    let input = input(&basis, &recipients);
    let payoff = ValuedPayoff {
        amount: -2.0,
        basis: basis.clone(),
        valuation_revision: "valuations-v1".into(),
    };
    let admitted = input.accept_value(&report(&input, &payoff))?;

    assert_eq!(admitted, &payoff);
    assert_eq!(admitted.amount.to_bits(), (-2.0_f64).to_bits());
    assert_eq!(input.context, context(&recipients));
    assert_eq!(input.target_actor, recipients.first());
    Ok(())
}

#[test]
fn social_value_keeps_weights_stage_transfers_and_resource_costs() -> Result<(), Box<dyn Error>> {
    let institution = PlayerId("institution".into());
    let public = PlayerId("public".into());
    let recipients = [institution.clone()];
    let basis = PayoffBasis {
        unit: "cardinal-welfare-unit".into(),
        perspective: "declared-social-welfare".into(),
    };
    let weights = BTreeMap::from([(institution.clone(), 1.0), (public.clone(), 1.0)]);
    let welfare = WelfareAssumptions {
        weights: &weights,
        ledger_stage: WelfareLedgerStage::PostTransfer,
        rationale: "Synthetic common-cardinal values",
    };
    let transfer = ValuedPayoff {
        amount: 1.0,
        basis: basis.clone(),
        valuation_revision: "transfer-v1".into(),
    };
    let cost = ValuedPayoff {
        amount: 0.5,
        basis: basis.clone(),
        valuation_revision: "resource-v1".into(),
    };
    let transfers = [Transfer {
        payer: &public,
        recipient: &institution,
        value: &transfer,
    }];
    let costs = [ResourceCost {
        actor: &institution,
        category: "information",
        value: &cost,
    }];
    let input = VoiageInput {
        metric: InformationMetric::SocialInformationValue,
        target_actor: None,
        context: InformationContext {
            design_id: "observe_with_accounting",
            ..context(&recipients)
        },
        welfare: Some(welfare),
        transfers: &transfers,
        costs: &costs,
        ..input(&basis, &recipients)
    };
    let social_value = ValuedPayoff {
        amount: 1.5,
        basis: basis.clone(),
        valuation_revision: "valuations-v1".into(),
    };
    assert_eq!(
        input.accept_value(&report(&input, &social_value))?,
        &social_value
    );
    assert_eq!(input.welfare, Some(welfare));
    assert_eq!(input.transfers[0].value, &transfer);
    assert_eq!(input.costs[0].value, &cost);
    assert_eq!(
        VoiageInput {
            welfare: None,
            ..input
        }
        .validate(),
        Err(VoiageInputError::WelfareRequired)
    );
    assert_eq!(
        VoiageInput {
            target_actor: Some(&institution),
            ..input
        }
        .validate(),
        Err(VoiageInputError::SocialActorTarget)
    );
    Ok(())
}

#[test]
fn result_admission_rejects_substituted_metric_comparison_basis_or_revision() {
    let recipients = [PlayerId("institution".into())];
    let basis = health_basis();
    let input = input(&basis, &recipients);
    let payoff = ValuedPayoff {
        amount: -2.0,
        basis: basis.clone(),
        valuation_revision: "valuations-v1".into(),
    };
    let result = report(&input, &payoff);
    assert_eq!(
        input.accept_value(&VoiageValue {
            metric: InformationMetric::Evpi,
            ..result
        }),
        Err(VoiageInputError::MetricMismatch)
    );
    assert_eq!(
        input.accept_value(&VoiageValue {
            comparator_design_id: "other_comparator",
            ..result
        }),
        Err(VoiageInputError::ComparisonMismatch)
    );
    let other_actor = PlayerId("manufacturer".into());
    assert_eq!(
        input.accept_value(&VoiageValue {
            target_actor: Some(&other_actor),
            ..result
        }),
        Err(VoiageInputError::ActorMismatch)
    );
    for other_basis in [
        PayoffBasis {
            perspective: "manufacturer".into(),
            ..basis.clone()
        },
        PayoffBasis {
            unit: "AUD-2026".into(),
            ..basis.clone()
        },
    ] {
        let foreign = ValuedPayoff {
            basis: other_basis,
            ..payoff.clone()
        };
        assert_eq!(
            input.accept_value(&report(&input, &foreign)),
            Err(VoiageInputError::BasisMismatch)
        );
    }
    let foreign = ValuedPayoff {
        valuation_revision: "valuations-v2".into(),
        ..payoff.clone()
    };
    assert_eq!(
        input.accept_value(&report(&input, &foreign)),
        Err(VoiageInputError::ValuationRevisionMismatch)
    );
    let nonfinite = ValuedPayoff {
        amount: f64::INFINITY,
        ..payoff
    };
    assert_eq!(
        input.accept_value(&report(&input, &nonfinite)),
        Err(VoiageInputError::NonFiniteValue)
    );
}

#[test]
fn context_requires_a_distinct_comparator_and_explicit_information_declarations() {
    let recipients = [PlayerId("institution".into())];
    let duplicate = [recipients[0].clone(), recipients[0].clone()];
    let basis = health_basis();
    let input = input(&basis, &recipients);
    let original = input.context;
    for (changed, expected, explanation) in [
        (
            InformationContext {
                comparator_design_id: original.design_id,
                ..original
            },
            VoiageInputError::SameDesignAndComparator,
            "the design and comparator must be distinct",
        ),
        (
            InformationContext {
                recipients: &duplicate,
                ..original
            },
            VoiageInputError::InvalidRecipients,
            "recipients need distinct declared identities",
        ),
        (
            InformationContext {
                observation_model: " ",
                ..original
            },
            VoiageInputError::InvalidDeclaration("observation model"),
            "missing or invalid observation model",
        ),
        (
            InformationContext {
                commitment: Some(" "),
                ..original
            },
            VoiageInputError::InvalidDeclaration("commitment"),
            "missing or invalid commitment",
        ),
        (
            InformationContext {
                selection: PolicySelection::RecomputedFiniteNash {
                    policy: "declared_equilibrium",
                    selection_rule: "",
                    receipt_revision: "catalogue-v1",
                },
                ..original
            },
            VoiageInputError::InvalidDeclaration("equilibrium selection rule"),
            "missing or invalid equilibrium selection rule",
        ),
    ] {
        let observed = VoiageInput {
            context: changed,
            ..input
        }
        .validate()
        .unwrap_err();
        assert_eq!(observed, expected);
        assert_eq!(observed.to_string(), explanation);
    }
    assert_eq!(
        VoiageInput {
            target_actor: None,
            ..input
        }
        .validate(),
        Err(VoiageInputError::ActorRequired)
    );
}

#[test]
fn each_policy_selection_mode_retains_its_declared_evidence() {
    let recipients = [PlayerId("institution".into())];
    let basis = health_basis();
    let input = input(&basis, &recipients);
    for selection in [
        PolicySelection::Fixed {
            policy: "status_quo",
        },
        PolicySelection::Centralized {
            objective: "declared_welfare",
            tie_rule: "stable_policy_id",
        },
        PolicySelection::RecomputedFiniteNash {
            policy: "selected_equilibrium",
            selection_rule: "declared_focal_policy",
            receipt_revision: "catalogue-v1",
        },
        input.context.selection,
    ] {
        let changed = VoiageInput {
            context: InformationContext {
                selection,
                ..input.context
            },
            ..input
        };
        assert_eq!(changed.validate(), Ok(()));
        assert_eq!(changed.context.selection, selection);
    }
}

#[test]
fn malformed_welfare_and_accounts_have_distinct_failures() {
    let institution = PlayerId("institution".into());
    let firm = PlayerId("manufacturer".into());
    let recipients = [institution.clone()];
    let basis = health_basis();
    let input = input(&basis, &recipients);
    let weights = BTreeMap::from([(institution.clone(), 1.0), (firm.clone(), f64::NAN)]);
    assert_eq!(
        VoiageInput {
            welfare: Some(WelfareAssumptions {
                weights: &weights,
                ledger_stage: WelfareLedgerStage::PreTransfer,
                rationale: "common units",
            }),
            ..input
        }
        .validate(),
        Err(VoiageInputError::InvalidWelfare)
    );

    let amount = ValuedPayoff {
        amount: -1.0,
        basis: basis.clone(),
        valuation_revision: "ledger-v1".into(),
    };
    assert_eq!(
        VoiageInput {
            transfers: &[Transfer {
                payer: &firm,
                recipient: &institution,
                value: &amount,
            }],
            ..input
        }
        .validate(),
        Err(VoiageInputError::InvalidTransfer)
    );
    assert_eq!(
        VoiageInput {
            costs: &[ResourceCost {
                actor: &institution,
                category: "information",
                value: &amount,
            }],
            ..input
        }
        .validate(),
        Err(VoiageInputError::InvalidCost)
    );
}
