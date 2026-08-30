# BEMPIC Initial Protocol Plan

**Status:** pre-wire-format planning baseline

**Date:** 2026-08-30

**Implementation status:** a non-normative executable semantic proof exists in `prototype/`; no reference implementation or stable wire format exists yet

This document records the initial BEMPIC audit, prior-art comparison, smallest useful application model, measurement plan, and implementation recommendation. It is intentionally earlier than a wire-format decision. Names of operations and fields in this document describe semantics, not assigned wire values.

## Outcome

BEMPIC should be developed as a compact, persistent, budget-aware application synchronization protocol for messaging. Its first proof should synchronize an immutable message representation and optional attachment representations across a simulated interrupted carrier.

BEMPIC should not become:

- another mesh or delay-tolerant network below OceanMail;
- an RF modem or DataLink API;
- a second packet-fragmentation layer above M4P;
- a per-frame ARQ protocol over PACTOR, VARA, or ARDOP ARQ;
- a compressed clone of SMTP, IMAP, MIME, BPv7, LTP, or CFDP;
- an encoding of OceanMail product and service policy.

No wire format, integer encoding, identifier width, compression algorithm, cryptographic suite, or version number is frozen by this plan.

## Current executable proof

The repository now contains a standard-library Python proof under `prototype/`. It implements the six abstract operations named in this plan using explicitly disposable generation-0 encodings. Two local endpoints can transfer one immutable message through multiple byte-constrained contact windows, reopen receiver state between contacts, resume at the retained prefix, verify the whole representation, and decode the original message. The proof now also separates attachment metadata from independently selectable binary representations, transfers selected attachments with the same resume engine, compares order-independent collection summaries, emits budget-bounded pages containing only unknown representations, and produces deterministic synthetic-corpus byte reports. Its pagination cursor is harness state, not a proposed wire field.

The initial recorded corpus result is `prototype/results/baseline-2026-08-30.json`. It establishes a measurement baseline rather than a performance claim: tiny and reply-chain uncompressed exchanges still slightly exceed their MIME inputs, while attachment deferral and text compression candidates show substantial gains. Warm no-change comparison is 58 bytes, cold no-change comparison is 76 bytes, and detecting then offering one new representation is 120 bytes. The B2F baseline is not yet integrated.

This artifact validates state-machine and accounting assumptions only. It is not the planned Rust reference implementation, an M4P binding, a security profile, or compatibility authority. See [`prototype/README.md`](../prototype/README.md) for its exact scope, commands, and measured demo output.

## Repository audit

The audited starting revision, commit `716c50a`, is documentation-only. Its files already supersede the historical assumption that BEMPIC would own mesh routing. No current file assigns routing, peer discovery, store-carry-forward, generic fragmentation, network TTL, or DataLink behavior to BEMPIC.

The audit found several areas that needed refinement before implementation:

| Area | Finding | Disposition |
|---|---|---|
| Layer boundary | Current scope is substantially correct. Some uses of “transport blocks,” “transport profiles,” and “selective acknowledgement” could still be read as generic fragmentation or modem ARQ. | Use application representations and persistent extents; call M4P and other substrates carriers/bindings. |
| Identity | The documents require stable object identity but do not distinguish a logical message from a particular encoded, compressed, preview, or attachment representation. | Use separate logical-message and immutable-representation identities. Exact construction remains experimental. |
| Mailbox synchronization | The desired capability is listed, but no minimal state model or conflict boundary exists. | Begin with append-oriented availability/completion state. Defer folder, read/unread, deletion, and concurrent-edit semantics. |
| Metering | Metering is a first-class principle, but accounting domains and benchmark gates were not defined. | Measure BEMPIC bytes, carrier bytes, and physical/link bytes separately; define hard BEMPIC budget semantics. |
| Resumption | The documents correctly require continuation across sessions but do not sharply separate it from M4P fragmentation and link ARQ. | Persist completed application extents. Do not ACK every extent on reliable carriers. |
| Security | The public/authenticated/confidential classes are directionally correct. The first proof does not need to select a cryptographic suite, and must not falsely claim security when running clear. | Build integrity-checked clear simulation first; design optional legal/security profiles before real user traffic. |
| Prior art | Existing notes identify the correct projects but are not a feature-by-feature decision record. | The matrix and dispositions below are the initial design baseline. |
| Implementation boundary | OceanMail already proposes separate specification and reference repositories, but BEMPIC has no implementation structure or license. | Keep normative work here; create `bempic-reference` only when implementation begins and after licensing is chosen. |

