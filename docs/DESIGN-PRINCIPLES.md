# BEMPIC Design Principles

## 1. Count bytes, not abstractions

Protocol decisions must be evaluated by total bytes transmitted on representative constrained links. Convenient but verbose encodings are not acceptable merely because they are common elsewhere.

## 2. Disconnection is normal

Peers must expect interruption. Transfer state should survive disconnects, reboots, transport changes, and long pauses where practical.

## 3. Resume cheaply

A peer that already possesses part of an object should request only what remains. Simple byte-offset resumption is preferred where it is cheaper than elaborate chunk metadata. Content-addressed chunking is optional and must justify its overhead.

## 4. Do not retransmit known context

Session-local identifiers, compact integer encodings, negotiated capabilities, and cached metadata should replace repeated long identifiers and descriptive fields whenever safe.

## 5. Separate application objects from transport blocks

An application object may be compressed and protected as a logical record while being carried in smaller transport blocks. This permits selective retransmission without requiring expensive application-level repetition.

## 6. Compress before encryption

When compression is appropriate, normalization/deduplication occurs before compression, and compression occurs before encryption. Tiny payloads may be sent uncompressed when compression framing would increase size.

## 7. Security strength is not traded for convenience

Use established cryptographic constructions rather than custom cryptography. Optimize framing, negotiation, session resumption, and metadata rather than weakening algorithms.

## 8. Observable transport is assumed

Radio and other shared media may be passively recorded by anyone in range. Sensitive application metadata should be protected along with payload content whenever legal and technically possible.

## 9. Transport law and capability matter

Some transports or jurisdictions may prohibit encrypted amateur-radio traffic or impose other restrictions. Security modes therefore belong to negotiated transport/security profiles; applications must not assume every transport permits confidentiality.

## 10. Integrity and confidentiality are distinct

Unencrypted data may still require authentication or integrity protection. Public broadcast, authenticated-public, and confidential modes may have different overhead and policy profiles.

## 11. Existing layers should be reused

BEMPIC should integrate with existing radio modems, satellite links, TCP/IP, serial transports, compression libraries, and established cryptography instead of replacing mature technology without measurable benefit.

## 12. The core remains application-neutral

Email, weather, files, telemetry, forms, and other data types should be implemented as application profiles or object types rather than hard-coded assumptions in the protocol core.

## 13. Extensions must degrade cleanly

Peers should be able to negotiate capabilities without large exchanges. Unknown optional extensions must not prevent core interoperability.

## 14. Optimize empirically

A protocol simulator and byte-accounting test suite should compare candidate encodings, block sizes, acknowledgement strategies, compression modes, and resumability schemes under realistic link loss and throughput conditions before the wire format is frozen.
