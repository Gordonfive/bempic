# BEMPIC Open Questions

This register contains only decisions not settled by the v0.1 semantic
specification. Items marked **release-blocking** must be resolved or explicitly
deferred by an accepted decision before `v0.1.0` is tagged.

## Release-blocking

- **Experimental codec selection:** Which candidate codec ID/revision will
  provide the v0.1 interoperability evidence while remaining explicitly
  non-stable?
- **Independent verifier:** Which implementation, language, and ownership will
  provide decoder/vector independence from the primary reference codec?
- **B2F oracle:** Which licensed implementation and version will produce the
  reproducible B2F/LZHUF comparison, and what notices are required?
- **M4P binding review:** What exact opaque-record API, maximum-opportunity,
  persistence, duplicate, and cost-reporting guarantees will the first binding
  consume? This must be coordinated upstream, not invented here.
- **Object-ID application profile:** What collision-resistant generation rule
  will the OceanMail application profile require for the core's 32-octet opaque
  object ID?
- **Protocol name:** Keep `BEMPIC` without an expansion, or adopt a durable
  expansion? The acronym's expansion has no wire consequence.

## Deliberately deferred beyond v0.1

- Missing-extent or selective-range resume extension.
- Unreliable/broadcast carrier recovery and its ownership boundary with M4P.
- Mutable mailbox state, deletion, read/unread, folders, labels, edits, and
  multi-writer conflict semantics.
- Delta representations and cross-object content deduplication policy.
- Standard compression codecs and static dictionaries.
- Authenticated-public and confidential cryptographic profiles, identity/key
  enrollment, replay epochs, revocation, and regulatory profiles.
- Provider/service envelopes for external delivery intent.
- Direct byte-stream binding for non-M4P deployments.
- IETF or another formal standards-track publication path.

Deferred items are not permission for an implementation to assign conflicting
core meanings. Experimental work uses registered extensions or later protocol
generations.

## Resolved for v0.1

- Architecture is OceanMail → BEMPIC → M4P → DataLink adapters.
- BEMPIC does not own routing, forwarding, mesh, generic fragmentation,
  network TTL, generic deduplication, or modem reliability.
- The core uses deterministic prepared representations and a durable contiguous
  prefix; missing ranges are deferred.
- Full 32-octet SHA-256 schema fingerprints, content digests, and
  representation IDs are specified.
- Canonical v0.1 core-operation, message-manifest, and opaque-binary schema
  descriptors and their exact fingerprints are published.
- Operation, schema, field, count, and resource bounds are mandatory.
- Protocol/schema/codec/extension negotiation and unknown-extension behavior
  are specified.
- Codecs are pluggable and must publish maximum and exact encoded-size analysis.
- DCCL is prior art only, with no dependency, wire, crypto, C++, or Protobuf
  adoption.
- The public specification remains here; executable reference work belongs in
  `bempic-reference`; the Python proof remains transitional pending parity.