## Authoritative layer boundary

| Concern | Owner | BEMPIC consequence |
|---|---|---|
| Message/mailbox semantics and compact representations | BEMPIC | Core responsibility. |
| Logical message identity and immutable representation identity | BEMPIC | Must survive sessions, peers, and carriers. |
| Application completion/delivery receipt | BEMPIC | Means a defined application state, not merely packet receipt. |
| Application usefulness expiry | BEMPIC/application profile | May stop an object from being offered after it is no longer useful. It is not a forwarding TTL. |
| Packet identity, deduplication, forwarding TTL, routing, and store-carry-forward | M4P | Do not reproduce them in BEMPIC. |
| Generic packet fragmentation, reassembly, and re-fragmentation | M4P | A BEMPIC operation is opaque application payload to M4P. |
| Persistent application continuation after a session or path is lost | BEMPIC | Receiver reports which immutable application bytes it already has. |
| PACTOR, VARA, and ARDOP connected-mode retransmission | Modem/DataLink | No BEMPIC checkpoint or per-frame retry loop. |
| Unreliable broadcast/FEC repair | Optional future BEMPIC carrier profile, only if not supplied below | Must be benchmarked and isolated from the reliable-carrier core. |
| Link opportunity, payload ceiling, airtime, and actual RF cost | M4P/DataLink | BEMPIC may consume estimates and expose them, but does not manufacture them. |
| Gateway scoring, relay participation, Mailcow integration, transformations, UI, quotas, and billing | OceanMail | Not normative BEMPIC behavior. |
| Application end-to-end protection | BEMPIC security profile | Optional confidentiality must coexist with a lawful clear/monitorable profile. |

The key distinction is that a BEMPIC **extent** is a persistent application synchronization unit. It allows another session or authorized source to continue the same immutable representation. It is not an M4P fragment and is not a link-layer frame.

## Concrete prior-art feature matrix

| Feature | Winlink B2F / FBB B1 | BPv7 | LTP | CFDP | BEMPIC disposition |
|---|---|---|---|---|---|
| Primary job | Connected constrained-email forwarding | DTN store-and-forward overlay networking | Pairwise convergence-layer reliability over very long/interrupted links | End-to-end file delivery | Compact application synchronization above M4P |
| Identity | MID, up to 12 text characters, identifies a Winlink message system-wide | Source node ID + creation timestamp identify a transmission request; fragment offset and length complete fragment identity | Originating engine ID + sender-generated session number identify one block-transfer session | Source entity ID + transaction sequence number identify a file transaction | Separate stable logical-message ID from immutable representation ID; do not reuse M4P packet identity |
| Message model | Text address header, ASCII body, and zero or more binary attachments | Opaque application data unit in a payload block plus optional extension blocks | Opaque contiguous client-service block | File metadata followed by offset-addressed file data | Compact message manifest with independently selectable body and attachment representations |
| Discovery/synchronization | Proposal block advertises messages; receiver accepts, rejects, defers, or resumes each proposal | No mailbox synchronization | None | A source initiates a file transaction; no mailbox set reconciliation | Compact summary/digest, offers, selection, and result state; append-oriented first |
| Batching | Proposal/turn cycles handle up to five messages and reduce direction changes | A bundle carries one ADU, though multiple bundles may be scheduled | One block per unidirectional session | One file per transaction | Batch control metadata and small selected representations when measurement shows a gain; large parts remain independently resumable |
| Compression | Winlink encapsulation is LZHUF-compressed; proposals include uncompressed and compressed sizes | Not a BPv7 core function | None | None | Negotiate codecs; always retain a no-compression baseline; precompute exact compressed cost where possible |
| Attachments | Header lists length and filename; attachment bytes follow the body | Opaque to BPv7 | Opaque to LTP | The transferred object is a file with source/destination names and size | First-class part descriptors; attachment bytes are deferred unless explicitly selected |
| Preview/reduced representation | Primarily a client/application feature, not a general B2F object model | Opaque to BPv7 | None | None | Multiple immutable representations may describe one logical part; selection is budgeted |
| Size advertisement | FC proposal carries uncompressed and compressed sizes | Bundle lengths are encoded, but user-facing cost quotation is not the purpose | Segment/block lengths are encoded | Metadata/EOF include file size information | Exact prepared representation size plus bounded protocol overhead; carrier estimate reported separately |
| Resume | FBB B1 `FS` can request restart at one offset in the exact compressed file; whole-file CRC validates completion | Fragmentation/reassembly is network behavior, not a cross-session application fetch protocol | Checkpoints trigger reception reports containing received byte-range claims | File Data PDUs carry offsets; acknowledged mode NAKs request missing segments | On reliable carriers, request a contiguous prefix or compact missing extents only after interruption; whole representation digest verifies completion |
| Fine-grained reliability | Underlying connected mode plus B1/B2 transfer checks and offset recovery | Delegated to convergence layers; BP handles DTN forwarding | Core purpose: red-part selective ARQ using checkpoints, reports, report ACKs, and retransmission | Class 2 ACK/NAK/FIN state machine; Class 1 is unacknowledged | Omit from reliable-carrier core. Study LTP/CFDP only for an optional unreliable-carrier profile |
| Completion/status | Session flow implies transfer acceptance; B2F is not a general end-to-end semantic receipt system | Optional reception, forwarding, delivery, and deletion status reports | Reports red-part reception and session completion | FIN reports transaction delivery/file status in acknowledged mode | Define representation verified/stored separately from logical application accepted/delivered; never expose hop forwarding as application delivery |
| Expiry | Primarily service policy | Bundle lifetime and Bundle Age govern network retention | Session timers/retry limits, not application usefulness | Transaction timers/fault policy | Optional application expiry prevents later synchronization; M4P retains ownership of forwarding TTL |
| Capabilities/versioning | SID feature flags and backward-compatible F/B/B1/B2 levels | BP version in every bundle plus extension-block registries | Version field and extension tags; no negotiation handshake | Configured interoperable entity parameters and extensible TLVs | Compact version/capability negotiation with a mandatory minimal baseline and clean skipping of optional features |
| Routing/store-carry-forward | Winlink service and connected BBS/RMS behavior around B2F | Core responsibility | Explicitly pairwise between adjacent engines | May operate end-to-end or through protocol features, but is file-transfer focused | Omit; M4P owns it |
| Security | Password challenge is service authentication; B2F compression is monitorable and not payload confidentiality | BP security is defined separately by BPSec | Assumes integrity from a lower layer and defines limited replay/DoS considerations | Commonly relies on protected/authenticated lower layers | Define optional application protection profiles without making confidentiality mandatory on legally restricted radio services |
| Metering/budgets | Compressed sizes permit an accept/reject decision, but no general hard application budget model | Not a user-byte-budget protocol | No application budget semantics | Size/progress are known, but no useful-information-per-byte selection model | Core differentiator: quote, approve, enforce, and report cost before optional content is sent |

