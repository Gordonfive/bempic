# BEMPIC

BEMPIC is an open protocol project for bandwidth-efficient messaging across severely bandwidth-constrained, high-latency, expensive, metered, and intermittently connected networks.

OceanMail is the first planned production application of BEMPIC and is the project's primary focus. BEMPIC should be designed cleanly enough that it may later be extended to other constrained-link data uses, whether by OceanMail or independent implementers, but general-purpose synchronization is not a current project requirement.

## Project status

**Stage:** protocol design / pre-implementation

The wire format, protocol name expansion, cryptographic profile, compression profile, licensing, and versioning are not yet frozen.

## Core goals

- Minimize total bytes transmitted over constrained links.
- Make byte metering and transfer budgets first-class protocol concepts.
- Let applications and users know, constrain, and prioritize how many bytes a synchronization or transfer may consume.
- Treat disconnection and resumption as normal protocol states, not exceptional failures.
- Optimize first for messaging and OceanMail's email use case.
- Remain transport-independent: IP, satellite, HF/SSB radio, amateur radio where legally permitted, serial links, and future transports.
- Assume the underlying network may be observable and hostile.
- Support strong confidentiality when the selected transport legally permits encryption.
- Avoid unnecessary metadata, repeated identifiers, verbose framing, and mandatory heavyweight handshakes.
- Measure protocol efficiency by actual bytes on the wire.
- Permit independent interoperable implementations through an open specification and conformance tests.

## Non-goals

BEMPIC is not intended to replace SMTP, IMAP, radio modem waveforms, IP, or existing physical/link-layer protocols. Applications and gateways may bridge those systems to BEMPIC.

BEMPIC is not presently intended to solve every constrained-network synchronization problem. Broader object types and non-messaging uses may be standardized later without making them requirements for OceanMail's initial development.

## Documents

- [Protocol scope](docs/SCOPE.md)
- [Design principles](docs/DESIGN-PRINCIPLES.md)
- [Security model](docs/SECURITY-MODEL.md)
- [Open questions](docs/OPEN-QUESTIONS.md)

## Relationship to OceanMail

OceanMail is a proprietary hosted service and application suite that implements BEMPIC. BEMPIC development is driven first by OceanMail's need for exceptionally efficient email and messaging over constrained links. The open BEMPIC specification must nevertheless remain implementable without OceanMail-specific services, code, credentials, or infrastructure.

## Licensing

Licensing is intentionally not yet finalized. The project intends to publish the protocol specification under terms suitable for an open standard and to permit independent implementations. No implementation license should be inferred until an explicit LICENSE file is adopted.
