# BEMPIC v0.1.0 Roadmap and Release Gates

**Status:** in progress; [REQ-GATE-001] `v0.1.0` MUST NOT be tagged yet

**Target:** first public semantic specification and governance baseline

This roadmap is release authority. Checked boxes require evidence linked from a
pull request or release issue. Aspirational performance targets do not become
passing results by documentation alone.

## 1. Specification and governance

- [x] Define repository and architecture ownership.
- [x] Define v0.1 scope, non-goals, terminology, bounds, states, invariants,
  operations, failure behavior, persistence, reopen/resume, accounting,
  compatibility, extensions, and codec-analysis requirements.
- [x] Adopt Apache-2.0 with copyright and notice text.
- [x] Publish governance, contribution, decision, security, conformance,
  vector-definition, changelog, and draft release-note documents.
- [x] Mark the Python proof transitional and its generation-0 bytes
  non-normative.
- [x] Define codec allocation/status rules, maximum-size proof evidence, the
  V01–V15 catalog, metric semantics, external M4P confirmation, a release-record
  template, and a machine-validated normative conformance matrix.
- [ ] Resolve every `release-blocking` item in
  [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md).
- [ ] Review normative terms for contradictions and approve the specification
  through the governance process.

## 2. Required work in `bempic-reference`

[REQ-GATE-002] Before this repository may tag v0.1.0, the sibling repository MUST:

- [ ] record its Apache-2.0 license, governance-compatible contribution terms,
  and exact dependency notices;
- [ ] implement the bounded message, part, representation, collection, and
  receipt model without OceanMail, M4P-routing, or modem policy types;
- [ ] implement the seven core semantic operations and all state transitions in
  [`SPECIFICATION.md`](../SPECIFICATION.md);
- [ ] implement deterministic preparation, full 32-octet schema fingerprints,
  SHA-256 representation IDs, strict validation, and exact reconstruction;
- [ ] implement append-only checkpoints, delta reconciliation, deterministic
  bounded full-inventory fallback, and durable page cursors;
- [ ] implement hard total and directional BEMPIC budgets plus exact preflight
  sizing and the required accounting counters, including reproducible
  directional `semantic_bytes` fixture breakdowns with a shared immutable
  endpoint-role binding and representation-descriptor exclusion;
- [ ] implement crash-consistent prefix persistence, process reopen, resume
  through a different authorized source, quarantine/retry after corruption, and
  idempotent duplicate operations and receipts;
- [ ] implement capability/version/schema/codec/extension negotiation and every
  required fail-closed incompatibility path;
- [ ] implement at least one clearly labeled experimental deterministic codec
  with declarative bounds, mandatory maximum encoded sizes, canonical
  parameters, exact encoded-size analysis, strict allocation limits, and all
  proof evidence required by [`REGISTRIES.md`](REGISTRIES.md);
- [ ] run malformed-input fuzzing and property tests over codec and state-machine
  boundaries with published tool versions and zero unresolved correctness or
  memory-safety findings;
- [ ] consume the vector format in [`TEST-VECTORS.md`](TEST-VECTORS.md), publish
  every V01–V15 case in
  [`../conformance/v0.1/vector-catalog.json`](../conformance/v0.1/vector-catalog.json),
  publish the mandatory vector bundle, and pass it on all supported platforms;
- [ ] provide an independent decoder or vector verifier that agrees byte for
  byte with the primary implementation;
- [ ] reproduce every required behavior of the transitional Python proof or
  link an accepted decision documenting the normative difference;
- [ ] publish deterministic raw, MIME, B2F/LZHUF, candidate codec, interrupted
  restart, and persistent-resume measurements required by
  [`METRICS.md`](METRICS.md), with dependency/license details;
- [ ] execute every row of the normative 24-row V08 interruption/restart/storage
  covering array, publish its pair-coverage proof and exact trace fields, and
  retain the separate before/after V14 durable-transition evidence;
- [ ] demonstrate zero deferred attachment payload before selection, exact
  budget enforcement, no resend of a fully durable prefix, and zero-byte quote
  error for deterministic no-fault plans;
- [ ] expose an opaque-record carrier trait and demonstrate a mock M4P binding
  without implementing routing, fragmentation, deduplication, or TTL; and
- [ ] record one immutable passing commit SHA and green CI URL in the v0.1.0
  release PR in this repository.

### Current sibling evidence checkpoint (not a passing gate)

