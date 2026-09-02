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
directional `semantic_bytes`, the shared immutable endpoint-role binding, and
evidence that representation descriptors contributed zero. V08 evidence MUST
include the complete 24-row covering array and pair-coverage proof.

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
keeps incomplete fields empty or failing and records all blockers. It is a
governance control, not evidence that v0.1.0 exists. The provisional codec
selection question is now narrowed to public-tuple vector and conformance
regeneration: experimental tuple `0x00010000/1` is allocated, but it is neither
approved nor mandatory and does not carry stable-wire or production-security
assurance. The independent verifier, B2F oracle, M4P confirmation,
protocol-name decision, complete sibling implementation evidence, and final
release candidate results remain unresolved.

The M4P technical review package is locally complete at
[`m4p-binding-review-package.json`](../conformance/v0.1/m4p-binding-review-package.json)
against authoritative specification commit
[`2eca9e8f57d43dab250cc26c1bbf2d255e3331de`](https://github.com/Poseidons-Forge/m4p-spec/commit/2eca9e8f57d43dab250cc26c1bbf2d255e3331de).
It defines the proposed complete opaque-record boundary, closed normalized
submission results, layer ownership, alternate-source/carrier resume,
receipt/lost-receipt behavior, conservative uncertain-acceptance accounting,
and six V09/V10/V12 traces. Its status is
`ready-for-external-review-not-submitted`; no upstream URL, reviewer, approval,
answers digest, concrete implementation mapping, or passing trace digest exists.
The release template records the package while keeping `m4p-binding-review`
blocked.

The B2F legal/technical decision is recorded in
[`B2F-ORACLE.md`](B2F-ORACLE.md) and its
[`machine-readable artifact`](../conformance/v0.1/b2f-oracle-decision.json).
Its decision status is `blocked-no-qualified-oracle`: ARSFI is authoritative and permissively licensed but does
not publish a complete standalone oracle; `paclink-unix` offers a GPL-2.0-or-
later process executable but lacks the pinned standalone build, prescribed
corpus, full-envelope, and cross-implementation evidence; and `wl2k-go`/Pat
retain an explicit LZHUF copyright-provenance caveat. The release template
records this decision without claiming results, and the B2F blocker and both
compactness thresholds remain unchanged.

The audited, non-passing Reference checkpoint is
[`bempic-reference@cf3485f6606d6462077e8edd1592264c3ce4ca5e`](https://github.com/Gordonfive/bempic-reference/commit/cf3485f6606d6462077e8edd1592264c3ce4ca5e),
whose [exact-head CI succeeded](https://github.com/Gordonfive/bempic-reference/actions/runs/33569955919).
Its immutable
[conformance report](https://github.com/Gordonfive/bempic-reference/blob/cf3485f6606d6462077e8edd1592264c3ce4ca5e/conformance/v0.1.0-report.json)
states `blocked-not-conformant`; its profile, proof, witnesses,
malformed/property results, same-owner Python verifier, and 35 B warm / 75 B
cold measurements are accepted only as provisional allocation evidence.
The report predates the normative clarifications and public allocation, binds
private candidate `0xffff0001/2`, and therefore still requires a rerun against
the exact clarified specification and `0x00010000/1`. No passing row is
silently promoted to release evidence.

Current immutable application-owned object-identity evidence is recorded from
[`oceanmail@cc55c1b7d5a03aa2e5cc8cd617f9d1bb7b6a3600`](https://github.com/Gordonfive/oceanmail/commit/cc55c1b7d5a03aa2e5cc8cd617f9d1bb7b6a3600),
with [successful exact-head CI](https://github.com/Gordonfive/oceanmail/actions/runs/33569928056),
the immutable
[application profile](https://github.com/Gordonfive/oceanmail/blob/cc55c1b7d5a03aa2e5cc8cd617f9d1bb7b6a3600/docs/BEMPIC-APPLICATION-PROFILE.md),
and its [fixture](https://github.com/Gordonfive/oceanmail/blob/cc55c1b7d5a03aa2e5cc8cd617f9d1bb7b6a3600/tests/fixtures/bempic-application-profile-v1.json).
OceanMail owns those application semantics; BEMPIC continues to treat
`object_id` as opaque. This resolves the missing application-profile artifact,
not the still-required BEMPIC V11 sender/receiver conflict evidence.
