# Paignia static v1 replay

This application checks that the optional Paignia interchange can still solve
the frozen static v1 request and emit the frozen response byte for byte. The
replay calls `paignia_io::solve_static_json` and appends the wire record's final
newline before comparing. The checked-in records are Paignia's synthetic public
fixture. Their expected policy selects the lottery and take actions, with
expected payoffs of 2 and 4. [Source records at the provider pin](https://github.com/edithatogo/paignia/tree/2f297bf3eb6031e455af41211063a949656a3bcf/verification/uogto_interchange/frozen-static-v1).

## Replay

From this directory, run the same locked replay as the application's Rust CI.

```sh
shasum -a 256 --check SHA256SUMS
cargo fetch --locked
cargo test --locked --offline
```

After a successful run, the CI job summary records the application revision,
resolved provider, Rust version, lockfile digest and fixture digests.

## Dependency decision

The replay uses Apache-2.0 `paignia-io` at an immutable Git revision with an
independent test lockfile. This keeps interchange qualification confined to
verification and preserves the Chapter 8 runtime's existing core and solver
pins. Advance the replay pin only after the next provider revision passes the
same frozen-byte contract. Use the [Chapter 8 acceptance path](../../docs/architecture/paignia-chapter8-application.md)
for application-model qualification.
