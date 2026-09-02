# BEMPIC development freeze — work report

**Date:** 2026-09-02

## Objective

Owner-authorized halt/freeze of BEMPIC development while OceanMail 0.2 establishes and measures an HERMES-derived real communications baseline.

This is preservation of research, not a release, conformance claim, or permanent abandonment decision.

## Preservation

Created `archive/v0.1-generation` from the pre-freeze `main` state. The archive preserves the complete active v0.1 roadmap, release gates, specification, research, vectors, and implementation handoffs as they existed before the freeze.

No `v0.1.0` tag/release was created. BEMPIC remained an unreleased release candidate with no stable public wire codec.

## Changes on `main`

- `docs/FROZEN-2026-09-02.md` — accepted freeze decision, rules, and evidence required for reactivation; commit `c0b1f7c1880390a7b3d61cdfb215be35070a0fa1`.
- `README.md` — makes frozen status prominent and describes the old OceanMail/BEMPIC/M4P stack as historical context; commit `2fffb13771ebe3bb912777b9a4ade9e05c4db2a9`.
- `docs/ROADMAP-v0.1.0.md` — replaces the former active release-gate roadmap on `main` with a frozen historical pointer; the full checklist remains on the archive branch; commit `2d4c3f78c9b697b228e5419958cb64328d2db249`.
- `AGENTS.md` — makes the freeze highest-priority agent authority and prevents silent protocol/codec/conformance development; commit `d2497b757cb7bb0c056c8e6e570817a81ede1d32`.

## Freeze rule

Until the owner explicitly lifts the freeze:

- no stable/public codec selection;
- no v0.1 release completion work;
- no new protocol/conformance feature work;
- no OceanMail integration work;
- no M4P-binding completion work; and
- no speculative changes to chase HERMES compatibility.

Maintenance/security/licensing/documentation corrections required to preserve the research accurately remain possible when explicitly authorized.

## Reactivation condition

BEMPIC may resume only after direct comparison against the HERMES `UUCP + uuxcomp` baseline under equivalent constrained-link/modem conditions demonstrates material value worth the new protocol's implementation, security, interoperability, and maintenance cost.

Potential evidence includes materially lower airtime/bytes, higher completion under interrupted/asymmetric contacts, useful cross-peer/cross-transport continuation, or selective synchronization/budget behavior not economically available from the baseline.

## Verification

This transition changed documentation/authority only. No BEMPIC executable source, codec, vectors, fixtures, schema, or test behavior was modified.

Existing executable verification suite: **not rerun / not applicable to documentation-only freeze changes**.

No tag, release, package publication, or deployment occurred.

## Cross-repository notes

The owner explicitly authorized matching changes in:

- `Gordonfive/oceanmail` — OceanMail 0.2 HERMES transition accepted;
- `Gordonfive/oceanmail-server` — hosted service retained with generic gateway boundary;
- `Gordonfive/oceanmail-infrastructure` — HERMES-derived gateway deployment direction; and
- `Gordonfive/bempic-reference` — implementation/conformance research frozen.

M4P integration is tabled in OceanMail. BEMPIC remains service-neutral research and is not being rewritten as an HERMES-specific protocol.

## Failures and recoveries

None in the BEMPIC repository during the freeze changes.

## Remaining blockers / deferred work

All former v0.1 release blockers remain intentionally unresolved while frozen. They are no longer an active work queue.

The next legitimate protocol-development step, if any, is a new roadmap created only after comparable HERMES-baseline measurements justify reactivation.

## Final revision note

The latest BEMPIC `main` commit before this report was `d2497b757cb7bb0c056c8e6e570817a81ede1d32`. The commit containing this report is the next Git history entry and is the authoritative freeze completion record.
