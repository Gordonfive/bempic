# BEMPIC Open Questions

These items are deliberately unresolved and should be tested or decided before a 1.0 wire format is frozen.

## Naming

- Keep `BEMPIC` as the project/protocol name or adopt a shorter 4–5 character name?
- If BEMPIC remains, what is its final expansion now that the protocol is broader than messaging?

## Wire model

- Deterministic operation encoding and length-delimited extension envelope?
- Contiguous-prefix resume, compact missing extents, or a measured combination for immutable application representations?
- What application extent sizes minimize resume waste without recreating generic fragmentation?
- When is a whole-representation digest sufficient on an integrity-preserving carrier?
- Does an optional unreliable-carrier profile need per-extent integrity or reception claims?
- What compact integer encoding should be normative?
- How are session-local object identifiers assigned and recycled?

## Synchronization

- Minimal manifest representation.
- Conflict semantics for bidirectional synchronization.
- Whether delta encoding belongs in core or application profiles.
- Whether content-addressed deduplication is worthwhile for any constrained-link profiles.

## Compression

- Zstandard, Brotli, or multiple negotiated algorithms?
- Shared static dictionaries by application profile?
- Minimum payload size before compression is attempted?
- Rules preventing compression side-channel problems with secrets.

## Security

- Cryptographic suite(s).
- Identity model and key enrollment.
- Full handshake versus pre-provisioned keys for extremely short contacts.
- Session resumption mechanism.
- Authentication tag size and record sizing.
- Regulatory/security profiles for amateur radio and other restricted transports.

## Carrier bindings

Initial candidates:

- M4P application payload binding for OceanMail production use;
- deterministic opaque-record simulator for development and testing;
- non-normative local/IP record adapter for the first proof;
- a direct byte-stream binding only if independent non-M4P deployments require one;
- optional unreliable/broadcast binding only after proving the carrier below BEMPIC lacks suitable recovery.

PACTOR, VARA, ARDOP, satellite, serial, TCP/IP, and future link technologies belong behind M4P/DataLink or another carrier. They are not separate BEMPIC modem/transport profiles.

## Standardization and licensing

- Specification document license.
- Reference implementation license (permissive licensing is the current direction).
- Governance model and contribution process.
- Whether future publication should pursue an IETF Internet-Draft/RFC path or remain an independent open specification initially.
