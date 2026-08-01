# External-gate resolution plan

This is the execution packet for gates that cannot be closed by repository
tests alone. It does not grant approval, promote candidate evidence, or make a
reimbursement recommendation. Each gate remains fail-closed until its named
receipt is supplied and checked.

## Recommended route

Proceed on two parallel lanes:

1. Keep the research software and synthetic Chapter 7 scenarios reproducible.
2. Collect the minimum real-world evidence and human decisions for a bounded
   NHS methodological pilot.

The release scope remains research software and methodology. Calibrated
recommendations, regulator-facing claims, and redistribution of restricted
source evidence remain out of scope until the applicable gates pass.

## Gate register

| Gate | Recommended closure route | Required receipt | Fallback while pending |
|---|---|---|---|
| NHS decision context | One real, narrowly scoped payer/service-line decision | Signed context packet naming payer, decision date, price year, intervention, comparator, displaced programme, stable programme ID, and accountable owner | Run synthetic scenarios; keep real calibration disabled |
| Displacement identity | One auditable displaced programme with baseline cost and unit | Programme identifier, source citation, baseline definition, and owner confirmation | Use a labelled synthetic comparator only |
| Atlas evidence | Atlas-produced approved-derived packet for the selected context | Packet ID, revision, source/licence metadata, mapping review, and approval receipt | Candidate dossier remains non-promotable |
| Source terms | Reconcile Atlas data terms and Hugging Face Hub metadata | Written owner/licence adjudication bound to exact revision and publication surface | Keep derived outputs private; do not publish source-derived data |
| Health-economics review | Named independent health economist plus technical review panel | Reviewer identity/role, conflict declaration, reviewed revision, comments, disposition, and sign-off date | Internal review may improve code but cannot close the gate |
| Discounting convention | Report DHSC 1.5% and NICE 3.5% sensitivities, then select a primary convention | Decision record naming primary rate, perspective, horizon, and rationale | Keep both sensitivities and mark primary unresolved |
| UOGTO/Kairos integration | Use exact released upstream contracts and acceptance evidence | Upstream revision, compatibility result, trace receipt, and owner disposition | Keep adapters isolated; make no native-integration claim |
| Extraction/release authorization | Research-software release only until owner approvals exist | Extraction approval, legal/regulatory disposition, release commit, and maintainer authorization | Do not publish calibrated or regulator-facing outputs |

## Evidence packet requirements

Every submitted packet must be immutable or hash-addressable and include the
exact revision, provenance and licence metadata, intended use, transformations,
unit conversions, reviewer or owner identity, approval date, and exclusions or
unresolved assumptions.

The application may consume only approved-derived Atlas records. Candidate or
raw records may support testing but cannot enter the approved calibration path.

## Recommended decisions

1. Select the real NHS context route rather than claiming calibration from the
   current candidate dossier.
2. Select approved-derived Atlas records rather than promoting candidates.
3. Use both discount rates as sensitivities until independent review selects the
   primary convention.
4. Keep the first release research-only and fail closed on unmet gates.

If a real context or approved packet cannot be obtained, retain the synthetic
methodological release. That is a deliberate limitation, not a failed build.

## Closure sequence

1. Record the NHS context and displaced-programme receipts.
2. Request the Atlas approved-derived packet and source-term disposition.
3. Bind the packet to named independent health-economics review.
4. Resolve discounting and interpretation choices in that review.
5. Re-run calibration, uncertainty, and provenance validation at bound revisions.
6. Record upstream, extraction, legal, and release dispositions separately.
7. Promote scope only after each applicable gate has a passing receipt.

Until then, the existing fail-closed readiness receipt remains authoritative.
