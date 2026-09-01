# BEMPIC

BEMPIC is an open protocol for extreme-efficiency, interruption-tolerant
application synchronization across severely bandwidth-constrained,
high-latency, expensive, metered, and intermittently connected networks.
OceanMail is its first production application; BEMPIC remains service-neutral
and independently implementable.

## Status

**v0.1.0 release candidate — not released or tagged.**

[`SPECIFICATION.md`](SPECIFICATION.md) is the normative semantic specification.
It defines exact behavior while intentionally leaving the final stable wire
codec open to measured implementation work. The generation-0 bytes in
`prototype/` are non-normative.

Do not claim a v0.1.0 release until every gate in
[`docs/ROADMAP-v0.1.0.md`](docs/ROADMAP-v0.1.0.md) passes, including the required
work in the sibling `bempic-reference` repository.

## Architecture

```text
OceanMail  ->  BEMPIC  ->  M4P  ->  DataLink adapters
```

- OceanMail owns application and service policy.
- BEMPIC owns compact application objects, synchronization, persistent
  cross-contact resume, exact integrity, semantic receipts, and byte budgets.
- M4P owns routing, addressing, mesh coordination, forwarding,
  store-carry-forward, generic fragmentation, network deduplication, network
  TTL, cross-modality behavior, and DataLink abstraction.
- DataLink adapters/modems own link framing, FEC, ARQ, retransmission,
  modulation, and hardware behavior.

BEMPIC does not duplicate M4P or modem reliability. Its persistent byte prefix
allows an immutable application representation to continue after a prior
contact, path, peer, process, or carrier is gone.

## v0.1 core

The release candidate specifies:

- bounded immutable messages, parts, and independently selectable
  representations;
- deterministic preparation, schema fingerprints, exact sizes, full content
  digests, and representation IDs;
- append-oriented collection summaries, delta offers, and bounded full
  reconciliation;
- explicit requests, hard total/directional BEMPIC-byte budgets, and exact
  accounting domains;
- offset data transfer, crash-safe persistence, reopen/resume, integrity
  verification, exact reconstruction, and idempotent receipts;
- version, schema, codec, extension, capability, and failure behavior; and
- pluggable codec requirements including declarative bounds and precision,
  mandatory maximum encoded sizes, exact-size analysis, and byte vectors.

DCCL is useful prior art for codec discipline only. BEMPIC does not depend on
DCCL, adopt its wire format or encryption, require C++, or require Protobuf.

## Repository map

- [Specification](SPECIFICATION.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Scope summary](docs/SCOPE.md)
- [Repository boundary](docs/REPOSITORY-BOUNDARY.md)
- [Design principles](docs/DESIGN-PRINCIPLES.md)
- [Security considerations](docs/SECURITY-MODEL.md)
- [Conformance checklist](docs/CONFORMANCE.md)
- [Normative requirement-to-evidence matrix](docs/CONFORMANCE-MATRIX.md)
- [Test-vector definitions](docs/TEST-VECTORS.md)
- [Machine-readable V01–V15 catalog](conformance/v0.1/vector-catalog.json)
- [Protocol registries](docs/REGISTRIES.md)
- [Required metrics](docs/METRICS.md)
- [M4P confirmation requirement](docs/M4P-CONFIRMATION.md)
- [Release-record requirements](docs/RELEASE-RECORD.md)
- [Canonical schema descriptors](schemas/README.md)
- [v0.1.0 roadmap and tag gates](docs/ROADMAP-v0.1.0.md)
- [Draft v0.1.0 release notes](docs/RELEASE-NOTES-v0.1.0.md)
- [Decision index](docs/DECISIONS.md)
- [Prior art and boundaries](docs/PRIOR-ART-AND-BOUNDARIES.md)
- [Initial planning rationale](docs/INITIAL-PROTOCOL-PLAN.md)
- [Great Parallel Work register](GREAT_PARALLEL_WORK.md)
- [Governance](GOVERNANCE.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [Transitional Python proof](prototype/README.md)

## Reference implementation boundary

This repository owns the specification, governance, conformance requirements,
test-vector definitions, and rationale. Executable reference work belongs in
the sibling `bempic-reference` repository. Do not add new reference
implementation code here.

The existing Python prototype is retained until behavioral parity exists in the
sibling. It remains useful as an independent transitional oracle but is neither
the reference implementation nor compatibility authority.

## Verification

```bash
python -m pip install --require-hashes -r requirements-validation.txt
python -m scripts.validate_docs
python -m scripts.validate_release_gates
node scripts/independent_verify.mjs
python -m unittest prototype.tests.test_proof -v
python -m prototype.demo
python -m prototype.benchmark
```

## License

Copyright 2026 Gordonfive and BEMPIC contributors. Licensed under the
[Apache License 2.0](LICENSE); see [`NOTICE`](NOTICE).
