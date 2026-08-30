"""Reusable restart-between-contacts runner for proof experiments."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .exchange import Accounting, ContactReport, ProofExchange
from .model import Message, PreparedRepresentation
from .store import ReceiverStore


@dataclass(frozen=True, slots=True)
class TransferRun:
    reports: tuple[ContactReport, ...]
    accounting: Accounting
    value: Message | bytes

    @property
    def contacts(self) -> int:
        return len(self.reports)

    @property
    def simulated_restarts(self) -> int:
        return max(0, self.contacts - 1)


def run_until_complete(
    root: Path,
    representation: PreparedRepresentation,
    contact_windows: tuple[int, ...],
    *,
    max_record_size: int = 96,
    max_contacts: int = 1_000,
    corrupt_contacts: frozenset[int] = frozenset(),
) -> TransferRun:
    """Reopen receiver state for every contact and run through final RESULT."""

    if not contact_windows:
        raise ValueError("at least one contact window is required")
    if max_contacts <= 0:
        raise ValueError("max_contacts must be positive")

    total = Accounting()
    reports = []
    for contact_number in range(1, max_contacts + 1):
        receiver = ReceiverStore(root, representation)
        exchange = ProofExchange(
            representation,
            receiver,
            max_record_size=max_record_size,
        )
        report = exchange.run_contact(
            contact_windows[(contact_number - 1) % len(contact_windows)],
            corrupt_next_data=contact_number in corrupt_contacts,
        )
        total.merge(report.accounting)
        reports.append(report)
        if report.result_sent:
            final_receiver = ReceiverStore(root, representation)
            return TransferRun(tuple(reports), total, final_receiver.read_complete())

    raise RuntimeError(f"proof did not complete within {max_contacts} contacts")
