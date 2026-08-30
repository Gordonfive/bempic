# BEMPIC Design Principles

## 1. Count bytes, not abstractions

Protocol decisions must be evaluated by total bytes transmitted on representative constrained links. Convenient but verbose encodings are not acceptable merely because they are common elsewhere.

## 2. Metering and byte budgets are first-class

BEMPIC is intended for links where bytes may be scarce because of throughput, airtime, power, monetary cost, connection windows, or all of these at once. Implementations must be able to measure actual bytes consumed and expose that cost to applications.

A session or operation should be able to express a byte budget and track bytes used and remaining. Applications should be able to make transfer decisions before consuming the budget—for example, fetching message metadata while deferring an attachment or image.

Budgeting must account for protocol overhead as well as application payload whenever practical. BEMPIC should not advertise a 10 KB transfer as 10 KB if framing, acknowledgements, cryptographic material, retransmissions, or other protocol traffic materially increase the actual link cost.

Metering also enables prioritization. OceanMail may spend a limited budget on urgent text messages before optional attachments, previews, bulk mail, or other lower-priority data.

## 3. Disconnection is normal

Peers must expect interruption. Transfer state should survive disconnects, reboots, transport changes, and long pauses where practical.

## 4. Resume cheaply

A peer that already possesses part of an immutable application representation should request only what remains. A contiguously stored prefix bound to the exact representation identity is preferred where it is cheaper than elaborate range metadata. Compact missing extents may be used when real holes exist. Content-addressed chunking is optional and must justify its overhead.

This is persistent application continuation after a lost session or changed source. It is not generic packet fragmentation and it is not per-frame ARQ.

## 5. Do not retransmit known context

Session-local identifiers, compact integer encodings, negotiated capabilities, and cached metadata should replace repeated long identifiers and descriptive fields whenever safe.

## 6. Separate application representations from carrier packets

An immutable application representation may be compressed and protected as a logical record while BEMPIC exposes persistent application extents for continuation. M4P may independently fragment and reassemble each BEMPIC operation to suit its network path.

BEMPIC extents are not transport blocks. On reliable carriers they are not individually acknowledged or retransmitted by BEMPIC during a healthy session. Their purpose is to avoid restarting a logical application transfer after the prior session/path is gone. Fine-grained selective repair belongs only in an optional unreliable-carrier profile when the layers below BEMPIC do not already provide it.

## 7. Compress before encryption

When compression is appropriate, normalization/deduplication occurs before compression, and compression occurs before encryption. Tiny payloads may be sent uncompressed when compression framing would increase size.

## 8. Security strength is not traded for convenience

Use established cryptographic constructions rather than custom cryptography. Optimize framing, negotiation, session resumption, and metadata rather than weakening algorithms.

## 9. Observable transport is assumed

Radio and other shared media may be passively recorded by anyone in range. Sensitive application metadata should be protected along with payload content whenever legal and technically possible.

## 10. Transport law and capability matter

Some transports or jurisdictions may prohibit encrypted amateur-radio traffic or impose other restrictions. Security modes therefore belong to negotiated transport/security profiles; applications must not assume every transport permits confidentiality.

## 11. Integrity and confidentiality are distinct

Unencrypted data may still require authentication or integrity protection. Public broadcast, authenticated-public, and confidential modes may have different overhead and policy profiles.

## 12. Existing layers should be reused

BEMPIC should integrate with existing radio modems, satellite links, TCP/IP, serial transports, compression libraries, and established cryptography instead of replacing mature technology without measurable benefit.

## 13. Messaging first, extensible later

BEMPIC is being developed first to support OceanMail and highly efficient email/messaging. The protocol should avoid unnecessary assumptions that would prevent later expansion, but general-purpose file synchronization, telemetry, forms, commands, or arbitrary application data are not initial requirements. Future expansion may be undertaken by OceanMail or independent implementers through compatible extensions or later protocol versions.

## 14. Extensions must degrade cleanly

Peers should be able to negotiate capabilities without large exchanges. Unknown optional extensions must not prevent core interoperability.

## 15. Optimize empirically

A protocol simulator and byte-accounting test suite should compare candidate encodings, application extent sizes, resume summaries, compression modes, security overhead, batching, resumability schemes, and metering accuracy under realistic carrier loss and throughput conditions before the wire format is frozen.

Carrier and link retransmission costs should be measured when exposed, but BEMPIC must not implement a competing RF/link retransmission system merely to optimize the measurement.
