# BEMPIC v0.1 Required Metrics

This document makes the release metrics reproducible without assigning carrier
behavior to BEMPIC. The machine-readable names, units, scopes, and thresholds
are in [`../conformance/v0.1/metrics.json`](../conformance/v0.1/metrics.json).

## Measurement envelope

A prescribed run starts with the first octet of the first BEMPIC `CAPABILITIES`
operation in a new budget scope and ends at the last encoded BEMPIC octet of the
terminal operation required by the case. Cached capability bytes from before the
scope are zero only in a named warm case. M4P, carrier, link, storage, and
lower-layer retry costs are separate domains. Security fields encoded inside a
BEMPIC operation count as BEMPIC bytes; only a handshake outside BEMPIC
operations is separately reported and eligible for a threshold exclusion.

[REQ-METRIC-001] A result MUST identify the specification commit, vector-bundle
digest, vector and case IDs, codec ID/revision/status and profile digest,
implementation commit, direction, budget ID, initial durable state, security
profile, carrier binding, run count, semantic-fixture digest, selected
representation IDs by logical direction, and whether each lower-layer counter
is exact, estimated, unavailable, or not applicable.

[REQ-METRIC-002] For each direction `d`, implementations MUST report
`bempic_operation_bytes[d]` as the sum of complete encoded BEMPIC operations,
including framing owned by the codec profile. They MUST also report
`bempic_total_bytes` and demonstrate
`bempic_total_bytes = bempic_operation_bytes[send] +
bempic_operation_bytes[receive]`. Representation payload octets are a subset of
operation bytes and MUST NOT be added to that identity a second time.

## Required counters

The following counters are unsigned integer octets unless noted otherwise:

- `semantic_bytes`, `semantic_bytes_send`, and `semantic_bytes_receive`;
- `bempic_total_bytes` and directional `bempic_operation_bytes`;
- `representation_payload_bytes` and `useful_committed_bytes`;
- `duplicate_bempic_bytes` and `duplicate_representation_payload_bytes`;
- `unselected_representation_payload_bytes`;
- `retransmitted_durable_prefix_bytes`;
- `retransmitted_prior_manifest_bytes`;
- `resume_control_bytes`;
- `bempic_bytes_to_first_body_payload_octet`;
- `bempic_bytes_to_first_body_commit`;
- `preflight_quoted_bempic_bytes` and signed `quote_error_bytes`;
- carrier and link bytes when those layers expose them; and
- wall time and energy only as optional, separately labeled observations.

`useful_committed_bytes` counts the canonical prepared representation octets
newly committed in the run. Matching overlap, replay, and previously durable
bytes are not useful bytes.

## Semantic-workload metrics

Every measurement scope binds two enduring fixture roles, `endpoint-a` and
`endpoint-b`, to its logical peers before the run. `send` is always the logical
flow from `endpoint-a` to `endpoint-b`; `receive` is always the flow from
`endpoint-b` to `endpoint-a`. Both endpoint reporters use that same binding.
The roles do not change when ownership/requester roles reverse for another
representation, or when a process restarts, an authorized source replaces it,
or the carrier changes. A representation selected in both directions is one
workload item in each direction.

[REQ-METRIC-010] Every result MUST compute `semantic_bytes_send` and
`semantic_bytes_receive` from Specification Section 12.1 and demonstrate
`semantic_bytes = semantic_bytes_send + semantic_bytes_receive`. The raw
scope record MUST contain `endpoint_a_binding` and `endpoint_b_binding`, whose
values identify the two enduring logical peer fixtures. It MUST contain, for
each counted representation, its direction, source and destination endpoint
roles, full representation ID, schema fingerprint, canonical semantic-fixture
path, SHA-256 digest, exact fixture length, independently recomputed
`semantic_octets`, `representation_descriptor_contribution`, and selection
event. The descriptor contribution MUST be zero, and the source/destination
roles MUST agree with the fixed direction. The same `(direction,
representation_id)` MUST appear at most once per scope. Protocol metadata,
every representation descriptor member, encoded payload, deferred payload,
duplicates, retransmission, padding, and lower-layer bytes MUST NOT change the
counter.
Aggregation is performed only after each raw run passes this identity; values
from different endpoint bindings, fixture digests, selection sets, or scopes
MUST NOT be pooled into one comparison.

