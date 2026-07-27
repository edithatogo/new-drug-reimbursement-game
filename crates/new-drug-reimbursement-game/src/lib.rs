//! Domain application using the domain-neutral game runtime.

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct OpportunitySet {
    pub expansion_icer: Option<f64>,
    pub contraction_icer: Option<f64>,
    pub displacement_icer: Option<f64>,
    pub additional_best_productivity: f64,
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
    let d = opportunities.displacement_icer?;
    if d <= 0.0 {
        return None;
    }
    let alternative = reallocation_productivity(opportunities)
        .max(opportunities.additional_best_productivity.max(0.0));
    let denominator = 1.0 / d + alternative;
    (denominator > 0.0).then_some(1.0 / denominator)
}

#[must_use]
pub fn net_economic_benefit_health(
    incremental_cost: f64,
    incremental_health_effect: f64,
    opportunities: OpportunitySet,
) -> Option<f64> {
    let d = opportunities.displacement_icer?;
    let alternative = reallocation_productivity(opportunities)
        .max(opportunities.additional_best_productivity.max(0.0));
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
}
