"""Validate local Markdown links and BEMPIC repository consistency."""

from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
from pathlib import Path
from urllib.parse import unquote

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
    "docs/ARCHITECTURE.md",
    "docs/REPOSITORY-BOUNDARY.md",
    "docs/ROADMAP-v0.1.0.md",
    "docs/CONFORMANCE.md",
    "docs/TEST-VECTORS.md",
    "docs/REGISTRIES.md",
    "docs/SECURITY-MODEL.md",
    "docs/RELEASE-NOTES-v0.1.0.md",
    "schemas/README.md",
    "schemas/v0.1/core-operations.schema.json",
    "schemas/v0.1/message-manifest.schema.json",
    "schemas/v0.1/opaque-binary.schema.json",
    "schemas/v0.1/fingerprints.json",
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


def validate_schema_fingerprints() -> list[str]:
    errors: list[str] = []
    schema_root = ROOT / "schemas" / "v0.1"
    expected_path = schema_root / "fingerprints.json"
    if not expected_path.is_file():
        return ["missing schema fingerprint manifest"]
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    descriptor_names = sorted(path.name for path in schema_root.glob("*.schema.json"))
    if sorted(expected) != descriptor_names:
        errors.append("schema descriptor set does not match fingerprints.json")
        return errors

    domain = b"BEMPIC-SCHEMA-FINGERPRINT-v0.1\0"
    for name in descriptor_names:
        value = json.loads((schema_root / name).read_text(encoding="utf-8"))
        canonical = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
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
    errors = link_errors + validate_consistency() + validate_schema_fingerprints()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Documentation validation failed with {len(errors)} error(s).")
        return 1
    print(
        f"Validated {len(markdown_files)} Markdown files and their local links "
        f"({external_count} external links recorded, not fetched)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
