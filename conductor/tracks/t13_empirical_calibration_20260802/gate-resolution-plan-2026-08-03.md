# T13 gate-resolution plan

This plan is the executable continuation for the remaining blockers. The
machine-readable source of truth is
`gate-resolution-plan-2026-08-03.json`; it is deliberately fail-closed.

## Execution order

1. Acquire and triangulate NHS context and displacement evidence.
2. Acquire and verify the immutable Atlas-approved packet and source terms.
3. Re-freeze inputs, reconcile equations/units/uncertainty, and rerun the
   subagent panel against the exact packet and repository commit.
4. Obtain packet-bound empirical authorization, including discounting and
   Scenario 4 decisions.
5. Requalify and promote only the claims explicitly covered by the approvals.

The recommended route is official NHS triangulation plus an owner-approved,
immutable Atlas packet. Public reconstruction and synthetic fixtures remain
useful fallbacks for research-only work, but cannot close displacement,
confidential price, source-term, or empirical-release gates.

## Stop and fallback behavior

Every acquisition records a hash, authority, locator, rights, and disposition.
Inaccessible, conflicting, incomplete, mutable, restricted, or no-record
outcomes are preserved as receipts and route to the contingencies in the JSON
plan. Agents may search, retrieve, hash, compare, refresh, invalidate, and
rerun validation autonomously. They must stop for custodian access, new terms,
confidential/raw-data permissions, intended-use changes, or accountable
empirical/release approval.
