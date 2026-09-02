# BEMPIC

BEMPIC is an open protocol research project for extreme-efficiency, interruption-tolerant application synchronization across severely bandwidth-constrained, high-latency, expensive, metered, and intermittently connected networks.

## Status

**Development frozen/halted as of 2026-09-02.**

**v0.1.0 release candidate — not released or tagged.**

BEMPIC is not abandoned, but it is no longer on OceanMail's mandatory implementation path. OceanMail 0.2 is establishing a real HERMES-derived baseline first. BEMPIC development may resume only after direct comparative testing against the HERMES `UUCP + uuxcomp` baseline under the same constrained-link/modem conditions demonstrates material value worth the additional protocol and maintenance burden.

See [the freeze decision](docs/FROZEN-2026-09-02.md). The exact pre-freeze generation is preserved at `archive/v0.1-generation`.

[`SPECIFICATION.md`](SPECIFICATION.md) remains the normative semantic specification for the frozen research state. It defines exact behavior while intentionally leaving the final stable wire codec open. Provisional experimental profile `bempic-compact-operation-v0.1` is allocated as `0x00010000/1`; it is neither approved nor mandatory and is not a stable-wire or production-security promise. The generation-0 bytes in `prototype/` are non-normative.

Do not claim a v0.1.0 release or conformance state while the project is frozen. The existing release gates remain historical/technical evidence, not an active instruction to continue implementation.

## Historical architecture context

BEMPIC was designed in the OceanMail 0.1 generation for this intended stack:

```text
OceanMail  ->  BEMPIC  ->  M4P  ->  DataLink adapters
```

That stack is no longer OceanMail's active critical path. OceanMail 0.2 has moved to an upstream-first HERMES/Mercury direction, with BEMPIC and M4P retained as optional future research.

Within its own specification boundary:

- BEMPIC owns compact application objects, synchronization, persistent cross-contact resume, exact integrity, semantic receipts, and byte budgets.
- It does not own generic routing/mesh behavior or modem/link reliability.
- Its persistent byte-prefix concept is intended to allow an immutable application representation to continue after a prior contact, path, peer, process, or carrier is gone.

Those ideas remain candidates for later comparison against the proven HERMES baseline.

## v0.1 research core

The frozen release candidate specifies:

- bounded immutable messages, parts, and independently selectable representations;
- deterministic preparation, schema fingerprints, exact sizes, full content digests, and representation IDs;
- append-oriented collection summaries, delta offers, and bounded full reconciliation;
- explicit requests, hard total/directional BEMPIC-byte budgets, and exact accounting domains;
- offset data transfer, crash-safe persistence, reopen/resume, integrity verification, exact reconstruction, and idempotent receipts;
- version, schema, codec, extension, capability, and failure behavior; and
- pluggable codec requirements including declarative bounds and precision, mandatory maximum encoded sizes, exact-size analysis, and byte vectors.

DCCL is useful prior art for codec discipline only. BEMPIC does not depend on DCCL, adopt its wire format or encryption, require C++, or require Protobuf.

## Repository map

- [Freeze decision](docs/FROZEN-2026-09-02.md)
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
- [Experimental compact codec profile](docs/codecs/EXPERIMENTAL-COMPACT-v0.1.md)
- [Experimental allocation evidence](conformance/v0.1/experimental-codec-allocation.json)
- [Required metrics](docs/METRICS.md)
- [B2F/LZHUF oracle decision and comparison profile](docs/B2F-ORACLE.md)
- [M4P confirmation requirement](docs/M4P-CONFIRMATION.md)
- [Release-record requirements](docs/RELEASE-RECORD.md)
- [Canonical schema descriptors](schemas/README.md)
- [v0.1.0 roadmap and tag gates](docs/ROADMAP-v0.1.0.md) — frozen roadmap evidence
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

The sibling `bempic-reference` repository contains the experimental reference implementation, simulator, fixtures, and conformance evidence. It is frozen under the same program decision.

The existing Python prototype is retained as independent transitional evidence but is neither a stable reference implementation nor compatibility authority.

## Verification

Verification commands remain useful for preserving the frozen state and reproducing its evidence:

```bash
python -m pip install --require-hashes -r requirements-validation.txt
python -m scripts.validate_docs
python -m scripts.validate_release_gates
node scripts/independent_verify.mjs
python -m unittest prototype.tests.test_proof -v
python -m prototype.demo
python -m prototype.benchmark
```

Passing these checks does not lift the freeze or create a v0.1.0 release.

## License

Copyright 2026 Gordonfive and BEMPIC contributors. Licensed under the [Apache License 2.0](LICENSE); see [`NOTICE`](NOTICE).
