# Codex repository activation and autonomous implementation prompt

You are now inside the restored Git repository for the ecosystem-first New Drug
Reimbursement Game project. The bundle restoration step has already preserved
its commit history. Do not reinitialize Git and do not replace its history.

This file is the **activation prompt**. Execute it; do not merely summarize it.
After setup and remote wiring, continue directly into
`CODEX_IMPLEMENTATION_PROMPT.md` and begin implementation autonomously.

## Fixed defaults

- GitHub owner: `edithatogo`
- GitHub repository: `new-drug-reimbursement-game`
- Expected remote: `edithatogo/new-drug-reimbursement-game`
- Default branch: `main`
- Working branch: `codex/ecosystem-integration`
- Remote name: `origin`
- Visibility: `NDRG_REMOTE_VISIBILITY` when exactly `public` or `private`;
  otherwise `private`
- Authoritative dependency pins: `ecosystem.lock.toml`
- Machine-local ecosystem manifest: `.local/ecosystem-paths.json`
- Portable discovery report: `docs/generated/ecosystem-discovery.md`

The default is private because public release requires separate licence,
provenance, model-risk, and implementation-readiness review.

## Completion contract

Do not conclude after repository setup. The task is complete only after all of
these outcomes have been pursued as far as the environment permits:

1. Existing Git history and the `v0.4.0` handoff tag are verified.
2. Baseline quality gates pass.
3. Required owner-controlled ecosystem clones are resolved at their pins without
   mutating pre-existing working trees.
4. A GitHub repository exists at the expected owner/name and is safely wired as
   `origin`.
5. `main`, tags, and the working branch are pushed without rewriting history.
6. Repository settings and CI are validated.
7. Conductor track T00 is closed with evidence and the next unblocked tracks are
   activated.
8. `CODEX_IMPLEMENTATION_PROMPT.md` is executed, not just converted into a plan.
9. Coherent implementation commits are produced on the working branch and
   pushed after relevant checks pass.

## Non-negotiable constraints

- Preserve all user work and commit history.
- Never force-push, reset destructively, delete a repository, or replace remote
  history.
- Never expose or commit tokens, credentials, absolute local paths, private
  keys, `.env` contents, or authentication state.
- Never add the source book, scans, copied figures, copied tables, lengthy
  excerpts, or another copyrighted source asset.
- Cite Pekarsky (2015), DOI `10.1007/978-3-319-08903-4`, and the relevant
  chapter/equation when code depends on the source concepts.
- UOGTO owns game semantics; Kairos owns deterministic time/events/ECS/DES/ABM;
  Voiage owns VOI; Reimbursement Atlas owns reimbursement evidence/provenance.
- Do not introduce Nashpy, Gambit/pygambit, OpenSpiel, BCEA, heemod, dampack, or
  another capability library that duplicates those owner-controlled directions.
- Generic dependencies require an ADR covering licence, boundary, migration,
  and removal/stabilization criteria.
- All executable Hugging Face references must remain under `edithatogo/*`.
- Keep domain-neutral Rust crates free of reimbursement, drug, manufacturer,
  QALY, HTA, and payer vocabulary.
- Do not mutate a pre-existing sibling clone during discovery or integration.
  Use `git show`, detached temporary worktrees under this repository, or a
  bootstrap-created cache clone instead.
- Do not upload to Hugging Face or publish a release in this activation.
- Do not claim regulator-grade validity.
- Never silently resolve ambiguous economics, ontology, licences, or evidence.

## Stop conditions

Pause for one focused user decision only if:

1. GitHub CLI cannot authenticate as `edithatogo`;
2. the expected remote exists with unrelated or divergent non-empty history;
3. a required component has two equally suitable local clones;
4. a required pinned revision cannot be obtained despite permitted network
   access;
5. an essential filesystem or network operation is denied;
6. a source or licence ambiguity makes the next implementation change unsafe.