For report serialization, `bempic_operation_bytes_send` and
`bempic_operation_bytes_receive` are the exact aliases of Specification
`bempic_tx_bytes` and `bempic_rx_bytes`; `duplicate_representation_payload_bytes`
is the exact alias of `duplicate_payload_bytes`. The longer names prevent
direction or domain ambiguity in a standalone metric record.

[REQ-METRIC-003] Every required counter MUST be computed per run before any
aggregation. A report MUST publish all raw run values plus count, minimum,
median, maximum, and arithmetic mean. Thresholds apply to each prescribed run
unless a threshold explicitly says `median`; a skipped or unavailable required
counter is a failure, not zero. `semantic_bytes` is aggregated like every other
required counter but is never multiplied by duplicate delivery, contact count,
or restart count.

## First-body metrics

The first body is the lowest part index whose role is `body`, followed by the
lowest selected representation ID for that part in unsigned byte order.
Selection is fixed by the vector.

[REQ-METRIC-004] `bempic_bytes_to_first_body_payload_octet` MUST count every
encoded BEMPIC octet in both directions from the measurement-envelope start
through and including the first payload octet of the first `DATA` operation for
that selected representation. `bempic_bytes_to_first_body_commit` MUST count
through and including the complete `RECEIPT(REPRESENTATION_COMMITTED)` for that
representation. A case with an empty selected body MUST report the payload
metric as not applicable with the reason `empty-body`, while the commit metric
remains required.

## Interruption and resume metrics

[REQ-METRIC-005] Every V08 and V09 case MUST report the durable prefix before
interruption, the prefix recovered on reopen, first resumed offset, newly sent
payload, matching duplicate payload, conflicting payload, resume control bytes,
retransmitted durable-prefix bytes, contacts before completion, and final
integrity/receipt result. A receiver MUST NOT recover a prefix beyond durable
bytes, and a sender with authoritative retained-prefix knowledge MUST produce
zero `retransmitted_durable_prefix_bytes`.

If durability knowledge is lost, matching duplicate bytes are permitted only as
specified by the state machine and are recorded in both duplicate counters;
they are never counted as useful bytes.

## Release thresholds

[REQ-METRIC-006] On the prescribed 100-message V01 fixture, every warm no-change
run MUST have `bempic_total_bytes <= 64`, and every cold no-change run MUST have
`bempic_total_bytes <= 128`, excluding only a separately reported
application-security handshake. V02 MUST have
`retransmitted_prior_manifest_bytes = 0`.

[REQ-METRIC-007] Every selected deterministic no-fault V12 plan MUST have
`quote_error_bytes = 0`, stay within its total and directional budgets, and emit
no partial operation. Every V05 case MUST have
`unselected_representation_payload_bytes = 0`. Applicable V08/V09 cases with
authoritative retained-prefix knowledge MUST have
`retransmitted_durable_prefix_bytes = 0`.

[REQ-METRIC-008] The prescribed text-corpus comparison MUST report total BEMPIC
bytes for the candidate codec and total bytes for the selected B2F/LZHUF oracle
under identical semantic input and declared envelope rules. The median candidate
result MUST be at least 10 percent smaller than B2F. Any fixture whose candidate
result exceeds B2F by more than 5 percent MUST have an accepted, measured
resumption or metering justification. Selection and licensing of the B2F oracle
remain release-blocking; no result may be claimed until that decision is
recorded.

No pass threshold is yet assigned to first-body, resume-control, carrier, link,
time, or energy metrics. They are mandatory observations so a later threshold
cannot be chosen after hiding unfavorable results.

## Evidence format

[REQ-METRIC-009] The conformance report MUST embed or content-address the raw
machine-readable metric records, calculation tool and version, input and output
digests, and threshold evaluation. Rerunning the same deterministic fixture,
codec, parameters, and implementation commit MUST reproduce every exact BEMPIC
counter byte for byte.
