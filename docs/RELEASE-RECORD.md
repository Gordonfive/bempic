# BEMPIC v0.1.0 Release Record Requirements

The release record is the auditable index for the tag decision. It is completed
in the release pull request; prose claims without linked immutable evidence do
not satisfy a gate. The current machine-readable template is
[`../conformance/v0.1/release-record-template.json`](../conformance/v0.1/release-record-template.json)
and is intentionally incomplete.

## Required content

[REQ-RELEASE-001] Before `v0.1.0` is tagged, the release pull request MUST add a
record derived from the template containing the exact specification commit and
pull request; final CI run; sibling `bempic-reference` commit, repository URL,
and green CI run; protocol generation; every schema fingerprint; selected codec
ID, revision, experimental status, profile digest, size-proof digest, and
license notices; vector-bundle and conformance-report digests; supported
platform results; fuzz/property evidence; benchmark and metric records; B2F
oracle identity/version/license/results; M4P confirmation; prototype parity
decision; resolution links for every release-blocking open question; security
classification; changelog/release-note review; and named approvals required by
governance. The metric records MUST include independently recomputed
directional `semantic_bytes`, and V08 evidence MUST include the complete
24-row covering array and pair-coverage proof.

[REQ-RELEASE-002] Every repository URL MUST identify an immutable commit or tag,
every CI URL MUST be for that commit and conclude successfully, and every digest
MUST state its algorithm. The record MUST distinguish `not-applicable` with a
reason from missing, pending, failed, or unavailable evidence. A mutable branch,
latest-build URL, chat assertion, or local-only result is insufficient.

[REQ-RELEASE-003] The release record MUST include a machine-generated gate list
in which every roadmap gate and every conformance-matrix requirement is `pass`,
with its evidence links or digests. Any `pending`, `fail`, `blocked`, missing, or
unknown value prevents the release-state field from becoming `ready`.

[REQ-RELEASE-004] The final release candidate verification MUST run from the
exact proposed tag commit in a clean checkout, validate documentation and all
machine-readable artifacts, recompute schema and vector digests independently,
run the complete Python tests, demo, benchmark, and required conformance suite,
and check for secrets, private corpus, generated local state, and sibling
changes. The record MUST contain commands, tool versions, exact results, and CI
links without embedding secrets or enormous logs.

[REQ-RELEASE-005] The tag field MUST remain JSON `null` and `release_state` MUST
remain `not-ready` until all gates pass and the reviewed tag procedure begins.
Creating or claiming the tag from this tranche is prohibited.

## Current state

The template names every release-decision evidence class but intentionally
keeps those fields empty or failing and records all blockers. It is a
governance control, not evidence that v0.1.0 exists.
The experimental codec, independent verifier, B2F oracle, M4P confirmation,
object-ID application profile, protocol-name decision, sibling implementation,
and final release candidate results are unresolved.

The template also records an audited, non-passing sibling checkpoint so that
existing work is not lost or overstated. The checkpoint is
[`bempic-reference@29be83fed70433ea958f9773539fb8b93fa00dc9`](https://github.com/Gordonfive/bempic-reference/commit/29be83fed70433ea958f9773539fb8b93fa00dc9),
its [push CI succeeded](https://github.com/Gordonfive/bempic-reference/actions/runs/33471197976),
and its immutable
[conformance report](https://github.com/Gordonfive/bempic-reference/blob/29be83fed70433ea958f9773539fb8b93fa00dc9/conformance/v0.1.0-report.json)
states `blocked-not-conformant`. That report names implementation commit
[`c8d940ca69fe98aecf72185f80f4a2b3254aaf24`](https://github.com/Gordonfive/bempic-reference/commit/c8d940ca69fe98aecf72185f80f4a2b3254aaf24)
and specification commit `c67a87e`; it predates the normative clarifications in
this change. Its passing rows remain useful evidence candidates, but no row is
promoted into release evidence until a new report evaluates the exact clarified
specification commit and satisfies every currently blocked or incomplete gate.
