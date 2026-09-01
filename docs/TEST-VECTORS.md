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

Each versioned bundle MUST have a canonical manifest containing:

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
Paths are relative, slash-separated, and MUST NOT escape the bundle root.

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

1. Empty collection, equal warm checkpoint, and equal cold negotiation.
2. Known checkpoint with one appended message and no retransmitted old manifest.
3. Unknown checkpoint with multi-page full inventory and durable cursor reopen.
4. Tiny, typical, international NFC, reply-chain, absent-subject, maximum
   recipients, maximum parts, and every maximum metadata length.
5. One body with full/preview alternatives and attachment metadata with the
   attachment unselected.
6. Selected compressible and incompressible attachments.
7. Empty, one-byte, maximum data-payload, and maximum representation boundary.
8. Interruption at all points required by `CONFORMANCE.md`, followed by reopen.
9. Resume through another authorized source and another carrier.
10. Duplicate offers, data, pages, receipts, and a lost final receipt.
11. Corrupt final byte, conflicting overlap, gap, false length, false digest,
    false representation ID, and object-ID metadata conflict.
12. Budgets one byte below and exactly equal to each next complete operation,
    including directional exhaustion.
13. Compatible and incompatible protocol/schema/codec negotiation, preference
    ties, stale cache recovery, optional unknown extension, and critical unknown
    extension.
14. Storage failure at each commit boundary and recovery without false receipt.
15. Every core failure code with retryable and non-retryable handling.

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
event. A runner MUST compare the full trace, not merely its final object.

## Updating vectors

Changing expected bytes requires a codec revision. Changing semantic outcomes
requires a protocol-generation change or an accepted correction decision. A
pull request must identify whether existing conformers remain compatible and
must not rewrite previously released bundles in place.
