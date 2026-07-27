# Start here in Codex

This repository is distributed with a Git bundle, a source ZIP, and a covering
prompt. The preferred restoration path is the Git bundle because it preserves
commit history and tags.

After the external handoff pack has restored this repository, Codex must execute:

1. `CODEX_REPOSITORY_ACTIVATION_PROMPT.md` — authenticates and wires GitHub,
   resolves pinned local ecosystem clones, validates the baseline, initializes
   the implementation branch, and activates Conductor.
2. `CODEX_IMPLEMENTATION_PROMPT.md` — performs the substantive autonomous
   implementation programme.

Do not run `git init` inside a bundle-restored checkout. Do not stop after merely
summarizing either prompt.
