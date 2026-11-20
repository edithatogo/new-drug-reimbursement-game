use std::collections::BTreeMap;
use std::error::Error;

use new_drug_reimbursement_game::payoff_input::{
    solve_valued_game, PayoffBasis, PayoffInputError, TerminalValuations, ValuedPayoff,
};
use paignia_core::{
    ActionEdge, ActionId, Game, GameInstanceId, GameSpecification, GameSpecificationId, Node,
    NodeId, PlayerId, ResultIdentityRecord, ResultStatus, SolverRunId,
    RESULT_IDENTITY_SCHEMA_VERSION, STATIC_GAME_PROFILE_V1,
};
use paignia_solve::ResultSolveError;

fn bind(game: Game) -> (GameSpecification, ResultIdentityRecord) {
    let id = "urn:ndrg:test:valued-payoffs".to_string();
    (
        GameSpecification {
            schema_version: "1.0.0".into(),
            id: id.clone(),
            game,
        },
        ResultIdentityRecord {
            schema_version: RESULT_IDENTITY_SCHEMA_VERSION.into(),
            specification_id: GameSpecificationId(id),
            game_instance_id: GameInstanceId("urn:ndrg:test:valued-payoffs:instance".into()),
            solver_run_id: SolverRunId("urn:ndrg:test:valued-payoffs:run".into()),
            session_id: None,
            policy_artifact_id: None,
            solver_trace_id: None,
        },
    )
}

fn fixture() -> (
    GameSpecification,
    ResultIdentityRecord,
    BTreeMap<PlayerId, PayoffBasis>,
    TerminalValuations,
) {
    let firm = PlayerId("firm".into());
    let institution = PlayerId("institution".into());
    let offer = NodeId("offer".into());
    let accepted = NodeId("accepted".into());
    let rejected = NodeId("rejected".into());
    let basis = BTreeMap::from([
        (
            firm.clone(),
            PayoffBasis {
                unit: "AUD-2026".into(),
                perspective: "manufacturing-firm".into(),
            },
        ),
        (
            institution.clone(),
            PayoffBasis {
                unit: "net-QALY".into(),
                perspective: "funding-institution".into(),
            },
        ),
    ]);
    let valuation = |player: &PlayerId, amount, branch: &str| ValuedPayoff {
        amount,
        basis: basis[player].clone(),
        valuation_revision: format!("{branch}-{}-v1", player.0),
    };
    let terminal = || Node::Terminal {
        payoffs: BTreeMap::new(),
    };
    let game = Game {
        root: offer.clone(),
        nodes: BTreeMap::from([
            (
                offer,
                Node::Decision {
                    player: institution.clone(),
                    edges: vec![
                        ActionEdge {
                            action: ActionId("accept".into()),
                            target: accepted.clone(),
                        },
                        ActionEdge {
                            action: ActionId("reject".into()),
                            target: rejected.clone(),
                        },
                    ],
                },
            ),
            (accepted.clone(), terminal()),
            (rejected.clone(), terminal()),
        ]),
    };
    let payoffs = BTreeMap::from([
        (
            accepted,
            BTreeMap::from([
                (firm.clone(), valuation(&firm, 80_000.0, "accepted")),
                (
                    institution.clone(),
                    valuation(&institution, 0.8, "accepted"),
                ),
            ]),
        ),
        (
            rejected,
            BTreeMap::from([
                (firm.clone(), valuation(&firm, 0.0, "rejected")),
                (
                    institution.clone(),
                    valuation(&institution, 0.0, "rejected"),
                ),
            ]),
        ),
    ]);
    let (specification, identities) = bind(game);
    (specification, identities, basis, payoffs)
}

#[test]
fn matching_basis_reaches_native_solver_and_preserves_provenance() {
    let (specification, identities, basis, payoffs) = fixture();
    let expected_inputs = payoffs.clone();
    let result = solve_valued_game(specification, identities.clone(), &basis, payoffs).unwrap();
    assert_eq!(result.policy.envelope.status, ResultStatus::Completed);
    assert_eq!(result.policy.envelope.identities, identities);
    assert_eq!(
        result.policy.envelope.semantic_profile,
        STATIC_GAME_PROFILE_V1
    );
    assert_eq!(result.policy.envelope.solutions.len(), 1);
    let solution = &result.policy.envelope.solutions[0];

    assert_eq!(
        solution.choices[&NodeId("offer".into())],
        ActionId("accept".into())
    );
    assert!((solution.expected_payoffs[&PlayerId("firm".into())] - 80_000.0).abs() < 1e-9);
    assert!((solution.expected_payoffs[&PlayerId("institution".into())] - 0.8).abs() < 1e-12);
    assert_eq!(result.valuations, expected_inputs);
}

fn assert_input_diagnostic(error: &PayoffInputError, message: &str) {
    assert_eq!(error.to_string(), message);
    assert!(error.source().is_none());
}