The latest audited public checkpoint is
[`bempic-reference` commit `cf3485f6606d6462077e8edd1592264c3ce4ca5e`](https://github.com/Gordonfive/bempic-reference/commit/cf3485f6606d6462077e8edd1592264c3ce4ca5e),
with successful [exact-head CI](https://github.com/Gordonfive/bempic-reference/actions/runs/33569955919).
Its immutable
[`conformance/v0.1.0-report.json`](https://github.com/Gordonfive/bempic-reference/blob/cf3485f6606d6462077e8edd1592264c3ce4ca5e/conformance/v0.1.0-report.json)
self-reports `blocked-not-conformant`, identifies implementation commit
[`38c01eb41d96a02c97478650efbde859888e6908`](https://github.com/Gordonfive/bempic-reference/commit/38c01eb41d96a02c97478650efbde859888e6908),
and still reports the older specification commit `c67a87e` for the overall
conformance run.

The same checkpoint's immutable compact-candidate profile, exact-size formulas,
maximum witnesses, malformed/property results, draft vectors, licensing, and
same-owner Python verifier satisfy the evidence minimum for provisional
experimental allocation. Its private candidate `0xffff0001/2` measured 35 B
warm and 75 B cold on the prescribed V01 fixture. Those lengths are useful
allocation evidence but are not public-tuple release results: the sibling has
to regenerate encoded records, representation IDs, checkpoint and collection
digests, vectors, and verification for allocated `0x00010000/1` and the exact
clarified specification commit. Mandatory V01–V15/codec-boundary evidence,
independent ownership, B2F, and external M4P approval remain incomplete.

### Current OceanMail application evidence

Application-owned object identity is now documented at immutable
[`oceanmail` commit `cc55c1b7d5a03aa2e5cc8cd617f9d1bb7b6a3600`](https://github.com/Gordonfive/oceanmail/commit/cc55c1b7d5a03aa2e5cc8cd617f9d1bb7b6a3600),
with successful [exact-head CI](https://github.com/Gordonfive/oceanmail/actions/runs/33569928056),
an immutable
[`BEMPIC-APPLICATION-PROFILE.md`](https://github.com/Gordonfive/oceanmail/blob/cc55c1b7d5a03aa2e5cc8cd617f9d1bb7b6a3600/docs/BEMPIC-APPLICATION-PROFILE.md),
and a content-addressed
[fixture](https://github.com/Gordonfive/oceanmail/blob/cc55c1b7d5a03aa2e5cc8cd617f9d1bb7b6a3600/tests/fixtures/bempic-application-profile-v1.json).
The profile uses an application-generated 32-octet CSPRNG identifier, durable
no-reuse binding, and conflict handling while leaving the BEMPIC core ID
opaque. It is current application evidence, not a BEMPIC wire change and not a
substitute for the required V11 conflict traces against the release candidate.

The sibling does not need to freeze a permanent wire format or ship production
cryptography for v0.1.0. It must label the codec experimental and [REQ-GATE-003] MUST NOT carry
real private user traffic without a separately reviewed security profile.

## 3. Transitional prototype parity gate

`prototype/` remains in this repository until all of the following are true:

- [ ] The sibling passes deterministic round-trip, interruption, reopen,
  corruption, retry, idempotency, deferred-attachment, reconciliation, exact
  quote, and budget tests at least as strong as the prototype tests.
- [ ] Published sibling results explain any byte difference from
  `prototype/results/baseline-2026-08-30.json`.
- [ ] Maintainers accept a decision that says whether the prototype will be
  archived, retained as an independent oracle, or removed in a later release.

Passing this gate authorizes a later change; it does not itself delete or move
the prototype.

## 4. Repository verification gates

- [ ] All existing Python unit tests pass on the supported Python matrix.
- [ ] The demo completes with exact decode, deferred attachment behavior, and
  no unexpected duplicate payload.
- [ ] The deterministic benchmark completes and any changed baseline is
  reviewed rather than silently replaced.
- [ ] Internal Markdown links and repository consistency checks pass.
- [ ] The normative requirement matrix, codec registry, vector catalog, metrics, and
  incomplete release-record controls pass `scripts.validate_release_gates`.
- [ ] All required conformance vector definitions have a corresponding sibling
  artifact.
- [ ] The release commit contains no secrets, private corpus, generated local
  state, or accidental sibling-repository changes.

## 5. Protocol acceptance gates

- [ ] All correctness items in [`CONFORMANCE.md`](CONFORMANCE.md) pass.
- [ ] Every row in [`CONFORMANCE-MATRIX.md`](CONFORMANCE-MATRIX.md) has immutable
  passing evidence in the release record.
- [ ] Warm no-change synchronization is no more than 64 B and cold no-change is
  no more than 128 B for the prescribed 100-message experimental-codec vector,
  excluding a separately reported application-security handshake. The private
  candidate measured 35 B/75 B; the gate remains open until regenerated
  public-tuple `0x00010000/1` vectors and exact-head verification exist.
- [ ] Adding one message to a valid retained checkpoint does not retransmit the
  other 100 manifests.
- [ ] No selected deterministic no-fault plan exceeds its accepted BEMPIC
  budget or differs from its exact preflight quote.
- [ ] Every prescribed fixture reproduces the exact directional
  `semantic_bytes` identity from its content-addressed decoded semantic inputs,
  fixed endpoint-role binding, and descriptor-exclusion rule.
- [ ] No unselected attachment representation payload is emitted.
- [ ] No fully durable prefix is resent after reopen; a matching duplicate
  caused by lost durability knowledge is counted explicitly.
- [ ] Every completed representation passes length, digest, ID, schema, and
  decode validation before a positive receipt.
- [ ] B2F comparison results are reproducible. The median prescribed text
  corpus target is at least 10% fewer total BEMPIC bytes; any fixture more than
  5% above B2F has an accepted, measured resumption/metering justification.
- [ ] M4P reviewers or maintainers confirm the proposed application binding
  does not duplicate M4P network responsibilities, with every field and trace
  required by [`M4P-CONFIRMATION.md`](M4P-CONFIRMATION.md).

## 6. Tag procedure

After every item above is checked with evidence:

1. Freeze the release candidate commit through a reviewed pull request.
2. Complete the immutable evidence record required by
   [`RELEASE-RECORD.md`](RELEASE-RECORD.md) and put the sibling passing commit
   SHA and vector-bundle digest in
   [`RELEASE-NOTES-v0.1.0.md`](RELEASE-NOTES-v0.1.0.md).
3. Change the specification and release notes from “release candidate” to
   “released”.
4. Confirm `CHANGELOG.md`, license notices, links, tests, demo, benchmark, and
   CI from the exact release commit.
5. Create signed annotated tag `v0.1.0` from that commit and publish the release.

Until then, branches, commits, and documents may say “for v0.1.0” but [REQ-GATE-004] MUST NOT
claim the release or tag exists.
