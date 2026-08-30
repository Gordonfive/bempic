# BEMPIC Protocol Scope

## Purpose

BEMPIC provides compact interoperable mechanisms for messaging synchronization, routing/discovery, transfer, resumption, and delivery state in environments where bandwidth, airtime, latency, reliability, or transfer cost is severely constrained.

BEMPIC is messaging-first and is being developed to serve OceanMail. The protocol supplies mechanisms. Applications such as OceanMail supply policy.

## Protocol areas

### Routing and discovery

BEMPIC may standardize compact interoperable primitives for:

- gateway/peer discovery;
- route advertisements;
- route epochs or equivalent freshness identifiers;
- reachability score exchange;
- hop/loop-prevention information;
- latency/link-quality information;
- discovery requests and responses;
- relay offers and route handoff signaling.

BEMPIC does not prescribe OceanMail's algorithm for calculating a score, deciding whether to advertise, choosing eager versus reluctant participation, or determining when a relay should intervene unless a behavior is strictly necessary for interoperability.

### Low-bandwidth intermittent transport and messaging

BEMPIC may standardize compact interoperable primitives for:

- message/object identification;
- compact mailbox/message synchronization;
- byte-offset or block/range resumption;
- burst transfer;
- selective acknowledgements;
- missing-range repair;
- delivery receipts;
- store-carry-forward state;
- cache/custody signaling;
- metering and byte budgets;
- compression negotiation;
- transport-specific framing where required.

## Data model

BEMPIC initially operates on messaging-oriented objects and state changes, including compact message representations, message metadata, attachment metadata/content, synchronization state, and delivery/relay state.

The constrained link should not require MIME, JSON, HTTP, SMTP, IMAP, or another verbose Internet-facing representation.

## Application-policy boundary

BEMPIC does not define product decisions such as:

- whether a user is an eager or reluctant relay;
- how much disk space a relay volunteers;
- whether an application caches everything it overhears;
- cache retention duration;
- how aggressively an application volunteers missing packets;
- when an application chooses to insert itself as an intermediate relay;
- whether an Internet-connected vessel volunteers as an OceanMail gateway;
- how often OceanMail initiates discovery beyond interoperability requirements;
- OceanMail message-priority policy;
- contributor incentives, quotas, badges, or scores;
- OceanMail weather policy;
- user-interface behavior;
- account billing or service policy.

Those belong to OceanMail or another BEMPIC application.

## Architectural boundary

BEMPIC also does not define Internet email delivery semantics, mailbox spam policy, radio modulation/modem waveforms, satellite service behavior, or OceanMail business logic.

## Constrained-link assumption

The protocol must remain useful on links where throughput can be measured in hundreds of bytes per second, connections may last only minutes, interruption may occur at any point, and some transports are half-duplex.

A lost connection is not a failed transaction. Persistent transfer state and later resumption are normal protocol behavior.

## Open-standard requirement

A conforming BEMPIC implementation must not require proprietary OceanMail components. The normative specification and conformance behavior must be sufficient for independent interoperable implementations. OceanMail-specific routing and relay policy may remain proprietary while using the public BEMPIC mechanisms.
