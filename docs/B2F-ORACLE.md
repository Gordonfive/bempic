# BEMPIC v0.1 B2F/LZHUF Oracle Decision

**Decision status:** no qualified oracle selected; v0.1 compactness evidence
remains blocked.

This document defines the B2F comparison required by
[`METRICS.md`](METRICS.md), records the legal and technical audit, and states
the evidence needed to select an oracle.
It does not implement B2F, copy an implementation, or change either compactness
threshold.

## Comparison profile

The comparison profile is `bempic-v0.1-b2f-text-single-message-v1`. It compares
one deterministic, attachment-free text message per independent no-fault run.
Batching is outside this profile: per-fixture results may not share or allocate
proposal, response, or framing bytes with another fixture.

### Source and MIME preparation

[REQ-B2F-001] Each corpus fixture MUST contain exact, content-addressed bytes
for all of the following: the source RFC 5322/MIME message, a lossless semantic
record, the prepared B2 message image, and the BEMPIC semantic fixture. The raw
message MUST use CRLF line endings, `text/plain; charset=us-ascii`, `7bit`
content-transfer encoding, one non-empty body, no multipart container, no
attachment, no `Bcc`, and no transport-added trace field. The corpus manifest
MUST fix the `Date`, `From`, ordered `To`, ordered `Cc`, `Subject`, MIME
`Message-ID`, B2 `Mid`, B2 `Mbo`, and body bytes. MIME parsing, address policy,
random ID generation, clock access, charset guessing, line-ending repair, and
content transformation are preparation work and MUST NOT occur during a measured
run.

The raw MIME bytes are a separately reported baseline; they are not B2F bytes.
The semantic record prevents an implementation-specific MIME parser from
changing the workload. The prepared B2 image is the exact input to the
compression executable and permits independent byte comparison before and
after compression.

For this profile, the prepared B2 image is ASCII and has this exact order and
spelling, with each line terminated by CRLF:

1. `Mid: <b2-mid>`;
2. `Date: <YYYY/MM/DD HH:MM>` in UTC;
3. `Type: Private`;
4. `From: <from>`;
5. each `To: <to>` in manifest order;
6. each `Cc: <cc>` in manifest order;
7. `Subject: <subject>`;
8. `Mbo: <mbo>`;
9. `Body: <decimal-body-octet-length>`;
10. one empty line, the exact body bytes, and one terminating CRLF not included
    in the `Body` length.

`Mid` is first because Open B2F requires it. The remaining fixed order is a
BEMPIC benchmark rule because Open B2F otherwise permits header reordering. A
fixture whose published prepared B2 bytes do not equal this construction is
invalid; the oracle must not silently rewrite it.

### LZHUF image

