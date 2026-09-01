# BEMPIC Prior Art and Boundaries

## Purpose

This document records the major protocol research conclusions that define what BEMPIC should borrow, what it should not duplicate, and why BEMPIC still exists alongside M4P and existing constrained-network protocols.

Git documentation is authoritative; these conclusions must not depend on chat history.

The historical feature matrix, borrow/reuse/omit/invent decisions, source list,
and pre-wire implementation plan are in
[`INITIAL-PROTOCOL-PLAN.md`](INITIAL-PROTOCOL-PLAN.md). Current requirements are
in [`../SPECIFICATION.md`](../SPECIFICATION.md); the architecture and repository
owners are in [`REPOSITORY-BOUNDARY.md`](REPOSITORY-BOUNDARY.md).

## Winlink B2F

B2F is the closest direct predecessor for constrained email transfer.

Relevant ideas to study and potentially reuse where licensing permits:

- efficient preparation of Internet email for radio transfer;
- batching multiple messages before compression;
- compression tuned for messaging workloads;
- attachment handling;
- transport/modem independence;
- openly documented interoperability enabling independent clients;
- partial recovery and forwarding concepts inherited from FBB-style systems.

BEMPIC should not simply become B2F because BEMPIC is intended to be service-neutral, explicitly metered, modernly extensible, and able to continue logical application synchronization through different peers/transports over time.

B2F remains the required initial performance baseline. It already proposes messages before payload, advertises compressed and uncompressed size, batches proposal/turn exchanges, packages attachments without MIME/base64 on the constrained transfer, and supports simple compressed-file offset recovery. BEMPIC must measure an actual improvement or document the specific metering/resumption benefit that justifies any additional bytes.

## IETF Bundle Protocol / DTN

Delay/Disruption Tolerant Networking provides important conceptual prior art:

- persistent objects/bundles;
- expiration/lifetime;
- store-and-forward over disrupted paths;
- delivery/status reporting;
- late binding and heterogeneous convergence layers.

M4P now owns the generic mesh/store-carry-forward networking role in the OceanMail architecture, so BEMPIC should borrow application-relevant DTN concepts without embedding another generic DTN network layer above M4P.

## Licklider Transmission Protocol (LTP)

LTP closely resembles the selective repair design independently discussed for OceanMail:

- long data bursts before report/checkpoint exchange;
- receiver reports received byte ranges;
- sender retransmits missing ranges;
- optimized for long-delay/disrupted links.

However, PACTOR, VARA HF, and ARDOP ARQ already perform reliable point-to-point link repair. BEMPIC must not add a second fine-grained retransmission layer over these transports.

LTP-style recovery is relevant only for carrier bindings that are unreliable/broadcast/FEC or otherwise do not provide adequate repair below BEMPIC.

## CCSDS File Delivery Protocol (CFDP)

CFDP is strong prior art for resumable object/file transfer:

- metadata + data segments;
- offset/range tracking;
- checksums;
- missing-range detection;
- retransmission of gaps rather than complete files;
- interrupted transfer continuation.

BEMPIC should borrow these ideas for attachments/large objects while remaining messaging-first rather than adopting CFDP wholesale.

## Dynamic Compact Control Language (DCCL)

DCCL is prior art for designing compact, analyzable codecs. BEMPIC borrows the
discipline of declarative field bounds and numeric precision, mandatory maximum
encoded size, schema fingerprints, pluggable codecs, strict validation, and
exact encoded-size analysis.

DCCL is **not** a dependency or compatibility target. BEMPIC does not adopt the
DCCL wire format, DCCL encryption, its C++ implementation, or a Protobuf
dependency. BEMPIC's v0.1 semantic core remains codec-neutral, and any codec
profile must be independently specified and registered.

See the [GobySoft DCCL project](https://github.com/GobySoft/dccl) for the
upstream implementation and documentation links.

## M4P boundary

M4P is the intended open mesh/network layer for OceanMail.

M4P already provides much of what earlier BEMPIC drafts attempted to own:

- decentralized peer/network coordination;
- store-carry-forward;
- cross-modality forwarding;
- fragmentation/reassembly;
- network-level deduplication;
- TTL/expiration;
- priorities and scheduling;
- forwarding deferral/cancel-on-seen suppression;
- DataLink abstraction;
- optional evidence such as link quality.

Therefore BEMPIC must not duplicate these capabilities.

## Reticulum findings

Reticulum is not selected as the OceanMail network layer, but it is important prior art for M4P/OMGP requirements.

Ideas worth studying/upstreaming into M4P where appropriate:

- very large decentralized address spaces;
- autonomous network participation;
- destination announcements;
- on-demand path requests;
- hop-aware route propagation;
- randomized announcement propagation;
- explicit control of announcement bandwidth;
- long-lived independently administered public networks.

M4P remains preferred because it is maritime-specific, explicitly multi-modal/store-carry-forward, optimized for very small transmission opportunities, has a conventional written open specification, and plans an Apache-2.0 reference implementation.

## BEMPIC retained role

BEMPIC should focus on what these systems do not jointly give OceanMail:

- ultra-compact service-neutral email/message representation;
- mailbox synchronization;
- batching/compression optimized for email;
- explicit byte budgets and predicted transfer cost;
- attachment metadata and selective/deferred retrieval;
- continuation of logical application state across lost sessions, changed peers, and changed transports;
- end-to-end application delivery receipts;
- provider/service envelopes;
- protocol capability/version negotiation;
- optional recovery only for unreliable links where the underlying layer does not already solve it.

Executable reference work for this retained role belongs in the sibling
`bempic-reference` repository. The Python proof in this repository is a
transitional, non-normative oracle until the published parity gate passes.

## Architectural rule

Before adding a BEMPIC mechanism, ask:

1. Is this generic mesh/network behavior already provided by M4P? If yes, keep it out of BEMPIC.
2. Is this RF/link reliability already provided by PACTOR/VARA/ARDOP or another DataLink? If yes, keep it out of BEMPIC.
3. Is this an application synchronization/representation problem that must survive across sessions and transports? If yes, it is a strong BEMPIC candidate.
4. Is this only OceanMail product policy? If yes, keep it in OceanMail.
