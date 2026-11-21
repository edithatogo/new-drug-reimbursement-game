use new_drug_reimbursement_game::paignia_acceptance::{accept, AcceptanceError, ResultUse};
use paignia_core::{
    ActionEdge, ActionId, CatalogueClaim, Game, GameInstanceId, GameSpecification,
    GameSpecificationId, Node, NodeId, PlayerId, ResultEnvelope, ResultIdentityRecord,
    ResultStatus, SolverRunId, GAME_SPEC_SCHEMA_VERSION, RESULT_IDENTITY_SCHEMA_VERSION,
    STATIC_GAME_PROFILE_V1,
};
use paignia_solve::{backward_induction_result, SolverConfig};

fn solved() -> (GameSpecification, ResultIdentityRecord, ResultEnvelope) {
    let root = NodeId("offer".into());
    let terminal = NodeId("accepted".into());
    let institution = PlayerId("institution".into());
    let specification = GameSpecification {
        schema_version: GAME_SPEC_SCHEMA_VERSION.into(),
        id: "urn:ndrg:test:result-admission".into(),
        game: Game {
            root: root.clone(),
            nodes: [
                (
                    root,
                    Node::Decision {
                        player: institution.clone(),
                        edges: vec![ActionEdge {
                            action: ActionId("accept".into()),
                            target: terminal.clone(),
                        }],
                    },
                ),
                (
                    terminal,
                    Node::Terminal {
                        payoffs: [(institution, 5.0)].into(),
                    },
                ),
            ]
            .into(),
        },
    };
    let identities = ResultIdentityRecord {
        schema_version: RESULT_IDENTITY_SCHEMA_VERSION.into(),
        specification_id: GameSpecificationId(specification.id.clone()),
        game_instance_id: GameInstanceId("instance:offer".into()),
        solver_run_id: SolverRunId("run:original".into()),
        session_id: None,
        policy_artifact_id: None,
        solver_trace_id: None,
    };
    let result = backward_induction_result(
        &specification,
        STATIC_GAME_PROFILE_V1,
        identities.clone(),
        SolverConfig::default(),
    )
    .unwrap();
    (specification, identities, result.envelope)
}

#[test]
fn admits_the_completed_policy_with_its_exact_result_binding() {
    let (specification, identities, envelope) = solved();
    accept(
        &envelope,
        &specification,
        &identities,
        ResultUse::ContingentPolicy,
    )
    .unwrap();
}

#[test]
fn reports_failure_outcomes_without_returning_a_policy() {
    let (specification, identities, mut envelope) = solved();
    envelope.solutions.clear();
    envelope.diagnostics.clear();
    envelope.catalogue = CatalogueClaim::NotApplicable;
    envelope.status_detail = Some("outside the qualified result".into());
    for status in [ResultStatus::Unsupported, ResultStatus::NotConverged] {
        envelope.status = status;
        envelope
            .validate_against(&specification, &identities.game_instance_id)
            .unwrap();
        assert!(matches!(
            accept(&envelope, &specification, &identities, ResultUse::ContingentPolicy),
            Err(AcceptanceError::Incomplete { status: actual, detail })
                if actual == status && detail == envelope.status_detail
        ));
    }
}

#[test]
fn refuses_an_exhaustive_claim_from_a_contingent_policy() {
    let (specification, identities, envelope) = solved();
    assert_eq!(envelope.catalogue, CatalogueClaim::OneFound);
    assert!(matches!(
        accept(
            &envelope,
            &specification,
            &identities,
            ResultUse::ExhaustiveCatalogue
        ),
        Err(AcceptanceError::ExhaustiveCatalogueUnavailable)
    ));
}

#[test]
fn refuses_a_matching_model_from_a_different_solver_run() {
    let (specification, identities, mut envelope) = solved();
    envelope.identities.solver_run_id = SolverRunId("run:substitute".into());
    envelope
        .validate_against(&specification, &identities.game_instance_id)
        .unwrap();
    assert!(matches!(
        accept(
            &envelope,
            &specification,
            &identities,
            ResultUse::ContingentPolicy
        ),
        Err(AcceptanceError::IdentityMismatch)
    ));
}

#[test]
fn rejects_missing_choices_and_an_unknown_algorithm_version() {
    let (specification, identities, envelope) = solved();
    let mut incomplete = envelope.clone();
    incomplete.solutions[0].choices.clear();
    let mut wrong_version = envelope;
    wrong_version.algorithm.version = "3.0.0".into();
    for result in [incomplete, wrong_version] {
        assert!(matches!(
            accept(
                &result,
                &specification,
                &identities,
                ResultUse::ContingentPolicy
            ),
            Err(AcceptanceError::InvalidEnvelope(_))
        ));
    }
}