[REQ-B2F-002] The compression behavior MUST be FBB `LZHUF_1`, byte-identical to
ARSFI `Winlink-Compression` commit
[`dbe96569817018e66e0e5f6add40eed12adc9fd7`](https://github.com/ARSFI/Winlink-Compression/commit/dbe96569817018e66e0e5f6add40eed12adc9fd7),
`Compression.Encode(prepared_b2_image, prependCRC := True)`. Generic LZH, an
archive-format LZH encoder, gzip, or a decoder-only match is not sufficient.
The pinned variant uses a 2,048-octet LZSS ring, a 60-octet look-ahead buffer,
threshold 2, an initial ring filled with ASCII space, adaptive Huffman coding
with 314 symbols and reconstruction at frequency `0x8000`, and the published
FBB position coding. Its compressed image is:

- a two-octet little-endian CRC-16/XMODEM value (polynomial `0x1021`, initial
  value zero, no reflection, no final XOR) over the following length and
  compressed-bitstream octets;
- the uncompressed input length as an unsigned four-octet little-endian value;
  and
- the deterministic LZHUF bitstream, padded only by the encoder's final partial
  output octet.

[REQ-B2F-006] An oracle record MUST publish the input and output lengths and SHA-256 digests,
the first two CRC octets, the decoded four-octet length, a successful independent
decode, and byte equality with independently generated expected output. Copying
ARSFI or another implementation's lookup tables or source into this repository
is not required by this behavioral reference and is prohibited unless a later
change records its exact license, provenance, and notices.

### B2F application envelope

[REQ-B2F-003] `b2f_total_bytes` MUST count the complete, process-visible B2F
application bytes from the first octet of the one-message FC proposal through
the checksum octet following EOT. For an initial transfer at offset zero, the
directional transcript is exactly:

- sender to receiver: `FC EM <mid> <u-size> <c-size> 0\r`, where `u-size` is the
  prepared B2 image length and `c-size` is the complete LZHUF image length;
- sender to receiver: `F> <HH>\r`, where `HH` is uppercase hexadecimal for the
  two's complement modulo 256 of the sum of every proposal octet including its
  terminating CR;
- receiver to sender: `FS +\r`;
- sender to receiver: SOH (`0x01`), one header-length octet, the ASCII subject,
  NUL, ASCII `0`, and NUL, where the header length is subject length plus three;
- sender to receiver: consecutive data blocks of STX (`0x02`), one length
  octet, and 1–250 LZHUF-image octets; every non-final block contains 250 data
  octets and the final block contains the remainder; and
- sender to receiver: EOT (`0x04`) followed by the two's complement modulo 256
  of the sum of every transmitted LZHUF-image data octet.

The count includes the FC line, proposal checksum line, FS response, binary
header, all block prefixes, the complete two-octet CRC/four-octet length/LZHUF
image, EOT, and the transfer checksum. It excludes raw MIME bytes, B2
preparation work, login/greeting/SID and `;PQ`/`;PR` authentication, comments,
line echo, a later turn or `FF`/`FQ` session close, modem/carrier/link framing,
FEC, lower-layer acknowledgements or retransmissions, and any failed or resumed
attempt. `b2f_send_bytes` counts the sender-to-receiver items;
`b2f_receive_bytes` counts `FS +\r`; every record must demonstrate
`b2f_total_bytes = b2f_send_bytes + b2f_receive_bytes`.

The 250-octet block size follows the Winlink data-packaging publication. A tool
that hard-codes another legal FBB block size, including `wl2k-go`'s current
125-octet choice, does not implement this comparison profile without a
separately verified framing adapter.

### Calculations and evidence

[REQ-B2F-004] Every fixture MUST report raw MIME, semantic, prepared-B2,
compressed-image, B2F-directional, and BEMPIC-directional lengths and SHA-256
digests. It MUST report the exact signed rational values
`candidate_reduction_percent = 100 * (b2f_total_bytes - bempic_total_bytes) /
b2f_total_bytes` and `candidate_increase_percent = 100 *
(bempic_total_bytes - b2f_total_bytes) / b2f_total_bytes` as an integer
numerator and positive integer denominator before any decimal rendering.
The median gate is the median of the per-fixture reduction rationals, ordered by
exact cross multiplication; for an even fixture count it is the arithmetic mean
of the two middle rationals. No ratio of aggregate byte totals or ratio of two
medians may replace it. The B2F metric gate remains at reduction at least 10
percent and per-fixture increase at most 5 percent absent an accepted measured
justification.

The raw result must also identify the exact specification commit, corpus
manifest digest, fixture ID, selected BEMPIC codec tuple/profile digest,
implementation commit, oracle executable digest, build provenance, operating
system and architecture, invocation, environment, exit code, stdout/stderr
digests, and parser version. Repeating the run on every claimed platform must
produce byte-identical prepared B2, LZHUF, and framed-transcript digests.

## Candidate audit

The legal descriptions below report source-file terms and project policy; they
are not legal advice. No audited third-party code or fixture is copied here.

| Candidate | Exact identity and authority | Language, dependencies, platforms, executable status | License and permitted role here | Decision deficiency |
|---|---|---|---|---|
| ARSFI Winlink Compression | Winlink Development Team/ARSFI source at [`dbe96569817018e66e0e5f6add40eed12adc9fd7`](https://github.com/ARSFI/Winlink-Compression/commit/dbe96569817018e66e0e5f6add40eed12adc9fd7); [`WinlinkSupport.vb`](https://github.com/ARSFI/Winlink-Compression/blob/dbe96569817018e66e0e5f6add40eed12adc9fd7/WinlinkSupport.vb) is the publisher-identified implementation | VB.NET, .NET base classes; the repository contains no project file, build lock, CLI, release, declared platform matrix, or fixtures | [Three-clause BSD license](https://github.com/ARSFI/Winlink-Compression/blob/dbe96569817018e66e0e5f6add40eed12adc9fd7/License.txt), copyright ARSFI; source/binary redistribution and linking are compatible when its notice and non-endorsement condition are preserved | Authoritative compression behavior, but not a complete, independently invokable B2F oracle and not an immutable built artifact |
| `wl2k-go` | Independent implementation release [`v1.0.1` / `efde6fbcb7bc8d6519fd8018ec544c793d4ef48d`](https://github.com/la5nta/wl2k-go/tree/efde6fbcb7bc8d6519fd8018ec544c793d4ef48d) maintained by Martin Hebnes Pedersen (LA5NTA) | Go 1.24 module; LZHUF package is a library, not a command; module dependencies are pinned in [`go.mod`](https://github.com/la5nta/wl2k-go/blob/efde6fbcb7bc8d6519fd8018ec544c793d4ef48d/go.mod); framing hard-codes 125-octet blocks | Root [MIT license](https://github.com/la5nta/wl2k-go/blob/efde6fbcb7bc8d6519fd8018ec544c793d4ef48d/LICENSE), but [`lzhuf/COPYRIGHT`](https://github.com/la5nta/wl2k-go/blob/efde6fbcb7bc8d6519fd8018ec544c793d4ef48d/lzhuf/COPYRIGHT) says the port's antecedent code had no particular license and not all authors were contacted; incorporation or linking cannot be approved from the root license alone | No standalone oracle interface, unresolved LZHUF provenance, and non-profile framing; existing tests do not establish this corpus and full transcript |
| Pat | Independent Winlink client release [`v1.0.0` / `2e6a8d14baf0268f4e2aa4d01784a54ca935cf52`](https://github.com/la5nta/pat/releases/tag/v1.0.0), maintained by LA5NTA and using `wl2k-go v1.0.1` | Go 1.24; immutable release assets cover macOS amd64, Linux amd64/arm64/armhf/i386, and Windows i386; it is a standalone client but has no deterministic offline B2F-image command | Root [MIT license](https://github.com/la5nta/pat/blob/2e6a8d14baf0268f4e2aa4d01784a54ca935cf52/LICENSE); inherited LZHUF provenance remains unresolved. Process-separated execution would avoid copying or linking, but does not cure missing deterministic output | Full network client, runtime mailbox/time/ID/session behavior, no oracle output contract, inherited provenance issue, and 125-octet framing through `wl2k-go` |
| `paclink-unix` `lzhuf_1` | Independent client at [`cc7b2f9474959a70856cabaf812bfce53d2da145`](https://github.com/nwdigitalradio/paclink-unix/tree/cc7b2f9474959a70856cabaf812bfce53d2da145), originally by Nicholas S. Castellano and maintained by NW Digital Radio contributors | C/autotools on Unix/Linux; full client dependencies include a C toolchain, autoconf/automake/libtool, MTA, Berkeley DB, GLib, zlib, ncurses, and GMime; `lzhuf_1 e1 input output` is a separately built command | [`GPL-2.0-or-later`](https://github.com/nwdigitalradio/paclink-unix/blob/cc7b2f9474959a70856cabaf812bfce53d2da145/COPYING). It must not be copied, vendored, or linked into BEMPIC. An unmodified, separately obtained executable may only be invoked as a process, with its distribution and GPL obligations kept outside this repository | Closest executable candidate, but no immutable standalone release artifact, prescribed-corpus output, ARSFI cross-check, full-envelope output, or hermetic cross-platform build evidence |
| F6FBB `B2Compress.exe` / LinFBB | Named by the original F6FBB and Winlink publications; no content-addressed `B2Compress.exe` release with an applicable license was identified in the audited primary sources | Historical executable/full BBS distribution; exact runtime, supported platforms, dependency set, and deterministic command contract are not pinned | No sufficiently specific artifact/license pair was found; it cannot be redistributed, linked, or used in CI on the present record | Identity, license, artifact digest, invocation, and reproducibility are all unresolved |

## Legal and repository boundaries

The following modes are distinct:

- **Incorporating source** copies third-party expression and requires a
  compatible license, provenance, preserved notices, and a repository decision.
  No B2F source is incorporated by this decision.
- **Linking a library** makes it part of the BEMPIC executable/dependency graph.
  BSD- or MIT-licensed code may be link-compatible with notices, but the
  `wl2k-go` LZHUF provenance caveat prevents a positive conclusion for that
  package. GPL/AGPL code must not be linked.
- **Invoking a separately installed executable** keeps code and address spaces
  separate. GPL `paclink-unix` may be considered only in this mode; BEMPIC must
  not distribute it, download it silently, or represent it as Apache-2.0. The
  result record must identify how the operator obtained it and its license.
- **Fixture generation only** permits an external implementation to produce
  content-addressed expected bytes. The fixtures still require license/provenance
  permission, and a second implementation must independently reproduce them.
- **Implementation from publications** must be an independently authored
  implementation of protocol behavior, not a transcription of source, lookup
  tables, fixtures, or substantial specification text. It requires its own
  copyright and dependency review plus differential evidence against the
  authoritative behavior.

## Decision and required next package

[REQ-B2F-005] No implementation is selected at this commit. A conformance or
release record MUST keep the B2F oracle and both B2F compactness thresholds
blocked and MUST NOT claim B2F results until one reviewed package provides all
of the following:

1. a synthetic, redistributable corpus manifest and all exact raw MIME,
   semantic, prepared-B2, and BEMPIC fixture digests required above;
2. either (a) a BSD-licensed ARSFI-derived standalone executable with required
   notice handling, or (b) the unmodified GPL `paclink-unix` command obtained
   and invoked strictly as a separately installed process, or (c) a clean-room
   executable built from the publications;
3. an immutable source commit or release, built-executable SHA-256, hermetic
   build/runtime dependencies, platform matrix, and exact invocation/parser;
4. byte-identical compression output against the pinned ARSFI behavior for
   every corpus fixture and boundary fixture, plus successful independent
   decode and malformed-input evidence;
5. byte-identical full B2F transcript construction using 250-octet data blocks
   and the inclusion/exclusion rules above on at least two platforms;
6. a licensing review that treats source incorporation, linking,
   process-separated execution, fixture redistribution, and CI use separately
   and includes every required notice without adding GPL/AGPL code here; and
7. raw per-fixture result records, exact rational calculations, aggregate
   calculation, and independent reproduction linked from the release record.

Maintainer confirmation could clear `wl2k-go`'s LZHUF copyright provenance, or
ARSFI could publish a pinned CLI/build and reference outputs. Either would
remove a licensing or tooling deficiency, but neither substitutes for the
corpus and independent full-envelope evidence.

## Primary source identities

The GitHub links above identify immutable commits. The publisher-hosted protocol
documents are mutable URLs, so this audit additionally content-addresses the
exact bytes retrieved on 2026-09-02 UTC:

- Winlink [Open B2F](https://winlink.org/B2F): SHA-256
  `cd6c5ab26753c6f8184334ba3d829ddcf5401731fa8738434501e7c3214aeafc`,
  37,310 octets; publisher page says “Last revised February, 2018”.
- Winlink [Data Flow and Data Packaging](https://winlink.org/sites/default/files/downloads/winlink_data_flow_and_data_packaging.pdf):
  SHA-256 `9336299e64401d23ad8027b4b710c3db0cd3eddf36490c0e246dc3fba83cbe7b`,
  64,355 octets; Winlink Development Team, 2017.
- F6FBB [forwarding protocol](https://www.f6fbb.org/protocole.html): SHA-256
  `07c49a1a5062b1d9129f58b35920297fa57dfb8f95fc2ea1f7a1486fae95c4de`,
  21,088 octets; an immutable independent repository snapshot is
  [`docs/F6FBB-B2F/protocole.html`](https://github.com/la5nta/wl2k-go/blob/efde6fbcb7bc8d6519fd8018ec544c793d4ef48d/docs/F6FBB-B2F/protocole.html).

The official publications define message preparation, FC proposals, FBB B1
resume and CRC/length prefixes, and B2 block framing. The immutable source files
define candidate behavior and licensing. Search-result summaries and secondary
descriptions are not evidence for this decision.
