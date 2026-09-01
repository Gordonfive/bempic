# BEMPIC v0.1 Registries

Registries prevent independently upgraded implementations from assigning the
same identifier to different behavior. Allocations are governed by
[`../GOVERNANCE.md`](../GOVERNANCE.md). This file records semantic allocations;
a codec may have a separate table for its compact wire tags.

## Protocol generations

| Major | Minor | Status | Specification |
|---:|---:|---|---|
| 0 | 1 | Release candidate, not tagged | [`../SPECIFICATION.md`](../SPECIFICATION.md) |

Patch versions identify document releases and are not negotiated.

## Core operation names

`CAPABILITIES`, `SUMMARY`, `OFFER`, `REQUEST`, `DATA`, `RECEIPT`, and `FAILURE`
are reserved core semantic names for generation 0.1. Their wire tags are
codec-profile assignments and are not allocated here.

## Core receipt statuses

`REPRESENTATION_COMMITTED`, `APPLICATION_ACCEPTED`, `APPLICATION_DELIVERED`, and
`APPLICATION_REJECTED` have the exact meanings in Specification Section 8.6.

## Core failure codes

The reserved names are `UNSUPPORTED_VERSION`, `UNSUPPORTED_SCHEMA`,
`UNSUPPORTED_CODEC`, `UNSUPPORTED_CRITICAL_EXTENSION`, `MALFORMED_OPERATION`,
`LIMIT_EXCEEDED`, `UNKNOWN_OBJECT`, `METADATA_CONFLICT`, `RANGE_INVALID`,
`INTEGRITY_FAILURE`, `STORAGE_FAILURE`, `POLICY_REJECTED`, and
`CHECKPOINT_UNKNOWN`.

## Schema fingerprints

The canonical descriptors and calculation instructions are in
[`../schemas/README.md`](../schemas/README.md). The prototype's `BMSG0` marker is
explicitly not an allocation.

| Fingerprint | Name | Status |
|---|---|---|
| `c4a686e7e9c6a40a5f187259a376b26cfc1d355179fd9fff487e105aeeac7302` | `bempic.core-operations`, revision 2 | v0.1 release candidate |
| `0ac001efba42837aade054401d9d307d16ad4715feac288fcb3d1711e4b961da` | `bempic.message-manifest`, revision 1 | v0.1 release candidate |
| `d8906a1cefbf89e4f29b4a0f636cfbfa1e9c6301e7e3a4fe213c090066f8e797` | `bempic.opaque-binary`, revision 1 | v0.1 release candidate |

## Codec IDs and revisions

No codec is approved yet. [REQ-REG-001] The Python generation-0 encoding has no codec ID and
MUST NOT be advertised as a v0.1 profile.

Codec IDs are unsigned 32-bit integers. Revisions are unsigned 32-bit integers
from 1 through `4,294,967,295`; revision zero is invalid. Compatibility is
defined by the exact `(codec_id, revision)` pair. A new revision is required
whenever any accepted byte sequence, emitted byte sequence, canonical parameter,
size result, or failure outcome changes.

| Inclusive codec-ID range | Class | Allocation rule |
|---|---|---|
| `0x00000000` | Reserved | Invalid/unset; never negotiated |
| `0x00000001`–`0x0000ffff` | Standards action | Maintainer allocation after approved-profile evidence |
| `0x00010000`–`0x7fffffff` | Experimental | Reviewed provisional allocation through a pull request |
| `0x80000000`–`0xfffffffe` | Private use | Local or coordinated experiments; never public conformance or release evidence |
| `0xffffffff` | Reserved | Future sentinel; never negotiated |

[REQ-REG-002] A sender MUST NOT emit reserved codec IDs, revision zero, or a
private-use ID as public interoperability evidence. A receiver MUST reject those
values with `UNSUPPORTED_CODEC` before protocol-state mutation. Private-use IDs
are a shared collision space, not vendor-owned allocations, and therefore may be
used only where every participant is configured out of band.

The authoritative machine-readable range table is
[`../conformance/v0.1/codec-registry.json`](../conformance/v0.1/codec-registry.json).
The table contains no codec allocation: the v0.1 experimental codec selection
is still release-blocking.

### Status progression

