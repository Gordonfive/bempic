# BEMPIC Test-Vector Definitions

## Ownership and location

This repository owns what a BEMPIC vector means, its required metadata, and the
mandatory vector catalog. Executable generators, runners, and published result
bundles belong in `bempic-reference`. Small normative vector data may later be
committed here when a codec profile is approved.

The generation-0 vectors implicit in `prototype/tests/` test the transitional
proof only and are not v0.1 wire vectors.

The small
[`JCS canonicalization fixture`](../schemas/v0.1/jcs-canonicalization-vectors.json)
is committed here because it protects normative schema-fingerprint inputs. It
includes ECMAScript number formatting, UTF-16 property ordering, duplicate-key,
non-JSON-number, and lone-surrogate cases derived from RFC 8785. It is not a
codec or operation-byte vector bundle.

## Bundle format

[REQ-VEC-001] Each versioned bundle MUST have a canonical manifest containing:

- bundle format version and immutable bundle digest;
- specification commit/tag;
- protocol generation;
- schema descriptor bytes and expected 32-octet fingerprints;
- codec ID, revision, status, canonical parameters, and declared maxima;
- extension IDs and criticality used;
- input semantic values in a lossless canonical form;
- expected encoded operation/representation bytes as lowercase hexadecimal;
- exact encoded length, SHA-256 content digest, representation ID, and decoded
  value for every valid vector;
- expected failure code and mutation prohibition for every invalid vector;
- expected state before/after each state-machine step;
- expected persistent checkpoint/prefix/receipt state after reopen;
- exact directional accounting by operation and budget scope;
- one immutable measurement-scope binding, serialized as `endpoint_a_binding`
  and `endpoint_b_binding`, of fixture roles `endpoint-a` and `endpoint-b` to
  the two logical peer fixtures and shared by both endpoint reporters;
- one canonical semantic-fixture artifact for every selected representation,
  with direction, source and destination endpoint roles, schema fingerprint,
  full representation ID, path, octet length, SHA-256 digest, expected
  `semantic_octets`, and `representation_descriptor_contribution` equal to
  zero; and
- expected `semantic_bytes_send`, `semantic_bytes_receive`, and their sum.

Canonical manifests use RFC 8785 JSON. Large byte payloads may be separate files
named by SHA-256; the canonical manifest includes their digest and length.
[REQ-VEC-002] Paths are relative, slash-separated, and MUST NOT escape the bundle root.

Octet strings are lowercase hexadecimal without a prefix. Unsigned 64-bit
semantic values are decimal JSON strings to avoid the I-JSON/IEEE-754 integer
limit; unsigned values of 32 bits or fewer are JSON integers.

To compute `bundle_digest`, set that manifest member to JSON `null`, canonicalize
the full manifest (including the sorted path/length/SHA-256 list for every
separate file) to bytes `M`, and calculate:

```text
SHA-256("BEMPIC-TEST-VECTOR-BUNDLE-v0.1\0" || U64(length(M)) || M)
```

The published manifest replaces `null` with the resulting lowercase
hexadecimal digest. A verifier restores `null` before recomputing it. Separate
files are authenticated through their manifest entries and are not concatenated
again into the bundle-digest input.

## Mandatory semantic vectors

[REQ-VEC-004] A v0.1 semantic conformance bundle MUST contain exactly the
catalog entries `V01` through `V15` below. Each entry may contain multiple
cases, but every required case and assertion in the authoritative
[`vector-catalog.json`](../conformance/v0.1/vector-catalog.json) MUST appear in
the bundle manifest with an unambiguous catalog ID and case ID. `blocked_by`
records release evidence still awaiting a decision; it does not make the
decided behavior optional.

