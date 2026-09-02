#!/usr/bin/env node

// Independent, dependency-free checks for release artifacts and schema hashes.
// The Python validator remains authoritative for full link/JCS-fixture checks.

import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("..", import.meta.url));
const readJson = (relative) => JSON.parse(readFileSync(join(root, relative), "utf8"));
const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

function rejectLoneSurrogates(value) {
  for (let index = 0; index < value.length; index += 1) {
    const code = value.charCodeAt(index);
    if (code >= 0xd800 && code <= 0xdbff) {
      const next = value.charCodeAt(index + 1);
      if (!(next >= 0xdc00 && next <= 0xdfff)) throw new Error("lone high surrogate");
      index += 1;
    } else if (code >= 0xdc00 && code <= 0xdfff) {
      throw new Error("lone low surrogate");
    }
  }
}

function canonicalize(value) {
  if (value === null || typeof value === "boolean") return JSON.stringify(value);
  if (typeof value === "number") {
    assert(Number.isFinite(value), "non-finite JSON number");
    return JSON.stringify(value);
  }
  if (typeof value === "string") {
    rejectLoneSurrogates(value);
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) return `[${value.map(canonicalize).join(",")}]`;
  assert(typeof value === "object", `unsupported JCS value: ${typeof value}`);
  const members = Object.keys(value).sort().map((key) => {
    rejectLoneSurrogates(key);
    return `${JSON.stringify(key)}:${canonicalize(value[key])}`;
  });
  return `{${members.join(",")}}`;
}

const fingerprints = readJson("schemas/v0.1/fingerprints.json");
const fingerprintResults = [];
for (const [name, expected] of Object.entries(fingerprints).sort()) {
  const canonical = Buffer.from(canonicalize(readJson(`schemas/v0.1/${name}`)), "utf8");
  const length = Buffer.alloc(4);
  length.writeUInt32BE(canonical.length);
  const actual = createHash("sha256")
    .update(Buffer.from("BEMPIC-SCHEMA-FINGERPRINT-v0.1\0", "utf8"))
    .update(length)
    .update(canonical)
    .digest("hex");
  assert(actual === expected, `${name}: ${actual} != ${expected}`);
  fingerprintResults.push(`${name}:${canonical.length}:${actual}`);
}

const registry = readJson("conformance/v0.1/codec-registry.json");
let next = 0;
for (const range of registry.ranges) {
  assert(range.first === next && range.last >= range.first, "non-contiguous codec range");
  next = range.last + 1;
}
assert(next === 2 ** 32, "codec registry does not cover uint32");
assert(registry.allocations.length === 1, "expected one reviewed v0.1 codec allocation");
const compact = registry.allocations[0];
const compactProfileSha256 =
  "bc82364f7ac2f563bbdc0ea15f3d9b1f9127d6ac88376bf19a6dc642dc731127";
assert(compact.id === 65536 && compact.id_hex === "0x00010000" &&
  compact.revision === 1 && compact.status === "experimental",
"compact public tuple changed");
assert(compact.approved === false && compact.mandatory === false &&
  compact.stable_wire_promise === false && compact.production_security_promise === false,
"experimental codec was promoted");
assert(compact.derived_from_private_candidate === "0xffff0001/2" &&
  compact.public_tuple_vectors_required === true,
"private provenance or public-vector requirement changed");
const actualCompactProfileSha256 = createHash("sha256")
  .update(readFileSync(join(root, compact.profile)))
  .digest("hex");
assert(actualCompactProfileSha256 === compactProfileSha256 &&
  compact.profile_sha256 === compactProfileSha256,
"compact profile digest changed");

const allocation = readJson("conformance/v0.1/experimental-codec-allocation.json");
assert(allocation.decision === "allocate-provisional-experimental" &&
  allocation.allocation.id === 65536 && allocation.allocation.revision === 1 &&
  allocation.allocation.status === "experimental",
"allocation package public tuple changed");
assert(Object.values(allocation.req_reg_003).every((value) => value === "pass"),
  "REQ-REG-003 checklist is incomplete");
