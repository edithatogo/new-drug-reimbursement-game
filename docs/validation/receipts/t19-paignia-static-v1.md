# T19 downstream acceptance

The New Drug Reimbursement Game replay passed on Rust 1.75.0 and 1.100.0
from application commit `e869cb362057ecf205d6719e9108e3801e8ada7f`. Both runs used
`cargo test --locked --offline` after fetching the locked dependencies.
The application test passed the frozen request to `paignia_io::solve_static_json`
and matched every response byte, including the final record newline.
The resulting policy selected lottery and take, with expected payoffs of 2 and 4.

The test resolved Apache-2.0 `paignia-io` 0.1.0 from Paignia commit
`2f297bf3eb6031e455af41211063a949656a3bcf`. The wire version was 1.0.0.

| Replay input | SHA-256 |
| --- | --- |
| Request | `1475a91753b587c93f6f460648246b60d44269662bff5e8d77c10bcdc21e1db5` |
| Expected response | `9c80fd97f6285f5cf1a9819da868910746090e0b2572d133ad4109c3df08a220` |
| Replay lockfile | `fd83db007b5e5cf010397e6ea9409ac3c1be917ec42b9c336c6d9f7d00b298c4` |

The application's Rust CI repeats the synthetic compatibility check and records
the executed revision and digests. [Replay commands and fixture provenance](../../../verification/paignia-static-v1/README.md).