Ordinary engineering choices covered by this prompt are not stop conditions.

---

# Phase 1 — verify the restored Git history

From the repository root:

1. Record OS, current directory, Python, Git, Cargo/Rust, and GitHub CLI versions.
2. Run:

   ```bash
   git status --short --branch
   git log --oneline --decorate --graph --all -n 20
   git tag -n
   git fsck --full
   ```

3. Confirm the repository includes the original ecosystem-first foundation
   commit and the bootstrap/activation commit.
4. Confirm the working tree is clean. Do not conceal unexpected changes.
5. Confirm `main` exists. When currently on another clean bootstrap-created
   branch, preserve it and determine why before switching.
6. Confirm tag `v0.4.0` resolves to the handoff commit. Do not recreate a
   different tag with the same name.
7. Set repository-local safety configuration when absent:

   ```bash
   git config --local pull.ff only
   git config --local fetch.prune true
   git config --local rerere.enabled true
   ```

8. Preserve global Git identity. Set a local identity only when none is usable,
   using the authenticated GitHub login and its GitHub noreply address.

# Phase 2 — read the governing context

Read in order:

1. `AGENTS.md`
2. `README.md`
3. `START_HERE_CODEX.md`
4. `DEPENDENCY_MIGRATION_PLAN.md`
5. `ecosystem.lock.toml`
6. `docs/architecture/capability-boundary.md`
7. `docs/architecture/rust-game-runtime.md`
8. `conductor/workflow.md`
9. `conductor/tracks.yaml`
10. `conductor/status.md`
11. `CODEX_IMPLEMENTATION_PROMPT.md`
12. `IMPLEMENTATION_STATUS.md`

Treat these documents as a contract. Reconcile inconsistencies explicitly rather
than choosing whichever is easiest.

# Phase 3 — establish the baseline

Run the full local baseline before changing code:

```bash
python scripts/validate_scope.py
python -m unittest discover -s tests -p 'test_*.py'
python -m compileall -q src scripts tests
python scripts/discover_ecosystem.py --offline-fixture-mode
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
python scripts/run_quality_gate.py
```

When a tool is missing, install it through the repository's declared tooling or
record the exact environmental blocker. Do not weaken a check to obtain a green
result.

Record exact baseline results in `.local/bootstrap-state.json`; never commit
that file. Update `BUILD_REPORT.md` only with portable, truthful results.

# Phase 4 — resolve owner-controlled ecosystem clones

Run discovery without cloning:

```bash
python scripts/discover_ecosystem.py --json
```

The required repositories and revisions must come from `ecosystem.lock.toml`,
not from this prose. The current intended components are UOGTO, Kairos, Voiage,
and Reimbursement Atlas. Detect `edithatogo/ecosystem-docs` as optional when it
is nearby, but do not turn it into a runtime dependency.

For each pre-existing selected clone:

- verify its normalized remote;
- record branch, HEAD, clean/dirty state, and whether the pin exists;
- fetch the pin only when absent and network access is approved;
- do not checkout, reset, pull, merge, rebase, stash, commit, or alter files.

When a required component is missing, run:

```bash
python scripts/discover_ecosystem.py --clone-missing --check
```

This may clone missing repositories only into the ignored
`.local/ecosystem/` cache. Re-run:

```bash
python scripts/discover_ecosystem.py --check
```

Review both outputs:

- `.local/ecosystem-paths.json` — machine-specific and ignored;
- `docs/generated/ecosystem-discovery.md` — portable and tracked.

Do not commit absolute paths. Commit the portable report only when it conveys
useful reproducible state and contains no workstation identifiers.

# Phase 5 — authenticate GitHub safely

1. Confirm `gh` is installed.
2. Run:

   ```bash
   gh auth status --active --hostname github.com
   ```

3. The active account must be `edithatogo`.
4. When another already-authenticated account is active, use:

   ```bash
   gh auth switch --hostname github.com --user edithatogo
   ```

