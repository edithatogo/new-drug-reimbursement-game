use new_drug_reimbursement_game::voiage_input::replicates::{
    DeclaredParameterDraw, DrawIdentity, DrawIdentityError, DrawPlan, InnerIdentity, RecordedDraws,
    SamplingPrecision,
};

const RUN: &str = "synthetic-reimbursement-run-v1";
const PARAMETER: &str = "only-parameter-state";

const FIRST: InnerIdentity<'static> = InnerIdentity {
    model_id: "reimbursement-model",
    equilibrium_id: Some("fixed-response"),
    measurement_id: Some("fixed-measurement"),
    replicate_id: "replicate-a",
};
const SECOND: InnerIdentity<'static> = InnerIdentity {
    replicate_id: "replicate-b",
    ..FIRST
};
const DECLARED: &[DeclaredParameterDraw<'static>] = &[DeclaredParameterDraw {
    id: PARAMETER,
    replicates: &[FIRST, SECOND],
}];
const ROWS: &[DrawIdentity<'static>] = &[
    DrawIdentity {
        parameter_draw_id: PARAMETER,
        inner: FIRST,
    },
    DrawIdentity {
        parameter_draw_id: PARAMETER,
        inner: SECOND,
    },
];
const PLAN: DrawPlan<'static> = DrawPlan {
    producer_run_id: RUN,
    parameter_draws: DECLARED,
    precision: SamplingPrecision::ExactEnumeration,
};

#[test]
fn one_parameter_state_has_two_replicates_and_one_outer_draw() {
    let reordered = [ROWS[1], ROWS[0]];
    let result = PLAN
        .accept(RecordedDraws {
            producer_run_id: RUN,
            draws: &reordered,
        })
        .unwrap();
    assert_eq!(result.outer_budget(), 1);
    assert_eq!(result.inner_budgets[PARAMETER], 2);
    assert_eq!(result.recorded.draws, &reordered);
    assert_eq!(result.precision, SamplingPrecision::ExactEnumeration);
}

#[test]
fn a_simulation_replicate_cannot_become_a_parameter_draw() {
    let flattened = ROWS
        .iter()
        .map(|row| DrawIdentity {
            parameter_draw_id: row.inner.replicate_id,
            ..*row
        })
        .collect::<Vec<_>>();
    assert_eq!(
        PLAN.accept(RecordedDraws {
            producer_run_id: RUN,
            draws: &flattened,
        }),
        Err(DrawIdentityError::UnknownParameterDraw)
    );
}

#[test]
fn model_equilibrium_and_measurement_coordinates_cannot_be_substituted() {
    for inner in [
        InnerIdentity {
            model_id: "foreign-model",
            ..FIRST
        },
        InnerIdentity {
            equilibrium_id: Some("foreign-response"),
            ..FIRST
        },
        InnerIdentity {
            measurement_id: None,
            ..FIRST
        },
        InnerIdentity {
            replicate_id: "foreign-replicate",
            ..FIRST
        },
    ] {
        assert_eq!(
            PLAN.accept(RecordedDraws {
                producer_run_id: RUN,
                draws: &[DrawIdentity { inner, ..ROWS[0] }, ROWS[1]],
            }),
            Err(DrawIdentityError::UnplannedInnerIdentity)
        );
    }
}

#[test]
fn outcome_draws_must_be_complete_unique_and_bound_to_the_run() {
    for (recorded, expected) in [
        (
            RecordedDraws {
                producer_run_id: "foreign-run",
                draws: ROWS,
            },
            DrawIdentityError::RunMismatch,
        ),
        (
            RecordedDraws {
                producer_run_id: RUN,
                draws: &ROWS[..1],
            },
            DrawIdentityError::MissingOutcome,
        ),
        (
            RecordedDraws {
                producer_run_id: RUN,
                draws: &[ROWS[0], ROWS[0]],
            },
            DrawIdentityError::DuplicateOutcome,
        ),
    ] {
        assert_eq!(PLAN.accept(recorded), Err(expected));
    }
}

#[test]
fn replicate_ids_are_scoped_to_their_own_parameter_draws() {
    let declarations = [
        DECLARED[0],
        DeclaredParameterDraw {
            id: "another-parameter-state",
            replicates: &[FIRST],
        },
    ];
    let rows = [
        ROWS[0],
        DrawIdentity {
            parameter_draw_id: declarations[1].id,
            inner: FIRST,
        },
        ROWS[1],
    ];
    let receipt = DrawPlan {
        parameter_draws: &declarations,
        ..PLAN
    }
    .accept(RecordedDraws {
        producer_run_id: RUN,
        draws: &rows,
    })
    .unwrap();
    assert_eq!(receipt.outer_budget(), 2);
    assert_eq!(receipt.inner_budgets[PARAMETER], 2);
    assert_eq!(receipt.inner_budgets["another-parameter-state"], 1);
    assert_eq!(receipt.recorded.draws, &rows);
}

#[test]
fn malformed_declarations_fail_before_counting_outer_draws() {
    for (declared, expected) in [
        (&[][..], DrawIdentityError::EmptyPlan),
        (
            &[DeclaredParameterDraw {
                id: "",
                ..DECLARED[0]
            }][..],
            DrawIdentityError::InvalidParameterDraw,
        ),
        (
            &[DeclaredParameterDraw {
                replicates: &[],
                ..DECLARED[0]
            }][..],
            DrawIdentityError::EmptyReplicateSet,
        ),
        (
            &[DECLARED[0], DECLARED[0]][..],
            DrawIdentityError::DuplicateParameterDraw,
        ),
        (
            &[DeclaredParameterDraw {
                replicates: &[InnerIdentity {
                    measurement_id: Some(" "),
                    ..FIRST
                }],
                ..DECLARED[0]
            }][..],
            DrawIdentityError::InvalidInnerIdentity,
        ),
        (
            &[DeclaredParameterDraw {
                replicates: &[FIRST, FIRST],
                ..DECLARED[0]
            }][..],
            DrawIdentityError::DuplicatePlannedReplicate,
        ),
    ] {
        assert_eq!(
            DrawPlan {
                parameter_draws: declared,
                ..PLAN
            }
            .accept(RecordedDraws {
                producer_run_id: RUN,
                draws: ROWS,
            }),
            Err(expected)
        );
    }
}

#[test]
fn monte_carlo_precision_keeps_unestimated_and_reported_error_distinct() {
    let recorded = RecordedDraws {
        producer_run_id: RUN,
        draws: ROWS,
    };
    for standard_error in [None, Some(0.0), Some(0.25)] {
        let precision = SamplingPrecision::MonteCarlo { standard_error };
        let report = DrawPlan { precision, ..PLAN }.accept(recorded).unwrap();
        assert_eq!(report.precision, precision);
        assert_eq!(report.outer_budget(), 1);
        assert_eq!(report.inner_budgets[PARAMETER], 2);
    }
    for error in [f64::NAN, f64::INFINITY, -0.1] {
        assert_eq!(
            DrawPlan {
                precision: SamplingPrecision::MonteCarlo {
                    standard_error: Some(error)
                },
                ..PLAN
            }
            .accept(recorded),
            Err(DrawIdentityError::InvalidPrecision)
        );
    }
}
