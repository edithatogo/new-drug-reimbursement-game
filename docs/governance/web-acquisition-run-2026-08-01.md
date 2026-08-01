# Web acquisition run — 2026-08-01

The repository acquisition utility was run against all six allow-listed official
sources. Five fetched successfully with HTTP 200; one source returned HTTP 404
and is retained as a negative receipt. These hashes bind this run's retrieved
bytes, not an approval or calibration decision.

| Source | Status | Bytes | SHA-256 prefix |
|---|---:|---:|---|
| NICE TA1121 recommendations | 200 | 21,159 | `303e62b62bc13168311a633a664d5bfd40a2a4f74a2189702f8f8987657a744a` |
| NICE TA1121 resource impact | 200 | 56,531 | `002ed229eb53c18c502ab5c290b7e3613052e7448518ecd619071d7146cf1213` |
| NHS Payment Scheme 2026/27 | 200 | 59,678 | `94c532a68a24a654febee24f0592a10785a65709656bcc2c54a02c59efdcaf8d` |
| Cheshire/Merseyside TA1121 adherence | 200 | 427,995 | `2aeecd61aeaf843f50697ab028779fa5cdcf712b2bbf7f945496f89144772c1b` |
| Kent and Medway TA1121 formulary | 200 | 37,525 | `4f9ebce3f69ef49aca016df4c738eb25912629cf2ecaa43b3d2a8475e7be18b9` |
| North West TAG acoramidis PDF | 404 | — | unavailable at queried URI |

The 404 is not treated as evidence of absence; the source URL or a current
official replacement must be resolved before relying on that document. All
successful records remain candidate-only and still do not identify a local
displaced programme or approved Atlas parameter values.
