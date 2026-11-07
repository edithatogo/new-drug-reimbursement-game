# T17 application specification — consume Paignia

## Current boundary and source history

Paignia is the implementation home for the generic Rust game library. This
application consumes its `paignia-core` and `paignia-solve` packages at one exact
reviewed Git revision. The dependency and lockfile must agree. Generic crate
source directories and local overrides are forbidden here; the native provider
has one owner.

The seed originated at application main
`f6c1c87b6b00875b33c1e19401c1de09481913ce`, with PR #101 naming head
`c7b2539b60ecb6457c75164c2a759730f5c1ec7c` reconciled into prepared source commit
`9ee388502bfe5f71d22b363dbb9c74f032a07ad4`. Original Apache-2.0 attribution is
preserved in Paignia's source/package notices and the extraction manifest.
Historical receipts retain their original repository and package identifiers.

## Application responsibilities

T17.09 constructs and solves the application's own game with Paignia. The
existing `paignia_static_game` test builds a finite offer/acceptance graph from
this application's valuation, with an independently calculable result. It is
source-level native consumer evidence, not a full economic model qualification
or registry release receipt. Domain institutions, health units, assumptions,
price/benefit construction and empirical interpretation stay here.

T17.11 will require explicit valued-payoff unit, perspective and provenance,
rejecting incompatible inputs before generic solving. HEOR valuation and Voiage
VOI remain separate capabilities; neither belongs in Paignia or Kairos.

The precise provider revision is recorded only after the Paignia commit exists;
mutable branches/tags and local path fallbacks cannot satisfy the boundary.
Consumer tests must execute with the actual Git dependency and lockfile.
Provider repository existence alone proves no numerical or release capability.

## Provider and semantic contracts

[Paignia T17](https://github.com/edithatogo/paignia/tree/main/conductor/tracks/t17_game_runtime_ecosystem_20261107)
owns the fourteen provider leaves: versioned game/result contracts, dependency
isolation, independent artifacts, S01–S04, optional Kairos adapter, release
eligibility, conversion, observations, random-stream isolation, replay and
information sets. UOGTO retains canonical IRIs, ontology, SHACL and executable
semantic profiles. Kairos retains native time/events/state/resources/RNG/replay.
The optional Paignia adapter depends on both; static solving remains independent.

The seed's unsupported information sets and advanced methods remain unsupported.
Source transfer does not close RK4, mixed Nash, CE or CFR/CFR+. Paignia and Kairos
retain the scientific completion and source-retirement records; this application
does not create a corrected solver fork. The solver's hypothetical diagnostic
trace must not be labelled as causal simulation execution.

## Acceptance and rollback

A passing immutable Git consumer is useful integration evidence. Complete
bounded release acceptance additionally needs Paignia T17.03 artifacts, a real
model/profile receipt here, and a distinct second application receipt under
T17.10. Optional native execution and unrelated algorithms are required only
when the selected case claims them. T17.12 remains the provider's release gate;
its former repository-creation wording is superseded by the user's chosen home.

Routine work uses small file-scoped slices and focused checks, plus coherent
public-contract/numerical review where relevant. No repeated human approval is
introduced. Rollback uses an actually qualified immutable provider revision or
an explicit ordinary revert preserving history, never a silent non-Rust or local
solver fallback. T17.09/.11 stay open until their full acceptance is recorded.
