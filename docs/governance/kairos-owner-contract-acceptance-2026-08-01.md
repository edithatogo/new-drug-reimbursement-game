# Kairos owner contract acceptance

**Receipt ID:** `kairos-owner-contract-acceptance-2026-08-01`
**Approving owner:** `edithatogo` (repository maintainer)
**Downstream revision:** `13e2475f90c4b3c66c498b12983b7106139bc38e`
**Kairos revision:** `fae901558f07b7b717a676adbafbe2cdc78dea1c`

The maintainer accepts the pinned Kairos adapter contract for the
research-only, domain-neutral integration at the exact revision above. This
acceptance is an owner disposition for this downstream project; it does not
claim that Kairos has a tagged public release or that an external consumer may
infer a broader API guarantee.

## Authorized boundary

- deterministic execution and trace DTOs already covered by the pinned local
  compatibility tests;
- adapter use from this repository only;
- no duplicated scheduler, RNG, DES, or ABM implementation;
- no application-domain reimbursement vocabulary in the runtime crate; and
- no redistribution of Kairos source or extracted payloads.

The native-integration claim is limited to this owner-approved pinned contract.
Any public release or incompatible Kairos revision requires a new receipt.
