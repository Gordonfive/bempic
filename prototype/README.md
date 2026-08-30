# BEMPIC Executable Semantic Proof

This directory contains the first runnable BEMPIC artifact. It proves that two local application endpoints can transfer one immutable message through multiple byte-constrained contact windows, persist a received prefix, reopen the receiver between contacts, resume at the retained offset, verify the whole representation, and decode the original message.

It is deliberately **non-normative**:

- the operation names follow the semantic plan, but their byte assignments are disposable;
- `BMSG0` and `B0` are experimental markers, not protocol identifiers;
- the 16-byte identifiers, integer widths, SHA-256 digest, record sizes, and state files are not frozen;
- this is a Python measurement/state-machine proof, not the planned Rust reference implementation;
- it implements no mesh, routing, M4P, modem, generic fragmentation, RF reliability, encryption, or real transport binding.

The proof uses only the Python standard library so it can run without installing dependencies.

## Run

From the repository root:

```bash
python3 -m prototype.demo
```

The JSON report includes every contact budget and expenditure, application-protocol bytes by direction and operation, representation payload bytes, duplicate payload bytes, integrity failures, useful committed bytes, and the final decode status.

To retain the receiver state for inspection:

```bash
python3 -m prototype.demo --state-dir /tmp/bempic-proof-state
```

## Test

```bash
python3 -m unittest prototype.tests.test_proof -v
```

The tests cover deterministic message encoding, strict decoding, all six abstract proof operations, hard byte-budget enforcement, restart/resume without duplicate payload, idempotent duplicate handling, corruption rejection, and clean retry.

## What this proves

- A prepared immutable representation has an exact known byte cost.
- No operation is emitted when it would exceed the current BEMPIC byte budget.
- A lost contact does not restart the application transfer.
- Receiver state survives reopening between every contact.
- On the reliable-carrier profile, there is no per-extent ACK loop; the next contact requests the retained offset.
- A representation is never committed until its whole SHA-256 digest and message decoding succeed.
- The final result is an application completion statement, not a network-hop acknowledgement.

## What remains

This proof intentionally postpones attachment representations, mailbox reconciliation beyond a one-object summary, compression candidates, security profiles, unreliable-carrier repair, independent decoding, and M4P binding. The next implementation phase should create the separate Rust reference repository once its repository and license are established, then port these tested semantics rather than treating this encoding as compatibility authority.
