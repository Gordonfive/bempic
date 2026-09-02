# BEMPIC Open Questions

This register contains only decisions not settled by the v0.1 semantic
specification. Items marked **release-blocking** must be resolved or explicitly
deferred by an accepted decision before `v0.1.0` is tagged.

## Release-blocking

- **Experimental codec release evidence:** Provisional experimental tuple
  `0x00010000/1` is allocated to `bempic-compact-operation-v0.1`, derived from
  Reference private candidate `0xffff0001/2`. Which exact public-tuple vector
  bundle and independently owned verification will complete the v0.1
  interoperability evidence? The allocation is not approval, mandatory status,
  or a stable-wire promise.
- **Independent verifier:** Which implementation, language, and ownership will
  provide decoder/vector independence from the primary reference codec?
- **B2F oracle:** The legal/technical audit in
  [`B2F-ORACLE.md`](B2F-ORACLE.md) selected no current candidate. Which next
  package will provide the prescribed synthetic corpus, immutable standalone
  executable, exact ARSFI-compatible output and 250-octet B2F envelope,
  process/link/redistribution/CI license review, and independent reproduction?
- **M4P binding review:** What exact opaque-record API, maximum-opportunity,
  persistence, duplicate, and cost-reporting guarantees will the first binding
  consume? The external record must satisfy
  [`M4P-CONFIRMATION.md`](M4P-CONFIRMATION.md); it must be coordinated upstream,
  not invented here.
- **Protocol name:** Keep `BEMPIC` without an expansion, or adopt a durable
  expansion? The acronym's expansion has no wire consequence.

An item is resolved only by an accepted decision linked from the v0.1 release
record. The minimum decision evidence is:

| Blocker | Evidence required to resolve it |
|---|---|
| Experimental codec release evidence | Regenerated `0x00010000/1` vector bundle, compatibility/security/license review, independent verification, and governance acceptance; private-tuple artifacts are allocation provenance only |
| Independent verifier | Independently maintained source commit, owner, implementation language, toolchain/dependencies, vector-bundle digest, byte/failure comparison, and green CI |
| B2F oracle | Every item in the `REQ-B2F-005` next package: exact executable/source/build identity and digest, mode-specific license/notices, prescribed corpus digest, ARSFI byte equality, 250-octet transcript, two-platform and independent reproduction, and raw exact-rational results |
| M4P binding review | The external confirmation and traces required by [`M4P-CONFIRMATION.md`](M4P-CONFIRMATION.md) |
| Protocol name | Governance decision selecting the durable display name/expansion and updating public documents consistently; no schema, negotiation, or byte change is implied |

A decision that merely postpones a blocker can satisfy the release only if it
explicitly changes v0.1 scope through governance and reconciles the roadmap,
conformance matrix, release record, compatibility impact, and release notes.
Silence, an implementation default, or a chat statement is not resolution.

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
- Codec ID ranges, status transitions, approval evidence, and worst-case-proof
  rules are defined; provisional experimental tuple `0x00010000/1` is allocated
  to `bempic-compact-operation-v0.1`, while approval and public-tuple release
  evidence remain open.
- OceanMail's immutable application profile and accepted ADR at
  [`cc55c1b7d5a03aa2e5cc8cd617f9d1bb7b6a3600`](https://github.com/Gordonfive/oceanmail/commit/cc55c1b7d5a03aa2e5cc8cd617f9d1bb7b6a3600)
  define a 32-octet CSPRNG object identifier, durable no-reuse binding, and
  metadata-conflict behavior. BEMPIC continues to treat the value as opaque;
  V11 cross-repository conformance evidence is still pending.
- Required metrics and V01–V15 semantic cases are defined; their release
  evidence is not yet available.
- DCCL is prior art only, with no dependency, wire, crypto, C++, or Protobuf
  adoption.
- The public specification remains here; executable reference work belongs in
  `bempic-reference`; the Python proof remains transitional pending parity.