5. When `edithatogo` is not authenticated, stop and request completion of:

   ```bash
   gh auth login --hostname github.com
   ```

6. Run `gh auth setup-git --hostname github.com` when required.
7. Never print `gh auth token`, token environment variables, or credential files.

# Phase 6 — inspect or create the GitHub repository

Resolve visibility:

- `public` only when `NDRG_REMOTE_VISIBILITY=public`;
- otherwise `private`.

Inspect the target first:

```bash
gh repo view edithatogo/new-drug-reimbursement-game \
  --json nameWithOwner,visibility,defaultBranchRef,url,isEmpty
```

Adapt to the installed GitHub CLI schema if `isEmpty` is unavailable.

## When the remote does not exist

Create it from the current repository, using the installed `gh repo create`
syntax and these properties:

- name: `edithatogo/new-drug-reimbursement-game`;
- resolved visibility;
- description: `Ecosystem-first, UOGTO-aligned implementation and extension of the new drug reimbursement game, with a Rust capability layer above Kairos.`;
- issues enabled;
- wiki disabled;
- source is the current repository;
- remote name is `origin`;
- push `main`.

A typical command is:

```bash
gh repo create edithatogo/new-drug-reimbursement-game \
  --source=. --remote=origin --push \
  --description "Ecosystem-first, UOGTO-aligned implementation and extension of the new drug reimbursement game, with a Rust capability layer above Kairos." \
  --private
```

Replace `--private` with `--public` only under the explicit environment setting.
Check `gh repo create --help` rather than guessing if flags differ.

## When the remote exists and is empty

- add or correct `origin` to the expected repository;
- push `main` with upstream tracking;
- push annotated tags.

## When the remote exists and is non-empty

- add it temporarily when needed and fetch without merging;
- compare commit ancestry and tree identity;
- proceed only when the local history is already contained in the remote, the
  remote is already contained in the local history, or a non-destructive
  reconciliation is demonstrably safe;
- unrelated or divergent history is a stop condition;
- never force-push.

When bundle restoration left a local `source-bundle` remote, remove it after the
GitHub `origin` is verified. It is not a collaboration remote.

Push:

```bash
git push -u origin main
git push origin --tags
```

Then set the GitHub CLI default repository:

```bash
gh repo set-default edithatogo/new-drug-reimbursement-game
```

Verify:

```bash
git remote -v
git branch -vv
git ls-remote origin
gh repo view --json nameWithOwner,visibility,defaultBranchRef,url
```

# Phase 7 — normalize GitHub repository settings

Inspect `gh repo edit --help` and configure, where supported:

- default branch `main`;
- issues enabled;
- wiki disabled;
- squash merges enabled;
- merge commits disabled;
- rebase merges disabled;
- automatic deletion of merged head branches enabled;
- update-branch support enabled;
- repository description as specified above;
- topics: `health-economics`, `game-theory`, `rust`, `python`, `hta`, `uogto`,
  `kairos`, `reimbursement`.

Do not change visibility after creation during this activation.

Do not create a ruleset that deadlocks the sole developer before CI check names
are known. After the first green run, inspect available ruleset support and add a
least-surprise `main` protection policy requiring pull requests and the actual
stable CI checks. Preserve an owner recovery route. When account capabilities do
not support the intended ruleset, document the exact deferral in
`docs/GITHUB_BOOTSTRAP.md`.

# Phase 8 — validate and repair CI

1. Confirm `.github/workflows/ci.yml` uses least-privilege permissions and
   fixture-backed ecosystem checks rather than private absolute paths.
2. Push any bootstrap-only documentation or CI correction on `main` only before
   the working branch is created, and only as a small explicit commit.
3. Observe the initial workflow:

   ```bash
   gh run list --limit 10
   ```

4. Inspect failures using `gh run view` and logs.
5. Fix genuine defects without weakening tests.
6. Confirm `main` is green before treating T00 as complete.

