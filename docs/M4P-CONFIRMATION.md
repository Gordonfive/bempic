# M4P v0.1 Binding Review Package

**Package status:** ready for external review; not submitted; not confirmed

**Binding profile:** `bempic-m4p-opaque-record-v0.1-review`, revision 1

This document defines BEMPIC's proposed opaque-record binding to M4P and the
evidence an external M4P reviewer is asked to confirm or correct. It does not
change M4P, claim M4P approval, allocate an M4P application Message Type ID, or
describe a released M4P implementation API. The machine-readable counterpart is
[`m4p-binding-review-package.json`](../conformance/v0.1/m4p-binding-review-package.json),
and the unsubmitted request is
[`2026-09-02-m4p-v0.1-binding-review.md`](review-requests/2026-09-02-m4p-v0.1-binding-review.md).

The required architecture remains:

```text
OceanMail → BEMPIC → M4P → DataLink adapters
```

## Authoritative M4P source and legal boundary

The review package is based on the M4P specification repository at immutable
commit
[`2eca9e8f57d43dab250cc26c1bbf2d255e3331de`](https://github.com/Poseidons-Forge/m4p-spec/commit/2eca9e8f57d43dab250cc26c1bbf2d255e3331de)
(tree `b06d1830c6156ead535542d9ff4c0a5acbfd1545`). That source identifies the
specification as version 0.1, status Proposal Draft. Its
[`README`](https://github.com/Poseidons-Forge/m4p-spec/blob/2eca9e8f57d43dab250cc26c1bbf2d255e3331de/README.md)
says a reference implementation is still under development, so this review can
pin specification behavior but cannot yet map it to a public implementation
API or test executable.

The M4P specification is copyright 2026 Poseidon's Forge, Inc. and licensed
under
[`CC-BY-4.0`](https://github.com/Poseidons-Forge/m4p-spec/blob/2eca9e8f57d43dab250cc26c1bbf2d255e3331de/LICENSE).
This BEMPIC document independently describes a proposed interface and
paraphrases protocol behavior with attribution. No M4P source code, AGPL code,
fixtures, lookup tables, or substantial specification text is copied here.

Primary clauses used by the review package are the immutable M4P source files
for
[`scope`](https://github.com/Poseidons-Forge/m4p-spec/blob/2eca9e8f57d43dab250cc26c1bbf2d255e3331de/sections/01-introduction.md),
[`protocol overview`](https://github.com/Poseidons-Forge/m4p-spec/blob/2eca9e8f57d43dab250cc26c1bbf2d255e3331de/sections/02-protocol-overview.md),
[`identity and addressing`](https://github.com/Poseidons-Forge/m4p-spec/blob/2eca9e8f57d43dab250cc26c1bbf2d255e3331de/sections/03-identity-addressing.md),
[`message classes`](https://github.com/Poseidons-Forge/m4p-spec/blob/2eca9e8f57d43dab250cc26c1bbf2d255e3331de/sections/04-message-classification.md),
[`wire formats`](https://github.com/Poseidons-Forge/m4p-spec/blob/2eca9e8f57d43dab250cc26c1bbf2d255e3331de/sections/05-on-wire-formats.md),
[`deduplication`](https://github.com/Poseidons-Forge/m4p-spec/blob/2eca9e8f57d43dab250cc26c1bbf2d255e3331de/sections/06-deduplication.md),
[`TTL`](https://github.com/Poseidons-Forge/m4p-spec/blob/2eca9e8f57d43dab250cc26c1bbf2d255e3331de/sections/07-ttl-expiration.md),
[`fragmentation`](https://github.com/Poseidons-Forge/m4p-spec/blob/2eca9e8f57d43dab250cc26c1bbf2d255e3331de/sections/08-fragmentation.md),
[`transport behavior`](https://github.com/Poseidons-Forge/m4p-spec/blob/2eca9e8f57d43dab250cc26c1bbf2d255e3331de/sections/09-transport-behavior.md),
[`DataLink abstraction`](https://github.com/Poseidons-Forge/m4p-spec/blob/2eca9e8f57d43dab250cc26c1bbf2d255e3331de/sections/10-datalink-abstraction.md),
and
[`integration guidance`](https://github.com/Poseidons-Forge/m4p-spec/blob/2eca9e8f57d43dab250cc26c1bbf2d255e3331de/sections/C-integration-guidelines.md).
Exact Git blob identities and their uses are in the machine-readable package.
The release template pins that package's RFC 8785 canonical SHA-256 as
`2154cbe49417a06647138ac8e3034280dfcbf6a135d55260f1e80ed3c58ca459`.

## Exact opaque-record interface

[REQ-M4P-002] A conforming BEMPIC-to-M4P binding contract MUST expose exactly
the normalized submit result and inbound delivery defined below, submit one
complete canonical BEMPIC operation as one opaque M4P application-message
payload, and deliver to BEMPIC only a complete reassembled payload. It MUST NOT
submit or deliver a partial BEMPIC operation. A concrete adapter may use
different programming-language names, but its evidence must provide a total,
unambiguous mapping to these fields and closed result values.

### Outbound `submit_record`

The inputs are:

| Binding field | Source | M4P mapping |
|---|---|---|
| `record_bytes` | one complete canonical encoded BEMPIC operation | application Message payload |
| `destination_client_uid` | application-authorized endpoint binding | directed Message destination `ClientUID` |
| `binding_message_type_id` | deployment binding configuration, never a BEMPIC operation field | application Message Type ID; allocation and class remain open review questions |
| `local_submission_ref` | adapter-local correlation | never encoded or forwarded |

Every BEMPIC semantic field remains inside `record_bytes`; M4P sees none of
those fields individually. BEMPIC does not pass an M4P Client Address, Node
Address, network ID, MIID, route, next hop, fragment offset or length, TTL
override, priority override, modality mask, authentication field, DataLink
opportunity, or physical-link parameter. Deployment M4P configuration may set
per-type priority, TTL, modality, and security policy outside the BEMPIC record.

The return record contains `local_submission_ref`, `status`, and a bounded
`diagnostic_code`. `status` is exactly one of:

| Status | Meaning at the BEMPIC boundary |
|---|---|
| `accepted` | the complete record was accepted by the local M4P runtime, including acceptance into pending address resolution; it says nothing about send, persistence across restart, peer delivery, application delivery, or a BEMPIC receipt |
| `not-accepted-record-too-large` | the binding's reviewed safe complete-record limit rejected the call before M4P acceptance |
| `not-accepted-invalid-destination` | the configured destination value is invalid for the binding |
| `not-accepted-binding-unconfigured` | no reviewed Message Type/configuration mapping exists |
| `not-accepted-backpressure` | the local runtime declined the complete record without accepting it |
| `not-accepted-local-error` | another local failure proves non-acceptance |
| `acceptance-unknown` | IPC/process/connection loss prevents the adapter from proving either acceptance or non-acceptance |

This is the BEMPIC normalization proposed for review. The current M4P
specification describes accepted pending-address state and DataLink outcomes,
but does not publish a concrete application API with this result vocabulary.
External confirmation must therefore identify an implementation mapping or
correct this contract before the binding can pass.

### Inbound `receive_record`

The delivery contains:

| Binding field | Source |
|---|---|
| `record_bytes` | one complete, reassembled M4P application Message payload |
| `source_client_uid` | M4P's resolved source `ClientUID`, or null when unresolved |
| `source_resolution` | `resolved` or `unresolved` |
| `local_delivery_ref` | adapter-local correlation, never encoded or forwarded |

[REQ-M4P-005] Before BEMPIC state mutation, the binding MUST validate the
configured inbound Message Type, complete-record size, source resolution, and
application-owned source authorization. An unresolved or unauthorized source
must be rejected or quarantined outside BEMPIC state and cannot cause a BEMPIC
receipt. The binding uses the resolved `ClientUID`; it does not expose M4P's
mission-scoped Client Address or Node Address to BEMPIC.

M4P allows local delivery while source identity is unresolved and initiates a
lookup. The source does not say whether an implementation can replay that
delivery after resolution. The review therefore asks whether quarantine may be
released after resolution or whether the sender must submit a fresh M4P Message.

### Capacity, opportunity, and cost

BEMPIC permits an outer operation up to 1,048,576 octets. M4P's packet
`payload_length` has a 65,535-octet ceiling, while a fragment has a 15-bit byte
offset and its own payload length. The M4P text defines reassembly as final
offset plus final-fragment length but does not state a safe maximum complete
application payload. This package deliberately does not infer one from the
field widths.

The M4P DataLink opportunity budget is presented to the M4P core, which builds
a complete Transmission, fragments application Messages when needed, or defers
them. No current authoritative clause exposes that opportunity to the M4P
application client. Likewise, the application boundary defines no exact
carrier-byte or physical-byte report. The binding therefore exposes no such
budget or cost by default; BEMPIC reports those domains as unavailable. A future
implementation-specific exposure needs its own exact scope, units, admission
semantics, and external review.

## Ownership and deliberate non-duplication

[REQ-M4P-003] The binding MUST preserve the ownership table below. In
particular, BEMPIC must remain an opaque application protocol and must not
implement or redefine M4P addressing, routing, forwarding, mesh coordination,
store-carry-forward scheduling, network TTL, generic fragmentation/reassembly,
retained-record resend/spacing, fragment NACK, network deduplication,
cross-modality forwarding, or DataLink behavior. M4P explicitly omits custody
transfer, so neither layer may claim an M4P custody guarantee. Any external
correction or exception remains release-blocking until reconciled through
governance.

| Concern | Owner | BEMPIC-visible consequence |
|---|---|---|
| Application object identity and authorized-source policy | OceanMail/application | supplies opaque identifiers and authorized endpoint binding |
| Operation selection, encoding, prefix resume, bounded operation replay, integrity, and semantic receipts | BEMPIC | durable application state independent of route/contact |
| `ClientUID` resolution to mission-scoped Client Addresses | M4P | BEMPIC names only authorized `ClientUID` endpoints |
| Routing, forwarding, mesh coordination, store-carry-forward | M4P | absent from BEMPIC operations |
| Retained-record resend, spacing, and opportunity scheduling | M4P | BEMPIC does not schedule or count M4P record resends |
| Network TTL and expiration | M4P | no BEMPIC TTL emulation |
| Generic fragmentation, re-fragmentation, reassembly, Fragment NACK | M4P | BEMPIC boundary remains complete records |
| MIID-based network deduplication | M4P | distinct from BEMPIC operation idempotency |
| M4P Packet/Transmission/resend byte accounting | M4P | recorded only if a reviewed application contract exposes scope and units |
| Link framing, FEC, ARQ, frame retransmission, physical bytes | DataLink/modem | only separately reported, labeled cost may be recorded |
| Custody transfer | neither; omitted by M4P | BEMPIC retains its own durable progress but claims no network custody |

M4P's `sent`, `busy`, `failed`, and `timed_out` values are DataLink-to-M4P
facts. A `sent` fact means the link accepted bytes and is not peer delivery.
Optional M4P link-acceptance, delivered-to-peers, receipt-envelope, or
peer-holding evidence also remains network evidence. None is a BEMPIC
application receipt or advances BEMPIC application state.

## Resume through another source, path, or carrier

[REQ-M4P-006] A V09 binding MUST preserve the durable BEMPIC prefix and
representation ID across source, process, contact, route, link, and modality
changes. A receiver may address a new complete BEMPIC `REQUEST` to any
application-authorized source `ClientUID` that holds identical prepared bytes;
the first returned `DATA` begins at the authoritative durable prefix. M4P alone
chooses routes, relays, links, and modalities. A change of M4P path or DataLink
is invisible to BEMPIC, while a move to a non-M4P carrier is outside this binding
and still cannot change BEMPIC's endpoint-role, prefix, or representation rules.

Source authorization remains an application decision. M4P proves the resolved
source `ClientUID`, not OceanMail's permission for that source to serve a given
representation. The binding performs the authorization check before BEMPIC
mutation and does not infer it from a Client Address, Node Address, route, or
carrier.

## Receipts, duplicates, and a lost final receipt

[REQ-M4P-007] A binding MUST carry a BEMPIC `RECEIPT` only as another complete
opaque BEMPIC operation and must not synthesize it from an M4P send, delivery,
receipt-envelope, or holding indication. After a final BEMPIC receipt is lost or
expires, the sender may boundedly replay the identical triggering BEMPIC
operation in a fresh M4P Message instance. The receiver must apply no duplicate
application effect, re-emit the same BEMPIC receipt idempotency identity after
durable commit, and let the sender advance exactly once.

The distinction between the two duplicate domains is intentional. M4P
suppresses repeated network copies with one M4P message identity. A deliberate
BEMPIC retry uses a new M4P Message instance so the complete operation can reach
the application again; BEMPIC then detects its own duplicate and preserves
application idempotency.

## Budget exhaustion and connection loss

[REQ-M4P-008] Before invoking `submit_record`, BEMPIC MUST compute the exact
encoded size of the next complete operation. If that operation exceeds the
remaining total or directional BEMPIC budget, BEMPIC emits nothing and pauses.
After `accepted`, M4P may fragment, defer, store, forward, or expire the Message
under M4P rules without splitting the BEMPIC operation at this interface. A
proven non-acceptance records no BEMPIC send and releases the preflight
reservation. `accepted` and `acceptance-unknown` each conservatively debit and
record the complete operation once; a later fresh replay debits and records it
again. `acceptance-unknown` permits only a bounded replay of the identical
operation as a fresh M4P Message; it never permits a false receipt or an
assertion that M4P durably retained the first attempt.

M4P is not a connection-oriented application transport. Loss of a physical
link after acceptance remains internal M4P scheduling/store state. Loss of the
local BEMPIC-to-M4P IPC call is the binding's `acceptance-unknown` case. BEMPIC's
own persisted prefix, commit, and receipt state remains authoritative after
either event. M4P restart durability and any application-visible expiration or
cancellation notification are still unconfirmed.

## Prescribed V09, V10, and V12 traces

[REQ-M4P-004] Reference binding evidence MUST execute every trace ID below,
record every ordered step and pass assertion from the machine-readable package,
identify the exact implementation/API mapping and M4P source commit, and bind
its result to the applicable BEMPIC vector. A skipped step, partial BEMPIC
operation, unauthorized or unresolved source mutation, wrong resume offset,
unreported acceptance uncertainty, duplicate application effect, false
receipt, inferred lower-layer cost, or lower-layer indication used as a BEMPIC
receipt is a failing trace.

| Trace ID | Vector/case | Required proof |
|---|---|---|
| `M4P-V09-AUTHORIZED-SOURCE` | V09 alternate authorized source | different authorized source `ClientUID`; same representation and endpoint-role binding; first resumed offset equals durable prefix; zero durable-prefix retransmission |
| `M4P-V09-CROSS-MODALITY` | V09 alternate carrier | M4P path/DataLink or modality changes; BEMPIC record interface and durable prefix do not |
| `M4P-V10-DUPLICATE` | V10 duplicate data | same-MIID network duplicate suppressed separately from a fresh-MIID BEMPIC replay; no duplicate application effect |
| `M4P-V10-LOST-FINAL-RECEIPT` | V10 lost final receipt | no M4P evidence becomes receipt; fresh-MIID replay causes idempotent re-emission and exactly-once sender advance |
| `M4P-V12-BUDGET` | V12 exact and one-byte-short | one-short submits nothing; exact submits one complete operation; M4P opportunity handling stays below boundary |
| `M4P-V12-CONNECTION-LOSS` | V12 binding connection loss | uncertain acceptance is reported, durable state reopens, bounded fresh-MIID replay has no false receipt or duplicate effect |

These are prescribed expected traces, not invented execution evidence. They
remain blocked until a binding implementation runs them against the externally
confirmed mapping.

## Questions for external review

The package asks an M4P maintainer or authorized reviewer to answer these exact
questions:

1. What maximum complete application payload can M4P accept, persist, fragment,
   reassemble, and deliver given the packet and fragment field widths?
2. Which deployment-owned directed Message Type IDs and Request/Response
   mapping may carry independent bidirectional BEMPIC operations without
   violating the one-response rule? BEMPIC allocates none here.
3. Which public implementation API maps to the normalized submit results, and
   what accepted state survives process or node restart?
4. Which application-visible cancellation, backpressure, expiry, carrier-byte,
   and physical-byte signals exist, with what units and scope?
5. Can one authorized-source set span M4P `network_id` deployments, or is an
   external federation boundary required? M4P addresses are deployment/mission
   scoped and runtime cross-network reassignment is deferred.
6. Should the binding reject before submission when peers run mixed M4P
   versions? Current M4P has no wire version field and requires one version per
   deployment.
7. What expiry/retry signal allows delivery lasting beyond M4P's approximately
   7.4-hour maximum encodable TTL without duplicating M4P store-carry-forward?
8. Can delivery quarantined for an unresolved source `ClientUID` be released
   after lookup, or must a fresh M4P Message be submitted?

The first four questions block an executable binding mapping. Questions five
through eight block claims about federation, mixed-version deployments,
long-lived delivery, and authorized-source handling. The package deliberately
does not answer them on M4P's behalf.

## External confirmation record

[REQ-M4P-001] The v0.1 release record MUST link an upstream M4P issue, pull
request, or immutable review record and identify the exact M4P specification
commit, this binding profile and revision, reviewer stable identity and M4P
authority, UTC confirmation date, answers or corrections to every open question,
and immutable binding-trace evidence. Silence, local-only BEMPIC review, issue
closure without an affirmative statement, or this unsubmitted draft is not
confirmation.

A later change to the identified M4P source commit, safe maximum, Message Type
mapping, API result mapping, persistence promise, or visible accounting signal
invalidates confirmation until reviewed again. As of this package, `upstream_url`,
reviewer, confirmation time, approval, and trace digests are null or false. The
external-confirmation and dependent V09/V10/V12 release gates remain blocked.
