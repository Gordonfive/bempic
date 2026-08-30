# BEMPIC

BEMPIC is an open protocol project for efficient, resilient synchronization and data transfer across severely bandwidth-constrained, high-latency, expensive, and intermittently connected networks.

OceanMail is the first planned production application of BEMPIC, but BEMPIC is intentionally not specific to email, marine communications, or any single transport.

## Project status

**Stage:** protocol design / pre-implementation

The wire format, protocol name expansion, cryptographic profile, compression profile, licensing, and versioning are not yet frozen.

## Core goals

- Minimize total bytes transmitted over constrained links.
- Treat disconnection and resumption as normal protocol states, not exceptional failures.
- Support synchronization and transfer of arbitrary application objects rather than only email messages.
- Remain transport-independent: IP, satellite, HF/SSB radio, amateur radio where legally permitted, serial links, and future transports.
- Assume the underlying network may be observable and hostile.
- Support strong confidentiality when the selected transport legally permits encryption.
- Avoid unnecessary metadata, repeated identifiers, verbose framing, and mandatory heavyweight handshakes.
- Measure protocol efficiency by actual bytes on the wire.
- Permit independent interoperable implementations through an open specification and conformance tests.

## Non-goals

BEMPIC is not intended to replace SMTP, IMAP, radio modem waveforms, IP, or existing physical/link-layer protocols. Applications and gateways may bridge those systems to BEMPIC.

## Documents

- [Protocol scope](docs/SCOPE.md)
- [Design principles](docs/DESIGN-PRINCIPLES.md)
- [Security model](docs/SECURITY-MODEL.md)
- [Open questions](docs/OPEN-QUESTIONS.md)

## Relationship to OceanMail

OceanMail is a proprietary hosted service and application suite that may implement BEMPIC. The open BEMPIC specification must remain implementable without OceanMail-specific services, code, credentials, or infrastructure.

## Licensing

Licensing is intentionally not yet finalized. The project intends to publish the protocol specification under terms suitable for an open standard and to permit independent implementations. No implementation license should be inferred until an explicit LICENSE file is adopted.
