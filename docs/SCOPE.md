# BEMPIC Protocol Scope

## Purpose

BEMPIC is an extreme-efficiency application synchronization protocol for messaging over links and networks where bandwidth, airtime, latency, reliability, or transfer cost is severely constrained.

BEMPIC is messaging-first and is being developed to serve OceanMail. It should remain independently implementable and service-neutral.

## Layer boundary

BEMPIC is not the mesh/network layer.

OceanMail intends to use M4P for:

- peer/network discovery;
- network addressing;
- generic store-carry-forward;
- cross-modality forwarding;
- generic fragmentation/reassembly;
- network-level deduplication;
- TTL and forwarding policy primitives;
- DataLink abstraction.

BEMPIC sits above that layer and represents application state efficiently.

## Required BEMPIC capabilities

BEMPIC should ultimately provide:

1. Compact email/message representation that avoids verbose Internet-facing formats on constrained links.
2. Minimal mailbox/message discovery and synchronization.
3. Stable application-level message/object identity.
4. Batching and compression negotiation optimized for small text-heavy messages.
5. Explicit byte metering, predicted transfer cost, and transfer budgets.
6. Attachment metadata and selective/deferred attachment retrieval.
7. Reduced representations such as thumbnails or downsampled content where an application requests them.
8. Application-level continuation/resumption after interruption, including continuation through a different peer or transport.
9. Logical/end-to-end delivery receipts and synchronization state.
10. Capability and protocol-version negotiation suitable for independently upgraded implementations.
11. Service/provider-neutral envelopes where an application needs to carry messages toward different external systems.
12. Optional unreliable-link recovery mechanisms only when the underlying transport does not already provide adequate reliable ARQ.

## Reliability boundary

Reliable point-to-point modems such as PACTOR, VARA HF, and ARDOP ARQ own RF-level frame reliability, acknowledgement, retransmission, FEC, adaptive modulation, and TX/RX turnaround behavior.

BEMPIC must not duplicate those mechanisms unnecessarily.

BEMPIC resumption applies above the modem session. A logical transfer can continue after a session has disappeared, potentially hours later and through another node or another modem technology.

For broadcast/FEC or otherwise unreliable links, a BEMPIC profile may use selective-range/checkpoint recovery inspired by LTP/CFDP where measurement shows that it is worthwhile.

## Application data model

BEMPIC initially operates on messaging-oriented objects and state changes, including:

- compact email/message bodies and metadata;
- mailbox state;
- attachment metadata and requested content;
- delivery/synchronization state;
- provider/service envelope information where needed.

The constrained link should not require MIME, JSON, HTTP, SMTP, IMAP, or another verbose Internet-facing representation.

## Explicit non-goals

BEMPIC does not define:

- M4P mesh routing/network behavior;
- OceanMail gateway scoring or route advertisements;
- eager/reluctant relay policy;
- modem waveforms or physical-layer behavior;
- Internet email delivery semantics;
- mailbox spam policy;
- user-interface behavior;
- billing/subscription policy;
- weather policy;
- OceanMail business logic.

## Constrained-link assumption

BEMPIC must remain useful on links where throughput can be extremely low, sessions can be brief, interruptions are normal, and the cost of unnecessary bytes is material.

A lost connection is not a failed application transaction. Persistent synchronization state and later continuation are normal behavior.

## Open-standard requirement

A conforming BEMPIC implementation must not require proprietary OceanMail components. The normative specification and conformance behavior must be sufficient for independent interoperable implementations.
