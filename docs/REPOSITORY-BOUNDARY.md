# Repository Boundary

## This repository: `bempic`

This Git repository is authoritative for:

- the public BEMPIC specification and terminology;
- architecture and layer ownership;
- protocol states, invariants, operations, failure behavior, and persistence
  requirements;
- schema, codec, extension, compatibility, and registry rules;
- conformance requirements and test-vector definitions;
- security considerations and deployment claims;
- governance, contribution rules, decisions, rationale, roadmap, changelog,
  and release notes; and
- the transitional Python semantic prototype until behavioral parity exists in
  `bempic-reference`.

Normative text uses explicit requirement language. Historical planning and the
prototype may illustrate behavior but cannot override
[`SPECIFICATION.md`](../SPECIFICATION.md).

## Sibling repository: `bempic-reference`

The sibling repository owns executable reference-implementation work:

- production-language model, state machine, codecs, persistence adapters, and
  carrier traits;
- deterministic simulator, fixtures, benchmark executables, fuzz/property
  tests, and vector runners;
- M4P binding implementation and non-normative local adapters; and
- published machine-readable implementation and benchmark results.

The specification repository defines the vector contract and conformance
outcome; the reference repository executes it. Changes to the sibling require a
separate review and are never made indirectly from this repository.

## Transitional Python prototype

`prototype/` predates the repository split. It is retained in place as a
non-normative semantic and measurement oracle. [REQ-REPO-001] It MUST NOT be deleted, moved,
or described as the reference implementation until `bempic-reference` passes
the behavioral-parity gate in [`ROADMAP-v0.1.0.md`](ROADMAP-v0.1.0.md).

Parity means the sibling implementation reproduces the required semantic
behaviors and published metrics or documents an approved normative difference;
it does not mean preserving the prototype's disposable bytes, 16-byte IDs,
generation-0 markers, local cursor, or clone-and-execute quotation technique.

## Other owners

- **OceanMail:** product/service policy, normalization and transformations,
  external mail-service integration, gateway and relay policy, UI, billing,
  quotas, and user decisions.
- **M4P:** routing, addressing, mesh coordination, store-carry-forward,
  forwarding, generic fragmentation/reassembly, network deduplication, network
  TTL, cross-modality behavior, and DataLink abstraction.
- **DataLink/modem projects:** link framing, modulation, FEC, ARQ,
  retransmission, RF scheduling, and hardware control.

## Change test

Before accepting work here, ask:

1. Does it define public BEMPIC semantics or the evidence required to conform?
   If yes, it belongs here.
2. Is it executable reference behavior, a codec implementation, simulator, or
   integration adapter? If yes, it belongs in `bempic-reference` after the
   specification requirement is recorded here.
3. Is it routing, mesh, forwarding, generic network reliability, or DataLink
   behavior? If yes, it belongs in M4P or the DataLink project.
4. Is it OceanMail policy or product code? If yes, it belongs in OceanMail.
