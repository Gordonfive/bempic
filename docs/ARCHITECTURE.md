# BEMPIC Architecture

## Required stack

```text
OceanMail
    |
    | normalized messages, selection, policy, user intent
    v
BEMPIC
    |
    | compact application objects and synchronization operations
    v
M4P
    |
    | addressing, mesh coordination, forwarding, DTN behavior,
    | fragmentation, deduplication, TTL, carrier opportunity
    v
DataLink adapters
    |
    | PACTOR / VARA / ARDOP / satellite / serial / IP / future links
    v
Physical or service link
```

This ordering is an invariant, not an example deployment. OceanMail may use a
different carrier outside its maritime grid, but BEMPIC still consumes an
opaque-record carrier contract and does not absorb the carrier's network role.

## BEMPIC components

- **Model and preparation:** validates bounded application values, selects a
  schema/codec, deterministically prepares immutable bytes, and computes exact
  identifiers and sizes.
- **Reconciliation:** compares append-only collection checkpoints and produces
  bounded delta or full-inventory offers.
- **Selection and budgeting:** allows the application to defer representations
  and authorizes only complete operations within an explicit BEMPIC-byte scope.
- **Transfer:** carries offset-addressed bytes for a prepared representation.
- **Persistence and verification:** durably records a contiguous prefix,
  reopens it after interruption, verifies exact bytes, and commits atomically.
- **Receipts:** distinguishes committed representation state from application
  acceptance and delivery.
- **Codec boundary:** maps semantic operations to a deterministic, bounded
  binary profile without making a particular codec part of the core.
- **Carrier boundary:** sends and receives complete opaque operations and
  consumes lower-layer opportunity/cost information when it exists.

## Carrier contract

A carrier binding exposes complete-record send/receive, an available payload or
opportunity limit, integrity/reliability capabilities, and actual or estimated
cost when known. M4P is the production carrier for OceanMail. A deterministic
simulator or local byte-stream adapter may be used for testing but is not an
M4P substitute or a normative direct network stack.

BEMPIC treats a carrier delivery outcome only as evidence that an operation was
handled by the carrier. It never converts that outcome into an application
receipt.

## Persistence boundary

M4P may persist packets for forwarding. BEMPIC separately persists application
representation progress because that progress must survive the loss of an M4P
packet, route, peer, contact, or carrier. These stores have different identity,
retention, and completion rules and MUST NOT be conflated.

## Reliability boundary

On a reliable connected DataLink, BEMPIC sends data without a per-extent ACK
loop. When a later contact begins, the receiver requests the suffix after its
durable contiguous prefix. This is cross-contact application continuation.

Unreliable/broadcast recovery is not in v0.1 core. If later standardized, it
must be isolated in a carrier profile and justified against what M4P and the
DataLink already supply.

## Security boundary

BEMPIC integrity identifies exact prepared bytes. Origin authentication,
confidentiality, replay protection, key management, and legal transport
profiles require an application security profile. M4P or DataLink protection
does not automatically provide end-to-end application protection.

## Dependency direction

The public specification may name M4P requirements and coordinate a binding,
but it MUST NOT import M4P routing data structures into the BEMPIC application
model. The reference implementation may depend on carrier traits or bindings;
the specification remains independently implementable.