assert(allocation.private_candidate_provenance.commit ===
  "cf3485f6606d6462077e8edd1592264c3ce4ca5e" &&
  allocation.private_candidate_provenance.private_id_hex === "0xffff0001" &&
  allocation.private_candidate_provenance.private_revision === 2,
"private compact provenance changed");
assert(allocation.private_candidate_measurements.warm_no_change_bempic_bytes === 35 &&
  allocation.private_candidate_measurements.cold_no_change_bempic_bytes === 75 &&
  allocation.private_candidate_measurements.accepted_as_public_tuple_release_evidence === false &&
  allocation.private_candidate_measurements.public_tuple_regeneration_required === true,
"private measurements changed or were promoted");
assert(allocation.maximum_encoded_sizes.DATA === 1048574 &&
  allocation.maximum_encoded_sizes.generic_content_ceiling === 1048569 &&
  allocation.maximum_encoded_sizes.data_payload_ceiling === 1048524 &&
  allocation.maximum_encoded_sizes.data_payload_one_past_rejected === 1048525 &&
  allocation.maximum_encoded_sizes.outer_record_ceiling === 1048576,
"compact DATA payload ceiling or maximum changed");
assert(allocation.oceanmail_application_evidence.commit ===
  "cc55c1b7d5a03aa2e5cc8cd617f9d1bb7b6a3600" &&
  allocation.oceanmail_application_evidence.application_profile_current === true &&
  allocation.oceanmail_application_evidence.accepted_as_complete_bempic_v11_release_evidence === false,
"OceanMail evidence changed or was over-promoted");

const vectors = readJson("conformance/v0.1/vector-catalog.json");
assert(vectors.catalog.map((entry) => entry.id).join(",") ===
  Array.from({ length: 15 }, (_, index) => `V${String(index + 1).padStart(2, "0")}`).join(","),
"vector IDs are not exactly V01-V15");
const v08 = vectors.catalog.find((entry) => entry.id === "V08");
const v08Points = ["offset-0", "offset-1-percent", "offset-10-percent", "offset-50-percent",
  "offset-90-percent", "final-byte", "post-verify-pre-commit", "post-commit-pre-receipt"];
const v08Restarts = ["sender", "receiver", "both"];
const v08Storage = ["memory", "representation-file", "durable-store"];
const expectedRows = v08Points.flatMap((point, pointIndex) =>
  v08Restarts.map((restart, restartIndex) => ({
    id: `V08-C${String(pointIndex * 3 + restartIndex + 1).padStart(2, "0")}`,
    point,
    restart,
    storage: v08Storage[(pointIndex + restartIndex) % v08Storage.length],
  })));
assert(JSON.stringify(v08.coverage_rows) === JSON.stringify(expectedRows),
  "V08 fixed pairwise covering array changed");
const pairs = (left, right) => new Set(v08.coverage_rows.map((row) => `${row[left]}\0${row[right]}`));
assert(pairs("point", "restart").size === v08Points.length * v08Restarts.length,
  "V08 misses an interruption-point/restart pair");
assert(pairs("point", "storage").size === v08Points.length * v08Storage.length,
  "V08 misses an interruption-point/storage pair");
assert(pairs("restart", "storage").size === v08Restarts.length * v08Storage.length,
  "V08 misses a restart/storage pair");

const metrics = readJson("conformance/v0.1/metrics.json");
assert(metrics.required.length === 18, "expected 18 required metrics");
assert(metrics.semantic_bytes_definition.identity ===
  "semantic_bytes=semantic_bytes_send+semantic_bytes_receive",
"semantic_bytes identity changed");
assert(metrics.semantic_bytes_definition.direction_basis.send ===
  "endpoint-a-to-endpoint-b" &&
  metrics.semantic_bytes_definition.direction_basis.receive ===
  "endpoint-b-to-endpoint-a",
"semantic_bytes direction basis changed");
assert(metrics.semantic_bytes_definition.scope_fields.join(",") ===
  "endpoint_a_binding,endpoint_b_binding" &&
  metrics.semantic_bytes_definition.fixture_fields.includes("representation_descriptor_contribution"),
"semantic_bytes reproducibility fields changed");
assert(metrics.semantic_bytes_definition.excluded.includes("duplicates") &&
  metrics.semantic_bytes_definition.excluded.includes("representation-descriptor-container-and-members") &&
  metrics.semantic_bytes_definition.excluded.includes("lower-layer-retransmissions"),
"semantic_bytes exclusion set is incomplete");
assert(metrics.thresholds.length === 8, "expected eight metric thresholds");
assert(metrics.b2f_comparison.profile ===
  "bempic-v0.1-b2f-text-single-message-v1" &&
  metrics.b2f_comparison.decision_status === "blocked-no-qualified-oracle" &&
  metrics.b2f_comparison.selected_oracle === null &&
  metrics.b2f_comparison.results_claimable === false &&
  metrics.b2f_comparison.thresholds_changed === false,
"B2F metric decision changed or was promoted");