### What B2F already does well

B2F is not obsolete merely because its syntax is textual. It already demonstrates several choices BEMPIC should preserve:

- independent clients can interoperate from a published protocol;
- a sender proposes work before sending the large payload;
- uncompressed and compressed sizes are known before acceptance;
- multiple proposals amortize turnarounds on long-delay links;
- message body and binary attachments are packaged without MIME/base64 on the constrained transfer;
- attachment length and filename arrive before attachment bytes;
- a simple offset can continue an interrupted exact compressed image;
- a whole-image CRC detects incorrect resumed reconstruction;
- capabilities are negotiated with backward-compatible feature flags;
- the same application protocol works over multiple connected modem and IP transports.

BEMPIC should improve or generalize the areas B2F does not target: service-neutral mailbox reconciliation, logical identity separate from a specific encoding, independently selectable representations, explicit budgets, exact cost accounting, continuation from different authorized sources, semantic receipts, modern extension rules, and optional end-to-end protection.

## Borrow, reuse, omit, and invent

### Borrow

- **From B2F:** propose before payload; advertise prepared size; batch control exchanges; avoid MIME/base64 on the constrained link; list attachments before bytes; keep a simple contiguous-offset fast path; retain backward-compatible capability signaling.
- **From BPv7:** distinguish transmission identity from application identity; treat disruption and late completion as normal; separate receipt states; carry an optional application usefulness lifetime without confusing it with network TTL; use explicit registries and deterministic encoding rules when the wire format is selected.
- **From LTP:** if an unreliable profile is later justified, use bounded report scopes and positive reception claims so missing ranges are inferred compactly. Do not reproduce its adjacent-engine session protocol in BEMPIC core.
- **From CFDP:** metadata before content, explicit sizes, offset-addressed data, end-of-object verification, persistent transaction state, and compact requests for missing extents.

### Reuse directly where appropriate

