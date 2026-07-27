# Rust style

- Let rustfmt decide mechanical layout.
- Model invariants in types and return `Result` for recoverable failures.
- Keep public surfaces small and document public APIs.
- Avoid unexplained panics and unsafe code.
- Treat Clippy warnings as errors and run the full workspace tests.
