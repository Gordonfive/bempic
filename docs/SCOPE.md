# BEMPIC Protocol Scope

## Purpose

BEMPIC provides a compact, resumable synchronization and transfer layer for environments where bandwidth, airtime, latency, reliability, or transfer cost is severely constrained.

The protocol is intentionally application-neutral. Email is an initial use case through OceanMail, not the boundary of the protocol.

## Data model

BEMPIC operates on application-defined objects and state changes. An object may represent, for example:

- a message or email representation;
- weather or GRIB-derived data;
- a position report;
- a file or file fragment;
- a form or structured record;
- telemetry;
- a command or response;
- software or configuration data;
- another application-defined payload.

The protocol should not require MIME, JSON, HTTP, SMTP, IMAP, or another verbose application representation on the constrained link.

## Required protocol capabilities

BEMPIC should ultimately provide:

1. Compact session establishment and capability negotiation.
2. Object discovery and synchronization with minimal metadata exchange.
3. Byte-offset or block-based resumption after interruption.
4. Compact acknowledgements and retransmission requests.
5. Integrity checking appropriate to the transport profile.
6. Compression negotiation and application-aware preprocessing support.
7. Confidentiality and authentication profiles where legally permitted.
8. Transport-independent framing or transport profiles.
9. Explicit accounting of bytes transmitted.
10. Version and extension negotiation without forcing legacy peers to understand new extensions.

## Architectural boundary

BEMPIC does not define:

- Internet email delivery semantics;
- mailbox spam policy;
- account billing;
- user-interface behavior;
- radio modulation or modem waveforms;
- satellite services;
- application-specific object semantics beyond extension/profile definitions;
- OceanMail business logic.

Those concerns belong to applications, gateways, transport adapters, or external systems.

## Constrained-link assumption

The protocol must remain useful on links where throughput can be measured in hundreds of bytes per second, connections may last only minutes, and interruption may occur at any point.

Therefore, a lost connection is not a failed transaction. Persistent transfer state and later resumption are normal protocol behavior.

## Open-standard requirement

A conforming BEMPIC implementation must not require proprietary OceanMail components. The normative specification and conformance behavior must be sufficient for independent interoperable implementations.
