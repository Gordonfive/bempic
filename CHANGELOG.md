# Changelog

This project follows semantic versioning for specification releases. During
major version zero, minor protocol generations may be incompatible. Patch
releases correct or clarify without intentionally changing protocol semantics.

## [Unreleased]

### Added

- Apache-2.0 license and project notice.
- Normative v0.1 semantic specification with exact scope, bounds, terminology,
  identifiers, states, invariants, operations, persistence, failure,
  accounting, versioning, schema, codec, and extension rules.
- Architecture and repository-boundary documents preserving OceanMail → BEMPIC
  → M4P → DataLink ownership.
- Governance, contribution, decision-record, conformance, test-vector,
  security, roadmap, and draft release-note material.
- Explicit `bempic-reference` completion and parity gates for v0.1.0.
- Documentation link and consistency validation.
- A governed codec-ID allocation process with approved, experimental,
  private-use, and reserved ranges; approval/mandatory evidence; and explicit
  maximum-size and worst-case-proof requirements.
- A machine-checkable V01–V15 semantic vector catalog, required metric catalog,
  M4P confirmation contract, release-record template, and normative
  requirement-to-evidence conformance matrix.
- CI validation for release-gate artifacts and an explicit not-ready release
  state retaining all unresolved blockers.

### Changed

- Defined codec-independent directional `semantic_bytes`, including exact
  scalar accounting, inclusion/exclusion, aggregation, and fixture evidence;
  replaced ambiguous independent V08 axis coverage with a fixed 24-row
  pairwise interruption/restart/storage covering array and exact pass/fail
  evidence, without changing any release threshold.
- Recorded the latest immutable `bempic-reference` conformance checkpoint as
  prior `blocked-not-conformant` evidence while retaining all incomplete gates.
- Replaced Python-specific JSON serialization in schema-fingerprint validation
  with genuine RFC 8785/JCS canonicalization and RFC-derived regression
  fixtures.
- Expanded the fingerprinted `REPRESENTATION_DATA` selection into an explicit
  bounded record and advanced the unreleased core-operations schema to revision
  2.
- Reclassified the Python proof as a retained transitional oracle rather than a
  future reference implementation or compatibility authority.
- Reconciled initial planning and Great Parallel Work with the sibling reference
  repository and semantic-before-wire design.
- Classified DCCL as prior art only and adopted no DCCL dependency or format.

### Not released

- No `v0.1.0` tag has been created. The remaining gates are tracked in
  [`docs/ROADMAP-v0.1.0.md`](docs/ROADMAP-v0.1.0.md).

## [0.1.0] - Unreleased

Reserved for the first public BEMPIC semantic specification. This heading will
receive a release date only after all gates pass.