- Mature compression and digest libraries rather than custom algorithms.
- The ARSFI Winlink compression implementation or an independently compatible implementation as a **benchmark oracle**, subject to its BSD-style license and notices; it is not a required BEMPIC runtime dependency.
- `wl2k-go` as an MIT-licensed independent B2F interoperability reference and comparator, not as the BEMPIC architecture.
- Existing fuzzing, property-testing, and deterministic network-simulation libraries where their dependency cost is justified.

No third-party source should be copied into BEMPIC until the BEMPIC reference implementation license is adopted and compatibility/notices are recorded.

### Omit

- BPv7 routing, convergence layers, bundle fragmentation, forwarding status, and network retention.
- LTP engine IDs, pairwise sessions, checkpoint timers, report ACKs, red/green segmentation, and ARQ on reliable carriers.
- CFDP entity routing, filestore commands, proxy operations, and the complete Class 2 timer/ACK state machine.
- B2F's service-specific callsign/account assumptions, fixed legacy message types, textual constrained-link headers, ASCII-only body restriction, fixed five-message policy, and mandatory LZHUF dependency.
- SMTP, IMAP, HTTP, JSON, MIME, and base64 as constrained-link requirements.
- OceanMail gateway selection, relay policy, service authorization, transformations, billing, and UI behavior.

### Invent or standardize for BEMPIC

- A two-level identity model: logical message identity and immutable representation identity.
- A compact mailbox summary/change mechanism optimized for the no-change case.
- First-class alternative representations for full text, preview text, thumbnails, and other application-supplied variants.
- Exact prepared-size quotation and explicit application byte budgets.
- A selection model that maximizes useful information within a budget rather than automatically transferring every offered byte.
- Persistent resumption state that can be used with a later session, carrier, or authorized source.
- A semantic receipt vocabulary that distinguishes verified bytes, stored representation, accepted message, and final application delivery.
- Compact, cacheable version/capability negotiation and extension registries for independently upgraded implementations.
- A compact optional service/provider envelope for cross-service application delivery, without turning it into network routing or making every native message pay for it.
- A clear/monitorable security profile and optional authenticated/confidential profiles with truthful capability signaling.

## Smallest initial application model

The first model should be immutable and intentionally narrower than an email mailbox.

### Logical message

Required semantics:

- stable logical message identity;
- creation time or ordering input;
- sender and one or more recipients;
- subject, which may be absent;
- one body part;
- zero or more attachment parts.

Read/unread flags, folders, labels, deletion, drafts, mutable edits, thread reconstruction, spam state, and concurrent conflict resolution are not part of the first proof.

A service/provider envelope is also deferred from the first proof. Add it only when a concrete native/Winlink/SailMail/third-party interoperability case establishes the minimum fields. It must identify application delivery intent, not select or advertise an M4P network route.

### Part descriptor

A part describes its role and available representations:

- role: body or attachment;
- media type or compact registered equivalent;
- optional filename and application metadata;
- one or more immutable representation descriptors.

The application, not BEMPIC, creates previews, strips HTML, downscales images, or decides that two representations are semantically related.

### Representation descriptor

Each exact byte representation needs:

- identity bound to its immutable bytes;
- encoded byte length known before transfer;
- decoded/logical length when useful;
- representation/codec identifier;
- whole-representation integrity value;
- optional application usefulness expiry.

The exact digest, truncation length, and identifier construction must be benchmarked and threat-reviewed before standardization. A verbose Internet `Message-ID` is not suitable as the only wire identity, and a content hash alone is not sufficient to describe the semantic relationship among variants.

### Mailbox/synchronization state

The initial state model is append-oriented:

- a compact summary says whether the peer's known set/state still matches;
- a changed summary leads to offers for unknown logical messages or representations;
- the receiver selects useful representations under an explicit budget;
- verified results are persistent and idempotent;
- a semantic receipt is optional and distinct from receipt of carrier bytes.

A summary digest is only an optimization. A peer must be able to recover by requesting a bounded manifest page or another explicit reconciliation path when summaries disagree.

## Smallest initial exchange

The following operation names are descriptive placeholders:

| Operation | Minimum purpose |
|---|---|
| `CAPABILITIES` | Establish compatible experimental protocol generation, maximum operation size, compression support, security class, and optional features. Cache by peer/profile where safe. |
| `SUMMARY` | Compare a compact mailbox/set generation or digest and identify whether detailed reconciliation is required. |
| `OFFER` | Describe logical messages/parts/representations and their exact prepared sizes without sending deferred content. |
| `REQUEST` | Select representations, state a hard BEMPIC byte budget, and describe any already-held contiguous prefix or compact missing extents. |
| `DATA` | Carry an offset and bytes from one immutable representation. M4P may fragment this operation independently. |
| `RESULT` | Report verified/stored representation state and, when requested, a separate logical application receipt. |