const b2fDecision = readJson("conformance/v0.1/b2f-oracle-decision.json");
assert(b2fDecision.decision.status === "blocked-no-qualified-oracle" &&
  b2fDecision.decision.selected_oracle === null &&
  b2fDecision.decision.release_gate === "blocked" &&
  b2fDecision.decision.thresholds_changed === false &&
  b2fDecision.decision.results_claimable === false,
"B2F oracle decision changed or was promoted");
const b2fProfile = b2fDecision.comparison_profile;
assert(b2fProfile.id === "bempic-v0.1-b2f-text-single-message-v1" &&
  b2fProfile.fixture_scope === "one-message-per-independent-no-fault-run" &&
  b2fProfile.batching === "forbidden",
"B2F fixture scope changed");
assert(b2fProfile.lzhuf.behavior_reference.commit ===
  "dbe96569817018e66e0e5f6add40eed12adc9fd7" &&
  b2fProfile.lzhuf.lzss_ring_octets === 2048 &&
  b2fProfile.lzhuf.lookahead_octets === 60 &&
  b2fProfile.lzhuf.match_threshold === 2 &&
  b2fProfile.lzhuf.crc.name === "CRC-16/XMODEM" &&
  b2fProfile.lzhuf.crc.coverage === "four-octet-length-plus-compressed-bitstream",
"B2F LZHUF behavior changed");
assert(b2fProfile.b2f_envelope.data_block_payload_octets === 250 &&
  b2fProfile.b2f_envelope.directions.identity ===
    "b2f_total_bytes=b2f_send_bytes+b2f_receive_bytes" &&
  b2fProfile.b2f_envelope.included.includes("complete-lzhuf-image") &&
  b2fProfile.b2f_envelope.excluded.includes("modem-carrier-link-framing"),
"B2F envelope or byte-count boundary changed");
assert(b2fDecision.required_corpus_manifest.status === "not-yet-published" &&
  b2fDecision.required_corpus_manifest.digest === null &&
  b2fDecision.candidates.length === 5 &&
  b2fDecision.candidates.every((candidate) => candidate.qualified === false),
"B2F corpus or candidate was promoted without evidence");
const paclink = b2fDecision.candidates.find((candidate) =>
  candidate.id === "paclink-unix-lzhuf-1");
assert(paclink.commit === "cc7b2f9474959a70856cabaf812bfce53d2da145" &&
  paclink.license === "GPL-2.0-or-later" &&
  paclink.incorporation === "forbidden-project-policy" &&
  paclink.linking === "forbidden-project-policy" &&
  paclink.ci_use === "separately-obtained-process-only",
"B2F GPL process boundary changed");
assert(b2fDecision.thresholds[0].value === 10 &&
  b2fDecision.thresholds[1].value === 5,
"B2F compactness thresholds changed");
assert(vectors.external_benchmarks.length === 1 &&
  vectors.external_benchmarks[0].status === "blocked" &&
  vectors.external_benchmarks[0].selected_oracle === null &&
  vectors.external_benchmarks[0].corpus_digest === null,
"external B2F benchmark was promoted without evidence");

const m4pCommit = "2eca9e8f57d43dab250cc26c1bbf2d255e3331de";
const m4pTree = "b06d1830c6156ead535542d9ff4c0a5acbfd1545";
const m4pProfile = "bempic-m4p-opaque-record-v0.1-review";
const m4pTraceIds = [
  "M4P-V09-AUTHORIZED-SOURCE",
  "M4P-V09-CROSS-MODALITY",
  "M4P-V10-DUPLICATE",
  "M4P-V10-LOST-FINAL-RECEIPT",
  "M4P-V12-BUDGET",
  "M4P-V12-CONNECTION-LOSS",
];
const m4p = readJson("conformance/v0.1/m4p-binding-review-package.json");
const m4pCanonicalDigest = createHash("sha256")
  .update(Buffer.from(canonicalize(m4p), "utf8"))
  .digest("hex");
