# BEMPIC v0.1 Normative Conformance Matrix

Every uppercase `MUST` or `MUST NOT` paragraph in the release-authoritative
documents carries one or more stable requirement IDs. This matrix maps every ID
to evidence. [`scripts/validate_release_gates.py`](../scripts/validate_release_gates.py)
fails if a normative paragraph has no ID, an ID has no row, or a row has no
source requirement. A row can cover multiple inseparable clauses in its marked
paragraph; all clauses must pass.

Evidence keys use `Vnn` for the mandatory semantic catalog, `CB` for all
applicable codec-boundary vectors, `CR` for the machine-readable conformance
report, `MR` for metric records, `RR` for the release record, `SR` for security
review, and `GR` for a governance review or accepted decision. “Inspection”
means an independently reproducible static or artifact check, not an assertion.

| Requirement | Source | Required evidence |
|---|---|---|
| REQ-REL-001 | `SPECIFICATION.md` release status | RR gate list and tag-state check |
| REQ-LAYER-001 | `SPECIFICATION.md` architecture | V09 trace plus M4P confirmation |
| REQ-BOUNDS-001 | `SPECIFICATION.md` core bounds | V04, V07, CB, allocation instrumentation |
| REQ-CANON-001 | `SPECIFICATION.md` scalar rules | CB non-minimal/ambiguous cases |
| REQ-META-001 | `SPECIFICATION.md` metadata | V04 and CB UTF-8/NFC/control cases |
| REQ-PART-001 | `SPECIFICATION.md` parts | V04 manifest reconstruction |
| REQ-PREP-001 | `SPECIFICATION.md` preparation | V04–V07 repeated deterministic preparation |
| REQ-PREP-002 | `SPECIFICATION.md` deterministic codec | byte-identical runs and independent vector check |
| REQ-JCS-001 | `SPECIFICATION.md` fingerprints | JCS fixture and independent fingerprint verification |
| REQ-ID-001 | `SPECIFICATION.md` identifiers | V11 conflict cases and application-profile decision |
| REQ-OPS-001 | `SPECIFICATION.md` operations | V01–V15 coverage and codec profile inspection |
| REQ-CAPS-001 | `SPECIFICATION.md` capabilities | V13 limits and stale-cache cases |
| REQ-OFFER-001 | `SPECIFICATION.md` offers | V05/V07 exact-length and no-deferred-payload checks |
| REQ-REQUEST-001 | `SPECIFICATION.md` requests | V07/V11 boundary and conflict cases |
| REQ-SELECTION-001 | `SPECIFICATION.md` selection | V05 and zero-unselected-payload MR |
| REQ-DATA-001 | `SPECIFICATION.md` data | V07, V08, V11, V12 state traces |
| REQ-RECEIPT-001 | `SPECIFICATION.md` receipts | V10 trace and M4P binding trace |
| REQ-STATE-001 | `SPECIFICATION.md` state machine | V08, V11, V14 reopen traces |
| REQ-IDEMP-001 | `SPECIFICATION.md` idempotency | V10 full-state traces |
| REQ-PERSIST-001 | `SPECIFICATION.md` persistence | V03, V08, V14 crash/reopen evidence |
| REQ-CRASH-001 | `SPECIFICATION.md` crash consistency | V08/V14 fault injection and storage audit |
| REQ-REOPEN-001 | `SPECIFICATION.md` reopen | V03, V08, V11, V14 reopen traces |
| REQ-RESUME-001 | `SPECIFICATION.md` resume boundary | V09 trace and architecture inspection |
| REQ-INTEGRITY-001 | `SPECIFICATION.md` integrity | V07/V11 overflow, length, digest, and ID cases |
| REQ-DECODE-001 | `SPECIFICATION.md` decode | V04/V06/V11 strict decode and reconstruction |
| REQ-BUDGET-001 | `SPECIFICATION.md` budgets | V12 and zero-quote-error MR |
| REQ-ACCOUNT-001 | `SPECIFICATION.md` counters | MR schema completeness and V01–V12 records |
| REQ-ACCOUNT-002 | `SPECIFICATION.md` cost domains | MR identity plus M4P cost-label inspection |
| REQ-ACCOUNT-003 | `SPECIFICATION.md` semantic bytes | descriptor-excluding fixture recomputation, fixed endpoint-role directional MR identity, V05/V08 duplicate/defer traces |
| REQ-CODEC-001 | `SPECIFICATION.md` codec publication | codec profile, size proof, CB, independent verifier |
| REQ-COMPACT-001 | `docs/codecs/EXPERIMENTAL-COMPACT-v0.1.md` status | registry/package tuple check and forbidden private-tuple vector check |
| REQ-COMPACT-002 | `docs/codecs/EXPERIMENTAL-COMPACT-v0.1.md` context | CB missing/stale/mismatched cache and noncanonical-full-form cases |
| REQ-COMPACT-003 | `docs/codecs/EXPERIMENTAL-COMPACT-v0.1.md` framing | CB prefix/tag/form/uvarint/length/ceiling cases and pre-allocation instrumentation |
| REQ-COMPACT-004 | `docs/codecs/EXPERIMENTAL-COMPACT-v0.1.md` fields | CB field/count/UTF-8/NFC/extension/cross-field boundaries |
| REQ-COMPACT-005 | `docs/codecs/EXPERIMENTAL-COMPACT-v0.1.md` aliases | static-alias expansion and canonical-empty-parameter vectors |
| REQ-COMPACT-006 | `docs/codecs/EXPERIMENTAL-COMPACT-v0.1.md` exact size | arithmetic-size/encoded-length equality and one-past tests |
| REQ-COMPACT-007 | `docs/codecs/EXPERIMENTAL-COMPACT-v0.1.md` maxima | seven public-tuple witnesses, malformed/property report, independent reproduction |
| REQ-COMPACT-008 | `docs/codecs/EXPERIMENTAL-COMPACT-v0.1.md` evidence | immutable provenance audit and public-tuple release-evidence lint |
| REQ-EXT-001 | `SPECIFICATION.md` extensions | V13 optional/critical/limit cases |
| REQ-FAIL-001 | `SPECIFICATION.md` fail closed | V11/V13/V15 and mutation traces |
| REQ-FAIL-002 | `SPECIFICATION.md` scoped failure/retry | V11/V15 unrelated-state and retry evidence |
| REQ-LAYER-002 | `SPECIFICATION.md` conformance boundary | architecture inspection and M4P confirmation |
| REQ-LAYER-003 | `SPECIFICATION.md` M4P record boundary | binding-package validation and V09/V10/V12 traces |
| REQ-ARCH-001 | `docs/ARCHITECTURE.md` state ownership | persistence/state-store integration tests and architecture inspection |
| REQ-ARCH-002 | `docs/ARCHITECTURE.md` reference boundary | dependency/type inspection and M4P binding review |
| REQ-REPO-001 | `docs/REPOSITORY-BOUNDARY.md` prototype retention | repository-tree inspection and accepted parity decision before later removal |
| REQ-SEC-001 | `docs/SECURITY-MODEL.md` prototype warning | source/package warning inspection and deployment SR |
| REQ-SEC-002 | `docs/SECURITY-MODEL.md` security claims | named-profile SR and negotiation vectors |
| REQ-SEC-003 | `docs/SECURITY-MODEL.md` decompression | CB expansion-limit tests and allocation instrumentation |
| REQ-VEC-001 | `docs/TEST-VECTORS.md` bundle | bundle-schema validation and digest recomputation |
| REQ-VEC-002 | `docs/TEST-VECTORS.md` paths | traversal-invalid bundle cases |
| REQ-VEC-003 | `docs/TEST-VECTORS.md` traces | independent step-by-step trace comparison |
| REQ-VEC-004 | `docs/TEST-VECTORS.md` catalog | catalog validator and V01–V15 result records |
| REQ-VEC-005 | `docs/TEST-VECTORS.md` updates | GR, compatibility statement, released-bundle immutability check |
| REQ-VEC-006 | `docs/TEST-VECTORS.md` V08 array | catalog validator, 24 complete row traces, pair-coverage proof |
| REQ-VEC-007 | `docs/TEST-VECTORS.md` public codec tuple | public-tuple bundle metadata, regenerated IDs/digests, private-tuple rejection |
| REQ-VEC-008 | `docs/TEST-VECTORS.md` external B2F corpus | corpus manifest, exact raw/prepared/expected artifacts, licenses, digest and independent reproduction |
| REQ-VEC-009 | `docs/TEST-VECTORS.md` M4P traces | six trace IDs, exact binding/source/API metadata, full step and counter comparison |
| REQ-CLAIM-001 | `docs/CONFORMANCE.md` claims | CR claim metadata schema validation |
| REQ-CONF-001 | `docs/CONFORMANCE.md` semantic core | CR checklist with V01–V15 links |
| REQ-CONF-002 | `docs/CONFORMANCE.md` interruptions | V08/V14 transition coverage report |
| REQ-CONF-003 | `docs/CONFORMANCE.md` pairwise coverage | V08 24-row evidence and V14 before/after fault report |
| REQ-CONF-004 | `docs/CONFORMANCE.md` B2F evidence | selected oracle, corpus, raw MR, license review and independent byte comparison |
| REQ-CONF-005 | `docs/CONFORMANCE.md` M4P evidence | external confirmation, concrete API mapping, package digest, and six passing traces |
| REQ-CLAIM-002 | `docs/CONFORMANCE.md` major-zero wording | RR/CR forbidden-claim lint |
| REQ-REG-001 | `docs/REGISTRIES.md` prototype codec | registry and prototype-advertisement inspection |
| REQ-REG-002 | `docs/REGISTRIES.md` ID ranges | registry validator and V13 invalid-ID cases |
| REQ-REG-003 | `docs/REGISTRIES.md` experimental evidence | allocation PR checklist and artifact validation |
| REQ-REG-004 | `docs/REGISTRIES.md` approval evidence | GR plus profile/proof/vector/fuzz/independent reports |
| REQ-REG-005 | `docs/REGISTRIES.md` mandatory evidence | GR, two implementation reports, MR, migration review |
| REQ-REG-006 | `docs/REGISTRIES.md` maximum sizes | profile size tables and layer-accounting inspection |
| REQ-REG-007 | `docs/REGISTRIES.md` worst-case proof | proof artifact, reaching witnesses, independent result |
| REQ-REG-008 | `docs/REGISTRIES.md` exact sizing | CB equality/one-past tests and allocation instrumentation |
| REQ-REG-009 | `docs/REGISTRIES.md` proof tests | CB, property/exhaustive report, independent verifier |
| REQ-REG-010 | `docs/REGISTRIES.md` allocation change | CI registry validator, changelog, GR |
| REQ-METRIC-001 | `docs/METRICS.md` envelope metadata | MR schema validation |
| REQ-METRIC-002 | `docs/METRICS.md` byte identity | per-direction capture and MR identity check |
| REQ-METRIC-003 | `docs/METRICS.md` aggregation | raw-run MR and recomputed summaries |
| REQ-METRIC-004 | `docs/METRICS.md` first body | V05/V06 traces and independently recomputed MR |
| REQ-METRIC-005 | `docs/METRICS.md` interruption/resume | V08/V09 raw traces and MR |
| REQ-METRIC-006 | `docs/METRICS.md` compactness | V01/V02 MR threshold evaluation |
| REQ-METRIC-007 | `docs/METRICS.md` budget/defer/resume | V05/V08/V09/V12 MR threshold evaluation |
| REQ-METRIC-008 | `docs/METRICS.md` B2F | oracle decision, licenses, raw corpus MR, justification GR |
| REQ-METRIC-009 | `docs/METRICS.md` reproducibility | content-addressed MR and independent rerun |
| REQ-METRIC-010 | `docs/METRICS.md` semantic workload | raw per-representation fixture records, shared endpoint-role binding, descriptor exclusion, and independently recomputed directional identity |
| REQ-METRIC-011 | `docs/METRICS.md` M4P result accounting | per-submit result/debit records and lower-layer unavailable/exact/estimated scope validation |
| REQ-B2F-001 | `docs/B2F-ORACLE.md` source preparation | exact raw MIME, semantic, prepared-B2 and BEMPIC fixture artifacts |
| REQ-B2F-002 | `docs/B2F-ORACLE.md` LZHUF image | pinned ARSFI behavior, parameters, image structure and independent byte/decode evidence |
| REQ-B2F-003 | `docs/B2F-ORACLE.md` B2F envelope | directional transcript reconstruction and byte identity |
| REQ-B2F-004 | `docs/B2F-ORACLE.md` calculations | exact per-fixture rationals, median recomputation and reproducibility metadata |
| REQ-B2F-005 | `docs/B2F-ORACLE.md` decision | blocked decision artifact, unchanged thresholds and complete next-package evidence |
| REQ-B2F-006 | `docs/B2F-ORACLE.md` oracle record | input/output digests, decoded prefix fields, independent decode and expected-byte equality |
| REQ-M4P-001 | `docs/M4P-CONFIRMATION.md` authority | external immutable confirmation, reviewer authority, question answers, and trace digest in RR |
| REQ-M4P-002 | `docs/M4P-CONFIRMATION.md` complete-record contract | machine package field/result equality and concrete API mapping |
| REQ-M4P-003 | `docs/M4P-CONFIRMATION.md` ownership | ownership-table validator and affirmative external boundary review |
| REQ-M4P-004 | `docs/M4P-CONFIRMATION.md` trace | six complete binding traces for V09/V10/V12 |
| REQ-M4P-005 | `docs/M4P-CONFIRMATION.md` ingress | resolved authorized-`ClientUID` fail-closed trace |
| REQ-M4P-006 | `docs/M4P-CONFIRMATION.md` resume | alternate-source and cross-modality V09 traces |
| REQ-M4P-007 | `docs/M4P-CONFIRMATION.md` receipts | duplicate and lost-final-receipt V10 traces |
| REQ-M4P-008 | `docs/M4P-CONFIRMATION.md` budget/loss | exact/one-short and uncertain-acceptance V12 traces |
| REQ-RELEASE-001 | `docs/RELEASE-RECORD.md` content | release-record schema validation and linked artifacts |
| REQ-RELEASE-002 | `docs/RELEASE-RECORD.md` immutability | URL/commit/digest validator and manual link review |
| REQ-RELEASE-003 | `docs/RELEASE-RECORD.md` gates | generated all-pass gate list |
| REQ-RELEASE-004 | `docs/RELEASE-RECORD.md` final verification | clean-checkout commands, CI, independent digest results |
| REQ-RELEASE-005 | `docs/RELEASE-RECORD.md` tag prohibition | template validator and RR inspection |
| REQ-GOV-001 | `GOVERNANCE.md` normative changes | diff check for specification, matrix, vectors, changelog |
| REQ-GATE-001 | `docs/ROADMAP-v0.1.0.md` status | RR tag-state check |
| REQ-GATE-002 | `docs/ROADMAP-v0.1.0.md` sibling work | immutable sibling commit, green CI, release evidence |
| REQ-GATE-003 | `docs/ROADMAP-v0.1.0.md` experimental security | codec status inspection and SR |
| REQ-GATE-004 | `docs/ROADMAP-v0.1.0.md` release claims | forbidden-claim lint and RR inspection |

## Release-blocking matrix dependencies

Rows may be precisely specified yet lack their required evidence. For v0.1.0,
`REQ-ID-001`, `REQ-CODEC-001`, `REQ-COMPACT-002` through
`REQ-COMPACT-008`, `REQ-REG-004` through `REQ-REG-009`,
`REQ-METRIC-006` through `REQ-METRIC-009`, `REQ-M4P-001` through
`REQ-M4P-008`, `REQ-GATE-002`, and the release-record rows remain incomplete
until their named external or sibling artifacts exist. The release record must
report them as blockers, not skips.

`REQ-REG-003` and the registry/package portion of `REQ-COMPACT-001` are
satisfied by the provisional allocation audit. They do not promote any later
row. `REQ-ID-001` now has current immutable OceanMail application-profile
evidence, but V11 sender/receiver conflict evidence against the exact
specification/profile commits is still required before that row passes.

The newly clarified `REQ-ACCOUNT-003`, `REQ-CONF-003`, `REQ-VEC-006`, and
`REQ-METRIC-010` also remain incomplete until `bempic-reference` publishes a
report and vector/metric artifacts against the specification commit containing
this clarification. Pre-clarification evidence is informative but cannot be
silently reclassified as passing.
