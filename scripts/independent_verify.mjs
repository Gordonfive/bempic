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

const metrics = readJson("conformance/v0.1/metrics.json");
assert(metrics.thresholds.length === 8, "expected eight metric thresholds");

const release = readJson("conformance/v0.1/release-record-template.json");
assert(release.release_state === "not-ready" && release.tag === null,
  "release template made a premature release claim");

console.log(`Independent Node verification passed (Node ${process.version}).`);
for (const result of fingerprintResults) console.log(`fingerprint MATCH ${result}`);
console.log("codec ranges cover uint32; V01-V15 present; 8 thresholds; release not-ready");
