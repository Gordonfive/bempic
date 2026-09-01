"""Validate local Markdown links and BEMPIC repository consistency."""

from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote

try:
    import rfc8785
except ModuleNotFoundError:
    rfc8785 = None

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:")

REQUIRED_FILES = (
    "AGENTS.md",
    "LICENSE",
    "NOTICE",
    "README.md",
    "SPECIFICATION.md",
    "GOVERNANCE.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "GREAT_PARALLEL_WORK.md",
    "requirements-validation.txt",
    "docs/ARCHITECTURE.md",
    "docs/REPOSITORY-BOUNDARY.md",
    "docs/ROADMAP-v0.1.0.md",
    "docs/CONFORMANCE.md",
    "docs/CONFORMANCE-MATRIX.md",
    "docs/TEST-VECTORS.md",
    "docs/REGISTRIES.md",
    "docs/METRICS.md",
    "docs/M4P-CONFIRMATION.md",
    "docs/RELEASE-RECORD.md",
    "docs/SECURITY-MODEL.md",
    "docs/RELEASE-NOTES-v0.1.0.md",
    "schemas/README.md",
    "schemas/v0.1/core-operations.schema.json",
    "schemas/v0.1/message-manifest.schema.json",
    "schemas/v0.1/opaque-binary.schema.json",
    "schemas/v0.1/fingerprints.json",
    "schemas/v0.1/jcs-canonicalization-vectors.json",
    "conformance/v0.1/codec-registry.json",
    "conformance/v0.1/vector-catalog.json",
    "conformance/v0.1/metrics.json",
    "conformance/v0.1/release-record-template.json",
    "scripts/validate_release_gates.py",
    "scripts/independent_verify.mjs",
    "scripts/tests/test_validate_release_gates.py",
)


