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
- expected persistent checkpoint/prefix/receipt state after reopen; and
- exact directional accounting by operation and budget scope.

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

The prescribed 100-message fixture used by V01 and V02 is an append-only
collection with object IDs `SHA-256("BEMPIC-V01-OBJECT\0" || U32(index))` for
indexes 0 through 99. Each message has one UTF-8 `text/plain` body containing
`message-` followed by the zero-padded three-digit index and LF. Creation time
is `2026-01-01T00:00:00Z` plus the index in seconds; sender and recipient are
`sender@example.test` and `recipient@example.test`; subject is `Message ` plus
the zero-padded index. V02 appends index 100 with the same construction. The
selected experimental codec profile will publish the canonical manifest bytes
and checkpoint values; that unresolved selection is recorded in V01/V02
`blocked_by`.

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

## State traces

State vectors are ordered operation traces. Each step records operation bytes,
direction, contact number, budget ID, budget before/after, volatile state,
durable state, emitted operations, counters, and injected crash or carrier
event. [REQ-VEC-003] A runner MUST compare the full trace, not merely its final object.

## Updating vectors

Changing expected bytes requires a codec revision. Changing semantic outcomes
requires a protocol-generation change or an accepted correction decision. A
[REQ-VEC-005] A pull request MUST identify whether existing conformers remain
compatible and MUST NOT rewrite previously released bundles in place.
