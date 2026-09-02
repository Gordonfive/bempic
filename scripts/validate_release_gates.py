#!/usr/bin/env python3
"""Validate v0.1 release-gate registries, catalogs, and MUST coverage."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NORMATIVE_DOCS = (
    "SPECIFICATION.md",
    "GOVERNANCE.md",
    "docs/ARCHITECTURE.md",
    "docs/REPOSITORY-BOUNDARY.md",
    "docs/ROADMAP-v0.1.0.md",
    "docs/SECURITY-MODEL.md",
    "docs/TEST-VECTORS.md",
    "docs/CONFORMANCE.md",
    "docs/REGISTRIES.md",
    "docs/METRICS.md",
    "docs/B2F-ORACLE.md",
    "docs/M4P-CONFIRMATION.md",
    "docs/RELEASE-RECORD.md",
    "docs/codecs/EXPERIMENTAL-COMPACT-v0.1.md",
)
REQ_RE = re.compile(r"\[?(REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*)\]?")
MUST_RE = re.compile(r"\bMUST(?: NOT)?\b")

V08_CASES = [
    "offset-0",
    "offset-1-percent",
    "offset-10-percent",
    "offset-50-percent",
    "offset-90-percent",
    "final-byte",
    "post-verify-pre-commit",
    "post-commit-pre-receipt",
]
V08_RESTART_PARTIES = ["sender", "receiver", "both"]
V08_STORAGE_SURFACES = ["memory", "representation-file", "durable-store"]

COMPACT_CODEC_ID = 65536
COMPACT_CODEC_REVISION = 1
COMPACT_PROFILE = "docs/codecs/EXPERIMENTAL-COMPACT-v0.1.md"
COMPACT_PROFILE_SHA256 = "bc82364f7ac2f563bbdc0ea15f3d9b1f9127d6ac88376bf19a6dc642dc731127"
COMPACT_PRIVATE_COMMIT = "cf3485f6606d6462077e8edd1592264c3ce4ca5e"
COMPACT_PRIVATE_TUPLE = "0xffff0001/2"
OCEANMAIL_PROFILE_COMMIT = "cc55c1b7d5a03aa2e5cc8cd617f9d1bb7b6a3600"
B2F_DECISION_PATH = "conformance/v0.1/b2f-oracle-decision.json"
B2F_PROFILE = "bempic-v0.1-b2f-text-single-message-v1"
B2F_ARSFI_COMMIT = "dbe96569817018e66e0e5f6add40eed12adc9fd7"
B2F_WL2K_COMMIT = "efde6fbcb7bc8d6519fd8018ec544c793d4ef48d"
B2F_PACLINK_COMMIT = "cc7b2f9474959a70856cabaf812bfce53d2da145"


def expected_v08_coverage_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for point_index, point in enumerate(V08_CASES):
        for restart_index, restart in enumerate(V08_RESTART_PARTIES):
            rows.append(
                {
                    "id": f"V08-C{len(rows) + 1:02d}",
                    "point": point,
                    "restart": restart,
                    "storage": V08_STORAGE_SURFACES[
                        (point_index + restart_index) % len(V08_STORAGE_SURFACES)
                    ],
                }
            )
    return rows


V08_EVIDENCE_FIELDS = [
    "row_id", "fixture_digest", "trace_digest", "encoded_length",
    "interruption_point", "computed_prefix", "restart_party",
    "storage_surface", "storage_backend", "durable_state_before",
    "recovered_state", "recovered_prefix", "first_resumed_offset",
    "new_payload_bytes", "duplicate_payload_bytes",
    "retransmitted_durable_prefix_bytes", "receipt_state_before",
    "receipt_state_after", "final_content_digest", "final_representation_id",
    "final_decode", "result",
]
V08_PASS_CRITERIA = [
    "interruption-reached-exactly-once",
    "volatile-state-discarded-when-named",
    "recovered-state-not-ahead",
    "no-false-prefix",
    "no-false-receipt",
    "first-resumed-offset-equals-authoritative-prefix",
    "duplicate-and-retransmission-counters-exact",
    "exact-reconstruction-after-resume",
    "positive-receipt-after-durable-commit",
    "pair-coverage-complete",
    "backend-specific-triples-covered-when-applicable",
]

EXPECTED_VECTOR_REQUIREMENTS = {
    "V01": {
        "cases": ["empty", "equal-warm-100", "equal-cold-100"],
        "assertions": ["no-object-payload", "warm-no-change-metric", "cold-no-change-metric"],
        "blocked_by": ["public-codec-vector-regeneration"],
    },
    "V02": {
        "cases": ["known-checkpoint-100-plus-1"],
        "assertions": ["new-manifest-only", "zero-retransmitted-prior-manifest-bytes"],
        "blocked_by": ["public-codec-vector-regeneration"],
    },
    "V03": {
        "cases": ["inventory-257-pages-128-128-1", "reopen-after-page-1"],
        "assertions": ["deterministic-page-order", "durable-cursor", "target-digest-consistent"],
    },
    "V04": {
        "cases": ["tiny", "typical", "international-nfc", "reply-chain", "absent-subject", "maximum-recipients", "maximum-parts", "every-maximum-metadata-length"],
        "maximum_fields": ["recipients", "parts", "representations-per-part", "sender-octets", "recipient-octets", "subject-octets", "filename-octets", "media-type-octets", "codec-parameter-octets"],
        "assertions": ["exact-reconstruction", "bounds-before-mutation", "nfc-canonical"],
    },
    "V05": {
        "cases": ["body-full-preview", "attachment-metadata-unselected"],
        "assertions": ["one-body-representation-selected", "zero-unselected-attachment-payload-bytes"],
    },
    "V06": {
        "cases": ["compressible-selected", "incompressible-selected"],
        "assertions": ["exact-reconstruction", "declared-encoded-length", "digest-and-id-verified"],
    },
    "V07": {
        "cases": ["empty-representation", "one-byte-representation", "maximum-data-payload", "maximum-representation"],
        "bound_sources": ["negotiated-max-data-payload-octets", "core-max-prepared-representation-octets", "codec-max-encoded-size"],
        "assertions": ["exact-size-equals-encoded-length", "one-past-bound-rejected-before-allocation"],
    },
    "V08": {
        "cases": V08_CASES,
        "prefix_percentage_points": [0, 1, 10, 50, 90],
        "prefix_offset_formula": "floor(encoded_length*percentage/100)",
        "minimum_encoded_length": 100,
        "point_definitions": {
            "final-byte": "prefix-length-L-durable-before-verification",
            "post-verify-pre-commit": "verified-state-durable-not-committed",
            "post-commit-pre-receipt": "committed-state-durable-no-positive-receipt-durable-or-emitted",
        },
        "restart_parties": V08_RESTART_PARTIES,
        "storage_surfaces": V08_STORAGE_SURFACES,
        "coverage_model": "fixed-pairwise-covering-array-v0.1",
        "full_cartesian_required": False,
        "conditional_additional_coverage": "all-affected-triples-for-point-restart-or-backend-specific-behavior",
        "coverage_rows": expected_v08_coverage_rows(),
        "evidence_fields": V08_EVIDENCE_FIELDS,
        "pass_criteria": V08_PASS_CRITERIA,
        "assertions": ["reopen-last-durable-state", "no-false-prefix", "no-false-receipt", "exact-reconstruction-after-resume", "pairwise-all-axis-pairs", "complete-row-evidence"],
    },
    "V09": {
        "cases": ["alternate-authorized-source", "alternate-carrier"],
        "assertions": ["identical-prepared-bytes", "zero-fully-durable-prefix-retransmission", "resume-metrics-recorded"],
        "blocked_by": ["m4p-binding-review"],
    },
    "V10": {
        "cases": ["duplicate-offer", "duplicate-data", "duplicate-page", "duplicate-receipt", "lost-final-receipt"],
        "assertions": ["idempotent-state", "duplicate-bytes-counted", "no-duplicate-application-effect"],
    },
    "V11": {
        "cases": ["corrupt-final-byte", "conflicting-overlap", "gap", "false-length-short", "false-length-long", "false-digest", "false-representation-id", "object-id-metadata-conflict"],
        "expected_outcomes": {
            "corrupt-final-byte": "INTEGRITY_FAILURE",
            "conflicting-overlap": "METADATA_CONFLICT",
            "gap": "RANGE_INVALID",
            "false-length-short": "RANGE_INVALID",
            "false-length-long": "PARTIAL-no-positive-receipt",
            "false-digest": "INTEGRITY_FAILURE",
            "false-representation-id": "INTEGRITY_FAILURE",
            "object-id-metadata-conflict": "METADATA_CONFLICT",
        },
        "assertions": ["expected-outcome", "no-positive-receipt", "unrelated-committed-state-usable"],
    },
    "V12": {
        "cases": ["total-one-byte-short", "total-exact", "send-one-byte-short", "send-exact", "receive-one-byte-short", "receive-exact"],
        "operation_types": ["CAPABILITIES", "SUMMARY", "OFFER", "REQUEST", "DATA", "RECEIPT", "FAILURE"],
        "budget_domains": ["total", "send", "receive"],
        "relative_budgets": [-1, 0],
        "assertions": ["complete-operation-only", "zero-quote-error", "directional-accounting-identity"],
    },
    "V13": {
        "cases": ["compatible-tuple", "incompatible-protocol", "incompatible-schema", "incompatible-codec", "preference-tie", "stale-cache-recovery", "unknown-optional-extension", "unknown-critical-extension"],
        "assertions": ["deterministic-highest-common-tuple", "critical-rejected-before-mutation", "optional-skipped-without-side-effect"],
    },
    "V14": {
        "cases": ["offer-page-commit", "prefix-length-update", "final-byte-persist", "digest-verification", "object-commit", "receipt-commit"],
        "fault_sides": ["before", "after"],
        "storage_surfaces": ["representation-file", "durable-store"],
        "evidence_fields": ["case", "fault_side", "storage_surface", "storage_backend", "fault_reached", "durable_state_before", "recoverable_prefix", "recovered_state", "recovered_prefix", "receipt_state", "unrelated_committed_state", "result"],
        "pass_criteria": ["storage-failure-scoped", "fault-reached-exactly-once", "recovered-not-ahead", "no-false-prefix", "no-false-receipt", "unrelated-committed-state-usable"],
        "assertions": ["storage-failure-scoped", "reopen-not-ahead", "no-false-receipt"],
    },
    "V15": {
        "cases": ["UNSUPPORTED_VERSION", "UNSUPPORTED_SCHEMA", "UNSUPPORTED_CODEC", "UNSUPPORTED_CRITICAL_EXTENSION", "MALFORMED_OPERATION", "LIMIT_EXCEEDED", "UNKNOWN_OBJECT", "METADATA_CONFLICT", "RANGE_INVALID", "INTEGRITY_FAILURE", "STORAGE_FAILURE", "POLICY_REJECTED", "CHECKPOINT_UNKNOWN"],
        "advertised_retryable_flags": [False, True],
        "assertions": ["exact-failure-code", "retry-classification", "bounded-retry", "scoped-mutation"],
    },
}

EXPECTED_SEMANTIC_BYTES_DEFINITION = {
    "counter": "semantic_bytes",
    "directional_counters": ["semantic_bytes_send", "semantic_bytes_receive"],
    "identity": "semantic_bytes=semantic_bytes_send+semantic_bytes_receive",
    "direction_basis": {
        "endpoint_roles": ["endpoint-a", "endpoint-b"],
        "send": "endpoint-a-to-endpoint-b",
        "receive": "endpoint-b-to-endpoint-a",
        "binding": "declared-once-per-measurement-scope-and-stable-across-ownership-reversals-restarts-sources-carriers-and-reporters",
    },
    "count_key": ["direction", "representation_id"],
    "count_event": "first-accepted-application-selection-in-scope",
    "scope_fields": ["endpoint_a_binding", "endpoint_b_binding"],
    "scalar_octets": {
        "octets": "length",
        "utf8-or-ascii": "normalized-utf8-length",
        "uint32": 4,
        "uint64": 8,
        "boolean-or-enum": 1,
        "absent-nullable": 0,
        "array-or-record": "sum-present-children",
    },
    "included": [
        "selected-decoded-application-scalar-values",
        "selected-manifest-application-fields-outside-representation-descriptors",
    ],
    "excluded": [
        "container-counts", "field-names", "tags", "presence-indicators",
        "length-prefixes", "representation-descriptor-container-and-members",
        "encoded-representation-payload",
        "deferred-or-unselected-payload", "duplicates", "retransmissions",
        "matching-overlap", "codec-padding",
        "bempic-operation-metadata-and-framing", "carrier-bytes", "m4p-bytes",
        "datalink-bytes", "fec", "lower-layer-retransmissions",
    ],
    "fixture_fields": [
        "direction", "source_endpoint_role", "destination_endpoint_role",
        "representation_id", "schema_fingerprint",
        "semantic_fixture_path", "semantic_fixture_sha256",
        "semantic_fixture_octets", "semantic_octets",
        "representation_descriptor_contribution", "selection_event",
    ],
}

EXPECTED_REQUIRED_METRICS = [
    "semantic_bytes",
    "semantic_bytes_send",
    "semantic_bytes_receive",
    "bempic_total_bytes",
    "bempic_operation_bytes_send",
    "bempic_operation_bytes_receive",
    "representation_payload_bytes",
    "useful_committed_bytes",
    "duplicate_bempic_bytes",
    "duplicate_representation_payload_bytes",
    "unselected_representation_payload_bytes",
    "retransmitted_durable_prefix_bytes",
    "retransmitted_prior_manifest_bytes",
    "resume_control_bytes",
    "bempic_bytes_to_first_body_payload_octet",
    "bempic_bytes_to_first_body_commit",
    "preflight_quoted_bempic_bytes",
    "quote_error_bytes",
]

EXPECTED_METRIC_IDENTITIES = [
    "semantic_bytes=semantic_bytes_send+semantic_bytes_receive",
    "bempic_total_bytes=bempic_operation_bytes_send+bempic_operation_bytes_receive",
]

EXPECTED_METRIC_THRESHOLDS = [
    {"id": "warm-no-change", "vector": "V01", "case": "equal-warm-100", "metric": "bempic_total_bytes", "operator": "<=", "value": 64, "aggregation": "each-run"},
    {"id": "cold-no-change", "vector": "V01", "case": "equal-cold-100", "metric": "bempic_total_bytes", "operator": "<=", "value": 128, "aggregation": "each-run"},
    {"id": "known-append-no-old-manifest", "vector": "V02", "case": "known-checkpoint-100-plus-1", "metric": "retransmitted_prior_manifest_bytes", "operator": "=", "value": 0, "aggregation": "each-run"},
    {"id": "no-unselected-payload", "vector": "V05", "case": "*", "metric": "unselected_representation_payload_bytes", "operator": "=", "value": 0, "aggregation": "each-run"},
    {"id": "exact-no-fault-quote", "vector": "V12", "case": "*", "metric": "quote_error_bytes", "operator": "=", "value": 0, "aggregation": "each-run"},
    {"id": "resume-no-durable-prefix-resend", "vector": "V09", "case": "*", "metric": "retransmitted_durable_prefix_bytes", "operator": "=", "value": 0, "aggregation": "each-run-with-authoritative-prefix"},
    {"id": "b2f-median-compactness", "vector": "external-text-corpus", "case": "*", "metric": "candidate_reduction_percent", "operator": ">=", "value": 10, "aggregation": "median"},
    {"id": "b2f-per-fixture-regression", "vector": "external-text-corpus", "case": "*", "metric": "candidate_increase_percent", "operator": "<=", "value": 5, "aggregation": "each-run-or-accepted-justification"},
]

EXPECTED_B2F_COMPARISON = {
    "profile": B2F_PROFILE,
    "decision_artifact": B2F_DECISION_PATH,
    "decision_status": "blocked-no-qualified-oracle",
    "selected_oracle": None,
    "corpus_digest": None,
    "results_claimable": False,
    "directional_identity": "b2f_total_bytes=b2f_send_bytes+b2f_receive_bytes",
    "candidate_reduction_percent": "100*(b2f_total_bytes-bempic_total_bytes)/b2f_total_bytes",
    "candidate_increase_percent": "100*(bempic_total_bytes-b2f_total_bytes)/b2f_total_bytes",
    "ratio_representation": "signed-integer-numerator-and-positive-integer-denominator",
    "median": "exact-median-of-per-fixture-reduction-rationals",
    "thresholds_changed": False,
}

EXPECTED_EXTERNAL_BENCHMARKS = [
    {
        "id": "external-text-corpus",
        "profile": B2F_PROFILE,
        "decision_artifact": B2F_DECISION_PATH,
        "status": "blocked",
        "selected_oracle": None,
        "corpus_digest": None,
        "blocked_by": [
            "b2f-oracle-selection",
            "prescribed-corpus-publication",
            "independent-reproduction",
        ],
        "threshold_ids": [
            "b2f-median-compactness",
            "b2f-per-fixture-regression",
        ],
    }
]

EXPECTED_B2F_THRESHOLDS = [
    {
        "id": "b2f-median-compactness",
        "metric": "candidate_reduction_percent",
        "operator": ">=",
        "value": 10,
        "aggregation": "median",
    },
    {
        "id": "b2f-per-fixture-regression",
        "metric": "candidate_increase_percent",
        "operator": "<=",
        "value": 5,
        "aggregation": "each-run-or-accepted-justification",
    },
]


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(relative: str) -> object:
    path = ROOT / relative
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_must_matrix() -> int:
    source_ids: dict[str, str] = {}
    must_paragraphs = 0
    for relative in NORMATIVE_DOCS:
        text = (ROOT / relative).read_text(encoding="utf-8")
        for req_id in REQ_RE.findall(text):
            if req_id in source_ids:
                fail(f"duplicate requirement ID {req_id}: {source_ids[req_id]} and {relative}")
            source_ids[req_id] = relative
        for paragraph in re.split(r"\n\s*\n", text):
            if not MUST_RE.search(paragraph):
                continue
            if "BCP 14" in paragraph and "interpreted" in paragraph:
                continue
            must_paragraphs += 1
            if not REQ_RE.search(paragraph):
                excerpt = " ".join(paragraph.split())[:160]
                fail(f"unidentified MUST paragraph in {relative}: {excerpt}")

    matrix_text = (ROOT / "docs/CONFORMANCE-MATRIX.md").read_text(encoding="utf-8")
    matrix_rows: dict[str, str] = {}
    for line in matrix_text.splitlines():
        if not line.startswith("| REQ-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3:
            fail(f"malformed conformance matrix row: {line}")
        req_id, source, evidence = cells
        if req_id in matrix_rows:
            fail(f"duplicate matrix row {req_id}")
        if not source or not evidence:
            fail(f"empty source/evidence for {req_id}")
        matrix_rows[req_id] = evidence

    missing = sorted(set(source_ids) - set(matrix_rows))
    extra = sorted(set(matrix_rows) - set(source_ids))
    if missing:
        fail(f"requirements missing matrix rows: {', '.join(missing)}")
    if extra:
        fail(f"matrix rows without source requirements: {', '.join(extra)}")
    return must_paragraphs


def validate_codec_registry() -> None:
    registry = load_json("conformance/v0.1/codec-registry.json")
    if registry.get("format") != "bempic-codec-registry-v0.1":
        fail("unexpected codec registry format")
    ranges = registry.get("ranges")
    if not isinstance(ranges, list) or not ranges:
        fail("codec registry ranges missing")
    expected_first = 0
    for item in ranges:
        first, last = item.get("first"), item.get("last")
        if first != expected_first or not isinstance(last, int) or last < first:
            fail(f"codec ranges are not contiguous at {item!r}")
        expected_first = last + 1
    if expected_first != 2**32:
        fail("codec ranges do not cover the complete uint32 domain")
    allocations = registry.get("allocations")
    if not isinstance(allocations, list):
        fail("codec allocations must be a list")
    pairs: set[tuple[int, int]] = set()
    for allocation in allocations:
        codec_id = allocation.get("id")
        revision = allocation.get("revision")
        status = allocation.get("status")
        pair = (codec_id, revision)
        if pair in pairs:
            fail(f"duplicate codec allocation {pair}")
        pairs.add(pair)
        if isinstance(codec_id, bool) or not isinstance(codec_id, int) or not 0 <= codec_id < 2**32:
            fail(f"invalid codec allocation {allocation!r}")
        if isinstance(revision, bool) or not isinstance(revision, int) or not 1 <= revision < 2**32:
            fail(f"invalid codec revision {allocation!r}")
        range_class = next(item["class"] for item in ranges if item["first"] <= codec_id <= item["last"])
        allowed_classes = {
            "experimental": {"experimental"},
            "approved": {"standards-action"},
            "mandatory": {"standards-action"},
            "deprecated": {"experimental", "standards-action"},
        }
        if status not in allowed_classes or range_class not in allowed_classes[status]:
            fail(f"codec allocation status/range mismatch {allocation!r}")

    if len(allocations) != 1:
        fail("v0.1 registry must contain exactly the reviewed compact allocation")
    compact = allocations[0]
    expected_compact = {
        "id": COMPACT_CODEC_ID,
        "id_hex": "0x00010000",
        "revision": COMPACT_CODEC_REVISION,
        "name": "bempic-compact-operation-v0.1",
        "status": "experimental",
        "owner": "Gordonfive/bempic maintainers",
        "contact": "https://github.com/Gordonfive/bempic/issues",
        "profile": COMPACT_PROFILE,
        "profile_sha256": COMPACT_PROFILE_SHA256,
        "allocation_evidence": "conformance/v0.1/experimental-codec-allocation.json",
        "canonical_parameters_hex": "",
        "derived_from_private_candidate": COMPACT_PRIVATE_TUPLE,
        "approved": False,
        "mandatory": False,
        "stable_wire_promise": False,
        "production_security_promise": False,
        "public_tuple_vectors_required": True,
    }
    if compact != expected_compact:
        fail("reviewed compact codec allocation changed")


def validate_experimental_codec_allocation() -> None:
    profile_path = ROOT / COMPACT_PROFILE
    actual_profile_sha256 = hashlib.sha256(profile_path.read_bytes()).hexdigest()
    if actual_profile_sha256 != COMPACT_PROFILE_SHA256:
        fail("compact profile digest differs from the reviewed allocation")

    data = load_json("conformance/v0.1/experimental-codec-allocation.json")
    if data.get("format") != "bempic-experimental-codec-allocation-v0.1":
        fail("unexpected experimental codec allocation format")
    if data.get("decision") != "allocate-provisional-experimental":
        fail("experimental codec allocation decision changed")
    allocation = data.get("allocation", {})
    expected_allocation = {
        "name": "bempic-compact-operation-v0.1",
        "id": COMPACT_CODEC_ID,
        "id_hex": "0x00010000",
        "revision": COMPACT_CODEC_REVISION,
        "status": "experimental",
        "owner": "Gordonfive/bempic maintainers",
        "contact": "https://github.com/Gordonfive/bempic/issues",
        "approved": False,
        "mandatory": False,
        "stable_wire_promise": False,
        "production_security_promise": False,
    }
    if allocation != expected_allocation:
        fail("allocation package public tuple or status changed")
    profile = data.get("profile", {})
    if profile.get("path") != COMPACT_PROFILE or profile.get("sha256") != COMPACT_PROFILE_SHA256:
        fail("allocation package profile path or digest changed")
    if profile.get("canonical_parameters_hex") != "":
        fail("compact codec canonical parameters must remain empty")

    collision = data.get("collision_check", {})
    if collision != {
        "range_class": "experimental",
        "range_first": 65536,
        "range_last": 2147483647,
        "allocations_before_request": [],
        "selected_first_free_id": COMPACT_CODEC_ID,
        "collision_free": True,
    }:
        fail("experimental allocation collision evidence changed")
    req_reg_003 = data.get("req_reg_003", {})
    expected_checklist = {
        "stable_name", "owner_and_contact", "exact_id_and_initial_revision",
        "public_profile", "canonical_parameters", "field_and_collection_bounds",
        "maximum_encoded_size_tables", "draft_worst_case_proof",
        "draft_valid_and_invalid_vectors", "security_analysis", "license_analysis",
        "registry_collision_check", "experimental_replacement_warning", "result",
    }
    if set(req_reg_003) != expected_checklist or any(
        value != "pass" for value in req_reg_003.values()
    ):
        fail("REQ-REG-003 allocation checklist is incomplete")
    if data.get("maximum_encoded_sizes") != {
        "CAPABILITIES": 34360,
        "SUMMARY": 33078,
        "OFFER": 186787,
        "REQUEST": 39184,
        "DATA": 1048574,
        "RECEIPT": 33339,
        "FAILURE": 33324,
        "generic_content_ceiling": 1048569,
        "data_payload_ceiling": 1048524,
        "data_payload_one_past_rejected": 1048525,
        "outer_record_ceiling": 1048576,
        "outer_one_past_rejected": 1048577,
    }:
        fail("compact maximum-size table or DATA payload ceiling changed")

    provenance = data.get("private_candidate_provenance", {})
    if (
        provenance.get("commit") != COMPACT_PRIVATE_COMMIT
        or provenance.get("private_id_hex") != "0xffff0001"
        or provenance.get("private_revision") != 2
        or provenance.get("ci_conclusion") != "success"
    ):
        fail("private compact candidate provenance changed")
    expected_hashes = {
        "profile": "0633ed81272a89d085ceb8ae01aef82ac1749a9babe2fac9b59d0d1f3529fce8",
        "size_proof_and_measurements": "fd3461c674921b9730c773f0eef01d34dcc8e60a472ca1bb2ec1f3027de2f525",
        "draft_vectors": "5edd10847be60cef384be726d7f3d83c6d78618ec38ce56db469cf24e794b8fb",
        "independent_language_verifier": "75c00d8e7af789a889669910cf945eaa7596d81054b6105a916475df02583dc4",
        "malformed_property_report": "5716f157c23fa631e748acb48f20f68ae28326b6251e4ecf1c0c77458155401d",
        "conformance_report": "40bbb7544a8b2c1eee1e9ac74fbb2fd0d73c9f8d8a5cbe505fb5abe3b33d1ba1",
    }
    artifacts = provenance.get("artifacts", {})
    for name, expected_hash in expected_hashes.items():
        if artifacts.get(name, {}).get("sha256") != expected_hash:
            fail(f"private candidate {name} digest changed")
    if artifacts.get("independent_language_verifier", {}).get("independent_ownership") is not False:
        fail("same-owner verifier cannot satisfy independent ownership")
    if artifacts.get("conformance_report", {}).get("accepted_as_release_evidence") is not False:
        fail("blocked private-candidate report cannot become release evidence")

    measurements = data.get("private_candidate_measurements", {})
    if (
        measurements.get("warm_no_change_bempic_bytes") != 35
        or measurements.get("cold_no_change_bempic_bytes") != 75
        or measurements.get("accepted_as_public_tuple_release_evidence") is not False
        or measurements.get("public_tuple_regeneration_required") is not True
    ):
        fail("private measurements were changed or promoted")
    transition = data.get("public_tuple_transition", {})
    if (
        transition.get("source_private_tuple") != COMPACT_PRIVATE_TUPLE
        or transition.get("allocated_public_tuple") != "0x00010000/1"
        or transition.get("id_change_changes_encoded_records") is not True
        or "vectors-and-bundle-digests" not in transition.get("regenerate", [])
    ):
        fail("public codec tuple transition requirements changed")

    oceanmail = data.get("oceanmail_application_evidence", {})
    if (
        oceanmail.get("commit") != OCEANMAIL_PROFILE_COMMIT
        or oceanmail.get("profile_sha256") != "b2e485c08d67ad0839c134829643905936dc2263bd52eaf5d88ddc71ee29d624"
        or oceanmail.get("fixture_sha256") != "2693e4007697f381f2ff5e500686876bbe1a90a9a3fa75c312a8edff6fb334fe"
        or oceanmail.get("application_profile_current") is not True
        or oceanmail.get("accepted_as_complete_bempic_v11_release_evidence") is not False
    ):
        fail("OceanMail application evidence changed or was over-promoted")


def validate_vector_catalog() -> None:
    data = load_json("conformance/v0.1/vector-catalog.json")
    if data.get("format") != "bempic-vector-catalog-v0.1":
        fail("unexpected vector catalog format")
    catalog = data.get("catalog")
    expected = [f"V{index:02d}" for index in range(1, 16)]
    actual = [entry.get("id") for entry in catalog]
    if actual != expected:
        fail(f"vector catalog IDs must be exactly {expected!r}, got {actual!r}")
    for entry in catalog:
        if not entry.get("subject") or not entry.get("cases") or not entry.get("assertions"):
            fail(f"incomplete vector catalog entry {entry.get('id')}")
        if len(entry["cases"]) != len(set(entry["cases"])):
            fail(f"duplicate case in {entry.get('id')}")
        if len(entry["assertions"]) != len(set(entry["assertions"])):
            fail(f"duplicate assertion in {entry.get('id')}")
    by_id = {entry["id"]: entry for entry in catalog}
    for vector_id, expected_fields in EXPECTED_VECTOR_REQUIREMENTS.items():
        for field, expected_value in expected_fields.items():
            if by_id[vector_id].get(field) != expected_value:
                fail(f"{vector_id} {field} differs from the normative catalog")
    validate_v08_pairwise(by_id["V08"]["coverage_rows"])
    if data.get("external_benchmarks") != EXPECTED_EXTERNAL_BENCHMARKS:
        fail("external B2F benchmark catalog changed or was promoted")


def validate_v08_pairwise(rows: object) -> None:
    if not isinstance(rows, list) or len(rows) != 24:
        fail("V08 coverage must contain exactly 24 rows")
    row_ids = [row.get("id") for row in rows]
    if len(row_ids) != len(set(row_ids)):
        fail("V08 coverage row IDs must be unique")
    point_restart = {(row.get("point"), row.get("restart")) for row in rows}
    point_storage = {(row.get("point"), row.get("storage")) for row in rows}
    restart_storage = {(row.get("restart"), row.get("storage")) for row in rows}
    expected_point_restart = {
        (point, restart)
        for point in V08_CASES
        for restart in V08_RESTART_PARTIES
    }
    expected_point_storage = {
        (point, storage)
        for point in V08_CASES
        for storage in V08_STORAGE_SURFACES
    }
    expected_restart_storage = {
        (restart, storage)
        for restart in V08_RESTART_PARTIES
        for storage in V08_STORAGE_SURFACES
    }
    if point_restart != expected_point_restart:
        fail("V08 coverage omits an interruption-point/restart pair")
    if point_storage != expected_point_storage:
        fail("V08 coverage omits an interruption-point/storage pair")
    if restart_storage != expected_restart_storage:
        fail("V08 coverage omits a restart/storage pair")


def validate_metrics() -> None:
    data = load_json("conformance/v0.1/metrics.json")
    if data.get("format") != "bempic-metrics-v0.1" or data.get("unit") != "octets":
        fail("unexpected metrics format or unit")
    required = data.get("required")
    if required != EXPECTED_REQUIRED_METRICS or len(required) != len(set(required)):
        fail("required metric names differ from the normative catalog")
    if data.get("semantic_bytes_definition") != EXPECTED_SEMANTIC_BYTES_DEFINITION:
        fail("semantic_bytes definition differs from the normative catalog")
    if data.get("identities") != EXPECTED_METRIC_IDENTITIES:
        fail("metric identities differ from the normative catalog")
    if data.get("b2f_comparison") != EXPECTED_B2F_COMPARISON:
        fail("B2F comparison metadata differs from the normative decision")
    if data.get("thresholds") != EXPECTED_METRIC_THRESHOLDS:
        fail("metric threshold definitions differ from the normative catalog")


def validate_b2f_oracle_decision() -> None:
    data = load_json(B2F_DECISION_PATH)
    if data.get("format") != "bempic-b2f-oracle-decision-v0.1":
        fail("unexpected B2F oracle-decision format")
    if data.get("decision") != {
        "status": "blocked-no-qualified-oracle",
        "selected_oracle": None,
        "release_gate": "blocked",
        "thresholds_changed": False,
        "results_claimable": False,
        "reason_codes": [
            "no-complete-immutable-executable-and-envelope",
            "no-prescribed-content-addressed-corpus-results",
            "no-independent-byte-for-byte-reproduction",
            "candidate-license-or-distribution-boundaries-incomplete",
        ],
    }:
        fail("B2F blocked decision changed or was promoted")

    profile = data.get("comparison_profile", {})
    if (
        profile.get("id") != B2F_PROFILE
        or profile.get("fixture_scope")
        != "one-message-per-independent-no-fault-run"
        or profile.get("batching") != "forbidden"
    ):
        fail("B2F fixture scope differs from the normative profile")
    raw = profile.get("raw_input", {})
    if raw != {
        "format": "rfc5322-mime-exact-bytes",
        "line_endings": "crlf",
        "content_type": "text/plain; charset=us-ascii",
        "content_transfer_encoding": "7bit",
        "body": "non-empty-single-part",
        "attachments": 0,
        "bcc": "forbidden",
        "transport_trace_fields": "forbidden",
        "measured_as_b2f_bytes": False,
    }:
        fail("B2F raw MIME preparation differs from the normative profile")
    prepared = profile.get("prepared_b2_image", {})
    if prepared.get("header_order") != [
        "Mid", "Date", "Type", "From", "To", "Cc", "Subject", "Mbo", "Body"
    ] or prepared.get("oracle_may_rewrite") is not False:
        fail("B2 prepared-image construction differs from the normative profile")

    lzhuf = profile.get("lzhuf", {})
    behavior = lzhuf.get("behavior_reference", {})
    if behavior != {
        "repository": "ARSFI/Winlink-Compression",
        "commit": B2F_ARSFI_COMMIT,
        "path": "WinlinkSupport.vb",
        "git_blob_sha1": "1430cf408b28d9345e6b4a75c1c97fdaebb3661d",
        "entry_point": "Compression.Encode(input, output, prependCRC=True)",
    }:
        fail("B2F LZHUF behavior reference changed")
    expected_lzhuf = {
        "variant": "FBB-LZHUF_1-with-B2-prefix",
        "lzss_ring_octets": 2048,
        "lookahead_octets": 60,
        "match_threshold": 2,
        "initial_ring_octet": 32,
        "adaptive_huffman_symbols": 314,
        "adaptive_huffman_rebuild_frequency": 32768,
    }
    for field, expected in expected_lzhuf.items():
        if lzhuf.get(field) != expected:
            fail(f"B2F LZHUF {field} differs from the normative profile")
    if lzhuf.get("crc") != {
        "name": "CRC-16/XMODEM",
        "polynomial": 4129,
        "initial": 0,
        "reflect_input": False,
        "reflect_output": False,
        "xor_output": 0,
        "stored_byte_order": "little-endian",
        "coverage": "four-octet-length-plus-compressed-bitstream",
    }:
        fail("B2F LZHUF CRC definition differs from the normative profile")

    envelope = profile.get("b2f_envelope", {})
    if (
        envelope.get("start") != "first-octet-of-fc-proposal"
        or envelope.get("end") != "checksum-octet-following-eot"
        or envelope.get("offset") != 0
        or envelope.get("data_block_payload_octets") != 250
        or envelope.get("proposal_template")
        != "FC EM {mid} {uncompressed_size} {compressed_size} 0\\r"
        or envelope.get("acceptance") != "FS +\\r"
    ):
        fail("B2F framing envelope differs from the normative profile")
    if envelope.get("directions", {}).get("identity") != (
        "b2f_total_bytes=b2f_send_bytes+b2f_receive_bytes"
    ):
        fail("B2F directional identity differs from the normative profile")
    if "complete-lzhuf-image" not in envelope.get("included", []):
        fail("B2F envelope omits the compressed image")
    if "modem-carrier-link-framing" not in envelope.get("excluded", []):
        fail("B2F envelope does not separate lower-layer bytes")

    calculations = profile.get("calculations", {})
    if calculations != {
        "candidate_reduction_percent": "100*(b2f_total_bytes-bempic_total_bytes)/b2f_total_bytes",
        "candidate_increase_percent": "100*(bempic_total_bytes-b2f_total_bytes)/b2f_total_bytes",
        "representation": "signed-integer-numerator-and-positive-integer-denominator",
        "median": "exact-median-of-per-fixture-reduction-rationals",
        "even_median": "arithmetic-mean-of-two-middle-rationals",
        "forbidden_aggregations": [
            "ratio-of-aggregate-byte-totals",
            "ratio-of-two-medians",
        ],
    }:
        fail("B2F exact-rational calculations differ from the normative profile")
    if data.get("thresholds") != EXPECTED_B2F_THRESHOLDS:
        fail("B2F decision thresholds changed")

    corpus = data.get("required_corpus_manifest", {})
    if corpus.get("status") != "not-yet-published" or corpus.get("digest") is not None:
        fail("B2F corpus was promoted without reviewed evidence")
    candidates = {item.get("id"): item for item in data.get("candidates", [])}
    if set(candidates) != {
        "arsfi-winlink-compression",
        "wl2k-go",
        "pat",
        "paclink-unix-lzhuf-1",
        "f6fbb-b2compress-linfbb",
    } or any(item.get("qualified") is not False for item in candidates.values()):
        fail("B2F candidate audit changed or promoted a candidate")
    if candidates["wl2k-go"].get("commit") != B2F_WL2K_COMMIT or (
        candidates["wl2k-go"].get("linking")
        != "not-approved-for-lzhuf-without-rights-clarification"
    ):
        fail("wl2k-go provenance boundary changed")
    paclink = candidates["paclink-unix-lzhuf-1"]
    if (
        paclink.get("commit") != B2F_PACLINK_COMMIT
        or paclink.get("license") != "GPL-2.0-or-later"
        or paclink.get("incorporation") != "forbidden-project-policy"
        or paclink.get("linking") != "forbidden-project-policy"
        or paclink.get("ci_use") != "separately-obtained-process-only"
    ):
        fail("paclink-unix process/license boundary changed")


def validate_release_template() -> None:
    data = load_json("conformance/v0.1/release-record-template.json")
    if data.get("format") != "bempic-release-record-v0.1":
        fail("unexpected release-record format")
    if data.get("release_state") != "not-ready" or data.get("tag") is not None:
        fail("release template must remain not-ready with a null tag")
    blockers = set(data.get("known_blockers", []))
    expected = {
        "public-codec-vector-regeneration",
        "complete-v01-v15-and-codec-boundary-evidence",
        "independent-verifier",
        "b2f-oracle",
        "m4p-binding-review",
        "protocol-name",
        "bempic-reference-implementation-and-evidence",
        "final-release-candidate-verification",
    }
    if blockers != expected:
        fail("release-record blockers do not match the required unresolved set")
    if data.get("metrics", {}).get("thresholds_passed") is not False:
        fail("incomplete release template cannot claim metric thresholds passed")
    metrics = data.get("metrics", {})
    if metrics.get("semantic_bytes_identity_passed") is not False:
        fail("incomplete release template cannot claim semantic_bytes evidence")
    interruption = data.get("interruption_coverage", {})
    expected_interruption = {
        "model": "fixed-pairwise-covering-array-v0.1",
        "required_rows": 24,
        "evidence_digest": None,
        "pair_coverage_passed": False,
        "v14_before_after_passed": False,
    }
    if interruption != expected_interruption:
        fail("release template interruption coverage differs from the normative catalog")
    b2f = data.get("b2f_oracle", {})
    if b2f != {
        "decision_status": "blocked-no-qualified-oracle",
        "decision_artifact": B2F_DECISION_PATH,
        "comparison_profile": B2F_PROFILE,
        "identity": None,
        "version": None,
        "executable_digest": None,
        "license": None,
        "corpus_digest": None,
        "results_digest": None,
        "independent_reproduction": None,
        "thresholds_changed": False,
    }:
        fail("release template B2F oracle changed or was promoted")
    codec = data.get("codec", {})
    if codec != {
        "id": COMPACT_CODEC_ID,
        "revision": COMPACT_CODEC_REVISION,
        "status": "experimental",
        "profile_digest": f"sha256:{COMPACT_PROFILE_SHA256}",
        "size_proof_digest": "sha256:fd3461c674921b9730c773f0eef01d34dcc8e60a472ca1bb2ec1f3027de2f525",
        "allocation_evidence": "conformance/v0.1/experimental-codec-allocation.json",
        "approved": False,
        "mandatory": False,
        "public_tuple_vectors_complete": False,
    }:
        fail("release template compact codec evidence changed or was promoted")
    reference = data.get("current_reference_evidence", {})
    if reference.get("evidence_commit") != COMPACT_PRIVATE_COMMIT:
        fail("current reference evidence commit changed without review")
    if reference.get("observed_status") != "blocked-not-conformant":
        fail("current reference evidence status must remain blocked-not-conformant")
    if reference.get("accepted_as_release_evidence") is not False:
        fail("current blocked reference report cannot be accepted as release evidence")
    if reference.get("accepted_for_experimental_allocation") is not True:
        fail("current reference allocation evidence was discarded")
    if reference.get("requires_rerun_against_clarified_specification") is not True:
        fail("current reference evidence must require a clarified-specification rerun")
    if reference.get("requires_rerun_against_allocated_public_tuple") is not True:
        fail("current reference evidence must require public-tuple regeneration")
    oceanmail = data.get("oceanmail_application_evidence", {})
    if (
        oceanmail.get("commit") != OCEANMAIL_PROFILE_COMMIT
        or oceanmail.get("application_profile_current") is not True
        or oceanmail.get("complete_v11_release_evidence") is not False
    ):
        fail("OceanMail evidence changed or was promoted to complete V11 evidence")


def validate_clarification_alignment() -> None:
    required_markers = {
        "SPECIFICATION.md": (
            "[REQ-ACCOUNT-003]",
            "semantic_bytes[d]",
            "sum of the send and receive directions",
            "`endpoint-a` and `endpoint-b`",
            "never representation descriptor members",
            "A deferred or unselected representation contributes zero until selected",
            "Repeated requests, contacts, duplicates, retransmissions, matching overlap, and restart/resume do not add semantic bytes",
            "Encoded representation payload, compression or security expansion",
        ),
        "docs/CONFORMANCE.md": (
            "[REQ-CONF-003]",
            "[REQ-CONF-004]",
            "exact 24 rows",
            "72-row full Cartesian product is not required",
            "memory",
            "representation-file",
            "durable-store",
            "floor(L*p/100)",
        ),
        "docs/TEST-VECTORS.md": (
            "[REQ-VEC-006]",
            "[REQ-VEC-007]",
            "V08-C01",
            "V08-C24",
            "public-codec-vector-regeneration",
            "0xffff0001/2",
            "[REQ-VEC-008]",
            B2F_PROFILE,
        ),
        "docs/METRICS.md": (
            "[REQ-METRIC-010]",
            "semantic_bytes = semantic_bytes_send + semantic_bytes_receive",
            "`endpoint-a` to `endpoint-b`",
            "every representation descriptor member",
            "`endpoint_a_binding` and `endpoint_b_binding`",
            "descriptor contribution MUST be zero",
            "The same `(direction, representation_id)` MUST appear at most once per scope",
            B2F_PROFILE,
            "neither threshold is weakened, removed, or treated as not applicable",
        ),
        "docs/ROADMAP-v0.1.0.md": (
            COMPACT_PRIVATE_COMMIT,
            "blocked-not-conformant",
            "35 B/75 B",
            OCEANMAIL_PROFILE_COMMIT,
        ),
        "docs/RELEASE-RECORD.md": (
            COMPACT_PRIVATE_COMMIT,
            "predates the normative clarifications",
            OCEANMAIL_PROFILE_COMMIT,
            "blocked-no-qualified-oracle",
            B2F_DECISION_PATH,
        ),
        "docs/REGISTRIES.md": (
            "0x00010000/1",
            COMPACT_PRIVATE_TUPLE,
            "neither approved nor mandatory",
        ),
        COMPACT_PROFILE: (
            "[REQ-COMPACT-001]",
            "[REQ-COMPACT-008]",
            "0x00010000/1",
            COMPACT_PRIVATE_TUPLE,
            "no stable-wire or production-security promise",
        ),
        "docs/B2F-ORACLE.md": (
            "[REQ-B2F-001]",
            "[REQ-B2F-002]",
            "[REQ-B2F-003]",
            "[REQ-B2F-004]",
            "[REQ-B2F-005]",
            "[REQ-B2F-006]",
            B2F_PROFILE,
            B2F_ARSFI_COMMIT,
            B2F_WL2K_COMMIT,
            B2F_PACLINK_COMMIT,
            "250-octet",
            "GPL/AGPL code must not be linked",
        ),
    }
    for relative, markers in required_markers.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        normalized_text = " ".join(text.split())
        for marker in markers:
            if marker not in text and marker not in normalized_text:
                fail(f"{relative} missing clarification marker {marker!r}")

    vector_text = (ROOT / "docs/TEST-VECTORS.md").read_text(encoding="utf-8")
    markdown_rows = []
    for line in vector_text.splitlines():
        if not line.startswith("| V08-C"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4:
            fail(f"malformed V08 Markdown coverage row: {line}")
        row_id, point, restart, storage = cells
        markdown_rows.append(
            {"id": row_id, "point": point, "restart": restart, "storage": storage}
        )
    if markdown_rows != expected_v08_coverage_rows():
        fail("V08 Markdown table differs from the machine-readable covering array")


def main() -> int:
    try:
        must_paragraphs = validate_must_matrix()
        validate_codec_registry()
        validate_experimental_codec_allocation()
        validate_vector_catalog()
        validate_metrics()
        validate_b2f_oracle_decision()
        validate_release_template()
        validate_clarification_alignment()
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"release-gate validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        "release-gate validation passed: "
        f"{must_paragraphs} MUST paragraphs, 15 vectors, 24 V08 coverage rows, "
        "18 required metrics, 8 metric thresholds, blocked B2F oracle decision, "
        "complete codec-ID range, "
        "experimental compact allocation 0x00010000/1 "
        "coverage, release state not-ready"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
