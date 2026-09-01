# BEMPIC v0.1 Security Considerations

## Security status

The v0.1 semantic core provides exact-length, SHA-256 content-integrity, and
representation-identity checks. It does **not** by itself provide origin
authentication, confidentiality, authorization, non-repudiation, traffic-flow
confidentiality, or replay protection against an active attacker.

[REQ-SEC-001] The transitional Python proof is cleartext experimental software and MUST NOT
carry real private user traffic. A deployment MUST describe its application
security profile and lower-layer assumptions truthfully.

## Threat model

A carrier may be monitored, recorded, replayed, delayed, duplicated, reordered,
truncated, modified, injected, or impersonated. An attacker may advertise large
lengths or counts, trigger decompression work, collide local short references,
repeat old receipts, manipulate negotiation, exhaust storage, and interrupt
every commit boundary. Radio observation may also reveal timing, duration,
frequency, approximate volume, participants, and physical location even when
payloads are encrypted.

M4P routing or DataLink encryption does not automatically establish end-to-end
BEMPIC identity. Conversely, BEMPIC application protection does not conceal
link metadata needed below it.

## Security classes

Capability negotiation names exactly one applicable class for an exchange:

- **Public:** content is intentionally readable. SHA-256 detects accidental or
  non-adversarial corruption but does not authenticate origin.
- **Authenticated public:** content may be readable; a separately registered
  profile authenticates origin, integrity, freshness, and downgrade state.
- **Confidential:** a separately registered profile authenticates and encrypts
  content and sensitive application metadata.

[REQ-SEC-002] An implementation MUST NOT claim authenticated or confidential behavior unless
the negotiated profile defines keys, algorithms, nonces, replay windows,
protected associated data, failure behavior, and test vectors. Failing to find
an acceptable class is an incompatibility; silent downgrade is forbidden.

## Mandatory core defenses

- Enforce all lengths, counts, offsets, decoded sizes, and nesting bounds before
  allocation or durable mutation.
- Check integer addition and conversion for overflow.
- Reject ambiguous, non-canonical, trailing, truncated, and unknown-critical
  input.
- Bind schema fingerprint, codec, parameters, exact length, and content digest
  into every representation ID.
- Compare digests and authentication values in constant time where practical.
- Treat a conflicting duplicate as an attack or corruption, never as progress.
- Keep staged bytes uncommitted until exact length, digest, ID, schema, and
  decoding checks succeed.
- Make positive receipts durable and idempotent; never infer them from carrier
  delivery.
- Bound retries, diagnostic output, offer pages, partial-object storage, and
  capability caches.
- Isolate failures so one hostile object cannot corrupt unrelated committed
  state.

## Compression and decompression

Compression precedes encryption. A codec profile states exact compressor
version/parameters, maximum encoded and decoded sizes, memory/CPU limits, and
whether attacker-controlled and secret fields may share a context. Profiles
SHOULD separate such contexts or disable compression to mitigate compression
side channels.

[REQ-SEC-003] A decoder MUST cap output independently of the compressed input length and
abort before exceeding its declared decoded maximum. Compression is selected
only when total encoded exchange cost, including framing and parameters, is no
larger than the selected uncompressed alternative unless the application
explicitly accepts a documented tradeoff.

## Identifiers and privacy

Content-derived representation IDs reveal equality for identical schema,
codec, parameters, length, and bytes. Applications that consider equality
sensitive need a confidential profile that protects descriptors or a later
privacy-preserving identifier extension. Object IDs are application-assigned
and must not embed personal data.

Short session-local references, if defined by a codec extension, must be bound
to full identifiers and the compatibility/security context. Conflicting reuse
fails closed.

## Replay and receipts

Core idempotency makes benign duplicates safe but does not prove freshness.
Authenticated/confidential profiles must bind protocol generation, schema,
codec, extension set, operation type, full subject IDs, budget ID, direction,
and a replay epoch/counter into protected associated data. Replay state must
survive process restart for at least the profile's acceptance window.

Application delivery receipts can expose communication relationships and
timing. Profiles should protect them at the same level as the object and
minimize diagnostic detail.

## Persistence and local compromise

Crash-safe state may contain private messages, metadata, partial plaintext,
keys, receipts, and equality-revealing digests. Implementations should use
platform-appropriate access control, encryption at rest where required, secure
key storage, bounded retention, and explicit deletion policy. BEMPIC does not
claim protection after endpoint compromise.

After reopen, persisted metadata and completed files are untrusted input and
must be revalidated. A stored `COMMITTED` flag without recoverable matching
bytes is a storage failure, not a receipt basis.

## Denial of service

Peers should authenticate before expensive work when a profile permits it.
Regardless, implementations enforce negotiated/local ceilings for operations,
collections, representations, partial bytes, concurrent objects, codecs,
decompression, CPU, retries, and diagnostics. An offer is never authority to
reserve its advertised size indefinitely.

## Transport law and policy

Some radio services or jurisdictions restrict communications encoded to
obscure meaning. BEMPIC cannot determine legal use. Carrier/application profiles
must expose restrictions, and applications must select a legally permitted
class. They must never display a confidentiality claim that the negotiated path
does not provide.

## Requirements before a production security profile

A profile requires public algorithm and key-management review; downgrade and
replay rules; nonce construction and crash behavior; metadata coverage;
fragment/retransmission interaction; byte overhead; regulatory description;
known-answer, tamper, replay, rollback, and restart vectors; and independent
interoperability evidence. Novel cryptographic primitives are prohibited.
