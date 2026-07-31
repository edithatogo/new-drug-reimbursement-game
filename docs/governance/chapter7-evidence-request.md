# Chapter 7 evidence record

This records the evidence used to close the implemented Scenario 3 Chapter 7
gate without copying the source book into the repository.

## Verified source evidence

1. Pekarsky (2015), DOI `10.1007/978-3-319-08903-4`.
2. Equations 7.2-7.5: printed pages 116, 118, and 119; PDF pages 126, 128,
   and 129.
3. Scenario 4 investment parameter `mu`: printed page 117; PDF page 127.
4. Reviewed PDF SHA-256:
   `8455ad153cf5b6c1570bfc945108efe659904b3c8f89fdf7b74b88c9523c4848`.
   The source artifact remains outside the repository.
5. Mapping decision: Scenario 3 reallocation productivity maps to
   `g* = max(0, 1/n - 1/m)`. Scenario 4 `mu` is a separate investment parameter
   and is not mapped to `g*`.

## Independent review receipt

The Codex economics panel reviewed the source and implementation and returned
PASS for source fidelity of the implemented Scenario 3 model, conditional on
keeping Scenario 4 `mu`/`beta_c^v` explicitly out of scope. This is a technical
review, not regulatory or legal approval.

## Current state

The implemented Scenario 3 derivation is internally consistent and
source-faithful. The remaining source requirement applies only if Scenario 4 is
implemented: obtain Pekarsky (2012, Appendix 5), derive `mu`/`beta_c^v`, and
repeat dimensional and implementation review.
