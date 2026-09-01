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
assert(registry.allocations.length === 0, "unexpected v0.1 codec allocation");

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
assert(metrics.semantic_bytes_definition.excluded.includes("duplicates") &&
  metrics.semantic_bytes_definition.excluded.includes("lower-layer-retransmissions"),
"semantic_bytes exclusion set is incomplete");
assert(metrics.thresholds.length === 8, "expected eight metric thresholds");

const release = readJson("conformance/v0.1/release-record-template.json");
assert(release.release_state === "not-ready" && release.tag === null,
  "release template made a premature release claim");
assert(release.interruption_coverage.required_rows === 24 &&
  release.interruption_coverage.pair_coverage_passed === false,
"release template interruption gate changed");
assert(release.current_reference_evidence.evidence_commit ===
  "29be83fed70433ea958f9773539fb8b93fa00dc9" &&
  release.current_reference_evidence.observed_status === "blocked-not-conformant" &&
  release.current_reference_evidence.accepted_as_release_evidence === false,
"blocked reference checkpoint changed or was promoted");

console.log(`Independent Node verification passed (Node ${process.version}).`);
for (const result of fingerprintResults) console.log(`fingerprint MATCH ${result}`);
console.log("codec ranges cover uint32; V01-V15 and 24 V08 rows present; 18 metrics; 8 thresholds; release not-ready");
