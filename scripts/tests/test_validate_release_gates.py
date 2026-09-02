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

    def test_reviewed_codec_allocation_is_pinned(self) -> None:
        registry = copy.deepcopy(gates.load_json("conformance/v0.1/codec-registry.json"))
        registry["allocations"][0]["id"] = 65537
        with patch.object(gates, "load_json", return_value=registry):
            with self.assertRaisesRegex(ValueError, "reviewed compact codec"):
                gates.validate_codec_registry()

        registry = copy.deepcopy(gates.load_json("conformance/v0.1/codec-registry.json"))
        registry["allocations"][0]["status"] = "approved"
        with patch.object(gates, "load_json", return_value=registry):
            with self.assertRaises(ValueError):
                gates.validate_codec_registry()

    def test_allocation_package_public_tuple_is_pinned(self) -> None:
        allocation = copy.deepcopy(
            gates.load_json("conformance/v0.1/experimental-codec-allocation.json")
        )
        allocation["allocation"]["revision"] = 2
        with patch.object(gates, "load_json", return_value=allocation):
            with self.assertRaisesRegex(ValueError, "public tuple or status"):
                gates.validate_experimental_codec_allocation()

    def test_private_candidate_cannot_be_promoted_to_release_evidence(self) -> None:
        allocation = copy.deepcopy(
            gates.load_json("conformance/v0.1/experimental-codec-allocation.json")
        )
        allocation["private_candidate_provenance"]["artifacts"][
            "conformance_report"
        ]["accepted_as_release_evidence"] = True
        with patch.object(gates, "load_json", return_value=allocation):
            with self.assertRaisesRegex(ValueError, "cannot become release evidence"):
                gates.validate_experimental_codec_allocation()

    def test_private_candidate_requires_public_vector_regeneration(self) -> None:
        allocation = copy.deepcopy(
            gates.load_json("conformance/v0.1/experimental-codec-allocation.json")
        )
        allocation["private_candidate_measurements"][
            "public_tuple_regeneration_required"
        ] = False
        with patch.object(gates, "load_json", return_value=allocation):
            with self.assertRaisesRegex(ValueError, "changed or promoted"):
                gates.validate_experimental_codec_allocation()

    def test_compact_data_payload_ceiling_is_pinned(self) -> None:
        allocation = copy.deepcopy(
            gates.load_json("conformance/v0.1/experimental-codec-allocation.json")
        )
        allocation["maximum_encoded_sizes"]["data_payload_ceiling"] = 1048526
        with patch.object(gates, "load_json", return_value=allocation):
            with self.assertRaisesRegex(ValueError, "DATA payload ceiling"):
                gates.validate_experimental_codec_allocation()

    def test_same_owner_verifier_cannot_claim_independent_ownership(self) -> None:
        allocation = copy.deepcopy(
            gates.load_json("conformance/v0.1/experimental-codec-allocation.json")
        )
        allocation["private_candidate_provenance"]["artifacts"][
            "independent_language_verifier"
        ]["independent_ownership"] = True
        with patch.object(gates, "load_json", return_value=allocation):
            with self.assertRaisesRegex(ValueError, "independent ownership"):
                gates.validate_experimental_codec_allocation()

    def test_oceanmail_profile_cannot_replace_v11_evidence(self) -> None:
        allocation = copy.deepcopy(
            gates.load_json("conformance/v0.1/experimental-codec-allocation.json")
        )
        allocation["oceanmail_application_evidence"][
            "accepted_as_complete_bempic_v11_release_evidence"
        ] = True
        with patch.object(gates, "load_json", return_value=allocation):
            with self.assertRaisesRegex(ValueError, "over-promoted"):
                gates.validate_experimental_codec_allocation()

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
