# Great Parallel Work

## Purpose

This document is the durable research register for existing protocols, software, standards, and projects that overlap BEMPIC's goals.

Git is authoritative. Discoveries that materially influence BEMPIC architecture, provide reusable code, establish prior art, or prevent unnecessary reinvention should be recorded here even when they are not adopted directly.

Entries should identify whether a project is primarily:

- **Adopt / depend on** — use directly where practical;
- **Borrow / study** — reuse concepts, algorithms, formats, tests, or code where licensing permits;
- **Interoperate** — compatibility is strategically useful;
- **Influence only** — useful prior art but not an implementation dependency;
- **Rejected / superseded** — considered and intentionally not adopted, with the reason retained.

Licensing must be checked before copying implementation code. Protocol ideas and software source licenses are separate questions.

## Winlink B2F

**Role:** Borrow / study; OceanMail interoperability target.

B2F is Winlink's published message-forwarding protocol and is the closest direct prior art for BEMPIC's initial email use case.

Relevant ideas include:

- bandwidth-conscious email transfer;
- batching multiple messages before compression;
- LZH-based compression;
- attachments;
- radio/modem independence;
- independent compatible client implementations;
- partial/recovery concepts inherited from the FBB forwarding family.

BEMPIC should establish what B2F already does efficiently before inventing an alternative mechanism. BEMPIC is intended to be service-neutral and more explicitly focused on metering, synchronization, resumability, capability/version negotiation, and modern application/object handling rather than becoming a renamed Winlink protocol.

The Winlink compression implementation/source is particularly relevant for benchmarking and comparison.

## IETF Bundle Protocol Version 7 (BPv7)

**Role:** Borrow / study.

BPv7 is major prior art for Delay/Disruption Tolerant Networking.

Relevant concepts include:

- persistent message/bundle identity;
- expiration/lifetime;
- disruption tolerance;
- delivery/status reporting;
- fragmentation concepts;
- late/intermittent connectivity;
- convergence-layer separation.

BEMPIC should borrow appropriate application-continuity concepts but should not embed a second generic DTN network beneath itself when M4P already owns mesh/store-carry-forward behavior.

## NASA/JPL ION-DTN

**Role:** Borrow / study implementation.

ION-DTN is an operational/research implementation of DTN concepts including Bundle Protocol and LTP. It is useful for understanding mature implementation choices, persistence, custody/delivery state, scheduling, and extreme-delay operation.

BEMPIC does not currently plan to adopt ION as its runtime.

## Licklider Transmission Protocol (LTP)

**Role:** Borrow / study selectively.

LTP is especially relevant because its checkpoint/reception-report model resembles the selective-gap recovery mechanism independently considered during BEMPIC/OceanMail design.

Relevant ideas include:

- long transmit intervals before reports;
- checkpoints;
- reception claims expressed as byte ranges;
- retransmission of missing ranges rather than complete objects;
- extreme-delay/disruption operation.

Important boundary: do **not** duplicate fine-grained LTP-style retransmission over reliable PACTOR, VARA HF ARQ, or ARDOP ARQ sessions. Those modem/link protocols already own RF-level ACK/retry behavior. LTP-like recovery is potentially useful only for unreliable/broadcast/FEC transports or other links that do not already provide suitable reliability.

## CCSDS File Delivery Protocol (CFDP)

**Role:** Borrow / study.

CFDP is strong prior art for interruption-tolerant file/object transfer.

Relevant ideas include:

- metadata before transfer;
- byte-offset data;
- checksums;
- EOF/completion state;
- acknowledged and unacknowledged modes;
- missing-range detection;
- retransmission of only missing data.

This is particularly relevant to future BEMPIC attachment/object resumption.

## M4P — Multi-Modal Maritime Mesh Protocol

**Role:** Adopt below BEMPIC; upstream dependency/partner.

M4P is the intended mesh/network layer below BEMPIC for OceanMail's maritime grid use case.

M4P already covers functionality that must therefore **not** be reinvented in BEMPIC:

- mesh/store-carry-forward;
- network coordination/addressing;
- generic TTL forwarding;
- generic fragmentation/reassembly;
- network-level deduplication;
- priority scheduling;
- cross-modality forwarding;
- DataLink abstraction;
- peer/network behavior.

BEMPIC should remain useful over other networking substrates as well, but OceanMail's planned grid architecture uses M4P.

## Reticulum

**Role:** Borrow / study; not selected as OceanMail's primary mesh layer.

Reticulum is mature prior art for extremely low-bandwidth decentralized networking across heterogeneous interfaces.

