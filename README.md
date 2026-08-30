# BEMPIC

BEMPIC is an open extreme-efficiency application synchronization protocol for messaging across severely bandwidth-constrained, high-latency, expensive, metered, and intermittently connected networks.

OceanMail is the first planned production application of BEMPIC and is the project's primary focus.

## Project status

**Stage:** protocol design / executable semantic proof

The wire format, protocol name expansion, compression profile, licensing, and versioning are not yet frozen.

## Architectural role

BEMPIC no longer attempts to define a mesh-routing/network protocol. OceanMail intends to adopt **M4P (Multi-Modal Maritime Mesh Protocol)** for peer/network coordination, store-carry-forward mesh behavior, cross-modality forwarding, generic fragmentation, TTL, network-level deduplication, and DataLink abstraction.

BEMPIC sits above M4P and focuses on application/message efficiency and continuity.

```text
OceanMail
   |
 BEMPIC
   |  extreme-efficiency application synchronization
   v
  M4P
   |  multi-modal delay-tolerant mesh/networking
   v
PACTOR / VARA / ARDOP / IP / other links
```

## Core goals

BEMPIC should provide compact interoperable mechanisms for:

- extremely efficient email/message representation;
- mailbox/message synchronization with minimal metadata exchange;
- message/object identity at the application layer;
- batching and compression negotiation;
- explicit byte metering and transfer budgets;
- attachment metadata, deferred retrieval, and reduced representations;
- application-level continuation/resumption after interruption, even through a different peer or transport;
- logical/end-to-end delivery receipts;
- capability and version negotiation;
- provider/service-neutral envelopes where needed;
- optional recovery mechanisms for unreliable/broadcast transports when the underlying link does not already provide reliable ARQ.

## Explicit non-goals

BEMPIC does **not** own:

- mesh routing or peer discovery;
- node/network addressing;
- generic store-carry-forward forwarding mechanics;
- generic network TTL handling;
- generic cross-modality forwarding;
- RF modulation, FEC, ARQ, fine-grained modem retransmission, or half-duplex turnaround control;
- OceanMail relay/gateway participation policy;
- OceanMail business logic.

Those concerns belong primarily to M4P, DataLink/modem layers, or OceanMail itself.

## Reliability boundary

PACTOR, VARA HF, and ARDOP ARQ already provide sophisticated RF-link reliability. BEMPIC should not duplicate their frame acknowledgements, FEC, retransmission loops, or adaptive modulation behavior.

BEMPIC remains responsible for continuity above a failed session. For example, a logical message transfer may resume hours later through a different peer or modem even though the original ARQ session is gone.

For unreliable/broadcast transports, BEMPIC may define an optional recovery profile inspired by selective-range/checkpoint designs such as LTP and CFDP, but only where this does not duplicate a reliable underlying link.

## Prior art and research direction

BEMPIC is intentionally not greenfield. Development should study and borrow compatible ideas from:

- Winlink B2F, especially constrained email packaging, batching, compression, and attachments;
- IETF Bundle Protocol / DTN concepts for disruption tolerance and delivery state;
- NASA/JPL LTP for checkpoint/selective-range recovery on unreliable links;
- CCSDS CFDP for resumable object/file transfer and missing-range repair;
- other open constrained-network protocols where useful.

See `docs/PRIOR-ART-AND-BOUNDARIES.md`.

## Documents

- [Protocol scope](docs/SCOPE.md)
- [Design principles](docs/DESIGN-PRINCIPLES.md)
- [Security model](docs/SECURITY-MODEL.md)
- [Prior art and boundaries](docs/PRIOR-ART-AND-BOUNDARIES.md)
- [Initial protocol plan, feature matrix, and benchmarks](docs/INITIAL-PROTOCOL-PLAN.md)
- [Open questions](docs/OPEN-QUESTIONS.md)
- [Executable interrupted-transfer semantic proof](prototype/README.md)

## Relationship to OceanMail

OceanMail is the first application and commercial service built around BEMPIC. BEMPIC must remain independently implementable and service-neutral even though OceanMail drives its initial requirements.

OceanMail's M4P/mesh behavior, gateway scoring, eager/reluctant relay policy, Winlink/SailMail interoperability, and product UI are not BEMPIC requirements unless an interoperability need proves they belong in the open protocol.

## Licensing

Licensing is intentionally not yet finalized. The project intends to publish the protocol specification under terms suitable for an open standard and to permit independent interoperable implementations. No implementation license should be inferred until an explicit LICENSE file is adopted.
