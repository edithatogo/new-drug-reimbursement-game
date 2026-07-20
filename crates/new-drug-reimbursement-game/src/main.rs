use new_drug_reimbursement_game::{fixed_budget_shadow_price, OpportunitySet};

fn main() {
    let opportunities = OpportunitySet {
        expansion_icer: Some(20_000.0),
        contraction_icer: Some(60_000.0),
        displacement_icer: Some(40_000.0),
        additional_best_productivity: 0.0,
    };
    let beta = fixed_budget_shadow_price(opportunities).expect("valid example");
    println!("health_shadow_price={beta:.6}");
}
