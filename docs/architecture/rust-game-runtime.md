# Rust game-theory runtime extraction plan

## Why a separate capability

The reimbursement games expose missing reusable capability: UOGTO-native,
executable, validated game specifications that can run through Kairos. Keeping
that logic inside a health application would make the ontology and runtime
non-reusable.

## Target stack

```text
UOGTO ontology and SHACL
          │
          ▼
Rust game specification + validator
          │
    ┌─────┴────────┐
    ▼              ▼
solver traits   execution compiler
    │              │
    ▼              ▼
equilibria      Kairos events/state/traces
          │
          ▼
Python/R/TS/Julia/.NET facades
```

## Extraction gates

1. Domain-neutral crate tests prohibit reimbursement vocabulary.
2. Canonical fixtures round-trip between JSON-LD, Rust, and Python.
3. UOGTO SHACL and competency questions pass.
4. Kairos adapter consumes released APIs rather than source-copying.
5. Backward induction agrees with analytic fixtures.
6. Imperfect-information and repeated-game semantics are specified before
   implementation.
7. FFI is generated from a stable schema, not handwritten separately per
   language.
8. The application depends on the released capability, then removes its Python
   conformance solver from the production path.

## Initial solver roadmap

- finite acyclic perfect-information backward induction;
- chance nodes and expected payoff;
- subgame-perfect equilibrium result representation;
- normal-form best response and pure Nash enumeration;
- information sets and behavioural strategies;
- mixed strategies and equilibrium algorithms;
- repeated/stochastic games;
- bargaining and mechanism-design interfaces;
- learning/agent simulation through Kairos.
