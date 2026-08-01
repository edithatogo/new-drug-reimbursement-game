# Voiage licence adjudication packet

## Historical conflict and resolution

The former locked Voiage revision was
`6141cc49a9ad41161756677840d6a61b25fd386a` (2026-07-17). The exact pinned
artifacts contain conflicting declarations:

| Artifact | Declaration | SHA-256 |
|---|---|---|
| `LICENSE` | Apache License 2.0 | `ce8c23436cf2f3540f1148fe4202293f1612837c0a21951ba71591164b1c5dce` |
| `pyproject.toml` | `license = { file = "LICENSE" }` | `54cbaec1350d7fdd6f1df3ff864824e47f055d19c4af14cd5f867b45addc97eb` |
| `README.md` | MIT badge and MIT licence statement | `974bab7eacf8309d840360c82d97ace9e712b13e1100971ce72139cc88ec8060` |

That conflict is now superseded. Voiage `main` at
`4b93ee04231bedaeae7e24d39b2b6f2c6ff9b9d6` aligns its README, Apache-2.0
`LICENSE`, and package metadata; its exact-head CI passed. This repository now
pins that revision and records Apache-2.0 as reconciled. Source-specific Atlas
and Hugging Face terms remain separate open gates.

## Options

1. **Adjudicate Apache-2.0 (completed):** the owner made the README match
   the existing `LICENSE` and package metadata, records an upstream correction
   commit, and this repository updates its pin and inventory.
2. **Adjudicate MIT (not selected):** the owner replaces the Voiage `LICENSE` and package
   metadata consistently, records the correction commit, and this repository
   updates its pin and inventory.
3. **Leave unresolved:** keep Voiage optional and prohibit distribution or
   release claims that depend on it. The local adapter and dependency-free core
   may continue to be tested.

Option 1 was selected because the pinned `LICENSE`, package declaration, and
current Voiage checkout are Apache-2.0 aligned. The application did not modify
the upstream repository; it advanced its pin after the owner-controlled
correction was already present.

## Closeout evidence required

The reconciliation evidence is the corrected Voiage revision, matching
`LICENSE`, package metadata, README, successful exact-head CI, the updated
`ecosystem.lock.toml`, and regenerated governance inventory. Source-specific
Atlas/Hugging Face terms still require separate owner decisions.
