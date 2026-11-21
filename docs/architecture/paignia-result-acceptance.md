# Static Paignia result admission

The valued-payoff entry point admits one completed contingent policy from the
locked Paignia static profile. It uses Paignia's graph and result validation
and binds the envelope to the complete requested identity record, including the
solver run and any supplied session, policy or diagnostic trace identifiers.
The caller receives the original result and valuation provenance together.

An unsupported or nonconverged result returns a typed failure with its recorded
reason. A valid contingent policy with `OneFound` fails an exhaustive catalogue
request. The application preserves the solver's class, information structure,
algorithm version, tolerance, selection rule and evidence fields. This boundary
qualifies result admission for T17.09.result. The real-model artifact receipt is
T17.09.artifact.

```bash
cargo test --locked -p new-drug-reimbursement-game --test paignia_result_contract
```
