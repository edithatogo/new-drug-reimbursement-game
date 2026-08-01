# Voiage licence adjudication packet

## Verified state

The locked Voiage revision is
`6141cc49a9ad41161756677840d6a61b25fd386a` (2026-07-17). The exact pinned
artifacts contain conflicting declarations:

| Artifact | Declaration | SHA-256 |
|---|---|---|
| `LICENSE` | Apache License 2.0 | `ce8c23436cf2f3540f1148fe4202293f1612837c0a21951ba71591164b1c5dce` |
| `pyproject.toml` | `license = { file = "LICENSE" }` | `54cbaec1350d7fdd6f1df3ff864824e47f055d19c4af14cd5f867b45addc97eb` |
| `README.md` | MIT badge and MIT licence statement | `974bab7eacf8309d840360c82d97ace9e712b13e1100971ce72139cc88ec8060` |

The current repository therefore correctly keeps the Voiage gate open. A
passing adapter test or a clean checkout cannot adjudicate an upstream licence
conflict.

## Options

1. **Adjudicate Apache-2.0 (recommended):** the owner makes the README match
   the existing `LICENSE` and package metadata, records an upstream correction
   commit, and this repository updates its pin and inventory.
2. **Adjudicate MIT:** the owner replaces the Voiage `LICENSE` and package
   metadata consistently, records the correction commit, and this repository
   updates its pin and inventory.
3. **Leave unresolved:** keep Voiage optional and prohibit distribution or
   release claims that depend on it. The local adapter and dependency-free core
   may continue to be tested.

Option 1 is recommended because the pinned `LICENSE`, package declaration, and
current Voiage checkout are Apache-2.0 aligned; the README is the outlier. The
owner must still make the upstream correction, since this application cannot
change another repository's licence terms.

## Closeout evidence required

The gate closes only after an owner supplies the corrected Voiage revision,
matching `LICENSE`, package metadata, README, and a signed or attributable
licence decision. Then update `ecosystem.lock.toml`, regenerate
`docs/generated/governance-inventory.json`, rerun the pinned ecosystem and
packaging checks, and append the adjudication receipt to Conductor.
