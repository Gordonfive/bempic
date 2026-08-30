# BEMPIC Open Questions

These items are deliberately unresolved and should be tested or decided before a 1.0 wire format is frozen.

## Naming

- Keep `BEMPIC` as the project/protocol name or adopt a shorter 4–5 character name?
- If BEMPIC remains, what is its final expansion now that the protocol is broader than messaging?

## Wire model

- Byte-stream framing versus discrete records?
- Byte-offset resume, fixed blocks, variable blocks, or negotiated combinations?
- When does per-block CRC provide enough accidental-error detection?
- When is whole-record authenticated integrity sufficient?
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

## Transport profiles

Initial candidates:

- ordinary IP/TCP for development and testing;
- HTTP-compatible/IP profile where infrastructure benefits justify it;
- serial/byte-stream adapter;
- satellite-IP links;
- HF/SSB modem integrations;
- amateur-radio integrations where legal constraints are understood.

## Standardization and licensing

- Specification document license.
- Reference implementation license (permissive licensing is the current direction).
- Governance model and contribution process.
- Whether future publication should pursue an IETF Internet-Draft/RFC path or remain an independent open specification initially.