# Phase 9 — create and activate the implementation branch

Create or resume the idempotent working branch:

```bash
git switch -c codex/ecosystem-integration
```

When it already exists, inspect it and switch only if it is the expected branch.
Push with upstream tracking:

```bash
git push -u origin codex/ecosystem-integration
```

All implementation work after bootstrap belongs on this branch or subsequent
focused branches/PRs. Do not continue direct feature work on `main`.

# Phase 10 — close bootstrap and synchronize Conductor

Update, in one coherent commit:

- `conductor/tracks.yaml`: T00 to `done` only when its exit evidence exists;
- `conductor/status.md`: exact remote, CI, and ecosystem-resolution state, with
  no absolute paths or secrets;
- `conductor/runlog.md`: commands, outcomes, commits, and unresolved blockers;
- `docs/GITHUB_BOOTSTRAP.md`: portable bootstrap decisions;
- `BUILD_REPORT.md`: exact baseline results;
- `IMPLEMENTATION_STATUS.md`: only what is actually true.

Create or synchronize GitHub issues for T01–T09 only after the remote exists.
Use deterministic titles beginning with `[T01]`, `[T02]`, and so on; search for
existing issues before creating any. Link dependencies in issue bodies rather
than creating duplicates. Add labels only when they can be created safely and
idempotently.

Commit and push this state on the working branch.

# Phase 11 — execute the implementation prompt autonomously

Now read `CODEX_IMPLEMENTATION_PROMPT.md` again and begin implementation. Do
not respond with a plan and stop.

Execution rules:

1. Choose the highest-priority unblocked tracks, generally T01, T02, and T09 in
   parallelizable slices.
2. Inspect authoritative pinned source using `.local/ecosystem-paths.json` and
   `git show <pin>:<path>`; never infer APIs from memory.
3. Use independent derivations and conformance fixtures before broad features.
4. Keep application semantics out of the generic Rust runtime.
5. Propose upstream-ready patches for UOGTO, Kairos, Voiage, and Reimbursement
   Atlas in this repository under `upstream/`; do not push changes to sibling
   repositories without separate explicit authorization.
6. Implement in small commits with tests and exact evidence.
7. Push the working branch after each coherent green milestone.
8. Continue through as much of the implementation programme as possible in the
   current Codex session. Do not stop merely because one workstream is large or
   research-intensive.
9. Where evidence is unresolved, implement named alternatives, interfaces,
   validation scaffolds, or fail-closed behavior rather than guessing.
10. Keep `conductor/` synchronized as work progresses.

Before every milestone push, run the relevant narrow checks and then the full
acceptance gate from `conductor/quality-gates.md`.

# Required final report

Report only verified facts and include:

## Repository restoration

- current repository path;
- commit graph summary;
- handoff tag verification;
- bootstrap and implementation commits;
- clean/dirty status.

## GitHub wiring

- authenticated account;
- `origin` URL;
- visibility and default branch;
- pushed branches/tags;
- repository settings;
- CI run URLs and outcomes;
- ruleset state or exact deferral.

## Ecosystem resolution

For every component in `ecosystem.lock.toml`:

- repository;
- pre-existing versus bootstrap-cache clone;
- current HEAD;
- pinned revision;
- pin availability;
- clean/dirty state;
- any ambiguity or access blocker.

Show absolute paths only in the private terminal report, never in committed
files.

## Implementation

- tracks activated and completed;
- important files and APIs changed;
- equations and games implemented with source locations;
- independent mathematical, ontology, cross-language, and integration checks;
- upstream proposals prepared;
- exact test/lint/type/coverage/build results.

## Remaining risk

- unresolved mathematical or source interpretations;
- licence/provenance decisions;
- work requiring health-economics, ontology, legal, governance, security, or
  deployment review;
- environmental blockers that prevented further autonomous work.

Do not say the implementation is complete unless every applicable acceptance
criterion is actually met.
