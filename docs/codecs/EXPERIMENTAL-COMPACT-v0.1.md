# BEMPIC experimental compact operation codec v0.1

## Allocation and status

| Field | Value |
|---|---|
| Stable name | `bempic-compact-operation-v0.1` |
| Codec ID | `0x00010000` (65,536) |
| Revision | `1` |
| Status | Experimental; neither approved nor mandatory |
| Owner | Gordonfive/bempic maintainers |
| Contact | <https://github.com/Gordonfive/bempic/issues> |
| Canonical parameter block | Empty |
| License | Specification: Apache-2.0; cited implementation evidence: Apache-2.0 |

This public experimental profile is derived from the Reference implementation's
private candidate `0xffff0001/2` at immutable commit
[`cf3485f6606d6462077e8edd1592264c3ce4ca5e`](https://github.com/Gordonfive/bempic-reference/commit/cf3485f6606d6462077e8edd1592264c3ce4ca5e).
The private tuple is evidence provenance, not an allocation.

[REQ-COMPACT-001] Implementations claiming this profile MUST use public tuple
`0x00010000/1` and MUST NOT emit or accept `0xffff0001/2` as public
interoperability evidence. This allocation is experimental, is neither
approved nor mandatory, and makes no stable-wire or production-security
promise. A later approved profile receives a standards-action ID; it does not
silently promote this experimental ID.

Changing the codec ID changes the semantic expansion and profile binding of the
static capability alias, the encoded bytes of every generic field that carries
the tuple, representation IDs that bind the tuple, and therefore dependent
descriptors, collection digests, operations, and bundle digests. The cited
private-candidate vectors support this allocation decision but are not
public-tuple conformance vectors. Public vectors have to be regenerated for
`0x00010000/1` before release evidence can pass.

## Semantic boundary and context

The codec maps the seven v0.1 semantic `Operation` variants to complete,
length-delimited records. It changes no collection, selection, budget,
persistence, integrity, receipt, carrier, application-object, or failure
semantics. Generic records use the field encoding below. Two compact forms are
lossless aliases:

1. A static capability alias expands to one exact capability value containing
   the full opaque-binary schema fingerprint, public codec tuple, maxima,
   receipt levels, security class, and empty extension lists.
2. A dynamic warm-summary alias is legal only when the caller supplies the
   exact durable `SUMMARY` expected for the peer/collection context and the
   semantic value is byte-for-byte equal to it. The alias carries a full
   32-octet SHA-256 binding of every cached summary field.

Aliases do not truncate identifiers or digests. The cold form carries the full
32-octet collection ID and digest. Encoding is deterministic for the pair
`(semantic record, explicit codec context)`. Empty context is canonical for
cold encoding; an exact durable checkpoint is an explicit warm-encoding input,
not hidden process state.

[REQ-COMPACT-002] A decoder MUST fail before returning an operation when a
summary-alias context is missing, stale, or mismatched. A short alias MUST NOT
override a full value. A full extension-free summary MUST be rejected as
noncanonical when the exact supplied cache permits the alias, and the alias
MUST be rejected when the exact cache is unavailable. No failed decode may
mutate protocol state.

## Complete record format

Every record is:

```text
header:u8 || body_length:canonical-uvarint || body[body_length]
```

`header & 0xf8` is `0xb0`; the low three bits are operation tags 1 through 7
in the specification order. Tag zero and every other prefix are invalid.
`body_length` is unsigned LEB128 in its shortest representation.

The first body octet is a form selector:

| Operation | Form | Meaning |
|---|---:|---|
| `CAPABILITIES` | `0x01` | Exact static profile capability; body ends immediately |
| `SUMMARY` | `0x01` | Cold full summary: 32-octet collection ID, minimal generation uvarint, minimal item-count uvarint, 32-octet digest |
| `SUMMARY` | `0x02` | Exact supplied durable checkpoint followed by its 32-octet cache binding |
| All operations | `0x00` | Generic operation content in the field layout below |

Generic `CAPABILITIES` is noncanonical when it decodes to the static alias.
Generic extension-free `SUMMARY` is noncanonical because the cold full form is
available. A summary with record extensions uses the generic form. All other
form/tag combinations are invalid.

[REQ-COMPACT-003] A record MUST be at most 1,048,576 octets, its declared body
length MUST equal the remaining record length, and its header, form, and
uvarint MUST be canonical. The decoder MUST check the outer ceiling, canonical
length, fixed widths, bounds, and nesting before allocating proportional to
remote input or returning an operation. It MUST reject trailing bytes,
truncation, unknown tags or forms, overlong integers, and a 1,048,577-octet
outer input before body allocation.

Unknown optional and critical record extensions retain core behavior: a
bounded unknown optional value is skipped without side effects; an unknown
critical extension fails before an operation is returned.

## Generic content fields

Fixed-width integers are unsigned big-endian. Booleans are exactly `0x00` or
`0x01`; counts are one octet; payload lengths are four octets;
descriptor/extension-value lengths are two octets where shown. No alternate or
overlong form is accepted.

| Operation/structure | Canonical field order and widths |
|---|---|
| `CAPABILITIES` | Protocol count then `(U16 major, U16 minor)`; schema count then 32-octet fingerprints; codec count then `(U32 ID, U32 revision, 32-octet fingerprint)`; U32 max operation; U64 max data payload; U8 receipt levels; U8 security class; extension-declaration count then `(U32 ID, bool critical)` |
| `SUMMARY` | 32-octet collection ID; U64 generation; U64 item count; 32-octet collection digest |
| `OFFER` | 32-octet collection ID; U8 mode; U64 base and target generations; first and last cursors; descriptor count and descriptors; bool `more` |
| Inventory `REQUEST` | U8 variant `0`; 32-octet collection ID; U64 target generation; U8 mode; cursor; U8 page limit |
| Data `REQUEST` | U8 variant `1`; 16-octet budget ID; three U64 budget limits; selection count; each selection is 32-octet representation ID plus U64 offset and U64 desired payload |
| `DATA` | 32-octet representation ID; U64 offset; U32 payload length; nonempty payload |
| `RECEIPT` | 32-octet subject ID; U8 status; digest-presence bool and optional 32-octet digest; 16-octet idempotency ID; optional text |
| `FAILURE` | U8 code; U8 scope length and scope; bool retryable; optional text |
| Delta cursor | U8 variant `0`; U64 sequence |
| Full cursor | U8 variant `1`; 32-octet object ID; U32 part ID; 32-octet representation ID |
| Descriptor | U64 sequence; 32-octet object ID; U32 part ID; 32-octet representation ID; 32-octet schema fingerprint; U32 codec ID; U32 revision; U16 parameter length and parameters; U64 encoded length; decoded-length presence and optional U64; 32-octet content digest; expiry presence and optional U64 |
| Optional text | Presence bool; when present, U16 UTF-8 length and bytes |
| Record extensions | U8 count; each value is U32 ID, bool critical, U16 value length, and opaque value |

For generic form, the body is `0x00`, the operation payload in the table, then
the record-extension structure. Operation tags and every enumerated octet are:

| Field | Numeric mapping |
|---|---|
| Operation tag | `1` `CAPABILITIES`; `2` `SUMMARY`; `3` `OFFER`; `4` `REQUEST`; `5` `DATA`; `6` `RECEIPT`; `7` `FAILURE` |
| Offer mode | `0` delta; `1` full |
| Cursor variant | `0` delta sequence; `1` full entry key |
| Request variant | `0` inventory page; `1` representation data |
| Security class | `0` public; `1` authenticated-public; `2` confidential |
| Receipt status | `0` representation committed; `1` application accepted; `2` application delivered; `3` application rejected |
| Failure code | `0` unsupported version; `1` unsupported schema; `2` unsupported codec; `3` unsupported critical extension; `4` malformed operation; `5` limit exceeded; `6` unknown object; `7` metadata conflict; `8` range invalid; `9` integrity failure; `10` storage failure; `11` policy rejected; `12` checkpoint unknown |

The capability receipt-level octet is a bitmap whose bits 0 through 3 name the
four receipt statuses in numeric order; other bits are zero in this revision.
All counts and extension IDs that core semantics require to be unique remain
unique. A delta offer uses delta cursors and a full offer uses full cursors.
Offer descriptors are nonempty and ordered as the core requires; representation
selections are nonempty. Inventory page limits are 1 through 128, and `DATA`
payload is nonempty. Optional text with presence `0` has no length or bytes;
presence `1` is valid UTF-8 with no NUL or control character and at most the
stated UTF-8-octet bound.

The bounds are: 8 protocols, 16 schemas, 16 codec preferences, 32 extensions,
1,024 extension-value or codec-parameter octets, 128 offer descriptors, 128
request selections, 1,000,000 collection entries, 64 failure-scope octets, and
256 diagnostic UTF-8 octets. Nesting is fixed to operation, bounded collection,
and descriptor/selection/extension depth; values are not recursive.

[REQ-COMPACT-004] Encoders and decoders MUST enforce the specification's core
bounds and the field widths and collection bounds in this section. UTF-8 and
NFC validation, semantic cross-field constraints, and extension criticality
MUST have exactly the outcomes required by the core specification. The codec
MUST NOT introduce alternate application-object meanings.

## Aliases and supported schema

The static capability expands exactly to:

- protocol generation `0.1`;
- opaque-binary fingerprint
  `d8906a1cefbf89e4f29b4a0f636cfbfa1e9c6301e7e3a4fe213c090066f8e797`;
- public codec tuple `0x00010000/1`;
- maximum operation 1,048,576 and maximum data payload 1,000,000;
- receipt levels `0x0f`, public security class, and no extensions.

The record semantics use the core-operations fingerprint
`c4a686e7e9c6a40a5f187259a376b26cfc1d355179fd9fff487e105aeeac7302`.
For opaque-binary data, exact encoded size is `n` for
`0 <= n <= 1,073,741,824`; the decoded bytes and maximum are identical. This
revision does not support the message-manifest schema fingerprint and makes no
manifest-schema codec claim.

The warm-summary binding is:

```text
SHA-256("BEMPIC-COMPACT-SUMMARY-CACHE-v0.1\0" ||
       collection_id || U64BE(generation) ||
       U64BE(item_count) || collection_digest)
```

[REQ-COMPACT-005] The canonical codec parameter block MUST be empty. The static
capability alias MUST expand to the exact values above, including public tuple
`0x00010000/1`. A nonempty parameter block or a different alias expansion MUST
be rejected as `UNSUPPORTED_CODEC` before protocol-state mutation.

## Exact encoded size

Let `V(x)` be the octet length of canonical unsigned LEB128 for nonnegative
`x`. Let `L(r)` be the arithmetic exact size of the generic fixed-width record
with its seven-octet legacy envelope. Let `C(r, context)` be this profile's
exact size.

```text
E(b) = 1 + V(b)

static capabilities:
  b = 1
  C = E(1) + 1 = 3

exact cached summary:
  b = 1 + 32
  C = E(33) + 33 = 35

cold full summary s:
  b = 1 + 32 + V(s.generation) + V(s.item_count) + 32
  C = E(b) + b

generic record r:
  b = 1 + (L(r) - 7)
  C = E(b) + b
```

For generation and count `(100, 100)`, the cold summary body is 67 octets and
the complete record is 69. Size analysis is arithmetic and does not perform
trial serialization or allocate in proportion to the encoded record.

[REQ-COMPACT-006] An encoder MUST compute exact encoded size before emission,
without trial serialization, and MUST produce exactly that many octets. It
MUST reject any semantic value whose exact size exceeds an applicable profile
or negotiated maximum before allocation proportional to the value. Decoder
acceptance MUST NOT exceed the same declared domains.

## Maximum sizes and witnesses

For a generic operation whose previous fixed-envelope reached maximum is
`M_fixed`, the direct content maximum is `M_fixed - 7`, the body maximum is
`1 + (M_fixed - 7)`, and the complete maximum is
`1 + V(body) + body`.

| Operation | Direct generic content | Complete maximum | Private-candidate witness SHA-256 (allocation provenance) |
|---|---:|---:|---|
| `CAPABILITIES` | 34,355 | 34,360 | `05c50ab66069508eb24589d2d939ebd6dff082c39704f65629cb6992b40841c1` |
| `SUMMARY` | 33,073 | 33,078 | `76eee08b2b181380a18df6db4fd60ed225e14cbd0257e77e725316451a658378` |
| `OFFER` | 186,782 | 186,787 | `508aca567f0626847cd8d0cc28eae0c10d6803540666efab2eb72fe00d089be9` |
| `REQUEST` | 39,179 | 39,184 | `f217a988a379a87e43b2baef17b2aab9f2c7fca440d614ec3f038a40a2635ac` |
| `DATA` | 1,048,569 | 1,048,574 | `58540c01d0f9f1488f5be6262405184499bd919d8c23d2568846066b9ef19902` |
| `RECEIPT` | 33,334 | 33,339 | `1feb5e18be0cbba37a4fb9c0ce8cd61f67b61ff5b861d902921400f43d3523f5` |
| `FAILURE` | 33,319 | 33,324 | `93725b078260b8354cc8b06e00b784d4ed439338a94ca37b87844bb7f52ac2f5` |

Each maximum is reachable by the semantic witness cited in the allocation
evidence. The listed byte digests bind private tuple `0xffff0001/2` and are
provenance, not the expected public-tuple digests. The outer accepted ceiling
remains 1,048,576; the tightest reachable semantic record is the
1,048,574-octet `DATA` witness. The two unused octets do not authorize a larger
payload or another accepted semantic record.

[REQ-COMPACT-007] A conformance claim MUST reproduce every maximum witness,
its exact encoded length, and its byte digest using public tuple
`0x00010000/1`; MUST demonstrate exact-size equality across mandatory and
generated boundary cases; and MUST reject the applicable one-past, malformed,
truncated, false-length, trailing-byte, nonminimal, unknown-form, and
context-failure cases before returning an operation. Approximate-number,
rounding, NaN, infinity, and negative-zero vectors are not applicable because
the profile has no approximate numeric type.

## Allocation evidence, measurements, and limits

The immutable allocation audit is recorded in
[`experimental-codec-allocation.json`](../../conformance/v0.1/experimental-codec-allocation.json).
Its private-candidate sources include:

- [profile](https://github.com/Gordonfive/bempic-reference/blob/cf3485f6606d6462077e8edd1592264c3ce4ca5e/docs/EXPERIMENTAL-COMPACT-CODEC-v0.1.md),
  SHA-256 `0633ed81272a89d085ceb8ae01aef82ac1749a9babe2fac9b59d0d1f3529fce8`;
- [evidence record](https://github.com/Gordonfive/bempic-reference/blob/cf3485f6606d6462077e8edd1592264c3ce4ca5e/benchmarks/results/compact-codec-evidence-2026-09-01.json),
  SHA-256 `fd3461c674921b9730c773f0eef01d34dcc8e60a472ca1bb2ec1f3027de2f525`;
- [draft vectors](https://github.com/Gordonfive/bempic-reference/blob/cf3485f6606d6462077e8edd1592264c3ce4ca5e/test-vectors/v0.1-compact-candidate/vectors.json),
  SHA-256 `5edd10847be60cef384be726d7f3d83c6d78618ec38ce56db469cf24e794b8fb`;
- [independent-language verifier](https://github.com/Gordonfive/bempic-reference/blob/cf3485f6606d6462077e8edd1592264c3ce4ca5e/scripts/verify_conformance.py),
  SHA-256 `75c00d8e7af789a889669910cf945eaa7596d81054b6105a916475df02583dc4`;
- [malformed/property report](https://github.com/Gordonfive/bempic-reference/blob/cf3485f6606d6462077e8edd1592264c3ce4ca5e/conformance/fuzz-report.json),
  SHA-256 `5716f157c23fa631e748acb48f20f68ae28326b6251e4ecf1c0c77458155401d`;
- [blocked conformance report](https://github.com/Gordonfive/bempic-reference/blob/cf3485f6606d6462077e8edd1592264c3ce4ca5e/conformance/v0.1.0-report.json),
  SHA-256 `40bbb7544a8b2c1eee1e9ac74fbb2fd0d73c9f8d8a5cbe505fb5abe3b33d1ba1`;
- [successful exact-head CI](https://github.com/Gordonfive/bempic-reference/actions/runs/33569955919).

The private candidate measured 35 B for warm no-change and 75 B for cold
no-change on the prescribed 100-message fixture, including every required
BEMPIC operation and excluding no BEMPIC byte. Those lengths remain the
profile's mathematical expectation because a U32 ID retains its width, but
they are not passing public-tuple release evidence until the encoded bytes,
representation IDs, collection digests, vector digests, and independent checks
are regenerated for this allocation.

The implementation evidence reports 50,000 general malformed random inputs,
175 compact structured malformed cases, 4,100 compact exact-size property
cases, 3 valid compact fixtures, 7 invalid/boundary fixtures, 7 maximum
witnesses, and zero reported unresolved correctness, panic, or exact-size
failure. The Python verifier is a distinct language and decoder, but it is in
the same repository and ownership boundary; it does not satisfy independent
implementation ownership.

[REQ-COMPACT-008] Public conformance and release evidence MUST bind
`0x00010000/1` and the exact specification/profile commit. Evidence generated
with `0xffff0001/2` MAY support allocation provenance only and MUST NOT be
promoted as public vectors, an approval, mandatory status, independent
ownership, stable-wire compatibility, production security, B2F evidence, M4P
approval, or final release evidence.

## Security and compatibility

This profile provides no authentication, confidentiality, replay protection,
compression, or application-security handshake. Security class `public` means
there is no application-protection claim. It has no DCCL or M4P dependency and
does not copy either format. Implementations must apply the resource ceilings
and fail-closed rules above. Real private user traffic remains prohibited
without a separately reviewed security profile.

The profile is wire-incompatible with the Reference private candidate because
the tuple is semantically bound even where a particular record happens not to
contain it. It is also incompatible with the Reference candidate's disposable
private revision 1. No private-candidate compatibility promise is made.