def _slug(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[`*_~]", "", value).strip().lower()
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    return re.sub(r"[ ]+", "-", value)


def _anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for heading in HEADING_RE.findall(text):
        base = _slug(heading)
        count = counts.get(base, 0)
        counts[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def _link_target(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        return value[1 : value.index(">")]
    # Markdown titles follow whitespace. Repository paths do not contain spaces.
    return value.split(maxsplit=1)[0]


def validate_links(markdown_files: list[Path]) -> tuple[list[str], int]:
    errors: list[str] = []
    external_count = 0
    anchor_cache: dict[Path, set[str]] = {}

    for source in markdown_files:
        text = source.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = _link_target(raw)
            if not target or target.startswith(EXTERNAL_PREFIXES):
                external_count += int(target.startswith(EXTERNAL_PREFIXES))
                continue
            if target.startswith("data:"):
                continue

            path_text, separator, fragment = target.partition("#")
            path_text = unquote(path_text)
            destination = source if not path_text else (source.parent / path_text)
            destination = destination.resolve()
            try:
                destination.relative_to(ROOT)
            except ValueError:
                errors.append(f"{source.relative_to(ROOT)}: link escapes repository: {target}")
                continue
            if not destination.exists():
                errors.append(f"{source.relative_to(ROOT)}: missing target: {target}")
                continue
            if separator and fragment and destination.suffix.lower() == ".md":
                anchors = anchor_cache.setdefault(
                    destination,
                    _anchors(destination.read_text(encoding="utf-8")),
                )
                if unquote(fragment).lower() not in anchors:
                    errors.append(
                        f"{source.relative_to(ROOT)}: missing anchor: {target}"
                    )
    return errors, external_count


def validate_consistency() -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    checks = {
        "AGENTS.md": (
            "Permanent work-report requirement",
            "Failures and recoveries",
            "MUST NOT claim completion while",
        ),
        "SPECIFICATION.md": (
            "OceanMail  ->  BEMPIC  ->  M4P  ->  DataLink adapters",
            "not yet released or tagged",
            "DCCL is prior art",
            "bempic-reference",
        ),
        "README.md": (
            "v0.1.0 release candidate",
            "transitional oracle",
            "Apache License 2.0",
        ),
        "docs/REPOSITORY-BOUNDARY.md": (
            "MUST NOT be deleted, moved",
            "bempic-reference",
        ),
        "docs/ROADMAP-v0.1.0.md": (
            "MUST NOT be tagged yet",
            "Required work in `bempic-reference`",
            "CONFORMANCE-MATRIX.md",
        ),
        "docs/RELEASE-NOTES-v0.1.0.md": (
            "does not exist and must not be created yet",
            "PENDING",
        ),
    }
    for relative, required_text in checks.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for value in required_text:
            if value not in text:
                errors.append(f"{relative}: missing consistency marker: {value!r}")

    obsolete_claims = {
        "README.md": (
            "Licensing is intentionally not yet finalized",
            "No implementation license should be inferred",
        ),
        "docs/OPEN-QUESTIONS.md": (
            "Specification document license.",
            "Reference implementation license (permissive licensing is the current direction).",
        ),
    }
    for relative, forbidden_text in obsolete_claims.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for value in forbidden_text:
            if value in text:
                errors.append(f"{relative}: obsolete claim remains: {value!r}")
    return errors


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON object member: {key!r}")
        value[key] = item
    return value


def _reject_non_json_number(value: str) -> None:
    raise ValueError(f"non-JSON numeric literal: {value}")


def _load_ijson_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_non_json_number,
    )


def _load_ijson(path: Path) -> Any:
    return _load_ijson_text(path.read_text(encoding="utf-8"))


def validate_jcs_vectors() -> list[str]:
    if rfc8785 is None:
        return [
            "missing rfc8785 validation dependency; install "
            "requirements-validation.txt"
        ]

    errors: list[str] = []
    path = ROOT / "schemas" / "v0.1" / "jcs-canonicalization-vectors.json"
    try:
        fixture = _load_ijson(path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"cannot load JCS fixture: {error}"]

    for vector in fixture.get("valid", []):
        try:
            actual = rfc8785.dumps(vector["value"]).decode("utf-8")
        except (KeyError, UnicodeError, rfc8785.CanonicalizationError) as error:
            errors.append(f"JCS vector {vector.get('name', '<unnamed>')}: {error}")
            continue
        if actual != vector.get("canonical"):
            errors.append(
                f"JCS vector {vector.get('name', '<unnamed>')}: "
                f"{actual!r} does not match {vector.get('canonical')!r}"
            )

    for vector in fixture.get("invalid", []):
        try:
            value = _load_ijson_text(vector["json"])
            rfc8785.dumps(value)
        except (KeyError, UnicodeError, ValueError, rfc8785.CanonicalizationError):
            continue
        errors.append(
            f"JCS invalid vector {vector.get('name', '<unnamed>')} was accepted"
        )
    return errors


def validate_schema_fingerprints() -> list[str]:
    if rfc8785 is None:
        return []

    errors: list[str] = []
    schema_root = ROOT / "schemas" / "v0.1"
    expected_path = schema_root / "fingerprints.json"
    if not expected_path.is_file():
        return ["missing schema fingerprint manifest"]
    try:
        expected = _load_ijson(expected_path)
    except (ValueError, json.JSONDecodeError) as error:
        return [f"cannot load schema fingerprint manifest: {error}"]
    descriptor_names = sorted(path.name for path in schema_root.glob("*.schema.json"))
    if sorted(expected) != descriptor_names:
        errors.append("schema descriptor set does not match fingerprints.json")
        return errors

    domain = b"BEMPIC-SCHEMA-FINGERPRINT-v0.1\0"
    for name in descriptor_names:
        try:
            value = _load_ijson(schema_root / name)
            canonical = rfc8785.dumps(value)
        except (ValueError, json.JSONDecodeError, rfc8785.CanonicalizationError) as error:
            errors.append(f"{name}: RFC 8785 canonicalization failed: {error}")
            continue
        actual = hashlib.sha256(
            domain + struct.pack(">I", len(canonical)) + canonical
        ).hexdigest()
        if actual != expected[name]:
            errors.append(
                f"{name}: fingerprint {actual} does not match {expected[name]}"
            )
    return errors


def main() -> int:
    markdown_files = sorted(
        path for path in ROOT.rglob("*.md") if ".git" not in path.parts
    )
    link_errors, external_count = validate_links(markdown_files)
    errors = (
        link_errors
        + validate_consistency()
        + validate_jcs_vectors()
        + validate_schema_fingerprints()
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Documentation validation failed with {len(errors)} error(s).")
        return 1
    print(
        f"Validated {len(markdown_files)} Markdown files and their local links "
        f"({external_count} external links recorded, not fetched); RFC 8785 "
        "fixtures and schema fingerprints passed."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
