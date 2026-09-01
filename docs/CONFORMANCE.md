# BEMPIC v0.1 Conformance

## Claims

[REQ-CLAIM-001] Conformance is scoped. An implementation MUST state each class and profile it
claims, the exact specification commit or tag, supported protocol generation,
schema fingerprints, codec IDs/revisions, extensions, limits, security class,
and carrier bindings.

### Semantic core conformer

Implements the v0.1 model, operations, states, persistence, failure, budget,
accounting, integrity, compatibility, and extension semantics independent of a
particular codec.

### Codec profile conformer

Implements one named experimental or stable codec profile and publishes every
artifact required by Specification Section 13. Codec conformance does not by
itself imply state-machine or persistence conformance.

### Carrier binding conformer

Maps complete BEMPIC operations to one named carrier, reports its guarantees
and cost domain truthfully, and preserves the M4P/DataLink boundary.

### Application profile conformer

Defines application acceptance/delivery meanings, address and media-type
policy, optional transformations, and any required extension or security
profile without changing core receipt meanings.

## Required semantic checklist

[REQ-CONF-001] A semantic core conformer MUST pass all applicable checks:

- [ ] Enforce every core bound before allocation or durable mutation.
- [ ] Normalize metadata and prepare identical inputs deterministically.
- [ ] Compute schema fingerprints, content digests, and representation IDs
  exactly as specified.
- [ ] Reject reuse of an object or representation ID with conflicting metadata.
- [ ] Defer every unselected representation and attachment payload.
- [ ] Reconcile equal collections, known checkpoints, and unknown checkpoints
  through bounded deterministic pages.
- [ ] Persist page cursors and reject inconsistent target digests.
- [ ] Send data only after an explicit request and only from its named offset.
- [ ] Accept matching duplicates idempotently; reject gaps and conflicts.
- [ ] Never emit a complete operation across a total or directional budget.
- [ ] Account for every encoded BEMPIC octet in the correct direction/scope.
- [ ] Label lower-layer counters as exact or estimated and never conflate them
  with BEMPIC counters.
- [ ] Recover the last durable prefix after process restart.
- [ ] Resume identical bytes through a different authorized source/carrier.
- [ ] Verify exact length, SHA-256, representation ID, schema, and deterministic
  decode before commit.
- [ ] Never issue `REPRESENTATION_COMMITTED` before atomic commit.
- [ ] Treat representation, application-accepted, and application-delivered
  receipts as distinct idempotent states.
- [ ] Negotiate the deterministic highest common semantic/schema/codec tuple.
- [ ] Skip unknown optional extensions and reject unknown critical extensions
  before state mutation.
- [ ] Fail closed on malformed, truncated, oversized, ambiguous, non-canonical,
  unsupported, overflowed, or corrupted input.
- [ ] Preserve unrelated committed state after a scoped failure.
- [ ] Treat contact loss and budget exhaustion as resumable pauses.
- [ ] Avoid routing, forwarding, network TTL, generic fragmentation, link ARQ,
  and other M4P/DataLink behavior.

## Required codec checklist

- [ ] Registered ID/revision and status (`experimental`, `approved`,
  `mandatory`, or `deprecated`) published under `REGISTRIES.md`.
- [ ] Exact supported schema fingerprints published.
- [ ] Field types, presence, order, bounds, precision, and rounding documented.
- [ ] Every operation is complete and length-delimited.
- [ ] Maximum encoded size is stated for every operation and schema.
- [ ] Exact encoded size is computable without trial serialization.
- [ ] Worst-case analysis proves the maximum-size claims.
- [ ] Encoding is deterministic and decoding is strict/canonical.
- [ ] Unknown-field and extension criticality behavior is demonstrated.
- [ ] Allocation and nesting limits are tested before allocation.
- [ ] Mandatory valid, boundary, malformed, and non-canonical vectors pass.
- [ ] At least one independent decoder/verifier agrees on the vector bundle.

Codec allocation, status progression, approval evidence, and worst-case proof
requirements are normative in [`REGISTRIES.md`](REGISTRIES.md).

## Required persistence and crash cases

[REQ-CONF-002] Tests MUST interrupt before and after every durable transition, including offer
page commit, prefix-length update, final byte, digest verification, object
commit, and receipt commit. On reopen, the implementation may roll back to the
last reported durable state but may not advance beyond recoverable bytes,
commit unverified content, or emit a false positive receipt.

Required interruption points include 0%, 1%, 10%, 50%, 90%, the final byte,
post-verification/pre-commit, and post-commit/pre-receipt. Sender, receiver, and
both processes must be restarted. At least one case resumes from a different
authorized source and one from a different carrier.

## Required accounting cases

For each prescribed fixture, report semantic, BEMPIC, representation payload,
useful committed, duplicate, carrier (when exposed), and link (when exposed)
bytes by direction. Verify exact no-fault plan quotes, hard total/directional
budgets, zero unselected payload, useful bytes to first body, resume control
cost, and full-restart versus persistent-resume cost.

The counter names, measurement envelope, first-body definitions, aggregation,
and pass thresholds are normative in [`METRICS.md`](METRICS.md).

## Evidence

A conformance report is machine-readable and includes:

- implementation name/version and immutable source commit;
- specification commit/tag;
- platform, compiler/runtime, dependency lock digest, and test tool versions;
- claimed classes/profiles and unsupported optional behavior;
- vector bundle digest and per-vector pass/fail/skip with reason;
- fuzz/property-test duration, seed corpus digest, and unresolved findings;
- benchmark input/result digests; and
- deviations linked to accepted decisions.

Self-attestation is permitted during major-zero development, but [REQ-CLAIM-002] the report
MUST NOT use “BEMPIC v0.1.0 conformant” until the specification tag exists.

Every normative requirement and its evidence class is indexed in
[`CONFORMANCE-MATRIX.md`](CONFORMANCE-MATRIX.md).
