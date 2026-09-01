#!/usr/bin/env python3
"""Validate v0.1 release-gate registries, catalogs, and MUST coverage."""

from __future__ import annotations

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
    "docs/M4P-CONFIRMATION.md",
    "docs/RELEASE-RECORD.md",
)
REQ_RE = re.compile(r"\[?(REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*)\]?")
MUST_RE = re.compile(r"\bMUST(?: NOT)?\b")

EXPECTED_VECTOR_REQUIREMENTS = {
    "V01": {
        "cases": ["empty", "equal-warm-100", "equal-cold-100"],
        "assertions": ["no-object-payload", "warm-no-change-metric", "cold-no-change-metric"],
        "blocked_by": ["experimental-codec-selection"],
    },
    "V02": {
        "cases": ["known-checkpoint-100-plus-1"],
        "assertions": ["new-manifest-only", "zero-retransmitted-prior-manifest-bytes"],
        "blocked_by": ["experimental-codec-selection"],
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
        "cases": ["offset-0", "offset-1-percent", "offset-10-percent", "offset-50-percent", "offset-90-percent", "final-byte", "post-verify-pre-commit", "post-commit-pre-receipt"],
        "restart_parties": ["sender", "receiver", "both"],
        "assertions": ["reopen-last-durable-state", "no-false-prefix", "no-false-receipt", "exact-reconstruction-after-resume"],
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
        "assertions": ["storage-failure-scoped", "reopen-not-ahead", "no-false-receipt"],
    },
    "V15": {
        "cases": ["UNSUPPORTED_VERSION", "UNSUPPORTED_SCHEMA", "UNSUPPORTED_CODEC", "UNSUPPORTED_CRITICAL_EXTENSION", "MALFORMED_OPERATION", "LIMIT_EXCEEDED", "UNKNOWN_OBJECT", "METADATA_CONFLICT", "RANGE_INVALID", "INTEGRITY_FAILURE", "STORAGE_FAILURE", "POLICY_REJECTED", "CHECKPOINT_UNKNOWN"],
        "advertised_retryable_flags": [False, True],
        "assertions": ["exact-failure-code", "retry-classification", "bounded-retry", "scoped-mutation"],
    },
}

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


def validate_metrics() -> None:
    data = load_json("conformance/v0.1/metrics.json")
    if data.get("format") != "bempic-metrics-v0.1" or data.get("unit") != "octets":
        fail("unexpected metrics format or unit")
    required = data.get("required")
    if not isinstance(required, list) or len(required) != len(set(required)):
        fail("required metric names must be a unique list")
    if data.get("thresholds") != EXPECTED_METRIC_THRESHOLDS:
        fail("metric threshold definitions differ from the normative catalog")


def validate_release_template() -> None:
    data = load_json("conformance/v0.1/release-record-template.json")
    if data.get("format") != "bempic-release-record-v0.1":
        fail("unexpected release-record format")
    if data.get("release_state") != "not-ready" or data.get("tag") is not None:
        fail("release template must remain not-ready with a null tag")
    blockers = set(data.get("known_blockers", []))
    expected = {
        "experimental-codec-selection",
        "independent-verifier",
        "b2f-oracle",
        "m4p-binding-review",
        "object-id-application-profile",
        "protocol-name",
        "bempic-reference-implementation-and-evidence",
        "final-release-candidate-verification",
    }
    if blockers != expected:
        fail("release-record blockers do not match the required unresolved set")
    if data.get("metrics", {}).get("thresholds_passed") is not False:
        fail("incomplete release template cannot claim metric thresholds passed")


def main() -> int:
    try:
        must_paragraphs = validate_must_matrix()
        validate_codec_registry()
        validate_vector_catalog()
        validate_metrics()
        validate_release_template()
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"release-gate validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        "release-gate validation passed: "
        f"{must_paragraphs} MUST paragraphs, 15 vectors, 8 metric thresholds, "
        "complete codec-ID range coverage, release state not-ready"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
