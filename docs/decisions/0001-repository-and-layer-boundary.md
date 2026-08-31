# Decision 0001: Repository and Layer Boundary

**Status:** Accepted

**Date:** 2026-08-31

## Context

Early planning risked making BEMPIC another mesh/network protocol and kept the
semantic prototype beside specification work. OceanMail has since selected M4P
for the network role, and executable reference work has a sibling repository.

## Decision

The authoritative architecture is OceanMail → BEMPIC → M4P → DataLink
adapters. BEMPIC owns application synchronization and must not duplicate M4P or
link behavior.

This repository owns the public specification, governance, conformance and
vector definitions, and rationale. `bempic-reference` owns executable reference
work. The existing Python prototype remains here, explicitly transitional,
until behavioral parity is demonstrated in the sibling.

## Consequences

- Network and routing proposals are redirected to M4P.
- Product policy is redirected to OceanMail.
- Normative requirements land here before or with reference work.
- No v0.1.0 tag is possible without a recorded, passing sibling commit.
- Removing the Python prototype requires a later decision after parity.
