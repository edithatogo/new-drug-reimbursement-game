# Atlas Scenario 4 packet request (draft; not sent)

**Status:** draft / no external request sent
**Purpose:** obtain one same-programme, approved-derived evidence packet for
Scenario 4. This request is limited to research-only derived values and does
not request raw patient, confidential, or undisclosed commercial payloads.

## Required identity and binding

Atlas should provide an immutable packet identifier and revision (commit or
content-addressed export), stable programme ID, payer, service line, decision
date, price year, intervention, comparator, displaced programme, and horizon.
Every field below must resolve to that same programme and decision context.

## Required derived fields

* `m`: annual programme health effect;
* `d`: annual displaced-programme health effect;
* `mu`: marginal health effect per unit of investment;
* `phi`: programme efficiency/scale parameter;
* annual programme incremental health effect and investment cost;
* primary discounting convention and rate, plus sensitivity convention;
* uncertainty distributions, covariance/correlation assumptions, and any
  truncation or transformation rules.

The packet must state units, currency, price base, time origin, and whether
values are discounted or undiscounted. It must document the transformations
from each source field to each derived field and identify missingness or
imputation explicitly.

## Provenance and source terms

For every input, include authoritative source URL or identifier, publisher,
publication/version date, page/table/field locator, retrieval timestamp,
SHA-256 of the captured source, and licence/source-term disposition. State
permitted destinations (repository, tests, research-only outputs), attribution
requirements, retention period, and any redistribution prohibition. No packet
is acceptable without an owner/curator approval record bound to the immutable
revision.

## Promotion checks

The receiving repository will verify finite values and the Scenario 4 domain:
`phi > 1`, `mu > 0`, `mu < m`, `d <= m`, and positive net investment health
gain. It will also verify the model identities:

```text
phi * DeltaE_G = DeltaC_P / mu
1 / beta_c^v = 1 / d + 1 / mu - 1 / m
```

Promotion from sensitivity-only to calibrated research output requires a
complete packet, source-term permission, reproducible fixture, and panel
receipts bound to the exact packet revision and repository commit. Calibrated
or regulatory claims remain out of scope.

## If Atlas cannot supply the packet

Please return an explicit negative/deferred disposition naming each missing
field, the immutable revision reviewed, and whether a future re-request is
permitted. Do not substitute cross-programme values or infer displacement.