Operations may be batched in one carrier payload. A session-local short reference may replace a stable identifier after an explicit mapping has been established. Unknown optional operations must be safely skippable once a length-delimited wire envelope exists.

### Reliable-carrier behavior

For M4P over PACTOR, VARA ARQ, ARDOP ARQ, or another reliable binding:

1. Do not acknowledge each `DATA` operation in BEMPIC.
2. Let M4P and the DataLink handle packet and RF reliability.
3. Persist only fully received application extents.
4. After a session/path loss, send one compact `REQUEST` describing retained progress.
5. Verify the whole immutable representation before issuing a successful `RESULT`.

### Unreliable-carrier behavior

The first implementation should expose loss, duplication, and reordering in the simulator, but it should not standardize an LTP-like recovery protocol yet. A later optional profile may add checkpointed reception claims only if measurements show that the carrier below BEMPIC does not provide suitable repair and that M4P cannot own the generic behavior.

## Compression experiment plan

The mandatory experimental baseline is uncompressed bytes. Candidate measurements should include:

- B2F-compatible LZHUF as the established constrained-email baseline;
- DEFLATE/gzip as a widely available baseline;
- Zstandard at low levels, with and without an application static dictionary;
- Brotli at practical low-memory/low-CPU settings;
- uncompressed transfer for tiny, pre-compressed, or incompressible data.

Measure per-message compression, batches of small bodies/manifests, and independently compressed attachments. Include every codec header, dictionary identifier, checksum, and any dictionary transfer in the byte total. A sender must not choose compression when the complete encoded representation is larger than the raw representation.

Large attachments should not be forced into the same compression context as message bodies. Doing so can make deferred retrieval and cheap resumption depend on bytes the receiver did not request.

## Byte-accounting model

BEMPIC cannot truthfully promise one universal “wire byte” number because M4P, DataLink framing, ARQ retries, FEC, and RF turnarounds live below it. Report distinct counters:

| Counter | Definition |
|---|---|
| `semantic_bytes` | Application bytes the user selected, measured in the agreed decoded representation. |
| `bempic_tx_bytes` / `bempic_rx_bytes` | Every serialized BEMPIC octet emitted in each direction, including negotiation, manifests, requests, data metadata, receipts, compression framing, and application protection. |
| `carrier_tx_bytes` / `carrier_rx_bytes` | Bytes presented to and reported by M4P or another carrier, including its framing/headers when exposed. |
| `link_tx_bytes` / `link_rx_bytes` | Actual DataLink/physical bytes or best available estimate, including retransmission/FEC when exposed. |
| `useful_committed_bytes` | Selected representation bytes that completed verification and became usable during the run. |
| `duplicate_payload_bytes` | BEMPIC representation bytes resent even though the receiver had already persisted them. |

Primary metrics:

- useful-byte efficiency = `useful_committed_bytes / (bempic_tx_bytes + bempic_rx_bytes)`;
- protocol overhead = total BEMPIC bytes minus selected encoded representation bytes;
- resume waste = duplicate representation payload sent after interruption;
- prediction error = `abs(quoted_bempic_bytes - actual_bempic_bytes) / actual_bempic_bytes`;
- time and bytes to first useful body;
- deferred-content avoidance = unrequested attachment payload bytes sent, which must be zero;
- budget utility yield = application-assigned fixture utility committed per total BEMPIC byte;
- codec net gain = raw complete BEMPIC exchange minus compressed complete BEMPIC exchange.

Budgets must name their domain. The first hard budget is total BEMPIC bytes for the approved operation. BEMPIC can stop emitting new operations at that limit, but it cannot retroactively cap modem retransmissions of bytes already handed to a lower layer. Carrier/link budgets are estimates or separately enforced lower-layer controls.

## Benchmark corpus

The repository should begin with deterministic, redistributable synthetic fixtures so results are reproducible and contain no private email. Add a real public corpus only after documenting its license and data-handling implications.

