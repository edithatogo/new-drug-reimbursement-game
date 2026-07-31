# Evidence calibration contract

## Boundary

Reimbursement Atlas owns evidence acquisition, source licensing,
transformations, and human approval. This application consumes a versioned
approved-derived JSON packet and adds only the Chapter 7 parameter-role
interpretation. Voiage owns VOI calculations; this application prepares
aligned `ValueArray` and `ParameterSet` inputs but does not calculate VOI.

The executable packet contract is
`schemas/parameter-evidence-packet-v1.schema.json`. It is bound to the Atlas and
Voiage revisions in `ecosystem.lock.toml`.

Public-source methodological triage uses the separate
`schemas/parameter-evidence-candidate-dossier-v1.schema.json` contract. Its
records are candidate-only, cannot be converted by the application, and never
enter the approved packet or calibration path. See
`docs/research/nhs-england-methodological-pilot.md`.

## Fail-closed controls

Every packet has one decision context: jurisdiction, payer, budget boundary,
service line, price year, decision date, implementation horizon, currency, and
health unit. Every record adds a programme identity, role, method, marginality,
causal assumptions, point value, uncertainty representation, scale limits,
source URI/checksum/licence, transformation, reviewer, approval state, and
evidence revision.

The parser rejects:

- raw, candidate, rejected, unreviewed, or structurally ambiguous records;
- non-finite values, numeric strings, unsupported units, and samples outside
  stated scale limits;
- average or incremental values labelled as marginal ICER roles;
- incomplete source hashes, transformations, reviewers, or causal assumptions;
- incompatible or missing scenario roles, duplicate role selections, and
  unequal uncertainty sample counts;
- Scenario 4 inputs that do not describe one investment programme or do not
  satisfy the source equations on every draw.

Deterministic records may be broadcast across an already aligned sampled
packet. This does not create uncertainty. No probability distribution is fit
or sampled by this repository.

## Calibration receipt

Each calibration creates a deterministic SHA-256 revision over the case ID,
scenario, decision-case cost/effect, packet identity, and the selected record
IDs, evidence revisions, roles, and source checksums. The receipt retains those
references and the evidence context. `decision_use_permitted` is always false:
software cannot upgrade a technical receipt into policy approval.

## Voiage handoff

For every aligned evidence draw, the strict Chapter 7 evaluator produces the
health value of `reimburse` and `best_available_alternative`. The adapter maps
those rows to Voiage `ValueArray` and maps the parameter draws to
`ParameterSet`. EVPI, EVPPI, EVSI, ENBS, sampling, and correlation estimation
remain outside this repository.

The pinned Voiage API requires its optional NumPy numerical environment. A
missing or broken optional runtime raises an explicit error after the
dependency-free bundle has been validated.

## Synthetic fixture

`fixtures/evidence/synthetic-chapter7-parameter-packet-v1.json` exists only for
conformance testing. Its jurisdiction is
`SYNTHETIC-NOT-FOR-DECISIONS`, and its output is never empirical or suitable
for reimbursement, HTA, or policy decisions.
