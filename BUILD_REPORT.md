# Build and validation report

- Generated: 2026-07-20T00:17:40.542154+00:00
- Critical checks passed: True

## scope

- Return code: `0`

```text
scope validation passed
```

## unittest

- Return code: `0`

```text
test_atlas_jsonl_reader (test_adapters.AdapterTests.test_atlas_jsonl_reader) ... ok
test_kairos_contract (test_adapters.AdapterTests.test_kairos_contract) ... ok
test_uogto_export (test_adapters.AdapterTests.test_uogto_export) ... ok
test_firm_offers_at_threshold (test_chapter8.Chapter8Tests.test_firm_offers_at_threshold) ... ok
test_no_trade_above_minimum_viable_price (test_chapter8.Chapter8Tests.test_no_trade_above_minimum_viable_price) ... ok
test_chapter_seven_shadow_price_identity (test_economics.EconomicsTests.test_chapter_seven_shadow_price_identity) ... ok
test_efficient_fixed_budget_reduces_to_d (test_economics.EconomicsTests.test_efficient_fixed_budget_reduces_to_d) ... ok
test_expandable_context_reduces_to_n (test_economics.EconomicsTests.test_expandable_context_reduces_to_n) ... ok
test_named_technical_alternative_can_bind (test_economics.EconomicsTests.test_named_technical_alternative_can_bind) ... ok
test_optimal_displacement_reduces_to_n (test_economics.EconomicsTests.test_optimal_displacement_reduces_to_n) ... ok
test_price_below_shadow_price_is_positive (test_economics.EconomicsTests.test_price_below_shadow_price_is_positive) ... ok
test_threshold_yields_zero_nebh (test_economics.EconomicsTests.test_threshold_yields_zero_nebh) ... ok
test_fixture (test_reference_game.ReferenceGameTests.test_fixture) ... ok
test_ecosystem_lock_pins_owned_repositories (test_scope.ScopeTests.test_ecosystem_lock_pins_owned_repositories) ... ok
test_hf_manifest_is_owner_scoped (test_scope.ScopeTests.test_hf_manifest_is_owner_scoped) ... ok
test_no_disallowed_runtime_dependencies (test_scope.ScopeTests.test_no_disallowed_runtime_dependencies) ... ok
test_ontology_cites_source_without_book_file (test_scope.ScopeTests.test_ontology_cites_source_without_book_file) ... ok

----------------------------------------------------------------------
Ran 17 tests in 0.006s

OK
```

## compileall

- Return code: `0`

```text

```

## cli-evaluate

- Return code: `0`

```text
{
  "adoption_health_gain": 10.0,
  "best_alternative_health_gain": 8.333333333333334,
  "binding_alternative": "reallocate_from_m_to_n",
  "displacement_health_loss": 6.25,
  "economic_value_clinical_innovation": 171428.57142857142,
  "health_shadow_price": 17142.85714285714,
  "iper": 25000.0,
  "net_economic_benefit_health": -4.583333333333334,
  "reimburse": false,
  "reimbursement_population_health_effect": 3.75
}
```

## cargo-test

- Return code: `None`

```text
cargo not installed; skipped
```