| ID | Normative subject |
|---|---|
| V01 | Empty collection and equal warm/cold synchronization |
| V02 | Known checkpoint with one appended message |
| V03 | Unknown checkpoint, bounded paging, and cursor reopen |
| V04 | Message model, Unicode, optional fields, and core maxima |
| V05 | Body alternatives and deferred attachment selection |
| V06 | Selected compressible and incompressible attachments |
| V07 | Representation and `DATA` payload boundaries |
| V08 | Required interruption points and process reopen |
| V09 | Resume through alternate authorized source and carrier |
| V10 | Duplicate operations and lost final receipt |
| V11 | Corruption, overlap, range, short/long false lengths, digest, ID, and metadata conflicts |
| V12 | Exact and one-byte-short total/directional budgets for every operation type |
| V13 | Negotiation, ties, cache recovery, and extensions |
| V14 | Storage failures at durable commit boundaries |
| V15 | Every core failure code with both advertised retryable-flag values |

### V08 interruption covering array

For percentage rows the fixture length is `L >= 100`, the offset is
`floor(L*p/100)`, and `p` is the percentage in the case name. `final-byte` is
after prefix `L` is durable and before verification; the final two points use
the durable states named by their case. Storage names are the logical surfaces
defined in [`CONFORMANCE.md`](CONFORMANCE.md), not a requirement to ship three
separate physical databases.

The following array is authoritative and intentionally pairwise rather than
the 72-row Cartesian product:

| Row | Interruption point | Restart | Storage surface |
|---|---|---|---|
| V08-C01 | `offset-0` | sender | memory |
| V08-C02 | `offset-0` | receiver | representation-file |
| V08-C03 | `offset-0` | both | durable-store |
| V08-C04 | `offset-1-percent` | sender | representation-file |
| V08-C05 | `offset-1-percent` | receiver | durable-store |
| V08-C06 | `offset-1-percent` | both | memory |
| V08-C07 | `offset-10-percent` | sender | durable-store |
| V08-C08 | `offset-10-percent` | receiver | memory |
| V08-C09 | `offset-10-percent` | both | representation-file |
| V08-C10 | `offset-50-percent` | sender | memory |
| V08-C11 | `offset-50-percent` | receiver | representation-file |
| V08-C12 | `offset-50-percent` | both | durable-store |
| V08-C13 | `offset-90-percent` | sender | representation-file |
| V08-C14 | `offset-90-percent` | receiver | durable-store |
| V08-C15 | `offset-90-percent` | both | memory |
| V08-C16 | `final-byte` | sender | durable-store |
| V08-C17 | `final-byte` | receiver | memory |
| V08-C18 | `final-byte` | both | representation-file |
| V08-C19 | `post-verify-pre-commit` | sender | memory |
| V08-C20 | `post-verify-pre-commit` | receiver | representation-file |
| V08-C21 | `post-verify-pre-commit` | both | durable-store |
| V08-C22 | `post-commit-pre-receipt` | sender | representation-file |
| V08-C23 | `post-commit-pre-receipt` | receiver | durable-store |
| V08-C24 | `post-commit-pre-receipt` | both | memory |

[REQ-VEC-006] A V08 bundle MUST contain all 24 row IDs exactly once and MUST
record, for every row: fixture and trace digests; encoded length; interruption
point and computed prefix; restart party; storage surface and mapped backend;
durable state before interruption; recovered state and prefix; first resumed
offset; new, duplicate, and retransmitted-durable-prefix payload octets;
receipt state before and after reopen; final content digest, representation ID,
decode result, and row result. A row passes only when all criteria in
`vector-catalog.json` and `CONFORMANCE.md` pass. The bundle MUST also record the
pair-coverage proof generated from its rows. A full Cartesian run MAY be
published as additional evidence but does not replace or alter these row IDs.

