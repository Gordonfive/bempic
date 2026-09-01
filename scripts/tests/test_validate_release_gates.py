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

    def test_every_vector_case_and_assertion_is_pinned(self) -> None:
        catalog = copy.deepcopy(gates.load_json("conformance/v0.1/vector-catalog.json"))
        v11 = next(entry for entry in catalog["catalog"] if entry["id"] == "V11")
        v11["cases"] = ["corrupt-final-byte"]
        v11["assertions"] = ["expected-outcome"]
        with patch.object(gates, "load_json", return_value=catalog):
            with self.assertRaisesRegex(ValueError, "V11 cases"):
                gates.validate_vector_catalog()

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


if __name__ == "__main__":
    unittest.main()
