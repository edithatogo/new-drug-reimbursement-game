//! The application-owned Chapter 8 fixed-budget model. The maintained example
//! uses synthetic inputs. The reference follows Pekarsky (2015), equation 8.2.

use new_drug_reimbursement_game::chapter8_finite::{
    solve_finite_game1, Chapter8FiniteError, Chapter8FiniteInputs,
};
use new_drug_reimbursement_game::OpportunitySet;
use paignia_core::{
    GameInstanceId, GameSpecificationId, ResultIdentityRecord, SolverRunId,
    RESULT_IDENTITY_SCHEMA_VERSION,
};

fn case(offers: &[f64]) -> Chapter8FiniteInputs<'_> {
    Chapter8FiniteInputs {
        incremental_health_effect: 10.0,
        opportunities: OpportunitySet {
            expansion_icer: Some(20_000.0),
            contraction_icer: Some(60_000.0),
            displacement_icer: Some(40_000.0),
            additional_best_productivity: 0.0,
        },
        offers,
        currency_unit: "example-currency-unit",
        health_unit: "example-net-health-unit",
        valuation_revision: "examples/cases/chapter8_example.json:synthetic-ch8-001",
    }
}

fn identities() -> ResultIdentityRecord {
    ResultIdentityRecord {
        schema_version: RESULT_IDENTITY_SCHEMA_VERSION.into(),
        specification_id: GameSpecificationId("urn:ndrg:chapter8:finite-offer:1".into()),
        game_instance_id: GameInstanceId("urn:ndrg:instance:synthetic-ch8-001".into()),
        solver_run_id: SolverRunId("urn:ndrg:run:chapter8-native-conformance".into()),
        session_id: None,
        policy_artifact_id: None,
        solver_trace_id: None,
    }
}

fn close(actual: f64, expected: f64, tolerance: f64) {
    assert!(
        (actual - expected).abs() <= tolerance,
        "{actual} vs {expected}"
    );
}

#[test]
fn chapter8_application_with_threshold_on_menu_matches_equation_8_2() {
    // Exact reciprocal threshold = (3 + 6 - 2) / 120000. The institution
    // receives 3 health units at the low quote and -17/6 at the high quote.
    let threshold = 120_000.0 / 7.0;
    let offers = [22_000.0, 12_000.0, threshold];
    let outcome = solve_finite_game1(case(&offers), identities()).unwrap();
    assert!(outcome.reimbursed);
    close(outcome.equilibrium.offered_iper, threshold, 1e-9);
    close(
        outcome.equilibrium.firm_economic_rent,
        1_200_000.0 / 7.0,
        1e-8,
    );
    close(outcome.equilibrium.institution_nebh, 0.0, 1e-12);
    assert_eq!(outcome.valued.policy.envelope.identities, identities());
    assert!(outcome
        .valued
        .valuations
        .values()
        .flatten()
        .all(|(_, payoff)| payoff.valuation_revision
            == "examples/cases/chapter8_example.json:synthetic-ch8-001"));
}

#[test]
fn finite_menu_below_threshold_selects_the_best_available_admitted_offer() {
    let outcome = solve_finite_game1(case(&[12_000.0, 22_000.0, 16_000.0]), identities()).unwrap();
    assert!(outcome.reimbursed);
    close(outcome.equilibrium.offered_iper, 16_000.0, 1e-9);
    close(outcome.equilibrium.firm_economic_rent, 160_000.0, 1e-8);
    close(outcome.equilibrium.institution_nebh, 2.0 / 3.0, 1e-12);
}

#[test]
fn no_reimbursable_offer_preserves_the_rejection_outcome() {
    let outcome = solve_finite_game1(case(&[23_000.0, 22_000.0]), identities()).unwrap();
    assert!(!outcome.reimbursed);
    close(outcome.equilibrium.offered_iper, 22_000.0, 0.0);
    close(outcome.equilibrium.firm_economic_rent, 0.0, 0.0);
    close(outcome.equilibrium.institution_nebh, 0.0, 0.0);
}

#[test]
fn rejects_out_of_profile_opportunities_and_invalid_offer_menus() {
    let mut unsupported = case(&[12_000.0]);
    unsupported.opportunities.additional_best_productivity = 1e-5;
    assert!(matches!(
        solve_finite_game1(unsupported, identities()),
        Err(Chapter8FiniteError::OutsideSourceModel)
    ));
    for offers in [&[][..], &[0.0], &[f64::NAN], &[12_000.0, 12_000.0]] {
        assert!(matches!(
            solve_finite_game1(case(offers), identities()),
            Err(Chapter8FiniteError::InvalidOfferMenu)
        ));
    }
}

#[test]
fn rejects_opportunities_whose_reciprocals_overflow() {
    let displacement = f64::MIN_POSITIVE / 4.0;
    let offers = [displacement];
    let mut inputs = case(&offers);
    inputs.incremental_health_effect = 1.0;
    inputs.opportunities = OpportunitySet {
        expansion_icer: Some(displacement / 2.0),
        contraction_icer: Some(displacement),
        displacement_icer: Some(displacement),
        additional_best_productivity: 0.0,
    };
    assert!(matches!(
        solve_finite_game1(inputs, identities()),
        Err(Chapter8FiniteError::OutsideSourceModel)
    ));
}

#[test]
fn near_tie_selection_is_invariant_to_offer_menu_order() {
    let h = 2.0_f64.powi(-40);
    for offers in [[h, 2.0 * h, 3.0 * h], [3.0 * h, 2.0 * h, h]] {
        let mut inputs = case(&offers);
        inputs.incremental_health_effect = 1.0;
        let outcome = solve_finite_game1(inputs, identities()).unwrap();
        assert!(outcome.reimbursed);
        close(outcome.equilibrium.offered_iper, 3.0 * h, 0.0);
    }
}
