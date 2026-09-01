# BEMPIC Protocol Specification v0.1.0

**Status:** release candidate; not yet released or tagged

**Protocol generation:** `0.1`

**Specification release:** `0.1.0`

This document is the normative, transport-independent BEMPIC semantic
specification. The words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**,
**SHOULD NOT**, and **MAY** are to be interpreted as described by
[BCP 14](https://www.rfc-editor.org/info/bcp14) when they appear in capitals.

Version 0.1.0 deliberately standardizes behavior before standardizing one
permanent wire image. A conforming codec profile supplies deterministic binary
encodings and byte assignments for these semantics. No encoding in
`prototype/`, including `BMSG0`, `B0`, generation `0`, or its 16-byte digest
prefixes, is a BEMPIC wire standard.

[REQ-REL-001] The repository MUST NOT be tagged `v0.1.0` until every gate in
[`docs/ROADMAP-v0.1.0.md`](docs/ROADMAP-v0.1.0.md) is satisfied.

## 1. Purpose and scope

BEMPIC is an extreme-efficiency, interruption-tolerant application
synchronization protocol for messaging on links where bytes, airtime, energy,
latency, contact duration, or monetary cost are scarce.

The v0.1 core supports:

1. one-way, append-oriented synchronization of immutable message manifests;
2. one body and zero or more independently selectable attachment parts;
3. multiple immutable representations of a part;
4. deterministic preparation, exact prepared sizes, offers, selection, and
   hard BEMPIC-byte budgets;
5. persistent contiguous-prefix transfer, reopen, and resume after an
   interruption or source change;
6. whole-representation integrity verification and exact reconstruction;
7. representation and application receipts with unambiguous meanings;
8. compact equality checks, delta offers when a checkpoint is retained, and a
   deterministic bounded full-inventory fallback;
9. semantic-version, schema, codec, extension, size, and capability
   negotiation; and
10. separate accounting for BEMPIC, carrier, and link cost domains.

The v0.1 core does not standardize mutable mailbox flags, deletion, folders,
labels, drafts, edits, multi-writer conflict resolution, delta encoding,
content transformation, unreliable-carrier selective repair, a cryptographic
suite, or a permanent wire codec. Such behavior requires an extension or later
protocol generation.

## 2. Architecture and ownership boundary

The required OceanMail stack is:

```text
OceanMail  ->  BEMPIC  ->  M4P  ->  DataLink adapters
application    application   mesh/network   link/modem
policy         synchronization behavior      behavior
```

BEMPIC owns compact application objects, synchronization, application
continuity, integrity state, semantic receipts, and BEMPIC-byte accounting.

M4P owns peer and network addressing, discovery, route selection, mesh
coordination, store-carry-forward, forwarding, generic fragmentation and
reassembly, network-level deduplication, network TTL, cross-modality behavior,
and the DataLink abstraction. BEMPIC operations are opaque application payloads
to M4P. [REQ-LAYER-001] BEMPIC MUST NOT infer application delivery from M4P forwarding or
packet delivery.

DataLink adapters and modems own waveforms, framing, FEC, ARQ, retransmission,
adaptive modulation, and link turnaround. BEMPIC prefix resumption exists only
to continue an application representation after a contact or path is gone; it
is not a second per-frame reliability protocol.

OceanMail owns address policy, external-service integration, gateway scoring,
relay participation, prioritization, quotas, billing, user approval, content
transformation, and UI. BEMPIC exposes facts and mechanisms, not those product
decisions.

The complete boundary is recorded in
[`docs/REPOSITORY-BOUNDARY.md`](docs/REPOSITORY-BOUNDARY.md) and
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## 3. Terminology

- **Application object:** An immutable logical message identified independently
  of any particular encoded representation.
- **Part:** A body or attachment role within an application object. Part IDs
  are unsigned 32-bit integers unique within that object.
- **Representation:** Exact immutable bytes for a part or manifest, prepared
  under one schema and codec configuration.
- **Prepared representation:** A representation whose bytes, byte length,
  digest, representation ID, schema fingerprint, codec, and codec parameters
  are frozen.
- **Application object ID (`object_id`):** A 32-octet, application-assigned,
  globally collision-resistant identifier. It remains stable across alternate
  representations. Reuse for different immutable semantics is an error.
- **Representation ID (`representation_id`):** A 32-octet, domain-separated
  digest derived by BEMPIC from the prepared representation descriptor.
- **Schema fingerprint:** A 32-octet digest naming the exact bounded semantic
  schema consumed by a codec.
- **Collection:** One append-only, single-authority ordered set of descriptors.
- **Checkpoint:** A collection generation and digest previously issued by its
  authority and durably retained by a peer.
- **Operation:** One complete codec-delimited BEMPIC semantic record. Partial
  operations are never applied.
- **Contact:** A temporary opportunity to exchange complete operations through
  a carrier. A contact is not a durable protocol session.
- **Carrier:** The opaque-record service below BEMPIC, normally M4P. A carrier
  may change between contacts.
- **Application extent:** Persisted bytes of a prepared representation. It is
  not an M4P fragment or DataLink frame.
- **Receipt:** An idempotent statement about a defined representation or
  application state. It is not a hop acknowledgement.
- **Budget scope:** The finite set of encoded BEMPIC operations authorized by
  one request and budget identifier.

## 4. Core bounds and scalar rules

[REQ-BOUNDS-001] All conforming v0.1 implementations MUST enforce these limits before allocating
or mutating durable state. A local policy MAY advertise smaller limits.

| Item | v0.1 core limit |
|---|---:|
| Encoded operation | 1,048,576 octets |
| Prepared representation, encoded or decoded | 1,073,741,824 octets |
| Decoded message manifest | 65,536 octets |
| Recipients per message | 32 |
| Parts per message | 64, exactly one of which is the body |
| Representations per part | 16 |
| UTF-8 sender or recipient | 320 octets |
| UTF-8 subject | 1,024 octets |
| UTF-8 filename | 255 octets |
| ASCII media type | 127 octets |
| Codec parameter block | 1,024 octets |
| Capability schema entries | 16 |
| Capability codec entries | 16 |
| Capability protocol generations | 8 |
| Negotiated extensions | 32 |
| Descriptors in one offer | 128 |
| Selections in one request | 128 |
| Entries in one collection | 1,000,000 |
| Human-readable failure detail | 256 UTF-8 octets |

Integers are unsigned unless explicitly stated. Semantic values are limited to
the indicated range even when a codec can express a larger integer. [REQ-CANON-001] Encodings
MUST reject non-minimal or ambiguous integer forms when their codec defines a
minimal form.

[REQ-META-001] Metadata strings MUST be valid UTF-8, normalized to Unicode NFC, and MUST NOT
contain NUL. Sender, recipient, filename, media type, and subject fields MUST
NOT contain C0 or C1 controls. Message-body representations are governed by
their media type and schema instead of the metadata control-character rule.
Media types MUST be lowercase ASCII `type/subtype` values. An absent optional
field is distinct from an empty present field.

## 5. Application and representation model

A v0.1 message manifest contains:

- one 32-octet `object_id`;
- `created_at`, an unsigned 64-bit count of seconds since the Unix epoch;
- one non-empty sender and between 1 and 32 non-empty recipients;
- an absent or non-empty subject;
- one body part and between 0 and 63 attachment parts; and
- descriptors for the available immutable representations of each part.

Each part contains a unique unsigned 32-bit `part_id`, a role (`body` or
`attachment`), media type, optional filename, and one to 16 representation
descriptors. [REQ-PART-001] The body filename MUST be absent. An attachment filename MAY be
absent. Transformation of HTML, images, or other content into reduced forms is
an application responsibility. BEMPIC only relates and transfers the resulting
immutable representations.

Each representation descriptor contains exactly:

- `representation_id` (32 octets);
- `schema_fingerprint` (32 octets);
- `codec_id` (unsigned 32-bit registry value);
- `codec_revision` (unsigned 32-bit value);
- canonical codec parameters (0 to 1,024 octets);
- exact encoded length (0 to 1,073,741,824 octets);
- decoded length when the schema can determine it, otherwise absent;
- SHA-256 digest of the exact encoded bytes (32 octets); and
- optional application usefulness expiry.

Expiry prevents new application offers after the object is no longer useful.
It is not an M4P forwarding TTL and does not direct a network route.

## 6. Deterministic preparation and identifiers

[REQ-PREP-001] Preparation MUST perform these steps in order:

1. Validate the application object and every bound in Section 4.
2. Normalize metadata as specified in Section 4 while preserving recipient and
   part order supplied by the application.
3. Select an exact registered schema descriptor, codec revision, and canonical
   codec parameter block.
4. Encode once using deterministic codec and compression settings. [REQ-PREP-002] A codec MUST
   produce identical bytes for identical normalized input and parameters.
5. Confirm the actual encoded length does not exceed both the schema's declared
   maximum and the v0.1 representation limit.
6. Compute `content_digest = SHA-256(encoded_bytes)`.
7. Compute `representation_id` with the construction below.
8. Freeze the descriptor and bytes. Any byte or parameter change creates a new
   representation ID.

Let `U32(n)` and `U64(n)` be fixed-width, unsigned, big-endian integers. Let
`P` be the canonical codec parameter bytes, `D` the 32-octet content digest,
and `F` the 32-octet schema fingerprint. The v0.1 representation ID is:

```text
SHA-256(
  "BEMPIC-REPRESENTATION-ID-v0.1\0" ||
  F || U32(codec_id) || U32(codec_revision) ||
  U32(length(P)) || P || U64(length(encoded_bytes)) || D
)
```

Schema descriptors are canonical JSON documents represented as UTF-8 using
[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) JSON Canonicalization Scheme.
[REQ-JCS-001] They MUST satisfy RFC 8785's I-JSON input constraints and exact ECMAScript
primitive serialization and UTF-16 property-ordering rules; ordinary
language-runtime sorted JSON is not a substitute.
If `S` is the canonical descriptor, its fingerprint is:

```text
SHA-256("BEMPIC-SCHEMA-FINGERPRINT-v0.1\0" || U32(length(S)) || S)
```

JSON is used only to publish and fingerprint schema descriptions. BEMPIC does
not require JSON on a constrained carrier.

[REQ-ID-001] An application generates `object_id` and MUST ensure stability and collision
resistance. A sender MUST fail with `METADATA_CONFLICT` if a known object ID is
associated with different immutable manifest semantics. A receiver MUST apply
the same rule. This preserves logical identity across alternative encodings
without making the logical object ID a wire-content hash.

### 6.1 Protocol invariants

At every observable boundary:

1. Prepared bytes and their descriptor are immutable.
2. Full identifiers, schema, codec, parameters, length, and digest agree; a
   short local alias never overrides them.
3. No representation payload is sent without an explicit request, and no
   unselected attachment payload is sent.
4. No complete operation is emitted beyond an accepted BEMPIC budget.
5. Advertised resume progress never exceeds recoverable durable bytes.
6. A gap never advances progress; a matching duplicate is idempotent; a
   conflicting duplicate fails closed.
7. Unverified bytes are never committed or receipted as committed.
8. Carrier delivery is never application acceptance or delivery.
9. Contact loss, process restart, source change, and carrier change do not alter
   representation identity.
10. Unknown optional extensions have no core side effect; unknown critical
    extensions cause no operation state mutation.
11. Every remotely influenced allocation and loop has a negotiated and local
    upper bound.
12. BEMPIC never performs M4P routing/forwarding or DataLink reliability work.

## 7. Collection summaries and reconciliation

The v0.1 core is single-authority and append-only per collection. A collection
authority assigns each added descriptor the next unsigned 64-bit sequence and
retains a change journal or checkpoint history sufficient for its advertised
resume policy. Removal and sequence reuse are not core operations.

The canonical collection entry key is:

```text
object_id (32 octets) || U32(part_id) || representation_id (32 octets)
```

Keys are compared as unsigned lexicographic octet strings. A collection digest
at generation `G` is SHA-256 of the domain string
`BEMPIC-COLLECTION-v0.1\0`, the 32-octet collection ID, `U64(G)`, `U64(count)`,
and all entry keys at or before `G` in ascending sequence order.

A receiver sends its last durable checkpoint in `SUMMARY`. The authority then:

- reports equality when generation and digest equal its current checkpoint;
- sends delta `OFFER` pages for later sequence values when the checkpoint is
  recognized; or
- sends full-inventory `OFFER` pages in entry-key order when the checkpoint is
  absent or unknown.

Every offer page states its mode, base generation, target generation, first and
last sequence or entry key, descriptor count, and whether more pages exist.
Delta pages are ordered by sequence. Full pages are ordered by entry key. A
descriptor always carries its authority-assigned sequence so the receiver can
reconstruct the target checkpoint independent of page order. A
peer requests the next page using the last committed cursor; cursors are data,
not implicit process memory. Repeating a page is idempotent. No page may exceed
128 descriptors or the negotiated maximum operation size.

After all accepted pages are durable, the receiver computes and stores the
authority's target checkpoint. A mismatched computed digest is
`METADATA_CONFLICT`, not a successful reconciliation.

## 8. Protocol operations

[REQ-OPS-001] Every codec profile MUST represent these seven core operation types. Operations
are complete, length-delimited, and independently size-checkable.

### 8.1 `CAPABILITIES`

Carries supported protocol generations, schema fingerprints, codec IDs and
revisions in preference order, maximum encoded operation size, maximum data
payload, supported receipt levels, security class, and extension declarations.
[REQ-CAPS-001] Lists MUST obey Section 4. Capabilities MAY be cached only with a peer/profile
identity and an expiry. Stale cache use MUST fall back to fresh negotiation on
any incompatibility.

### 8.2 `SUMMARY`

Carries collection ID, generation, item count, and collection digest. A zero
generation and empty-set digest mean no retained checkpoint. Summary equality
is an optimization; disagreement always has the bounded offer fallback in
Section 7.

### 8.3 `OFFER`

Carries one bounded reconciliation page and complete descriptors for offered
[REQ-OFFER-001] Representations in an offer MUST expose exact prepared byte lengths before content.
An offer never authorizes payload transfer and MUST NOT contain deferred
attachment payload bytes.

### 8.4 `REQUEST`

Has one of two variants:

- `INVENTORY_PAGE` names a collection, target generation, mode, committed
  cursor, and desired page-entry limit.
- `REPRESENTATION_DATA` carries a 16-octet budget ID and one to 128 selections.
  Each selection contains `representation_id` (exactly 32 octets),
  `durable_prefix_offset` (unsigned 64-bit octet offset, 0 through 1,073,741,824),
  and `max_desired_payload_octets` (unsigned 64-bit integer, 1 through
  1,073,741,824). [REQ-REQUEST-001] The offset MUST NOT exceed the offered encoded length, and
  the desired payload count MUST NOT exceed the encoded length minus that
  offset. Representation IDs MUST be unique within the request. The operation
  also states total and directional BEMPIC-byte limits for the budget scope.

A request is explicit authorization. [REQ-SELECTION-001] Unselected representations, including
attachments, MUST NOT be sent.

### 8.5 `DATA`

Carries representation ID, unsigned 64-bit offset, and non-empty payload. In
[REQ-DATA-001] In the core reliable-carrier profile, the offset MUST be at or below the durable
prefix. A matching overlap is idempotently discarded. A conflicting overlap is
`METADATA_CONFLICT`; a gap is `RANGE_INVALID`. Each operation MUST fit the
negotiated maximum. No per-`DATA` acknowledgement exists in the core.

### 8.6 `RECEIPT`

Carries a subject identifier, status, optional verified digest, and an
idempotency identifier. Core statuses are:

- `REPRESENTATION_COMMITTED`: exact bytes verified and atomically committed;
- `APPLICATION_ACCEPTED`: the application accepted the logical object;
- `APPLICATION_DELIVERED`: the application completed its profile-defined final
  delivery; and
- `APPLICATION_REJECTED`: the application rejected it, with a bounded reason.

Receipt levels are independent. [REQ-RECEIPT-001] A carrier or M4P delivery indication MUST NOT
be translated into any of these statuses. Duplicate receipts have no additional
effect.

### 8.7 `FAILURE`

Carries a code, scope, retryable flag, and optional bounded diagnostic. The core
codes are `UNSUPPORTED_VERSION`, `UNSUPPORTED_SCHEMA`, `UNSUPPORTED_CODEC`,
`UNSUPPORTED_CRITICAL_EXTENSION`, `MALFORMED_OPERATION`, `LIMIT_EXCEEDED`,
`UNKNOWN_OBJECT`, `METADATA_CONFLICT`, `RANGE_INVALID`, `INTEGRITY_FAILURE`,
`STORAGE_FAILURE`, `POLICY_REJECTED`, and `CHECKPOINT_UNKNOWN`.

A failure response is optional when sending it would exceed a budget or reveal
sensitive information. Local failure behavior remains mandatory.

## 9. States and transitions

### 9.1 Compatibility state

`IDLE -> NEGOTIATING -> COMPATIBLE` is the successful path.
`NEGOTIATING -> INCOMPATIBLE` occurs when no common protocol generation, schema,
codec, required extension set, security class, or operation size exists. Only
`CAPABILITIES` and a bounded `FAILURE` may be processed before compatibility.
Contact loss returns the volatile state to `IDLE`; it does not erase a valid
cached capability record or representation progress.

### 9.2 Collection state

`UNCHECKED -> EQUAL` requires matching checkpoints. A mismatch follows
`UNCHECKED -> RECONCILING -> SELECTING`. Durable accepted offer pages advance a
cursor monotonically. When all pages validate, the receiver atomically records
the target checkpoint and enters `SELECTING`. An interruption leaves the last
durable cursor intact. Any conflicting page enters `FAILED` for that target
generation without changing the prior valid checkpoint.

### 9.3 Representation state

The durable receiver states and only allowed forward transitions are:

```text
ABSENT -> OFFERED -> PARTIAL -> COMPLETE_UNVERIFIED -> VERIFIED -> COMMITTED
   |         |          |                 |               |
   +---------+----------+-----------------+---------------+-> REJECTED
```

`PARTIAL -> PARTIAL` accepts only a contiguous suffix or matching duplicate.
`COMPLETE_UNVERIFIED` is never externally receipted as success. Verification
failure moves staged bytes to quarantine or discards them and returns to
`OFFERED`; [REQ-STATE-001] it MUST NOT retain a false durable prefix. `COMMITTED` is immutable.
`REJECTED` records application policy and does not imply byte corruption.

The sender's observable progression is `AVAILABLE -> OFFERED -> REQUESTED ->
SENDING -> AWAITING_RECEIPT -> RECEIPTED`. Interruption from `REQUESTED`,
`SENDING`, or `AWAITING_RECEIPT` returns to `AVAILABLE` while preserving the
receiver-reported prefix and any received receipt. [REQ-IDEMP-001] A repeated request or
receipt MUST be safe.

## 10. Interruption, persistence, reopen, and resume

Contact interruption is normal and has no implicit rollback. [REQ-PERSIST-001] Before advertising
a retained prefix or positive receipt, a receiver MUST durably store:

- the full prepared descriptor and its collection/object/part association;
- negotiated protocol, schema, codec, and parameter identifiers;
- the exact contiguous prefix length;
- the prefix bytes or an equally durable content store;
- prior checkpoint and offer-page cursor state;
- committed receipt idempotency identifiers; and
- the complete/verified/committed state.

[REQ-CRASH-001] Durable updates MUST be crash-consistent. A write-ahead journal, copy-on-write
record, or atomic replace is acceptable. A crash may lose bytes that were not
reported durable; it MUST NOT create a prefix longer than the bytes recoverable
on reopen.

[REQ-REOPEN-001] On reopen, an implementation MUST validate metadata, bounds, persisted length,
and committed content digest before using the state. Conflict or corruption
fails closed. The next request names the recovered contiguous prefix. Any peer
authorized by the application and holding the identical representation ID may
provide the suffix. A different carrier or M4P path does not change identity or
progress.

The core supports one contiguous prefix. A compact missing-range extension MAY
be standardized later, but [REQ-RESUME-001] it MUST remain application resumption rather than
generic fragmentation or reliable-carrier ARQ.

## 11. Integrity and exact reconstruction

The receiver accepts bytes only for an offered descriptor. [REQ-INTEGRITY-001] Offset arithmetic
MUST be checked for overflow. Completion requires exactly the advertised byte
length and a constant-time comparison of the computed SHA-256 digest with the
descriptor digest. It then recomputes the representation ID and compares it
with the offered ID.

[REQ-DECODE-001] For a manifest, deterministic decoding MUST produce a value valid under the
advertised schema and with the offered object/part relationships. For an opaque
binary part, exact reconstruction is byte equality with the prepared bytes.
Only after all checks may storage atomically transition to `COMMITTED` and emit
`REPRESENTATION_COMMITTED`.

Exact reconstruction refers to the selected prepared representation. If an
application normalized or transformed an RFC 5322/MIME message, HTML body, or
image before preparation, BEMPIC does not recreate the discarded source. The
application must offer the original bytes as a separate representation when
their exact recovery is required.

Integrity is not origin authentication. The security properties and deployment
limits are defined in [`docs/SECURITY-MODEL.md`](docs/SECURITY-MODEL.md).

## 12. Byte budgets and accounting

Every `REPRESENTATION_DATA` request defines a budget scope. Its request bytes,
all responsive `DATA`, `RECEIPT`, and `FAILURE` operations, and any extension
fields inside those operations count toward `bempic_total_bytes`. [REQ-BUDGET-001] Both peers
MUST compute encoded sizes before emission. An operation that would make total
or directional use exceed the request limit MUST NOT be emitted or split. The
scope pauses without failure when no next complete operation fits.

[REQ-ACCOUNT-001] Implementations MUST expose at least:

- `semantic_bytes`: the codec-independent logical workload selected by the
  application, as defined below;
- `bempic_tx_bytes` and `bempic_rx_bytes`: every encoded BEMPIC octet, including
  envelopes, negotiation when included in the reported scope, metadata,
  payload, receipts, failures, compression framing, and application security;
- `representation_payload_bytes`: encoded representation bytes inside `DATA`;
- `useful_committed_bytes`: representation bytes newly committed;
- `duplicate_payload_bytes`: payload bytes received but already durable;
- `carrier_tx_bytes` and `carrier_rx_bytes`, only when reported by the carrier;
  and
- `link_tx_bytes` and `link_rx_bytes`, only when measured or estimated by the
  DataLink, with the estimate method identified.

### 12.1 `semantic_bytes`

`semantic_bytes` is a logical-workload counter, not a wire, storage, or
completion counter. For a decoded schema value, `semantic_octets(value)` is
computed recursively without codec framing: an octet string contributes its
length; a UTF-8 or ASCII string contributes the length of its normalized UTF-8
bytes; an unsigned 32-bit or 64-bit integer contributes four or eight octets;
a Boolean or enumeration contributes one octet; an absent nullable value
contributes zero; and an array or record contributes the sum of its present
children. Container counts, field names, tags, presence indicators, length
prefixes, alignment, and padding contribute zero. Thus an opaque-binary value
contributes its exact decoded length. For a message-manifest value, the walk
includes only `object_id`, `created_at`, `sender`, `recipients`, `subject`, and
each part's `part_id`, `role`, `media_type`, and `filename`. The
`representations` container and every member of every representation descriptor
(`representation_id`, `schema_fingerprint`, `codec_id`, `codec_revision`,
codec parameters, encoded length, decoded length, content digest, and
usefulness expiry) contribute zero. Those descriptor members identify or
describe prepared codec output and therefore cannot change a codec-independent
logical workload. A descriptor's `representation_id` remains the evidence key
for count-once selection; using it as a key does not add its octets to
`semantic_octets`.

[REQ-ACCOUNT-003] Each measurement scope MUST bind the two enduring logical
peer roles `endpoint-a` and `endpoint-b` once, before measurement. `send` means
logical flow from `endpoint-a` to `endpoint-b`, and `receive` means logical flow
from `endpoint-b` to `endpoint-a`. The binding is shared by both reporters and
MUST NOT change across process restart, authorized-source replacement, carrier
change, or ownership/requester reversal for another representation. Within one
scope and logical direction `d`, `semantic_bytes[d]` MUST equal the sum of
`semantic_octets` once for each distinct `(d, representation_id)` first
authorized by an accepted application selection in that scope. Repeated
requests, contacts, duplicates, retransmissions, matching overlap, and
restart/resume do not add semantic bytes. A deferred or unselected
representation contributes zero until selected; a message manifest contributes
only the application metadata enumerated above and never representation
descriptor members. Encoded representation payload, compression or security
expansion, BEMPIC operation metadata and framing, codec padding, carrier bytes,
M4P bytes, DataLink framing/FEC/retransmission, and RF cost do not contribute.
`semantic_bytes` without a direction MUST be the sum of the send and receive
directions, and both endpoints MUST report the same value for the same endpoint
binding, fixture, selections, and scope. Selection counts the declared logical
workload even if the run later pauses or fails; `useful_committed_bytes` records
successful completion separately.

[REQ-ACCOUNT-002] Counters MUST identify their direction, scope, and whether they are exact or
estimated. BEMPIC MUST NOT label carrier or RF cost as exact when the lower
layer did not report it. A BEMPIC budget cannot retroactively cap M4P headers,
FEC, modem retransmissions, or bytes already accepted below the BEMPIC API.

The exact v0.1 measurement envelopes, counter names, first-body definitions,
and release thresholds are in [`docs/METRICS.md`](docs/METRICS.md).

A carrier binding MAY expose a carrier-byte or link-byte opportunity budget.
BEMPIC may use an exact binding cost function or a labeled conservative
estimate when selecting operations. The binding or DataLink enforces a hard
lower-layer budget; BEMPIC only enforces it directly when the binding provides
an exact pre-admission cost contract. Carrier budgeting never changes core
operation semantics or introduces transport-specific fields into a message.

## 13. Version, schema, codec, and extension negotiation

The negotiated protocol value is the pair `(major, minor)`. Patch versions are
document releases and are not carried. Because major zero denotes active
development, different `0.x` minor generations are incompatible unless an
explicit compatibility profile lists both. Peers select the highest identical
pair they both advertise.

Schema compatibility requires an exact fingerprint match. Codec compatibility
requires matching ID and revision. Peers choose the pair with the lowest sum of
their advertised preference indexes; ties use the lower codec ID, then lower
revision, then lexicographically lower schema fingerprint. Failure to find a
complete common tuple is incompatible, never an invitation to guess.

[REQ-CODEC-001] Every codec profile MUST publish:

1. a registry ID and revision;
2. every supported schema fingerprint;
3. deterministic encoding and strict decoding rules;
4. declarative type, count, length, and numeric bounds;
5. numeric precision and rounding rules where applicable;
6. a mandatory maximum encoded size for every operation and schema;
7. an exact encoded-size function for every concrete value;
8. worst-case size analysis demonstrating the declared maximum;
9. canonical parameter encoding;
10. malformed, overlong, unknown-field, and resource-exhaustion behavior; and
11. byte-exact vectors in the format defined by
    [`docs/TEST-VECTORS.md`](docs/TEST-VECTORS.md).

Codecs are pluggable. No v0.1 codec may be assumed merely because another
implementation uses it. DCCL is prior art for these requirements, not a BEMPIC
dependency or wire format.

Extensions use unsigned 32-bit IDs and a critical bit. [REQ-EXT-001] Extension contents MUST
be length-delimited and included in size limits. Unknown optional extensions
are skipped without side effects. An unknown critical extension fails before
any operation state mutation. Extensions MUST NOT weaken bounds, redefine core
fields or receipt meanings, claim compatibility with a different core
generation, or introduce M4P/network behavior into BEMPIC.

Current protocol, operation, receipt, failure, schema, codec, extension, and
security-profile allocations are recorded in
[`docs/REGISTRIES.md`](docs/REGISTRIES.md). Absence from that registry is not an
implicit allocation. The registry also defines codec status progression and
the proof required for maximum encoded sizes.

## 14. Failure and recovery rules

Malformed, truncated, oversized, ambiguous, non-canonical, unsupported, or
integrity-invalid input fails closed. [REQ-FAIL-001] A decoder MUST finish structural and
bound validation before durable protocol mutation. Staged payload writes are
the sole exception and remain uncommitted until Section 11 succeeds.

Failures are scoped to the smallest affected operation, representation,
collection target, or compatibility attempt. [REQ-FAIL-002] An unrelated committed object
MUST remain usable. Retrying is allowed only when the failure code is marked
retryable and the conflicting input or local condition has changed. Automatic
retry MUST be bounded by application or carrier policy.

Budget exhaustion and contact interruption are pauses, not protocol failures.
Storage failure is never reported as successful persistence. Policy rejection
is not an integrity failure. Diagnostics must not echo secrets or unbounded
attacker-controlled text.

## 15. Non-goals and prohibited duplication

[REQ-LAYER-002] A v0.1 implementation MUST NOT claim core conformance for behavior that depends
on BEMPIC performing routing, peer discovery, mesh coordination, forwarding,
network custody, network TTL, generic fragmentation/reassembly, generic
network deduplication, modem ARQ/FEC, RF scheduling, Internet mail delivery,
service authorization, billing, content transformation, or UI policy.

An optional unreliable-carrier recovery profile is future work. It may borrow
bounded checkpoint/range ideas from LTP or CFDP only when the carrier and M4P do
not already provide suitable recovery.

## 16. Conformance and release status

Conformance classes, required evidence, and the checklist are in
[`docs/CONFORMANCE.md`](docs/CONFORMANCE.md). Test-vector bundle requirements
are in [`docs/TEST-VECTORS.md`](docs/TEST-VECTORS.md). Security requirements are
in [`docs/SECURITY-MODEL.md`](docs/SECURITY-MODEL.md). The normative
requirement-to-evidence index is in
[`docs/CONFORMANCE-MATRIX.md`](docs/CONFORMANCE-MATRIX.md); M4P confirmation and
release-record requirements are in
[`docs/M4P-CONFIRMATION.md`](docs/M4P-CONFIRMATION.md) and
[`docs/RELEASE-RECORD.md`](docs/RELEASE-RECORD.md).

This document is prepared for v0.1.0, but the release is not complete. In
particular, the sibling `bempic-reference` repository must demonstrate this
semantic contract, codec analysis, persistence, interruption/reopen/resume,
byte accounting, bounded parsing, and required vectors before this repository
may create the tag.
