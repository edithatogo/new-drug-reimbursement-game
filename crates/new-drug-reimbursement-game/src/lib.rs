//! Domain application using the domain-neutral game runtime.

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct OpportunitySet {
    pub expansion_icer: Option<f64>,
    pub contraction_icer: Option<f64>,
    pub displacement_icer: Option<f64>,
    pub additional_best_productivity: f64,
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
pub fn reallocation_productivity(opportunities: OpportunitySet) -> f64 {
    match (opportunities.expansion_icer, opportunities.contraction_icer) {
        (Some(n), Some(m)) if n > 0.0 && m > 0.0 => (1.0 / n - 1.0 / m).max(0.0),
        _ => 0.0,
    }
}

#[must_use]
pub fn fixed_budget_shadow_price(opportunities: OpportunitySet) -> Option<f64> {
    if !valid_opportunity_set(opportunities) {
        return None;
    }
    let d = opportunities.displacement_icer?;
    let alternative =
        reallocation_productivity(opportunities).max(opportunities.additional_best_productivity);
    let denominator = 1.0 / d + alternative;
    (denominator > 0.0).then_some(1.0 / denominator)
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
        reallocation_productivity(opportunities).max(opportunities.additional_best_productivity);
    Some(incremental_health_effect - incremental_cost / d - incremental_cost * alternative)
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
        assert_eq!(net_economic_benefit_health(1.0, 1.0, invalid), None);
    }
}
