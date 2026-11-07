# Paignia provider and consumer boundary

The generic source has transferred to [Paignia](https://github.com/edithatogo/paignia).
This repository's `extraction-manifest.json` now records the immutable provider
and historical source provenance. `scripts/validate_extraction.py` rejects local
generic cores, mutable Git refs, dependency patch overrides and lockfile drift.
It does not claim registry artifacts or a fully qualified economic model.

Native consumer tests exercise actual Paignia APIs. Paignia's provider CI owns
its own unit tests and extracted-source smoke. The current application target
has an analytic finite offer/response oracle. Exact dependency and native results
are recorded in T17 metadata/runlog; artifact and real-consumer release gates
remain open.

The chosen repository exists; ordinary authorized source/dependency work needs
no additional approval chain. Registry publishing and scientific qualification
remain separate. Original source licences and history are retained in
[the transfer map](../architecture/paignia-transfer-map.md) and Paignia notices.