#[test]
fn empty_invalid_and_missing_player_bases_fail_with_context() {
    let (specification, identities, mut basis, mut payoffs) = fixture();
    let error = solve_valued_game(
        specification.clone(),
        identities.clone(),
        &BTreeMap::new(),
        payoffs.clone(),
    )
    .unwrap_err();
    assert!(matches!(error, PayoffInputError::NoPlayerBasis));
    assert_input_diagnostic(&error, "the game needs a payoff basis");

    let institution = PlayerId("institution".into());
    let message = "missing or invalid payoff basis for \"institution\"";
    basis.get_mut(&institution).unwrap().perspective = " ".into();
    let error = solve_valued_game(
        specification.clone(),
        identities.clone(),
        &basis,
        payoffs.clone(),
    )
    .unwrap_err();
    assert!(
        matches!(&error, PayoffInputError::InvalidPlayerBasis { player } if player == &institution)
    );
    assert_input_diagnostic(&error, message);

    basis.remove(&institution);
    for values in payoffs.values_mut() {
        values.remove(&institution);
    }
    let error = solve_valued_game(specification, identities, &basis, payoffs).unwrap_err();
    assert!(
        matches!(&error, PayoffInputError::InvalidPlayerBasis { player } if player == &institution)
    );
    assert_input_diagnostic(&error, message);
}

#[test]
fn wrong_unit_and_wrong_perspective_are_rejected_before_the_solver() {
    let (mut specification, identities, basis, mut payoffs) = fixture();
    // Independently invalid for the native solver. The tagged value must be
    // rejected before the invalid graph reaches the solver.
    specification.game.root = NodeId("missing-root".into());
    let node = NodeId("accepted".into());
    let player = PlayerId("firm".into());
    let value = payoffs.get_mut(&node).unwrap().get_mut(&player).unwrap();
    value.basis.unit = "USD-2026".into();
    let error = solve_valued_game(
        specification.clone(),
        identities.clone(),
        &basis,
        payoffs.clone(),
    )
    .unwrap_err();
    assert!(matches!(error, PayoffInputError::UnitMismatch { .. }));
    assert_input_diagnostic(&error, "payoff unit mismatch for \"firm\" at \"accepted\"");

    let value = payoffs.get_mut(&node).unwrap().get_mut(&player).unwrap();
    value.basis.unit = "AUD-2026".into();
    value.basis.perspective = "societal".into();
    let error = solve_valued_game(specification, identities, &basis, payoffs).unwrap_err();
    assert!(matches!(
        error,
        PayoffInputError::PerspectiveMismatch { .. }
    ));
    assert_input_diagnostic(
        &error,
        "payoff perspective mismatch for \"firm\" at \"accepted\"",
    );
}

#[test]
fn omitted_and_unproven_payoffs_do_not_become_zero_values() {
    let (specification, identities, basis, mut payoffs) = fixture();
    let node = NodeId("accepted".into());
    let player = PlayerId("firm".into());
    let mut value = payoffs.get_mut(&node).unwrap().remove(&player).unwrap();
    let error = solve_valued_game(
        specification.clone(),
        identities.clone(),
        &basis,
        payoffs.clone(),
    )
    .unwrap_err();
    assert!(matches!(error, PayoffInputError::PlayerPayoffSet { .. }));
    assert_input_diagnostic(
        &error,
        "incomplete or undeclared player payoffs at \"accepted\"",
    );

    let mut unproven = value.clone();
    unproven.valuation_revision.clear();
    value.amount = f64::INFINITY;
    for invalid in [unproven, value] {
        payoffs
            .get_mut(&node)
            .unwrap()
            .insert(player.clone(), invalid);
        let error = solve_valued_game(
            specification.clone(),
            identities.clone(),
            &basis,
            payoffs.clone(),
        )
        .unwrap_err();
        assert!(matches!(error, PayoffInputError::InvalidValue { .. }));
        assert_input_diagnostic(
            &error,
            "non-finite payoff or missing valuation revision for \"firm\" at \"accepted\"",
        );
    }
}

#[test]
fn raw_values_and_valuations_for_decision_nodes_are_rejected() {
    let (mut specification, identities, basis, mut payoffs) = fixture();
    let accepted = NodeId("accepted".into());
    let raw = specification.game.nodes.get_mut(&accepted).unwrap();
    let Node::Terminal { payoffs: raw } = raw else {
        panic!("accepted is a terminal");
    };
    raw.insert(PlayerId("firm".into()), 80_000.0);
    let error = solve_valued_game(
        specification.clone(),
        identities.clone(),
        &basis,
        payoffs.clone(),
    )
    .unwrap_err();
    assert!(matches!(error, PayoffInputError::RawPayoffs { .. }));
    assert_input_diagnostic(&error, "unvalued payoffs supplied at \"accepted\"");

    let values = payoffs.remove(&accepted).unwrap();
    payoffs.insert(specification.game.root.clone(), values);
    let error = solve_valued_game(specification, identities, &basis, payoffs).unwrap_err();
    assert!(matches!(error, PayoffInputError::UnknownTerminal { .. }));
    assert_input_diagnostic(&error, "valuations reference a nonterminal node \"offer\"");
}

#[test]
fn version_and_identity_admission_fail_closed_at_the_provider_boundary() {
    let (mut specification, mut identities, basis, payoffs) = fixture();
    specification.schema_version = "unknown".into();
    let error = solve_valued_game(
        specification.clone(),
        identities.clone(),
        &basis,
        payoffs.clone(),
    )
    .unwrap_err();
    assert!(matches!(
        error,
        PayoffInputError::Solver(ResultSolveError::Input(_))
    ));
    let cause = error.source().expect("the native cause is exposed");
    assert_eq!(error.to_string(), cause.to_string());
    specification.schema_version = "1.0.0".into();
    identities.specification_id = GameSpecificationId("urn:ndrg:test:other-specification".into());
    assert!(matches!(
        solve_valued_game(specification, identities, &basis, payoffs),
        Err(PayoffInputError::Solver(
            ResultSolveError::SpecificationIdentityMismatch
        ))
    ));
}