The statuses are `experimental`, `approved`, `mandatory`, `deprecated`, and
`reserved`. `Approved` means suitable for claimed interoperability under its
published profile; it does not mean mandatory-to-implement. `Mandatory` means
every conformer in the named protocol generation/profile implements it. An
experimental-range ID is never promoted in place: approval assigns an ID from
the standards-action range, and the experimental ID is retained with its old
meaning and normally marked deprecated. This avoids making experimental bytes
silently stable.

[REQ-REG-003] An experimental allocation request MUST provide a stable name and
owner/contact, the proposed exact ID and initial revision, a public profile,
canonical parameters, field and collection bounds, maximum-encoded-size tables,
a draft worst-case proof, draft valid and invalid vectors, security and license
analysis, and a registry collision check. The allocation pull request MUST state
that the bytes are experimental and may be replaced by a new ID or revision.

[REQ-REG-004] Approval requires all experimental evidence plus a complete
normative profile; exact-size functions; completed worst-case proofs and witness
vectors; all mandatory semantic and codec-boundary vectors; strict decoder,
fuzz, and property-test results with no unresolved correctness or memory-safety
finding; reproducible results from an independent decoder or verifier; license
notices; compatibility analysis; and an accepted governance decision. Every
artifact MUST identify immutable source commits and tool versions. An approved
allocation MUST use the standards-action range and MUST state whether it is
byte-identical to a named experimental revision or is a new revision/profile.

[REQ-REG-005] Mandatory-to-implement status additionally requires prior
approval, two independently maintained interoperable implementations, evidence
that the codec meets the release compactness and operational metrics, migration
and downgrade analysis, an accepted normative change, and maintainer approval.
The decision MUST name the protocol generation or application profile for which
the requirement applies. No codec has this status for v0.1.

Deprecation prevents new negotiation preference but does not reassign the ID or
revision. Released ID/revision meanings are permanent.

### Maximum encoded size and worst-case proof

[REQ-REG-006] Every codec revision MUST publish a finite maximum encoded size
for each core operation variant, every supported schema value, each extension
envelope, and the complete outer record. Each maximum MUST include tags,
presence indicators, lengths, counts, padding, canonical parameters, and every
codec-owned transform or compression expansion. Security- or carrier-owned
overhead is reported separately and MUST NOT be silently included in BEMPIC
bytes.

[REQ-REG-007] For every published maximum, the profile MUST publish a closed
formula or machine-checked derivation over the normative field bounds, identify
every assumption, and provide a semantic witness whose canonical encoding
reaches that maximum. If a mathematical maximum is unreachable because of a
cross-field invariant, the proof MUST state the tighter reachable domain and
give a witness for it. The proof artifact MUST record the profile digest,
implementation commit, tool versions, exact encoded length, byte digest, and
the result of independent verification.

[REQ-REG-008] An encoder MUST compute exact encoded size without trial
serialization or allocation proportional to the encoded object. Boundary tests
MUST show equality between the exact-size result and actual encoded length for
every mandatory vector and generated boundary case. A decoder MUST reject an
outer record, field, collection, nesting depth, or decoded transform that
exceeds its declared maximum before allocating or mutating durable protocol
state.

[REQ-REG-009] A codec profile MUST include, for each maximum, the reaching
witness, one-past-bound invalid inputs where the semantic domain permits them,
malformed/truncated length cases, and a property or exhaustive-domain test that
no accepted value exceeds the declared maximum. An approved profile MUST have
the proof and witness reproduced by an implementation independent of the
primary encoder.

## Extension IDs

No extension is required or allocated by v0.1 core. Experimental work must use
a reviewed provisional allocation before exchanging bytes between independent
implementations; an implementation-local number is not an interoperability
claim.

## Security profile IDs

No authenticated-public or confidential profile is allocated. “Public” names
the absence of an application-protection claim, not a cryptographic suite.

## Allocation request

A pull request requesting an allocation includes a stable name, owner/contact,
status, complete specification, bounds, compatibility and security analysis,
conformance/vector changes, and collision check. Codec and schema requests also
include maximum/exact encoded-size analysis and canonical artifacts. Provisional
allocations may be withdrawn before a release; released meanings are never
reassigned. [REQ-REG-010] The pull request MUST update the Markdown registry,
the machine-readable registry, conformance matrix, vectors, and changelog in one
reviewed change; CI MUST prove that the ranges remain non-overlapping and that
no released allocation changed meaning.
