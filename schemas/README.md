# BEMPIC Schema Descriptors

These JSON files describe bounded v0.1 semantic values. They are fingerprint
inputs, not a constrained-carrier JSON wire format and not executable reference
code.

To calculate a fingerprint, parse a descriptor, serialize it as RFC 8785
canonical JSON UTF-8 bytes `S`, and apply the construction in Specification
Section 6. Exact expected values are in
[`v0.1/fingerprints.json`](v0.1/fingerprints.json).

| Descriptor | SHA-256 schema fingerprint |
|---|---|
| [`core-operations.schema.json`](v0.1/core-operations.schema.json) | `a9479fc4fc1770a0385abbe3a351e9b517c00e135f74f82b11f7113281fb14b0` |
| [`message-manifest.schema.json`](v0.1/message-manifest.schema.json) | `0ac001efba42837aade054401d9d307d16ad4715feac288fcb3d1711e4b961da` |
| [`opaque-binary.schema.json`](v0.1/opaque-binary.schema.json) | `d8906a1cefbf89e4f29b4a0f636cfbfa1e9c6301e7e3a4fe213c090066f8e797` |

Changing a descriptor changes its fingerprint and requires compatibility,
registry, conformance, vector, and changelog review.