| Fixture | Required variants |
|---|---|
| No-change mailbox | Empty set and 100-message set, both cold and warm capability state |
| Tiny plain message | Approximately 80-200 UTF-8 body bytes, one sender, one recipient |
| Typical plain message | Approximately 1 KiB body, multiple recipients, realistic subject |
| HTML-origin message | Original RFC/MIME baseline plus an application-supplied normalized text representation |
| Reply chain | Repeated quoted text and signatures |
| Five-message batch | Mix of tiny and typical messages for direct B2F comparison |
| International text | Multi-byte UTF-8 names, addresses, subject, and body |
| Mailbox delta | 100 known messages plus one new message |
| Small attachment | 10 KiB compressible and already-compressed variants |
| Medium attachment | 100 KiB compressible and already-compressed variants |
| Large attachment | 1 MiB, metadata-only and selected-transfer cases |
| Multiple representations | Full text plus preview; image plus thumbnail metadata |

Every fixture should retain the original RFC 5322/MIME bytes when applicable, the application-normalized semantic model, and expected decoded output. This keeps OceanMail normalization gains separate from BEMPIC protocol gains.

## Baselines and initial measurable gates

Compare each applicable run against:

1. original RFC 5322/MIME message bytes;
2. the same semantic BEMPIC model encoded without compression;
3. B2F/LZHUF using a compatible implementation;
4. each negotiated candidate compressor;
5. full restart after interruption;
6. BEMPIC persistent resume.

Initial gates are hypotheses to validate, not wire-format promises:

| Gate | Initial target |
|---|---|
| Deterministic round trip | All fixtures decode to the expected immutable representation and semantic model. |
| Deferred attachment | Zero attachment payload bytes are emitted until that representation is selected. |
| Idempotency | Duplicate, delayed, and reordered complete operations never create duplicate logical delivery. |
| Warm no-change sync | At most 64 total BEMPIC bytes across both directions for a previously negotiated 100-message mailbox. |
| Cold no-change sync | At most 128 total BEMPIC bytes across both directions, excluding application security handshake experiments. |
| Incremental discovery | Adding one message to a known 100-message mailbox does not require retransmitting the other 100 manifests. |
| Tiny-message fixed overhead | At most 64 BEMPIC bytes beyond selected encoded content in a warm, one-message, no-attachment exchange; at most 128 bytes cold. |
| B2F comparison | Median total BEMPIC bytes for the prescribed text-message corpus should be at least 10% below B2F; no fixture should exceed B2F by more than 5% without a documented metering/resumption benefit. |
| Exact prepared cost | With no injected faults and a prepared immutable representation, quoted and actual BEMPIC bytes match exactly. |
| Hard budget | Neither peer emits a BEMPIC operation that would cross the accepted BEMPIC budget. |
| Useful-first selection | Under 128 B, 512 B, 2 KiB, and 10 KiB budgets, report which fixture utility classes completed and the bytes spent before the first readable body. |
| Resume waste | After interruption, no fully persisted extent is resent; at most one partially delivered/in-flight extent is repeated. |
| Resume control cost | After cached capabilities, resume negotiation should require at most 64 BEMPIC bytes before new useful payload. |
| Compression safety | The selected compressed form, including all framing, is never larger than the raw form sent by the same exchange. |

If a target cannot be met without disproportionate complexity, record the measured tradeoff and revise the target in Git rather than hiding the miss.

## Simulator and test strategy

### Carrier contract

The core simulator should present BEMPIC with an opaque-record carrier resembling an M4P application payload API:

- maximum payload size or current payload opportunity;
- send/receive of complete opaque application records;
- optional delivery outcome information;
- reliable/unreliable capability declaration;
- reported carrier byte cost when available.

M4P may fragment, reassemble, retain, deduplicate, and forward those records. The BEMPIC simulator must not implement M4P routing. A local length-prefixed byte-stream adapter may be used for development, but it is non-normative unless a direct-stream binding is later specified.

### Deterministic fault scenarios

The harness should reproduce every run from a seed and event log. Required scenarios:

- bandwidth ceilings from tens of bytes/second upward;
- fixed and variable latency;
- short contact windows and abrupt disconnects;
- interruption at 0%, 1%, 10%, 50%, 90%, and just before completion;
- restart of sender, receiver, or both from persisted state;
- continuation through a different authorized source that has the exact representation;
- duplicate and reordered complete records;
- record loss on unreliable carriers;
- corruption only where the simulated carrier does not guarantee integrity;
- stale summaries and stale capability caches;
- budget exhaustion during discovery and during payload transfer;
- loss of a completion/result message after the receiver committed the object;
- already-complete object offered again.

### Test layers

