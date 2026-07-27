# GitHub bootstrap

The distributable handoff restores this repository from a Git bundle so the
original commit history and annotated tags are retained. The outer covering
prompt then activates `CODEX_REPOSITORY_ACTIVATION_PROMPT.md` inside the restored
checkout.

The activation prompt is intentionally idempotent and fail-closed. It:

1. validates the restored history and baseline;
2. discovers pinned owner-controlled ecosystem clones without modifying them;
3. creates or safely connects `edithatogo/new-drug-reimbursement-game`;
4. pushes `main`, annotated tags, and `codex/ecosystem-integration` without
   rewriting history;
5. validates CI and records portable evidence;
6. continues into `CODEX_IMPLEMENTATION_PROMPT.md`.

Remote visibility defaults to private. The workstation may set
`NDRG_REMOTE_VISIBILITY=public` before activation, but the task must never change
visibility after repository creation.

Machine-specific paths are written only to the ignored
`.local/ecosystem-paths.json`. The tracked discovery report contains no absolute
paths. Authentication tokens and credential material are never written by the
repository tooling.