Particularly relevant ideas include:

- very large decentralized destination identities;
- autonomous network formation;
- destination announcements;
- randomized announcement propagation;
- hop-aware path information;
- on-demand path requests;
- announcement bandwidth limits;
- routing across heterogeneous interfaces.

These ideas are especially relevant to M4P's current gaps around long-lived public-network participation, scale, and route discovery.

Reticulum was not selected in place of M4P because M4P is more directly maritime/multi-modal, is designed around extremely small transmission opportunities, provides a conventional standalone specification, has a planned Apache-2.0 implementation, and better matches the desired optional-security/public-radio profile.

## LXMF

**Role:** Borrow / study.

LXMF is a low-bandwidth messaging layer built on Reticulum. It is relevant prior art for asynchronous messaging, propagation/store-and-forward nodes, compact message delivery, and application UX over constrained networks.

BEMPIC should compare its eventual message representation and synchronization behavior against LXMF where appropriate.

## DTN7 implementations

**Role:** Borrow / study software architecture.

DTN7 implementations demonstrate useful daemon/API separation for DTN networking. Relevant patterns include:

- networking daemon separated from applications;
- application APIs over local sockets/REST-like interfaces;
- pluggable convergence/link layers;
- externally replaceable routing strategies.

This architecture may influence how OceanMail Full consumes M4P middleware rather than embedding every networking concern directly into the UI/application process.

## PACTOR

**Role:** Interoperate; link-layer dependency, not BEMPIC implementation.

PACTOR is mature adaptive HF ARQ technology from SCS and is important because of its existing offshore/SailMail installed base.

BEMPIC should treat a connected PACTOR session as a reliable underlying link and must not duplicate PACTOR's FEC, ARQ, retransmission, modulation adaptation, or half-duplex timing.

## VARA HF

**Role:** Interoperate; link-layer dependency, not BEMPIC implementation.

VARA HF is a software modem widely used with Winlink. It provides adaptive half-duplex ARQ and already handles RF-level DATA/ACK/retransmission and speed/robustness adaptation.

It is strategically important as a relatively accessible OceanMail HF transport.

## ARDOP

**Role:** Interoperate; borrow/study open radio protocol.

ARDOP provides software-based HF operation including ARQ and broadcast/FEC-oriented modes.

ARDOP ARQ should own RF-link reliability during connected operation. Its broadcast/FEC capabilities are especially interesting for future cooperative one-to-many OceanMail/M4P operation where application/network-level caching and repair may add value.

## Winlink ecosystem clients and gateways

**Role:** Interoperate / borrow / study.

Relevant projects/components include Winlink Express, Pat, RMS software, Linux RMS Gateway and other independent clients/gateways.

Pat is particularly relevant as prior art for an independent cross-platform Winlink-compatible client. Open RMS implementations and gateway components should be studied for gateway, B2F, modem-interface, and operational patterns where licensing permits.

## SailMail / AirMail

**Role:** Interoperate; product and protocol prior art.

SailMail is major prior art for commercial/offshore low-bandwidth email using PACTOR coast stations. AirMail demonstrates a maritime client serving established radio-email workflows and multiple service contexts.

OceanMail should pursue authorized/official SailMail client integration rather than assuming SailMail's radio-service protocol is an open third-party interface.

## OpenSail and bandwidth-budgeted offshore services

**Role:** Influence / potential future integration.

OpenSail and similar offshore tools demonstrate explicit bandwidth-aware weather/routing requests and integration with SailMail/Winlink-style workflows.

OceanMail should prefer integrating proven weather/routing providers later rather than unnecessarily becoming a weather-forecasting service.

## Briar

**Role:** Influence, especially future chat UX.

Briar demonstrates messaging that transitions between Internet and local/offline transports while retaining user-facing conversation continuity. It is not an HF email solution but is useful prior art for OceanMail Chat and offline-first UX.

## Other constrained/off-grid messaging projects

Projects such as LoRa mesh messengers and emerging off-grid messaging protocols should be recorded here when they reveal useful compact-wire, discovery, routing, power-management, or UX techniques. They are not automatically implementation dependencies.

## Research rule

Before BEMPIC invents a substantial new mechanism, search this register and current external work first. Prefer, in order:

1. use a proven compatible mechanism;
2. adapt a proven open mechanism;
3. contribute a generally useful improvement upstream;
4. design something new only where existing work does not satisfy the requirement.

When a new project materially affects BEMPIC, add it here and record the architectural consequence in the appropriate authoritative design document as well.
