from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from prototype.bempic_proof import (
    Accounting,
    IntegrityError,
    Message,
    ProofExchange,
    ReceiverStore,
    StoreError,
    decode_message,
    encode_message,
    prepare_message,
)
from prototype.bempic_proof.codec import DecodeError
from prototype.bempic_proof.operations import (
    Capabilities,
    Data,
    Offer,
    OperationError,
    Request,
    Result,
    Summary,
    decode_operation,
    encode_operation,
)


def fixture_message(body: str | None = None) -> Message:
    return Message(
        logical_id=hashlib.sha256(b"fixture-message").digest()[:16],
        created_at=1_788_112_800,
        sender="sender@example.test",
        recipients=("one@example.test", "two@example.test"),
        subject="Interrupted synchronization",
        body=body or ("useful text " * 40),
    )


class CodecTests(unittest.TestCase):
    def test_message_round_trip_is_deterministic(self) -> None:
        message = fixture_message()
        first = encode_message(message)
        second = encode_message(message)
        self.assertEqual(first, second)
        self.assertEqual(decode_message(first), message)
        self.assertEqual(prepare_message(message).size, len(first))

    def test_message_decoder_rejects_truncation_and_trailing_bytes(self) -> None:
        encoded = encode_message(fixture_message())
        with self.assertRaises(DecodeError):
            decode_message(encoded[:-1])
        with self.assertRaises(DecodeError):
            decode_message(encoded + b"x")

    def test_all_proof_operations_round_trip(self) -> None:
        representation = prepare_message(fixture_message())
        operations = (
            Capabilities(0, 96, 0),
            Summary(1, representation.representation_id),
            Offer(representation.representation_id, representation.size, representation.digest),
            Request(representation.representation_id, 17, 31),
            Data(representation.representation_id, 17, b"payload"),
            Result(representation.representation_id, True, representation.digest),
        )
        for operation in operations:
            with self.subTest(operation=type(operation).__name__):
                self.assertEqual(decode_operation(encode_operation(operation)), operation)

    def test_unknown_operation_is_rejected(self) -> None:
        with self.assertRaises(OperationError):
            decode_operation(b"B0\xff\x00\x00")


class ExchangeTests(unittest.TestCase):
    def test_interrupted_contacts_resume_without_payload_retransmission(self) -> None:
        message = fixture_message()
        representation = prepare_message(message)
        total = Accounting()
        contacts = 0
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            windows = (128, 71, 83, 67, 96)
            for contacts in range(1, 101):
                receiver = ReceiverStore(root, representation)
                report = ProofExchange(representation, receiver).run_contact(
                    windows[(contacts - 1) % len(windows)]
                )
                total.merge(report.accounting)
                self.assertLessEqual(report.spent_bytes, report.budget_bytes)
                if report.result_sent:
                    break
            else:
                self.fail("exchange did not complete")

            reopened = ReceiverStore(root, representation)
            self.assertEqual(reopened.read_complete(), message)

        self.assertGreater(contacts, 2)
        self.assertEqual(total.representation_payload_bytes, representation.size)
        self.assertEqual(total.duplicate_payload_bytes, 0)
        self.assertEqual(total.useful_committed_bytes, representation.size)

    def test_every_contact_respects_its_hard_budget(self) -> None:
        representation = prepare_message(fixture_message())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for budget in range(0, 130):
                receiver = ReceiverStore(root, representation)
                report = ProofExchange(representation, receiver).run_contact(budget)
                self.assertLessEqual(report.spent_bytes, budget)

    def test_corruption_is_never_committed_and_clean_retry_recovers(self) -> None:
        message = fixture_message("integrity proof " * 8)
        representation = prepare_message(message)
        total = Accounting()
        saw_failure = False
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            corrupt = True
            for _ in range(20):
                receiver = ReceiverStore(root, representation)
                report = ProofExchange(representation, receiver).run_contact(
                    256, corrupt_next_data=corrupt
                )
                corrupt = False
                total.merge(report.accounting)
                if report.accounting.integrity_failures:
                    saw_failure = True
                    self.assertFalse(ReceiverStore(root, representation).is_complete)
                    break
            self.assertTrue(saw_failure)

            for _ in range(20):
                receiver = ReceiverStore(root, representation)
                report = ProofExchange(representation, receiver).run_contact(256)
                total.merge(report.accounting)
                if report.result_sent:
                    break
            else:
                self.fail("clean retry did not complete")
            self.assertEqual(ReceiverStore(root, representation).read_complete(), message)

        self.assertEqual(total.integrity_failures, 1)
        self.assertGreater(total.representation_payload_bytes, representation.size)

    def test_matching_duplicate_is_idempotent_and_conflict_is_rejected(self) -> None:
        representation = prepare_message(fixture_message("duplicate proof"))
        with tempfile.TemporaryDirectory() as temporary:
            store = ReceiverStore(Path(temporary), representation)
            chunk = representation.encoded[:12]
            self.assertEqual(store.accept_data(0, chunk), (12, 0))
            self.assertEqual(store.accept_data(0, chunk), (0, 12))
            self.assertEqual(store.progress, 12)
            with self.assertRaises(StoreError):
                store.accept_data(0, b"x" + chunk[1:])

    def test_reopened_committed_file_is_reverified(self) -> None:
        representation = prepare_message(fixture_message("commit verification"))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for _ in range(20):
                store = ReceiverStore(root, representation)
                report = ProofExchange(representation, store).run_contact(256)
                if report.result_sent:
                    break
            else:
                self.fail("exchange did not complete")

            store = ReceiverStore(root, representation)
            committed = bytearray(store.complete_path.read_bytes())
            committed[-1] ^= 0x01
            store.complete_path.write_bytes(committed)
            with self.assertRaises(IntegrityError):
                ReceiverStore(root, representation)


if __name__ == "__main__":
    unittest.main()
