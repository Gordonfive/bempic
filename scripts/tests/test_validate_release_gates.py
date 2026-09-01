from __future__ import annotations

import copy
import unittest
from unittest.mock import patch

from scripts import validate_release_gates as gates


class ReleaseGateValidatorTests(unittest.TestCase):
    def test_metric_threshold_fields_are_pinned(self) -> None:
        metrics = copy.deepcopy(gates.load_json("conformance/v0.1/metrics.json"))
        metrics["thresholds"][0]["operator"] = ">="
        metrics["thresholds"][0]["value"] = 999999
        with patch.object(gates, "load_json", return_value=metrics):
            with self.assertRaisesRegex(ValueError, "threshold definitions"):
                gates.validate_metrics()

    def test_semantic_bytes_definition_and_required_counters_are_pinned(self) -> None:
        metrics = copy.deepcopy(gates.load_json("conformance/v0.1/metrics.json"))
        metrics["semantic_bytes_definition"]["excluded"].remove("duplicates")
        with patch.object(gates, "load_json", return_value=metrics):
            with self.assertRaisesRegex(ValueError, "semantic_bytes definition"):
                gates.validate_metrics()

        metrics = copy.deepcopy(gates.load_json("conformance/v0.1/metrics.json"))
        metrics["required"].remove("semantic_bytes_receive")
        with patch.object(gates, "load_json", return_value=metrics):
            with self.assertRaisesRegex(ValueError, "required metric names"):
                gates.validate_metrics()

    def test_semantic_direction_and_descriptor_exclusion_are_pinned(self) -> None:
        metrics = copy.deepcopy(gates.load_json("conformance/v0.1/metrics.json"))
        metrics["semantic_bytes_definition"]["direction_basis"]["send"] = (
            "owner-to-requester"
        )
        with patch.object(gates, "load_json", return_value=metrics):
            with self.assertRaisesRegex(ValueError, "semantic_bytes definition"):
                gates.validate_metrics()

        metrics = copy.deepcopy(gates.load_json("conformance/v0.1/metrics.json"))
        metrics["semantic_bytes_definition"]["excluded"].remove(
            "representation-descriptor-container-and-members"
        )
        with patch.object(gates, "load_json", return_value=metrics):
            with self.assertRaisesRegex(ValueError, "semantic_bytes definition"):
                gates.validate_metrics()

    def test_every_vector_case_and_assertion_is_pinned(self) -> None:
        catalog = copy.deepcopy(gates.load_json("conformance/v0.1/vector-catalog.json"))
        v11 = next(entry for entry in catalog["catalog"] if entry["id"] == "V11")
        v11["cases"] = ["corrupt-final-byte"]
        v11["assertions"] = ["expected-outcome"]
        with patch.object(gates, "load_json", return_value=catalog):
            with self.assertRaisesRegex(ValueError, "V11 cases"):
                gates.validate_vector_catalog()

    def test_v08_pairwise_rows_and_storage_axes_are_pinned(self) -> None:
        catalog = copy.deepcopy(gates.load_json("conformance/v0.1/vector-catalog.json"))
        v08 = next(entry for entry in catalog["catalog"] if entry["id"] == "V08")
        v08["coverage_rows"][0]["storage"] = "durable-store"
        with patch.object(gates, "load_json", return_value=catalog):
            with self.assertRaisesRegex(ValueError, "V08 coverage_rows"):
                gates.validate_vector_catalog()

    def test_v08_pairwise_proof_rejects_missing_pair(self) -> None:
        rows = gates.expected_v08_coverage_rows()
        rows[0] = copy.deepcopy(rows[1])
        rows[0]["id"] = "V08-C01"
        with self.assertRaisesRegex(ValueError, "interruption-point/restart pair"):
            gates.validate_v08_pairwise(rows)

    def test_codec_allocation_must_match_allocatable_range(self) -> None:
        registry = copy.deepcopy(gates.load_json("conformance/v0.1/codec-registry.json"))
        invalid_allocations = (
            {"id": -1, "revision": 1, "status": "experimental"},
            {"id": 0, "revision": 1, "status": "experimental"},
            {"id": 65536, "revision": 1, "status": "approved"},
            {"id": 2147483648, "revision": 1, "status": "experimental"},
            {"id": 4294967296, "revision": 1, "status": "mandatory"},
        )
        for allocation in invalid_allocations:
            with self.subTest(allocation=allocation):
                candidate = copy.deepcopy(registry)
                candidate["allocations"] = [allocation]
                with patch.object(gates, "load_json", return_value=candidate):
                    with self.assertRaises(ValueError):
                        gates.validate_codec_registry()

    def test_allocatable_codec_statuses_are_accepted(self) -> None:
        registry = copy.deepcopy(gates.load_json("conformance/v0.1/codec-registry.json"))
        registry["allocations"] = [
            {"id": 1, "revision": 1, "status": "approved"},
            {"id": 1, "revision": 2, "status": "mandatory"},
            {"id": 65536, "revision": 1, "status": "experimental"},
            {"id": 65536, "revision": 2, "status": "deprecated"},
        ]
        with patch.object(gates, "load_json", return_value=registry):
            gates.validate_codec_registry()

    def test_blocked_reference_checkpoint_cannot_be_promoted(self) -> None:
        release = copy.deepcopy(
            gates.load_json("conformance/v0.1/release-record-template.json")
        )
        release["current_reference_evidence"]["accepted_as_release_evidence"] = True
        with patch.object(gates, "load_json", return_value=release):
            with self.assertRaisesRegex(ValueError, "cannot be accepted"):
                gates.validate_release_template()


if __name__ == "__main__":
    unittest.main()
