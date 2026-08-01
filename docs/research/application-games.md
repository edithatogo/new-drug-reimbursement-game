# Pekarsky application games 1–3

The strict Chapter 7 evaluator remains the source-conformance path. This
module adds application game surfaces for the broader Chapter 8 and post-2015
programme while retaining explicit assumptions and provenance.

| Game | Implementation | Source boundary |
| --- | --- | --- |
| 1 | `solve_game1_grid`, hidden-threshold variant | The grid approximates the continuous-price corner solution in Chapter 8 equation 8.2; production cost and hidden thresholds are extensions. |
| 2 | `solve_game2` | Firm do-nothing/lobby/borrow choices with Bernoulli R&amp;D and financing are an application extension; no claim of a printed equilibrium equation. |
| 3 | `evaluate_game3` | Two-period development/manufacturing, competition, contract terms, and spillover accounting are explicit extension states; empirical calibration is out of scope. |

All outputs are deterministic for fixed inputs. Prices, costs, success
probability, contract terms, and spillovers are caller-supplied; no parameter is
silently inferred. The source concepts are cross-referenced to Pekarsky (2015)
Chapter 8 and the Chapter 7 source-conformance audit, with the full book
metadata recorded in `docs/research/pekarsky-foundation.md`.
