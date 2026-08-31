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
| `a9479fc4fc1770a0385abbe3a351e9b517c00e135f74f82b11f7113281fb14b0` | `bempic.core-operations`, revision 1 | v0.1 release candidate |
| `0ac001efba42837aade054401d9d307d16ad4715feac288fcb3d1711e4b961da` | `bempic.message-manifest`, revision 1 | v0.1 release candidate |
| `d8906a1cefbf89e4f29b4a0f636cfbfa1e9c6301e7e3a4fe213c090066f8e797` | `bempic.opaque-binary`, revision 1 | v0.1 release candidate |

## Codec IDs and revisions

No codec is approved yet. The Python generation-0 encoding has no codec ID and
MUST NOT be advertised as a v0.1 profile.

| Codec ID | Revision | Name | Status |
|---:|---:|---|---|
| — | — | v0.1 experimental interoperability codec | Pending release gate |

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
reassigned.
