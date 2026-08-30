# BEMPIC Protocol Scope

## Purpose

BEMPIC provides a compact, resumable messaging synchronization and transfer layer for environments where bandwidth, airtime, latency, reliability, or transfer cost is severely constrained.

BEMPIC is messaging-first and is being developed to serve OceanMail. The protocol should avoid needless assumptions that block later expansion, but arbitrary application synchronization is not an initial requirement.

## Data model

BEMPIC initially operates on messaging-oriented objects and state changes, including:

- compact email/message representations;
- message metadata and mailbox state;
- attachment metadata and selectively requested attachment content;
- delivery, custody, relay, and synchronization state;
- explicitly requested auxiliary message content where defined by an application profile.

The protocol should not require MIME, JSON, HTTP, SMTP, IMAP, or another verbose application representation on the constrained link.

## Required protocol capabilities

BEMPIC should ultimately provide:

1. Compact session establishment and capability negotiation.
2. Message discovery and synchronization with minimal metadata exchange.
3. Byte-offset or block-based resumption after interruption.
4. Compact acknowledgements and retransmission requests.
5. Integrity checking appropriate to the transport profile.
6. Compression negotiation and application-aware preprocessing support.
7. Transport-independent framing or transport profiles.
8. Explicit accounting, budgeting, and prioritization of bytes transmitted.
9. Version and extension negotiation without forcing legacy peers to understand new extensions.
10. Support for future store-carry-forward and relay behavior without requiring it for the initial OceanMail implementation.

## Architectural boundary

BEMPIC does not define:

- Internet email delivery semantics;
- mailbox spam policy;
- account billing;
- user-interface behavior;
- radio modulation or modem waveforms;
- satellite services;
- OceanMail business logic.

Those concerns belong to applications, gateways, transport adapters, or external systems.

## Weather and auxiliary data

Weather is not a default BEMPIC synchronization workload. OceanMail should normally rely on purpose-built onboard, broadcast, satellite, or other weather sources. Weather delivery through OceanMail is an explicit fallback request for cases where preferred weather sources are unavailable.

The protocol may later support additional application profiles without making them part of the initial messaging core.

## Constrained-link assumption

The protocol must remain useful on links where throughput can be measured in hundreds of bytes per second, connections may last only minutes, and interruption may occur at any point.

Therefore, a lost connection is not a failed transaction. Persistent transfer state and later resumption are normal protocol behavior.

## Open-standard requirement

A conforming BEMPIC implementation must not require proprietary OceanMail components. The normative specification and conformance behavior must be sufficient for independent interoperable implementations.
