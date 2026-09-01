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
        pair = (allocation.get("id"), allocation.get("revision"))
        if pair in pairs:
            fail(f"duplicate codec allocation {pair}")
        pairs.add(pair)
        if not isinstance(pair[0], int) or not isinstance(pair[1], int) or pair[1] < 1:
            fail(f"invalid codec allocation {allocation!r}")


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
    if by_id["V03"]["cases"] != ["inventory-257-pages-128-128-1", "reopen-after-page-1"]:
        fail("V03 must pin the 257-entry 128/128/1 paging cases")
    if by_id["V08"].get("restart_parties") != ["sender", "receiver", "both"]:
        fail("V08 must cover sender, receiver, and joint restart")
    operations = ["CAPABILITIES", "SUMMARY", "OFFER", "REQUEST", "DATA", "RECEIPT", "FAILURE"]
    if by_id["V12"].get("operation_types") != operations:
        fail("V12 must cover all seven core operation types")
    if by_id["V12"].get("budget_domains") != ["total", "send", "receive"] or by_id["V12"].get("relative_budgets") != [-1, 0]:
        fail("V12 must cover exact and one-byte-short total/directional budgets")
    failure_codes = {
        "UNSUPPORTED_VERSION", "UNSUPPORTED_SCHEMA", "UNSUPPORTED_CODEC",
        "UNSUPPORTED_CRITICAL_EXTENSION", "MALFORMED_OPERATION", "LIMIT_EXCEEDED",
        "UNKNOWN_OBJECT", "METADATA_CONFLICT", "RANGE_INVALID", "INTEGRITY_FAILURE",
        "STORAGE_FAILURE", "POLICY_REJECTED", "CHECKPOINT_UNKNOWN",
    }
    if set(by_id["V15"]["cases"]) != failure_codes or by_id["V15"].get("advertised_retryable_flags") != [False, True]:
        fail("V15 must cover every core failure code with both retryable flags")


def validate_metrics() -> None:
    data = load_json("conformance/v0.1/metrics.json")
    if data.get("format") != "bempic-metrics-v0.1" or data.get("unit") != "octets":
        fail("unexpected metrics format or unit")
    required = data.get("required")
    if not isinstance(required, list) or len(required) != len(set(required)):
        fail("required metric names must be a unique list")
    threshold_ids = [item.get("id") for item in data.get("thresholds", [])]
    expected = {
        "warm-no-change",
        "cold-no-change",
        "known-append-no-old-manifest",
        "no-unselected-payload",
        "exact-no-fault-quote",
        "resume-no-durable-prefix-resend",
        "b2f-median-compactness",
        "b2f-per-fixture-regression",
    }
    if set(threshold_ids) != expected or len(threshold_ids) != len(expected):
        fail("metric threshold catalog is incomplete or duplicated")


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