The prescribed 100-message fixture used by V01 and V02 is an append-only
collection with object IDs `SHA-256("BEMPIC-V01-OBJECT\0" || U32(index))` for
indexes 0 through 99. Each message has one UTF-8 `text/plain` body containing
`message-` followed by the zero-padded three-digit index and LF. Creation time
is `2026-01-01T00:00:00Z` plus the index in seconds; sender and recipient are
`sender@example.test` and `recipient@example.test`; subject is `Message ` plus
the zero-padded index. V02 appends index 100 with the same construction. The
selected experimental codec is public tuple `0x00010000/1` and its profile is
[`bempic-compact-operation-v0.1`](codecs/EXPERIMENTAL-COMPACT-v0.1.md).
V01 and V02 remain blocked on regeneration of their canonical manifest bytes,
representation IDs, checkpoint values, operations, and bundle digests for that
public tuple; the catalog records `public-codec-vector-regeneration`.

[REQ-VEC-007] A bundle claiming the experimental compact profile MUST identify
codec `0x00010000`, revision `1`, the exact profile digest, and the exact
specification commit. It MUST regenerate every tuple-bound byte, representation
ID, descriptor, collection digest, operation, and bundle digest. Evidence for
the Reference private candidate `0xffff0001/2` MUST NOT be presented as a
public-tuple vector, even when an encoded length is unchanged.

## Mandatory codec boundary vectors

Each codec profile adds, for every field and collection count:

- minimum, maximum, absent (when optional), empty (when distinct), and one past
  maximum;
- malformed length, truncated envelope, trailing bytes, overlong integer,
  non-canonical ordering, invalid UTF-8/NFC, unknown operation, and nesting or
  allocation attack;
- exact-size equality between analysis and actual encoding;
- worst-case value that reaches the declared maximum encoded size; and
- a value that would exceed the maximum and is rejected before allocation.

Numeric codecs also include half-way rounding, minimum/maximum precision,
overflow, NaN/infinity policy where relevant, and canonical negative-zero
behavior. A codec with no approximate numeric fields explicitly records that
the precision vectors are not applicable.

## External B2F corpus bundle

[REQ-VEC-008] The prescribed B2F text corpus MUST be a synthetic,
redistributable, content-addressed bundle conforming to
[`bempic-v0.1-b2f-text-single-message-v1`](B2F-ORACLE.md). Its manifest MUST
bind each fixture ID to exact raw RFC 5322/MIME, semantic-record, prepared-B2,
BEMPIC-semantic-fixture, expected LZHUF-image, and expected directional B2F
transcript paths, octet lengths, SHA-256 digests, fixed header values, and
licenses. It MUST include the calculation profile ID and digest, corpus digest,
generator commit, and independent reproduction. Until that bundle and a
qualified oracle are published, `external-text-corpus` remains blocked and no
private mail, implementation-generated timestamp or identifier, mutable URL,
or unlicensed upstream fixture may substitute for it.

## State traces

State vectors are ordered operation traces. Each step records operation bytes,
direction, contact number, budget ID, budget before/after, volatile state,
durable state, emitted operations, counters, and injected crash or carrier
event. [REQ-VEC-003] A runner MUST compare the full trace, not merely its final object.

For semantic accounting, a fixture artifact represents the exact decoded value
walked by Specification Section 12.1. Octet strings are stored as exact bytes;
structured values use the lossless canonical input already named by the bundle,
while `semantic_octets` is computed from the decoded scalar values rather than
from the artifact's JSON punctuation, field names, hexadecimal spelling, or
container framing. For a message manifest, the recomputation walks the
application fields enumerated by Specification Section 12.1 and skips the
`representations` container and every representation descriptor member.
Fixture direction is derived only from the immutable endpoint-role binding:
`endpoint-a` to `endpoint-b` is `send`, and the reverse is `receive`. Deferred
fixture artifacts remain listed for reproducibility but contribute zero until
their selection event.

## Updating vectors

Changing expected bytes requires a codec revision. Changing semantic outcomes
requires a protocol-generation change or an accepted correction decision. A
[REQ-VEC-005] A pull request MUST identify whether existing conformers remain
compatible and MUST NOT rewrite previously released bundles in place.