assert(m4pCanonicalDigest ===
  "b1908c3d86522410454a375054310c75282a4a34dc29689d887a2a4406651e4e",
"M4P review package canonical digest changed");
assert(m4p.package_status === "ready-for-external-review-not-submitted" &&
  m4p.binding_profile.id === m4pProfile &&
  m4p.binding_profile.approval_status === "unconfirmed" &&
  m4p.external_confirmation.status === "blocked-not-requested" &&
  m4p.external_confirmation.upstream_url === null &&
  m4p.external_confirmation.reviewer === null &&
  m4p.external_confirmation.approved === false,
"M4P package status or external confirmation was promoted");
assert(m4p.authoritative_m4p_source.commit === m4pCommit &&
  m4p.authoritative_m4p_source.tree === m4pTree &&
  m4p.authoritative_m4p_source.license === "CC-BY-4.0" &&
  m4p.authoritative_m4p_source.implementation_source_status ===
    "announced-not-publicly-released" &&
  m4p.authoritative_m4p_source.source_files.length === 14 &&
  m4p.authoritative_m4p_source.source_files.every((source) =>
    source.url.includes(m4pCommit) && source.blob.length === 40),
"M4P source identity, license, or immutable inventory changed");
assert(m4p.copyright_and_repository_boundary.copied_m4p_code === false &&
  m4p.copyright_and_repository_boundary.copied_agpl_code === false &&
  m4p.copyright_and_repository_boundary.copied_lookup_tables_or_fixtures === false &&
  m4p.copyright_and_repository_boundary.substantial_source_text_copied === false,
"M4P copyright/repository boundary changed");
const m4pInterface = m4p.opaque_record_interface;
assert(m4pInterface.boundary ===
  "one-complete-canonical-bempic-operation-per-m4p-application-message-payload" &&
  m4pInterface.partial_operation_submission === "forbidden" &&
  m4pInterface.m4p_payload_interpretation === "opaque" &&
  m4pInterface.bempic_operation_fields_visible_to_m4p.length === 0,
"M4P opaque complete-record interface changed");
assert(m4pInterface.submit_result.status_values.join(",") === [
  "accepted", "not-accepted-record-too-large", "not-accepted-invalid-destination",
  "not-accepted-binding-unconfigured", "not-accepted-backpressure",
  "not-accepted-local-error", "acceptance-unknown",
].join(",") &&
  m4pInterface.submit_result.m4p_api_mapping_status ===
    "external-confirmation-required" &&
  m4pInterface.lower_layer_observations.consumed_as_bempic_receipt.length === 0,
"M4P submit results or receipt separation changed");
assert(m4pInterface.capacity_and_cost.bempic_outer_record_ceiling_octets === 1048576 &&
  m4pInterface.capacity_and_cost.m4p_packet_payload_length_ceiling_octets === 65535 &&
  m4pInterface.capacity_and_cost.m4p_safe_complete_application_record_ceiling_octets === null &&
  m4pInterface.capacity_and_cost.safe_ceiling_status ===
    "unresolved-external-confirmation-required" &&
  m4pInterface.capacity_and_cost.m4p_opportunity_visibility_to_bempic ===
    "none-prescribed",
"M4P maximum or opportunity uncertainty was silently resolved");
assert(m4p.receipt_rules.m4p_delivery_evidence_is_bempic_receipt === false &&
  m4p.ownership.find((item) => item.concern === "custody-transfer").owner ===
    "none-m4p-deliberately-omits-it" &&
  m4p.binding_traces.map((trace) => trace.id).join(",") === m4pTraceIds.join(",") &&
  m4p.open_review_questions.length === 8 &&
  m4p.open_review_questions.every((question) => question.status === "open-blocking") &&
  m4p.release_effect.m4p_binding_gate === "blocked" &&
  m4p.release_effect.unrelated_gates_changed === false,
"M4P ownership, traces, questions, or release blocker changed");
for (const [vectorId, traceIds] of Object.entries({
  V09: m4pTraceIds.slice(0, 2),
  V10: m4pTraceIds.slice(2, 4),
  V12: m4pTraceIds.slice(4, 6),
})) {
  assert(vectors.catalog.find((entry) => entry.id === vectorId)
    .m4p_binding_trace_ids.join(",") === traceIds.join(","),
  `${vectorId} M4P trace mapping changed`);
}
for (const trace of m4p.binding_traces) {
  const catalogEntry = vectors.catalog.find((entry) => entry.id === trace.vector);
  const hasCase = Object.hasOwn(trace, "case");
  const hasCases = Object.hasOwn(trace, "cases");
  const caseReferences = hasCases ? trace.cases : [trace.case];
  assert(catalogEntry && hasCase !== hasCases && Array.isArray(caseReferences) &&
    caseReferences.length > 0 &&
    new Set(caseReferences).size === caseReferences.length &&
    caseReferences.every((caseId) => catalogEntry.cases.includes(caseId)),
  `${trace.id} references an undeclared vector case`);
}
assert(metrics.m4p_binding_accounting.profile === m4pProfile &&
  metrics.m4p_binding_accounting.external_confirmation_complete === false &&
  metrics.m4p_binding_accounting.bempic_tx_charge["acceptance-unknown"] ===
    "record-octets-once-conservative-debit" &&
  metrics.m4p_binding_accounting.carrier_bytes ===
    "unavailable-unless-externally-confirmed-implementation-contract",
"M4P accounting boundary changed or was promoted");

