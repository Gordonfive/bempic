# BEMPIC

BEMPIC is an open protocol suite for bandwidth-efficient messaging across severely bandwidth-constrained, high-latency, expensive, metered, and intermittently connected networks.

OceanMail is the first planned production application of BEMPIC and is the project's primary focus. BEMPIC defines interoperable mechanisms; OceanMail decides how and when to use those mechanisms.

## Project status

**Stage:** protocol design / pre-implementation

The wire format, protocol name expansion, compression profile, licensing, and versioning are not yet frozen.

## Protocol-suite structure

BEMPIC is expected to contain two separately specified but cooperating areas:

1. **Routing and discovery mechanisms** — compact primitives that applications can use to discover gateways/peers, advertise route information, identify freshness, and support relay-capable topologies.
2. **Low-bandwidth intermittent transport/messaging mechanisms** — compact transfer, metering, resumption, selective acknowledgement, retransmission, delivery state, and store-carry-forward primitives.

Neither area defines OceanMail's user-facing relay policy.

## Core goals

- Minimize total bytes and, for half-duplex transports, total airtime and unnecessary direction changes.
- Make byte metering and transfer budgets first-class protocol concepts.
- Treat disconnection and resumption as normal protocol states.
- Optimize first for messaging and OceanMail's email use case.
- Remain transport-independent while permitting transport-specific profiles.
- Avoid unnecessary metadata, repeated identifiers, verbose framing, and mandatory heavyweight exchanges.
- Permit independent interoperable implementations through an open specification and conformance tests.

## Mechanism, not product policy

BEMPIC may define interoperable primitives such as route advertisements, route epochs, scores, hop information, latency fields, discovery requests, selective acknowledgements, packet/range identifiers, delivery receipts, cache/custody state, and relay offers.

BEMPIC does **not** decide whether a particular application should eagerly relay traffic, reluctantly relay traffic, cache overheard messages, volunteer Internet access, retain data for a particular duration, spend additional airtime repairing another transfer, provide user incentives, or request weather. Those are application policies.

OceanMail may implement sophisticated cooperative HF behavior using BEMPIC primitives without making that behavior mandatory for every BEMPIC implementation.

## Non-goals

BEMPIC is not intended to replace SMTP, IMAP, radio modem waveforms, IP, or existing physical/link-layer protocols. Applications and gateways may bridge those systems to BEMPIC.

BEMPIC is not presently intended to solve every constrained-network synchronization problem. Broader non-messaging uses may be standardized later without making them requirements for OceanMail's initial development.

## Documents

- [Protocol scope](docs/SCOPE.md)
- [Design principles](docs/DESIGN-PRINCIPLES.md)
- [Security model](docs/SECURITY-MODEL.md)
- [Open questions](docs/OPEN-QUESTIONS.md)

## Relationship to OceanMail

OceanMail is a proprietary hosted service and application suite that implements BEMPIC. BEMPIC development is driven first by OceanMail's need for exceptionally efficient email and messaging over constrained links. The open BEMPIC specification must nevertheless remain implementable without OceanMail-specific services, code, credentials, policies, or infrastructure.

## Licensing

Licensing is intentionally not yet finalized. The project intends to publish the protocol specification under terms suitable for an open standard and to permit independent implementations. No implementation license should be inferred until an explicit LICENSE file is adopted.