1. **Model tests:** identity stability, canonical application normalization inputs, immutable representation rules.
2. **Codec tests:** round trips, rejection of malformed/truncated input, size accounting, unknown optional fields, allocation limits.
3. **State-machine tests:** every operation is idempotent and crash-safe at every persistence boundary.
4. **Property tests:** arbitrary valid messages, extents, ordering, duplicate delivery, and budgets.
5. **Fuzzing:** parser and state transitions with untrusted lengths, counts, offsets, and capability combinations.
6. **Golden vectors:** experimental vectors during design; normative vectors only after the encoding stabilizes.
7. **Differential tests:** independent decoder/oracle before the wire is frozen.
8. **Benchmark tests:** byte counters, completion time, peak memory, codec CPU, and regression thresholds.
9. **End-to-end proof:** application message -> BEMPIC -> constrained/interrupted carrier -> persistent resume -> BEMPIC -> equal application message.

## Implementation recommendation

Use Rust for the reference implementation.

Reasons:

- explicit byte-level control without requiring unsafe memory handling;
- strong enums and state modeling for hostile input and crash-safe transitions;
- cross-platform support for OceanMail desktop/server use;
- straightforward C ABI, Python binding, and WebAssembly options later;
- mature compression, hashing, fuzzing, property-testing, and SQLite ecosystems;
- good alignment with the M4P project's announced Rust SDK direction while keeping BEMPIC independently usable.

Python should be used for corpus generation, result analysis, and plots, not as the only conformance implementation. B2F benchmark tooling may call a compatible Go or ARSFI implementation rather than porting legacy code into the BEMPIC core.

### Proposed `bempic-reference` Rust workspace

| Package | Responsibility |
|---|---|
| `bempic-model` | Logical messages, parts, representations, identities, and validation; no carrier or OceanMail types |
| `bempic-codec` | Experimental candidate encodings and exact size calculation; no socket or persistence code |
| `bempic-sync` | Pure synchronization state machine and operation semantics |
| `bempic-store` | Persistence traits plus reference memory/file/SQLite adapters |
| `bempic-carrier` | Minimal opaque-record carrier trait and non-normative local/IP adapter |
| `bempic-sim` | Deterministic carrier, fault scheduler, event log, and byte accounting |
| `bempic-cli` | Encode, inspect, synchronize, interrupt, resume, and report proof commands |
| `bempic-bench` | Fixture runners, B2F/compressor comparators, and machine-readable results |

The core crates should deny unsafe code initially, bound all remotely supplied sizes/counts, and avoid global mutable protocol state. Storage, clocks, randomness, compression, security, and carrier behavior should be injected behind narrow interfaces so tests remain deterministic.

## Specification and implementation separation

### `Gordonfive/bempic`

This repository remains authoritative for:

- scope and layer boundaries;
- normative terminology and application model;
- operation semantics and state machines;
- wire specification after it is selected;
- extension/version registries;
- security and carrier-binding requirements;
- conformance requirements and protocol decision records.

### `Gordonfive/bempic-reference`

Create this repository when coding begins. It should contain:

- the Rust workspace;
- deterministic fixtures and simulator;
- candidate codecs;
- benchmark tools and published results;
- experimental and later normative test vectors;
- fuzz/property/conformance tests;
- small interoperability examples.

It must not contain OceanMail accounts, Mailcow integration, proprietary service logic, product UI, infrastructure, gateway scoring, or relay policy.

The specification and reference implementation need explicit licenses before code or third-party source is added. A permissive implementation license is recommended; the exact license remains an owner decision.

## Work plan before wire freeze

### Phase 0 — Measurement foundation

1. Adopt licenses and contribution rules.
2. Create `bempic-reference` with the Rust workspace and CI.
3. Add deterministic fixtures and byte-accounting schema.
4. Integrate a B2F/LZHUF comparison oracle without making it a runtime dependency.
5. Implement the deterministic opaque-record carrier simulator.

**Exit:** raw, B2F, and candidate BEMPIC exchanges can be reproduced and compared byte for byte.

### Phase 1 — Semantic prototype

1. Implement the immutable message/part/representation model.
2. Implement in-memory operations with deliberately replaceable encoding.
3. Add persistent store/resume and hard BEMPIC budgets.
4. Pass all restart, duplicate, deferred-attachment, and round-trip tests.

**Exit:** the OceanMail proof flow works over the simulator without claiming a stable wire format.

### Phase 2 — Encoding bake-off

1. Implement at least two plausible deterministic binary encodings or profiles.
2. Benchmark integer encoding, identifiers, manifests, local references, batching, extent sizes, and capability envelopes.
3. Benchmark raw, LZHUF, DEFLATE, Zstandard, Brotli, and any justified static dictionaries.
4. Publish corpus, versions, machine details, raw results, and analysis.

