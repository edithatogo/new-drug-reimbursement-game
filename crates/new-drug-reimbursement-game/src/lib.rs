//! Domain application using the domain-neutral game runtime.

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct OpportunitySet {
    pub expansion_icer: Option<f64>,
    pub contraction_icer: Option<f64>,
    pub displacement_icer: Option<f64>,
    pub additional_best_productivity: f64,
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Chapter8Game1Equilibrium {
    pub offered_iper: f64,
    pub firm_economic_rent: f64,
    pub institution_nebh: f64,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Chapter7Scenario {
    Scenario1,
    Scenario2,
    Scenario3,
    Scenario4,
}

#[derive(Clone, Debug, PartialEq)]
pub enum Chapter7ScenarioInputs {
    Scenario1 {
        incremental_cost: f64,
        incremental_health_effect: f64,
        expansion_icer: f64,
    },
    Scenario2 {
        incremental_cost: f64,
        incremental_health_effect: f64,
        expansion_icer: f64,
        contraction_icer: f64,
        displacement_icer: f64,
    },
    Scenario3 {
        incremental_cost: f64,
        incremental_health_effect: f64,
        expansion_icer: f64,
        contraction_icer: f64,
        displacement_icer: f64,
    },
    Scenario4 {
        incremental_cost: f64,
        incremental_health_effect: f64,
        contraction_icer: f64,
        displacement_icer: f64,
        investment_icer: f64,
        present_value_multiplier: f64,
        annual_program_health_effect: f64,
        evidence_revision: String,
    },
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Chapter7ScenarioEvaluation {
    pub scenario: Chapter7Scenario,
    pub iper: f64,
    pub reimbursement_health_effect: f64,
    pub alternative_health_gain: f64,
    pub nebh: f64,
    pub beta: f64,
    pub evci: f64,
    pub net_financial_cost: f64,
    pub adoption_required: bool,
    pub economically_preferred: bool,
    pub tolerance: f64,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Chapter7Error(pub &'static str);

impl std::fmt::Display for Chapter7Error {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str(self.0)
    }
}

impl std::error::Error for Chapter7Error {}

fn chapter7_positive(name: &'static str, value: f64) -> Result<f64, Chapter7Error> {
    if value.is_finite() && value > 0.0 {
        Ok(value)
    } else {
        Err(Chapter7Error(name))
    }
}

fn chapter7_close(left: f64, right: f64) -> bool {
    let tolerance = 1e-12 * left.abs().max(right.abs()).max(1.0);
    (left - right).abs() <= tolerance
}

struct Chapter7Core {
    scenario: Chapter7Scenario,
    cost: f64,
    effect: f64,
    reimbursement_effect: f64,
    alternative_gain: f64,
    beta: f64,
    net_cost: f64,
}

fn chapter7_scenario1(cost: f64, effect: f64, n: f64) -> Result<Chapter7Core, Chapter7Error> {
    let cost = chapter7_positive("incremental_cost", cost)?;
    let effect = chapter7_positive("incremental_health_effect", effect)?;
    let n = chapter7_positive("expansion_icer", n)?;
    Ok(Chapter7Core {
        scenario: Chapter7Scenario::Scenario1,
        cost,
        effect,
        reimbursement_effect: effect,
        alternative_gain: cost / n,
        beta: n,
        net_cost: cost,
    })
}

fn chapter7_scenario2(
    cost: f64,
    effect: f64,
    n: f64,
    m: f64,
    d: f64,
) -> Result<Chapter7Core, Chapter7Error> {
    let cost = chapter7_positive("incremental_cost", cost)?;
    let effect = chapter7_positive("incremental_health_effect", effect)?;
    let n = chapter7_positive("expansion_icer", n)?;
    let m = chapter7_positive("contraction_icer", m)?;
    let d = chapter7_positive("displacement_icer", d)?;
    if !chapter7_close(n, m) {
        return Err(Chapter7Error("Scenario 2 requires n = m"));
    }
    Ok(Chapter7Core {
        scenario: Chapter7Scenario::Scenario2,
        cost,
        effect,
        reimbursement_effect: effect - cost / d,
        alternative_gain: 0.0,
        beta: d,
        net_cost: 0.0,
    })
}

fn chapter7_scenario3(
    cost: f64,
    effect: f64,
    n: f64,
    m: f64,
    d: f64,
) -> Result<Chapter7Core, Chapter7Error> {
    let cost = chapter7_positive("incremental_cost", cost)?;
    let effect = chapter7_positive("incremental_health_effect", effect)?;
    let n = chapter7_positive("expansion_icer", n)?;
    let m = chapter7_positive("contraction_icer", m)?;
    let d = chapter7_positive("displacement_icer", d)?;
    if m <= n {
        return Err(Chapter7Error("Scenario 3 requires m > n"));
    }
    if !(n <= d && d <= m) {
        return Err(Chapter7Error("Scenario 3 requires n <= d <= m"));
    }
    Ok(Chapter7Core {
        scenario: Chapter7Scenario::Scenario3,
        cost,
        effect,
        reimbursement_effect: effect - cost / d,
        alternative_gain: cost * (1.0 / n - 1.0 / m),
        beta: 1.0 / (1.0 / d + 1.0 / n - 1.0 / m),
        net_cost: 0.0,
    })
}

fn chapter7_scenario4(
    cost: f64,
    effect: f64,
    m: f64,
    d: f64,
    investment: (f64, f64, f64),
    evidence_revision: &str,
) -> Result<Chapter7Core, Chapter7Error> {
    let (mu, phi, annual_effect) = investment;
    let cost = chapter7_positive("incremental_cost", cost)?;
    let effect = chapter7_positive("incremental_health_effect", effect)?;
    let m = chapter7_positive("contraction_icer", m)?;
    let d = chapter7_positive("displacement_icer", d)?;
    let mu = chapter7_positive("investment_icer", mu)?;
    let phi = chapter7_positive("present_value_multiplier", phi)?;
    let annual_effect = chapter7_positive("annual_program_health_effect", annual_effect)?;
    if evidence_revision.trim().is_empty() {
        return Err(Chapter7Error("Scenario 4 requires evidence_revision"));
    }
    if phi <= 1.0 || mu >= m || d > m {
        return Err(Chapter7Error("Scenario 4 ordering assumptions failed"));
    }
    let present_value_gain = phi * annual_effect;
    if !present_value_gain.is_finite() || !chapter7_close(present_value_gain, cost / mu) {
        return Err(Chapter7Error(
            "Scenario 4 requires phi * DeltaE_G = incremental_cost / mu",
        ));
    }
    let alternative_gain = present_value_gain - cost / m;
    if !alternative_gain.is_finite() || alternative_gain <= 0.0 {
        return Err(Chapter7Error(
            "Scenario 4 requires positive net investment gain",
        ));
    }
    Ok(Chapter7Core {
        scenario: Chapter7Scenario::Scenario4,
        cost,
        effect,
        reimbursement_effect: effect - cost / d,
        alternative_gain,
        beta: 1.0 / (1.0 / d + 1.0 / mu - 1.0 / m),
        net_cost: 0.0,
    })
}

/// Evaluate one strict Pekarsky Chapter 7 scenario.
///
/// # Errors
///
/// Returns [`Chapter7Error`] when an input violates its scenario's source
/// domain or when a derived value is non-finite.
pub fn evaluate_chapter7_scenario(
    inputs: &Chapter7ScenarioInputs,
) -> Result<Chapter7ScenarioEvaluation, Chapter7Error> {
    let core = match inputs {
        Chapter7ScenarioInputs::Scenario1 {
            incremental_cost,
            incremental_health_effect,
            expansion_icer,
        } => chapter7_scenario1(
            *incremental_cost,
            *incremental_health_effect,
            *expansion_icer,
        )?,
        Chapter7ScenarioInputs::Scenario2 {
            incremental_cost,
            incremental_health_effect,
            expansion_icer,
            contraction_icer,
            displacement_icer,
        } => chapter7_scenario2(
            *incremental_cost,
            *incremental_health_effect,
            *expansion_icer,
            *contraction_icer,
            *displacement_icer,
        )?,
        Chapter7ScenarioInputs::Scenario3 {
            incremental_cost,
            incremental_health_effect,
            expansion_icer,
            contraction_icer,
            displacement_icer,
        } => chapter7_scenario3(
            *incremental_cost,
            *incremental_health_effect,
            *expansion_icer,
            *contraction_icer,
            *displacement_icer,
        )?,
        Chapter7ScenarioInputs::Scenario4 {
            incremental_cost,
            incremental_health_effect,
            contraction_icer,
            displacement_icer,
            investment_icer,
            present_value_multiplier,
            annual_program_health_effect,
            evidence_revision,
        } => chapter7_scenario4(
            *incremental_cost,
            *incremental_health_effect,
            *contraction_icer,
            *displacement_icer,
            (
                *investment_icer,
                *present_value_multiplier,
                *annual_program_health_effect,
            ),
            evidence_revision,
        )?,
    };
    let iper = core.cost / core.effect;
    let nebh = core.reimbursement_effect - core.alternative_gain;
    let evci = core.beta * core.effect;
    let values = [
        iper,
        core.reimbursement_effect,
        core.alternative_gain,
        nebh,
        core.beta,
        evci,
        core.net_cost,
    ];
    if !values.iter().all(|value| value.is_finite()) {
        return Err(Chapter7Error("derived values must be finite"));
    }
    let tolerance = 1e-12 * core.beta.abs().max(iper.abs()).max(nebh.abs()).max(1.0);
    Ok(Chapter7ScenarioEvaluation {
        scenario: core.scenario,
        iper,
        reimbursement_health_effect: core.reimbursement_effect,
        alternative_health_gain: core.alternative_gain,
        nebh,
        beta: core.beta,
        evci,
        net_financial_cost: core.net_cost,
        adoption_required: true,
        economically_preferred: nebh >= -tolerance,
        tolerance,
    })
}

fn valid_positive(value: Option<f64>) -> bool {
    match value {
        None => true,
        Some(item) => item.is_finite() && item > 0.0,
    }
}

fn valid_opportunity_set(opportunities: OpportunitySet) -> bool {
    valid_positive(opportunities.expansion_icer)
        && valid_positive(opportunities.contraction_icer)
        && valid_positive(opportunities.displacement_icer)
        && opportunities.additional_best_productivity.is_finite()
        && opportunities.additional_best_productivity >= 0.0
}

#[must_use]
pub fn reallocation_productivity(opportunities: OpportunitySet) -> Option<f64> {
    if !valid_opportunity_set(opportunities) {
        return None;
    }
    let productivity = match (opportunities.expansion_icer, opportunities.contraction_icer) {
        (Some(n), Some(m)) => (1.0 / n - 1.0 / m).max(0.0),
        _ => 0.0,
    };
    productivity.is_finite().then_some(productivity)
}

#[must_use]
pub fn fixed_budget_shadow_price(opportunities: OpportunitySet) -> Option<f64> {
    if !valid_opportunity_set(opportunities) {
        return None;
    }
    let d = opportunities.displacement_icer?;
    let alternative =
        reallocation_productivity(opportunities)?.max(opportunities.additional_best_productivity);
    let denominator = 1.0 / d + alternative;
    let shadow_price = 1.0 / denominator;
    (denominator.is_finite() && denominator > 0.0 && shadow_price.is_finite())
        .then_some(shadow_price)
}

#[must_use]
pub fn net_economic_benefit_health(
    incremental_cost: f64,
    incremental_health_effect: f64,
    opportunities: OpportunitySet,
) -> Option<f64> {
    if !incremental_cost.is_finite()
        || incremental_cost <= 0.0
        || !incremental_health_effect.is_finite()
        || incremental_health_effect <= 0.0
        || !valid_opportunity_set(opportunities)
    {
        return None;
    }
    let d = opportunities.displacement_icer?;
    let alternative =
        reallocation_productivity(opportunities)?.max(opportunities.additional_best_productivity);
    let result = incremental_health_effect - incremental_cost / d - incremental_cost * alternative;
    result.is_finite().then_some(result)
}

/// Solve Pekarsky Chapter 8 Game 1 only when its quantitative assumptions hold.
#[must_use]
pub fn solve_pekarsky_game1(
    incremental_health_effect: f64,
    opportunities: OpportunitySet,
) -> Option<Chapter8Game1Equilibrium> {
    if !incremental_health_effect.is_finite()
        || incremental_health_effect <= 0.0
        || !valid_opportunity_set(opportunities)
        || opportunities.additional_best_productivity != 0.0
    {
        return None;
    }
    let n = opportunities.expansion_icer?;
    let m = opportunities.contraction_icer?;
    let d = opportunities.displacement_icer?;
    if !(m > n && n <= d && d <= m) {
        return None;
    }
    let offered_iper = fixed_budget_shadow_price(opportunities)?;
    let incremental_cost = offered_iper * incremental_health_effect;
    let institution_nebh =
        net_economic_benefit_health(incremental_cost, incremental_health_effect, opportunities)?;
    let firm_economic_rent = offered_iper * incremental_health_effect;
    (offered_iper.is_finite() && firm_economic_rent.is_finite() && institution_nebh.is_finite())
        .then_some(Chapter8Game1Equilibrium {
            offered_iper,
            firm_economic_rent,
            institution_nebh,
        })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn chapter_seven_identity_holds() {
        let opportunities = OpportunitySet {
            expansion_icer: Some(20_000.0),
            contraction_icer: Some(60_000.0),
            displacement_icer: Some(40_000.0),
            additional_best_productivity: 0.0,
        };
        let beta = fixed_budget_shadow_price(opportunities).unwrap();
        let expected = 1.0 / (1.0 / 40_000.0 + 1.0 / 20_000.0 - 1.0 / 60_000.0);
        assert!((beta - expected).abs() < 1e-9);
        let effect = 10.0;
        let cost = beta * effect;
        assert!(
            net_economic_benefit_health(cost, effect, opportunities)
                .unwrap()
                .abs()
                < 1e-10
        );
    }

    #[test]
    fn chapter_seven_special_cases_hold() {
        let efficient = OpportunitySet {
            expansion_icer: Some(30_000.0),
            contraction_icer: Some(30_000.0),
            displacement_icer: Some(45_000.0),
            additional_best_productivity: 0.0,
        };
        assert_eq!(fixed_budget_shadow_price(efficient), Some(45_000.0));

        let optimal_displacement = OpportunitySet {
            expansion_icer: Some(25_000.0),
            contraction_icer: Some(50_000.0),
            displacement_icer: Some(50_000.0),
            additional_best_productivity: 0.0,
        };
        let beta = fixed_budget_shadow_price(optimal_displacement).unwrap();
        assert!((beta - 25_000.0).abs() < 1e-9);
    }

    #[test]
    fn sign_and_unit_rescaling_invariants_hold() {
        let opportunities = OpportunitySet {
            expansion_icer: Some(20_000.0),
            contraction_icer: Some(60_000.0),
            displacement_icer: Some(40_000.0),
            additional_best_productivity: 0.0,
        };
        let beta = fixed_budget_shadow_price(opportunities).unwrap();
        let effect = 10.0;
        let below =
            net_economic_benefit_health(beta * effect * 0.9, effect, opportunities).unwrap();
        let above =
            net_economic_benefit_health(beta * effect * 1.1, effect, opportunities).unwrap();
        assert!(below > 0.0);
        assert!(above < 0.0);

        let scale = 100.0;
        let rescaled = OpportunitySet {
            expansion_icer: opportunities.expansion_icer.map(|value| value * scale),
            contraction_icer: opportunities.contraction_icer.map(|value| value * scale),
            displacement_icer: opportunities.displacement_icer.map(|value| value * scale),
            additional_best_productivity: 0.0,
        };
        let scaled_beta = fixed_budget_shadow_price(rescaled).unwrap();
        assert!((scaled_beta - beta * scale).abs() < 1e-8);
        let scaled_nebh =
            net_economic_benefit_health(beta * effect * scale, effect, rescaled).unwrap();
        assert!(scaled_nebh.abs() < 1e-10);
    }

    #[test]
    fn invalid_or_non_identifiable_inputs_fail_closed() {
        let missing_displacement = OpportunitySet {
            expansion_icer: Some(20_000.0),
            contraction_icer: Some(60_000.0),
            displacement_icer: None,
            additional_best_productivity: 0.0,
        };
        assert_eq!(fixed_budget_shadow_price(missing_displacement), None);

        let invalid = OpportunitySet {
            expansion_icer: Some(f64::NAN),
            contraction_icer: Some(60_000.0),
            displacement_icer: Some(40_000.0),
            additional_best_productivity: 0.0,
        };
        assert_eq!(fixed_budget_shadow_price(invalid), None);
        assert_eq!(reallocation_productivity(invalid), None);
        assert_eq!(net_economic_benefit_health(1.0, 1.0, invalid), None);

        let smallest_positive_subnormal = f64::from_bits(1);
        let extreme = OpportunitySet {
            expansion_icer: Some(smallest_positive_subnormal),
            contraction_icer: Some(1.0),
            displacement_icer: Some(smallest_positive_subnormal),
            additional_best_productivity: 0.0,
        };
        assert_eq!(reallocation_productivity(extreme), None);
        assert_eq!(fixed_budget_shadow_price(extreme), None);
        assert_eq!(net_economic_benefit_health(f64::MAX, 1.0, extreme), None);
    }

    #[test]
    fn versioned_cross_language_conformance_fixture() {
        let fixture = include_str!("../../../fixtures/conformance/economics-v1.csv");
        let mut lines = fixture.lines();
        let header = lines.next().unwrap();
        assert_eq!(
            header,
            "schema_version,case_id,expansion_icer,contraction_icer,displacement_icer,\
incremental_cost,incremental_health_effect,expected_shadow_price,expected_nebh,\
expected_reimburse"
        );
        for line in lines {
            let fields: Vec<_> = line.split(',').collect();
            assert_eq!(fields.len(), 10);
            assert_eq!(fields[0], "1");
            let parse = |index: usize| fields[index].parse::<f64>().unwrap();
            let opportunities = OpportunitySet {
                expansion_icer: Some(parse(2)),
                contraction_icer: Some(parse(3)),
                displacement_icer: Some(parse(4)),
                additional_best_productivity: 0.0,
            };
            let expected_beta = parse(7);
            let expected_nebh = parse(8);
            let beta = fixed_budget_shadow_price(opportunities).unwrap();
            let nebh = net_economic_benefit_health(parse(5), parse(6), opportunities).unwrap();
            let iper = parse(5) / parse(6);
            let tolerance = 1e-12 * beta.abs().max(iper.abs()).max(1.0);
            assert!(
                (beta - expected_beta).abs() < 1e-9,
                "shadow-price drift in {}",
                fields[1]
            );
            assert!(
                (nebh - expected_nebh).abs() < 1e-9,
                "NEBhR drift in {}",
                fields[1]
            );
            assert_eq!(iper <= beta + tolerance, fields[9] == "true");
        }
    }

    #[test]
    fn deterministic_monotonicity_sweeps_hold() {
        let base = OpportunitySet {
            expansion_icer: Some(20_000.0),
            contraction_icer: Some(60_000.0),
            displacement_icer: Some(40_000.0),
            additional_best_productivity: 0.0,
        };
        let mut prior_beta = fixed_budget_shadow_price(base).unwrap();
        for displacement in [45_000.0, 60_000.0, 100_000.0] {
            let opportunities = OpportunitySet {
                displacement_icer: Some(displacement),
                ..base
            };
            let beta = fixed_budget_shadow_price(opportunities).unwrap();
            assert!(beta > prior_beta);
            prior_beta = beta;
        }

        let beta = fixed_budget_shadow_price(base).unwrap();
        let mut prior_nebh = f64::INFINITY;
        for multiplier in [0.25, 0.5, 0.75, 1.0, 1.25, 2.0] {
            let nebh = net_economic_benefit_health(beta * multiplier * 10.0, 10.0, base).unwrap();
            assert!(nebh < prior_nebh);
            prior_nebh = nebh;
        }
    }

    #[test]
    fn chapter_eight_game_one_fixture_conforms() {
        let fixture = include_str!("../../../fixtures/conformance/chapter8-game1-v1.csv");
        let mut lines = fixture.lines();
        assert_eq!(
            lines.next().unwrap(),
            "schema_version,case_id,expansion_icer,contraction_icer,displacement_icer,\
incremental_health_effect,expected_price,expected_firm_rent,expected_nebh"
        );
        for line in lines {
            let fields: Vec<_> = line.split(',').collect();
            assert_eq!(fields.len(), 9);
            assert_eq!(fields[0], "1");
            let parse = |index: usize| fields[index].parse::<f64>().unwrap();
            let result = solve_pekarsky_game1(
                parse(5),
                OpportunitySet {
                    expansion_icer: Some(parse(2)),
                    contraction_icer: Some(parse(3)),
                    displacement_icer: Some(parse(4)),
                    additional_best_productivity: 0.0,
                },
            )
            .unwrap();
            assert!((result.offered_iper - parse(6)).abs() < 1e-9);
            assert!((result.firm_economic_rent - parse(7)).abs() < 1e-9);
            assert!((result.institution_nebh - parse(8)).abs() < 1e-9);
        }
    }

    #[test]
    fn chapter_eight_game_one_rejects_generalized_domains() {
        let invalid_ordering = OpportunitySet {
            expansion_icer: Some(60_000.0),
            contraction_icer: Some(20_000.0),
            displacement_icer: Some(40_000.0),
            additional_best_productivity: 0.0,
        };
        assert_eq!(solve_pekarsky_game1(1.0, invalid_ordering), None);

        let extra_strategy = OpportunitySet {
            expansion_icer: Some(20_000.0),
            contraction_icer: Some(60_000.0),
            displacement_icer: Some(40_000.0),
            additional_best_productivity: 1.0 / 10_000.0,
        };
        assert_eq!(solve_pekarsky_game1(1.0, extra_strategy), None);
    }

    #[test]
    fn chapter_seven_all_scenario_fixture_conforms() {
        let fixture = include_str!("../../../fixtures/conformance/chapter7-scenarios-v1.csv");
        let mut lines = fixture.lines();
        let header = lines.next().unwrap();
        assert!(header.starts_with("schema_version,case_id,scenario,"));
        for line in lines {
            let fields: Vec<_> = line.split(',').collect();
            assert_eq!(fields.len(), 18);
            assert_eq!(fields[0], "1");
            let parse = |index: usize| fields[index].parse::<f64>().unwrap();
            let inputs = match fields[2] {
                "scenario_1" => Chapter7ScenarioInputs::Scenario1 {
                    incremental_cost: parse(3),
                    incremental_health_effect: parse(4),
                    expansion_icer: parse(5),
                },
                "scenario_2" => Chapter7ScenarioInputs::Scenario2 {
                    incremental_cost: parse(3),
                    incremental_health_effect: parse(4),
                    expansion_icer: parse(5),
                    contraction_icer: parse(6),
                    displacement_icer: parse(7),
                },
                "scenario_3" => Chapter7ScenarioInputs::Scenario3 {
                    incremental_cost: parse(3),
                    incremental_health_effect: parse(4),
                    expansion_icer: parse(5),
                    contraction_icer: parse(6),
                    displacement_icer: parse(7),
                },
                "scenario_4" => Chapter7ScenarioInputs::Scenario4 {
                    incremental_cost: parse(3),
                    incremental_health_effect: parse(4),
                    contraction_icer: parse(6),
                    displacement_icer: parse(7),
                    investment_icer: parse(8),
                    present_value_multiplier: parse(9),
                    annual_program_health_effect: parse(10),
                    evidence_revision: "synthetic-fixture-v1".to_owned(),
                },
                _ => panic!("unknown fixture scenario"),
            };
            let result = evaluate_chapter7_scenario(&inputs).unwrap();
            assert!((result.iper - parse(11)).abs() < 1e-9);
            assert!((result.reimbursement_health_effect - parse(12)).abs() < 1e-9);
            assert!((result.alternative_health_gain - parse(13)).abs() < 1e-9);
            assert!((result.nebh - parse(14)).abs() < 1e-9);
            assert!((result.beta - parse(15)).abs() < 1e-9);
            assert!((result.evci - parse(16)).abs() < 1e-9);
            assert!((result.net_financial_cost - parse(17)).abs() < 1e-9);
            assert!(result.adoption_required);
            assert_eq!(
                result.economically_preferred,
                result.nebh >= -result.tolerance
            );
        }
    }

    #[test]
    fn chapter_seven_scenario_domains_fail_closed() {
        let invalid = [
            Chapter7ScenarioInputs::Scenario2 {
                incremental_cost: 1.0,
                incremental_health_effect: 1.0,
                expansion_icer: 20.0,
                contraction_icer: 21.0,
                displacement_icer: 20.0,
            },
            Chapter7ScenarioInputs::Scenario3 {
                incremental_cost: 1.0,
                incremental_health_effect: 1.0,
                expansion_icer: 30.0,
                contraction_icer: 20.0,
                displacement_icer: 25.0,
            },
            Chapter7ScenarioInputs::Scenario4 {
                incremental_cost: 100.0,
                incremental_health_effect: 1.0,
                contraction_icer: 50.0,
                displacement_icer: 40.0,
                investment_icer: 60.0,
                present_value_multiplier: 2.0,
                annual_program_health_effect: 100.0 / 60.0 / 2.0,
                evidence_revision: "source".to_owned(),
            },
        ];
        for inputs in invalid {
            assert!(evaluate_chapter7_scenario(&inputs).is_err());
        }
    }
}
