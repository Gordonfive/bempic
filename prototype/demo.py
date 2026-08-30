"""Run the two-node interrupted-transfer proof."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from .bempic_proof import Accounting, Message, ProofExchange, ReceiverStore, prepare_message

DEFAULT_WINDOWS = (128, 71, 83, 67, 96)


def _message() -> Message:
    identity = hashlib.sha256(b"bempic-proof-message-1").digest()[:16]
    return Message(
        logical_id=identity,
        created_at=1_788_112_800,
        sender="shore@example.test",
        recipients=("sea-witch@example.test",),
        subject="BEMPIC interrupted-link proof",
        body=(
            "This tiny message crosses several constrained contact windows. "
            "The receiver is reopened from disk between contacts and requests "
            "only the unreceived suffix of the immutable representation."
        ),
    )


def run_demo(root: Path, windows: tuple[int, ...] = DEFAULT_WINDOWS) -> dict[str, object]:
    message = _message()
    representation = prepare_message(message)
    total = Accounting()
    reports: list[dict[str, object]] = []

    for contact_number in range(1, 101):
        window = windows[(contact_number - 1) % len(windows)]
        receiver = ReceiverStore(root, representation)
        exchange = ProofExchange(representation, receiver, max_record_size=96)
        report = exchange.run_contact(window)
        total.merge(report.accounting)
        reports.append(
            {
                "contact": contact_number,
                "budget": window,
                "spent": report.spent_bytes,
                "progress_before": report.progress_before,
                "progress_after": report.progress_after,
                "complete": report.complete,
                "result_sent": report.result_sent,
            }
        )
        if report.result_sent:
            break
    else:
        raise RuntimeError("proof did not complete within 100 contacts")

    receiver = ReceiverStore(root, representation)
    decoded = receiver.read_complete()
    return {
        "status": "complete" if decoded == message else "decode-mismatch",
        "contacts": len(reports),
        "simulated_restarts": max(0, len(reports) - 1),
        "representation_bytes": representation.size,
        "bempic_sender_to_receiver_bytes": total.sender_to_receiver_bytes,
        "bempic_receiver_to_sender_bytes": total.receiver_to_sender_bytes,
        "bempic_total_bytes": total.total_bempic_bytes,
        "representation_payload_bytes": total.representation_payload_bytes,
        "duplicate_payload_bytes": total.duplicate_payload_bytes,
        "useful_committed_bytes": total.useful_committed_bytes,
        "integrity_failures": total.integrity_failures,
        "operation_bytes": dict(sorted(total.operation_bytes.items())),
        "contact_reports": reports,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--state-dir",
        type=Path,
        help="retain proof state in this directory instead of a temporary directory",
    )
    args = parser.parse_args()

    if args.state_dir is not None:
        result = run_demo(args.state_dir)
    else:
        with tempfile.TemporaryDirectory(prefix="bempic-proof-") as temporary:
            result = run_demo(Path(temporary))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
