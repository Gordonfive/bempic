# BEMPIC v0.1.0 Draft Release Notes

**Release status:** not released

**Tag status:** `v0.1.0` does not exist and must not be created yet

## Intended release

BEMPIC v0.1.0 will be the first public, independently implementable semantic
protocol baseline for extreme-efficiency, interruption-tolerant application
synchronization. It preserves the architecture OceanMail → BEMPIC → M4P →
DataLink adapters and assigns no routing, forwarding, mesh coordination,
generic fragmentation, network TTL, or modem reliability to BEMPIC.

The release defines immutable messaging objects, deterministic preparation,
full-length identifiers and schema fingerprints, append-oriented
reconciliation, bounded offers and requests, explicit selection, exact BEMPIC
budgets, offset data transfer, crash-safe prefix persistence, reopen/resume,
integrity verification, exact reconstruction, receipts, failures, negotiation,
extensions, accounting, and codec-analysis requirements.

The release candidate also defines codec-independent `semantic_bytes`, with a
stable endpoint-role orientation and representation-descriptor exclusion, and
an exact 24-row pairwise interruption/restart/storage covering array so
evidence can be independently reproduced without choosing results after a run.

## Wire-format status

Version 0.1.0 does not freeze a permanent wire codec. It defines how a codec is
registered and proven: declarative bounds and precision, mandatory maximum
encoded sizes, deterministic encoding, exact per-value size analysis, strict
decoding, schema fingerprints, canonical parameters, and byte vectors. DCCL is
prior art only; BEMPIC adopts neither its bytes nor its software dependencies.

Provisional experimental tuple `0x00010000/1` is allocated to
`bempic-compact-operation-v0.1`. It is derived from the Reference private
candidate `0xffff0001/2`, but implementations use the public tuple and
regenerate every ID-bound record and vector. The allocation is neither
approved nor mandatory and provides no stable-wire or production-security
promise.

## Compatibility

The negotiated semantic generation is `0.1`; exact schema fingerprints and
codec ID/revision must also match. Different `0.x` minor generations are
incompatible unless a compatibility profile explicitly supports both. Unknown
optional extensions are skipped; unknown critical extensions fail before state
mutation.

## Known limitations

- Mutable mailbox state and multi-writer conflicts are out of scope.
- The core has contiguous-prefix resume, not missing-range selective repair.
- No production cryptographic suite is standardized.
- No permanent codec or M4P binding is frozen.
- The retained Python proof uses non-normative generation-0 bytes and does not
  implement the complete v0.1 contract.
- The latest immutable `bempic-reference` report is
  [`blocked-not-conformant`](https://github.com/Gordonfive/bempic-reference/blob/cf3485f6606d6462077e8edd1592264c3ce4ca5e/conformance/v0.1.0-report.json),
  predates the clarified semantic-byte and V08 requirements, and binds the
  private candidate rather than allocated public tuple `0x00010000/1`.

## Required release evidence

Before publication, replace these placeholders:

- Specification commit: `PENDING`
- Passing `bempic-reference` commit: `PENDING`
- Conformance report digest: `PENDING`
- Test-vector bundle digest: `PENDING`
- Codec allocation: experimental `0x00010000/1`; public-tuple profile,
  size-proof, vector, license, and independent release evidence: `PENDING`
- V01–V15 and normative conformance-matrix results: `PENDING`
- Required metric-record digest and threshold evaluation: `PENDING`
- B2F oracle decision: `blocked-no-qualified-oracle`; comparison profile and
  source/license audit published, corpus/executable/results: `PENDING`
- Benchmark result digest and selected B2F comparator version: `PENDING`
- M4P boundary review: `PENDING`
- Release CI URL: `PENDING`

The complete gate list is
[`ROADMAP-v0.1.0.md`](ROADMAP-v0.1.0.md), and the immutable record format is in
[`RELEASE-RECORD.md`](RELEASE-RECORD.md). These notes are intentionally a draft
and are not evidence of a release.