**Exit:** one candidate wins on measured total bytes and implementability, not preference.

### Phase 3 — Mailbox and attachment proof

1. Add warm no-change summary and bounded mismatch reconciliation.
2. Add metadata-only attachment offers and selective retrieval.
3. Add multiple representations and cost quotes.
4. Validate continuation from another authorized source.

**Exit:** all initial byte gates have measured pass/fail results.

### Phase 4 — Interoperability and security design

1. Build an independent decoder or second implementation.
2. Specify clear/monitorable, authenticated-public, and confidential application profiles.
3. Measure all security overhead and replay state.
4. Define the M4P application binding with upstream coordination.
5. Define version negotiation, extension registry, error behavior, and downgrade rules.

**Exit:** two implementations interoperate and security modes make truthful, legally selectable claims.

### Wire-freeze gates

Do not freeze the first wire generation until:

- the layer boundary in this document is still intact;
- B2F baseline results are reproducible;
- all correctness gates pass;
- byte targets have measured results and documented exceptions;
- parser fuzzing and resource-limit tests pass;
- version and unknown-extension behavior are specified;
- at least two independent decoders agree on test vectors;
- the M4P binding does not duplicate M4P fragmentation, deduplication, TTL, or routing;
- clear operation and optional security profiles have an explicit design;
- the specification and implementation licenses are adopted.

## Cross-project handoff notes

### For the OceanMail thread

- OceanMail should supply normalized message objects and optional previews; BEMPIC should not standardize HTML stripping or image transformation policy.
- OceanMail should keep the original RFC 5322/MIME fixture so product normalization savings are reported separately from BEMPIC protocol savings.
- User approval, quota, priority, and route/service policy remain OceanMail decisions even when BEMPIC exposes exact sizes and budgets.
- Winlink/B2F account integration and external-network routing remain OceanMail interoperability work. BEMPIC uses B2F as prior art and a benchmark, not as a hidden service dependency.

### For the M4P thread

Before a normative binding, BEMPIC needs to learn the reference middleware's:

- application payload API and registered Message Type/profile mechanism;
- maximum payload/opportunity reporting;
- application send outcome semantics;
- persistence behavior across restart and path changes;
- packet-expiration interaction with longer-lived application synchronization state;
- available carrier and actual-byte accounting;
- guarantees for duplicate suppression and complete payload delivery to applications.

These are questions/handoff inputs. This BEMPIC thread must not implement or redefine the missing M4P behavior.

## Research sources

Primary specifications and maintained implementations reviewed for this plan:

- [Winlink Open B2F — Message Structure and B2 Forwarding Protocol](https://winlink.org/B2F)
- [Winlink Data Flow and Data Packaging](https://winlink.org/sites/default/files/downloads/winlink_data_flow_and_data_packaging.pdf)
- [F6FBB forwarding protocol](https://www.f6fbb.org/protocole.html)
- [ARSFI Winlink Compression source](https://github.com/ARSFI/Winlink-Compression)
- [wl2k-go independent B2F implementation](https://github.com/la5nta/wl2k-go)
- [RFC 9171 — Bundle Protocol Version 7](https://www.rfc-editor.org/rfc/rfc9171.html)
- [RFC 5326 — Licklider Transmission Protocol](https://www.rfc-editor.org/rfc/rfc5326.html)
- [CCSDS 727.0-B-5 — CCSDS File Delivery Protocol, Issue 5](https://ccsds.org/Pubs/727x0b5.pdf)
- [NASA F Prime CFDP Manager design](https://fprime.jpl.nasa.gov/latest/Svc/Ccsds/CfdpManager/docs/sdd/)
- [M4P specification repository](https://github.com/Poseidons-Forge/m4p-spec), reviewed at `main` commit `4977dfc`

Relevant OceanMail authority was read from `README.md`, `docs/ARCHITECTURE.md`, `docs/ARCHITECTURE-DECISIONS-2026-08-30.md`, `docs/BEMPIC-POLICY-BOUNDARY.md`, `docs/OMGP-DESIGN-GOALS.md`, `docs/EXTERNAL-NETWORK-ROUTING.md`, `docs/REPOSITORY-BOUNDARY.md`, `docs/M4P-UPSTREAM-ENGAGEMENT.md`, and `docs/MVP-ROADMAP.md`. Those files were treated as read-only inputs.