const release = readJson("conformance/v0.1/release-record-template.json");
assert(release.release_state === "not-ready" && release.tag === null,
  "release template made a premature release claim");
assert(release.interruption_coverage.required_rows === 24 &&
  release.interruption_coverage.pair_coverage_passed === false,
"release template interruption gate changed");
assert(release.current_reference_evidence.evidence_commit ===
  "cf3485f6606d6462077e8edd1592264c3ce4ca5e" &&
  release.current_reference_evidence.observed_status === "blocked-not-conformant" &&
  release.current_reference_evidence.accepted_for_experimental_allocation === true &&
  release.current_reference_evidence.accepted_as_release_evidence === false &&
  release.current_reference_evidence.requires_rerun_against_allocated_public_tuple === true,
"blocked reference checkpoint changed or was promoted");
assert(release.codec.id === 65536 && release.codec.revision === 1 &&
  release.codec.status === "experimental" && release.codec.approved === false &&
  release.codec.mandatory === false && release.codec.public_tuple_vectors_complete === false,
"release record codec state changed or was promoted");
assert(release.oceanmail_application_evidence.commit ===
  "cc55c1b7d5a03aa2e5cc8cd617f9d1bb7b6a3600" &&
  release.oceanmail_application_evidence.complete_v11_release_evidence === false,
"release record OceanMail evidence changed or was over-promoted");
assert(release.b2f_oracle.decision_status === "blocked-no-qualified-oracle" &&
  release.b2f_oracle.identity === null &&
  release.b2f_oracle.executable_digest === null &&
  release.b2f_oracle.corpus_digest === null &&
  release.b2f_oracle.results_digest === null &&
  release.b2f_oracle.thresholds_changed === false,
"release record B2F oracle changed or was promoted");
assert(release.m4p_confirmation.review_package_status ===
  "ready-for-external-review-not-submitted" &&
  release.m4p_confirmation.review_package_digest ===
    `sha256:${m4pCanonicalDigest}` &&
  release.m4p_confirmation.package_m4p_commit === m4pCommit &&
  release.m4p_confirmation.external_confirmation_status === "blocked-not-requested" &&
  release.m4p_confirmation.upstream_url === null &&
  release.m4p_confirmation.reviewer === null &&
  release.m4p_confirmation.required_trace_ids.join(",") === m4pTraceIds.join(",") &&
  release.m4p_confirmation.all_required_traces_passed === false &&
  release.m4p_confirmation.approved === false,
"release record M4P package or blocked confirmation state changed");

console.log(`Independent Node verification passed (Node ${process.version}).`);
for (const result of fingerprintResults) console.log(`fingerprint MATCH ${result}`);
console.log("codec ranges cover uint32; compact 0x00010000/1 profile MATCH; V01-V15 and 24 V08 rows present; 18 metrics; 8 thresholds; B2F oracle blocked; M4P package unconfirmed with 6 traces; release not-ready");
