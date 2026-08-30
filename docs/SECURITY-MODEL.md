# BEMPIC Security Model

## Threat assumption

BEMPIC assumes that a transport may be passively monitored, recorded, replayed, modified, or impersonated. This is especially important for radio transports, where reception may require no physical access to either endpoint.

Encryption does not conceal the existence of a transmission, its approximate duration, radio characteristics, or necessarily the transmitter's physical location. Those are outside the confidentiality guarantees of the protocol.

## Security classes

The protocol design should support at least three logical classes. Exact wire representation remains undecided.

### Public

Payload is intentionally readable. Appropriate for information intended for unrestricted distribution.

Examples: public bulletins, discovery information, public weather broadcasts.

### Authenticated public

Payload may be readable but should provide cryptographic origin/integrity assurance where the transport and profile permit it.

Examples: trusted public weather products, gateway announcements, signed bulletins.

### Confidential

Payload and sensitive application metadata are encrypted and authenticated.

Examples: personal messages, email contents, private position reports, credentials, files, commands, account data.

For OceanMail, confidential transport should be the default for user content whenever legally permitted by the underlying transport.

## Metadata

Where confidentiality is enabled, sender addresses, recipient addresses, subjects, filenames, coordinates, application object types, and other sensitive metadata should be carried inside the protected payload when practical.

Minimum routing/session information may remain observable. The specification should minimize this exposed information.

## Cryptography

BEMPIC will use established, reviewed cryptographic primitives and libraries. It will not define novel encryption algorithms.

Candidate algorithms and handshake mechanisms must be evaluated for:

- security maturity;
- compact wire overhead;
- suitability for low-power software implementations;
- session resumption;
- resistance to nonce misuse and replay;
- ability to protect stable application representations while M4P or another carrier independently packetizes and retransmits them.

No algorithm is selected by this document.

## Initial proof boundary

The first encode/synchronize/decode proof may run in a clear simulator with a whole-representation integrity digest. That validates identity, resumption, metering, parsing, and state-machine behavior; it does not constitute an authenticated or confidential deployment profile.

Real user traffic must not rely on the experimental proof as a security protocol. Clear/monitorable, authenticated-public, and confidential profiles need explicit capabilities, downgrade behavior, replay rules, test vectors, and measured byte overhead before they are standardized.

## Compression

Compression, when used with confidential data, occurs before encryption. Implementations must consider compression side channels when attacker-controlled and secret data share a compression context. Profiles may require separate compression contexts or disable compression for particular sensitive data.

## Transport legality

Encryption policy cannot be determined by BEMPIC alone. Amateur-radio services in some jurisdictions restrict messages encoded for the purpose of obscuring their meaning. Marine, commercial, satellite, cellular, and Internet services may operate under different rules.

Transport profiles must therefore expose security capabilities and restrictions. Applications should select the strongest legally permitted profile and must not silently claim confidentiality when a transport prohibits it.

## Open questions

The following remain design decisions:

- identity and key distribution;
- first-contact authentication;
- session key establishment and resumption;
- authentication-tag size and record granularity;
- replay protection across interrupted sessions;
- forward secrecy requirements;
- multi-device identity and revocation;
- public/authenticated/confidential wire signaling;
- regulatory profiles for radio transports.
