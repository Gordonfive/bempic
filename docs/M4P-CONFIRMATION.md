# M4P Binding Confirmation Requirement

The v0.1 release needs external confirmation of one proposed BEMPIC-to-M4P
application binding. This document defines the evidence; it does not define M4P
behavior. The architecture remains:

```text
OceanMail → BEMPIC → M4P → DataLink adapters
```

## Confirmation record

[REQ-M4P-001] The release record MUST link an upstream M4P issue, pull request,
or immutable review record and MUST identify the exact M4P specification commit,
binding document revision, reviewer name or stable identity, reviewer authority
as an M4P reviewer or maintainer, and UTC confirmation date. Silence, issue
closure without an affirmative statement, or review by only BEMPIC maintainers
is not confirmation.

[REQ-M4P-002] The reviewed binding contract MUST state, using M4P's own terms:

- how BEMPIC submits and receives one opaque complete record;
- maximum record size and how an available transmission opportunity is exposed;
- ordering, loss, duplication, and corruption guarantees visible to BEMPIC;
- persistence or custody guarantees and their failure/restart behavior;
- what M4P delivery indications mean and why they are not BEMPIC application
  receipts;
- exact or estimated cost information exposed to BEMPIC and its units/scope;
- interruption, cancellation, and backpressure signals; and
- ownership of peer addressing, routing, forwarding, mesh coordination,
  fragmentation/reassembly, network deduplication, TTL, and DataLink behavior.

[REQ-M4P-003] The external reviewer MUST affirm that the binding treats BEMPIC
operations as opaque application records and does not make BEMPIC implement or
redefine M4P routing, forwarding, mesh coordination, generic fragmentation,
network deduplication, TTL, custody, or modem reliability. Any exception,
condition, or unresolved semantic mismatch MUST be quoted or faithfully
summarized in the release record and remains release-blocking until resolved by
an accepted decision.

[REQ-M4P-004] The reference evidence MUST include a mock or real binding test
trace for record-size rejection, opportunity exhaustion, interruption,
duplicate delivery, restart/persistence behavior, and cost reporting. The trace
MUST map each observed effect to the exact M4P contract clause and applicable
BEMPIC vector without treating a lower-layer indication as a BEMPIC receipt.

A later change to any identified M4P contract commit, maximum, or visible
guarantee invalidates the confirmation for release purposes until it is reviewed
again. As of this document, no qualifying external confirmation is recorded;
the release gate remains open.
