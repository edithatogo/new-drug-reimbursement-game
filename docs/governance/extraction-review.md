# Extraction review packet

The extraction boundary was validated with `scripts/validate_extraction.py`.
The manifest contains only `uogto-game-core` and `uogto-game-solve`, permits
only the declared internal dependency, and rejects reimbursement/application
vocabulary in Rust sources. The workspace quality gate also runs formatting,
Clippy, and tests for the extracted crates.

Current disposition: repository-owned extraction checks pass. A separate
extraction-repository owner must still approve transfer, publication, and
release authorization.
