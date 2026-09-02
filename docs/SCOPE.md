# BEMPIC v0.1 Scope

This document summarizes scope. [`SPECIFICATION.md`](../SPECIFICATION.md) is
normative if wording differs.

## Purpose

BEMPIC synchronizes messaging-oriented application state with extreme byte
efficiency across interrupted contacts. It remains service-neutral even though
OceanMail drives the initial requirements.

## Included in v0.1

- Immutable logical messages with one body and optional attachments.
- Independently selectable representations, including application-supplied
  previews or reduced forms.
- Deterministic preparation, exact size, full digest, representation ID, schema
  fingerprint, codec identity, and strict bounds.
- Append-only single-authority collection checkpoints, bounded delta offers, and
  deterministic full reconciliation.
- Explicit selection and deferral; an offer never authorizes content.
- Hard BEMPIC-byte budgets and separate semantic, BEMPIC, carrier, and link
  accounting.
- Reliable-carrier contiguous-prefix transfer, interruption, durable state,
  process reopen, changed-source/carrier resume, verification, and atomic
  commit.
- Distinct representation-committed, application-accepted, and
  application-delivered receipts.
- Protocol/schema/codec/extension negotiation and fail-closed compatibility.
- A contract for pluggable deterministic codecs without selecting a permanent
  wire codec.

## Excluded from v0.1

- Mutable mailbox flags, folders, labels, deletion, drafts, edits, or
  multi-writer conflict resolution.
- Application content transformation or preview generation.
- A mandatory compression algorithm or permanent wire encoding.
- A production cryptographic suite, identity system, or key distribution.
- Missing-range/selective repair on unreliable carriers.
- Internet email delivery semantics, external-provider integration, or account
  policy.
- General file synchronization, telemetry, commands, forms, and arbitrary
  mutable application state.

## Permanent layer boundary

BEMPIC does not define routing, addressing, discovery, mesh coordination,
store-carry-forward, forwarding, generic fragmentation/reassembly, network
deduplication, network TTL, cross-modality behavior, or DataLink abstraction.
M4P owns those concerns for OceanMail.
The current M4P specification explicitly omits custody transfer; BEMPIC does
not add or claim a custody layer in response.

BEMPIC also does not define modem framing, FEC, ARQ, retransmission, modulation,
RF turnaround, or hardware control. DataLink adapters and modems own them.

BEMPIC persists application representation progress because it must outlive a
lost network path or contact. That extent state is not a packet fragment and
does not acknowledge every reliable-carrier record.

OceanMail owns gateway/relay policy, prioritization, user approval, billing,
quotas, normalization, transforms, product UI, and external mail-service
behavior.

## Repository scope

This repository owns public semantics, architecture, governance, conformance,
vector definitions, security requirements, roadmap, and rationale. Executable
reference work belongs in `bempic-reference`. The existing Python proof remains
here only as a transitional oracle until the documented parity gate passes.
