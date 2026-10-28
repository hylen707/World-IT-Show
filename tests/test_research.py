import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("research_checks", ROOT / "research.py")
research = importlib.util.module_from_spec(spec)
spec.loader.exec_module(research)


class ResearchContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def tearDown(self):
        self.temp.cleanup()

    def mutate(self, path, transform):
        data = json.loads((self.root / path).read_text())
        transform(data)
        (self.root / path).write_text(json.dumps(data, indent=2) + "\n")

    def test_current_research_contract(self):
        self.assertEqual(research.validate(self.root), [])
        self.assertEqual(research.check_outputs(self.root), [])

    def test_unknown_company_link_is_rejected(self):
        self.mutate("research/assessments.json", lambda d: d["assessments"][0].update(entity_ids=["missing"]))
        self.assertTrue(any("unknown reference" in e for e in research.validate(self.root)))

    def test_unknown_claim_is_rejected(self):
        self.mutate("research/entities.json", lambda d: d["entities"][0].update(claim_ids=["missing"]))
        self.assertTrue(any("unknown reference" in e for e in research.validate(self.root)))

    def test_missing_analytical_claim_route_is_rejected(self):
        evidence = research.read(self.root, "evidence.json")
        evidence["claims"].append({"id": "new-unrouted-claim", "kind": "retrospective_analysis"})
        (self.root / "evidence.json").write_text(json.dumps(evidence))
        self.assertTrue(any("no company or technology route" in e for e in research.validate(self.root)))

    def test_upstream_branch_is_not_an_immutable_pin(self):
        self.mutate("research/benchmarks.json", lambda d: d["benchmarks"][0].update(commit_sha="main"))
        self.assertTrue(any("exact upstream commit" in e for e in research.validate(self.root)))

    def test_upstream_url_cannot_drift_from_pin(self):
        self.mutate("research/benchmarks.json", lambda d: d["benchmarks"][0]["inspected_file"].update(url="https://github.com/example/repo/blob/main/README.md"))
        self.assertTrue(any("not pinned" in e for e in research.validate(self.root)))

    def test_benchmarking_cannot_become_an_endorsement(self):
        self.mutate("research/benchmarks.json", lambda d: d["benchmarks"][0].update(endorsement=True))
        self.assertTrue(any("not endorsement" in e for e in research.validate(self.root)))

    def test_commercial_metric_requires_a_record(self):
        self.mutate("research/entities.json", lambda d: d["entities"][0]["commercial_evidence"].update(revenue=100))
        self.assertTrue(any("located evidence record" in e for e in research.validate(self.root)))

    def test_vendor_material_cannot_verify_commercial_metrics(self):
        evidence = research.read(self.root, "evidence.json")
        roles = research.read(self.root, "research/protocol.json")["source_roles"]
        observation = next(o for o in evidence["observations"] if roles[o["source_id"]] in {"vendor_primary", "supplied_report", "supplied_slides"})
        self.mutate("research/entities.json", lambda d: d["entities"][0]["commercial_evidence"].update(
            revenue={"value": 100, "unit": "synthetic-test", "as_of": "2026-10-29", "observation_ids": [observation["id"]]}))
        self.assertTrue(any("lacks independent evidence" in e for e in research.validate(self.root)))

    def test_measured_stage_requires_measurement_record(self):
        self.mutate("research/assessments.json", lambda d: d["assessments"][0].update(evidence_stage="fixture_measured"))
        self.assertTrue(any("hashed measurement" in e for e in research.validate(self.root)))

    def test_synthetic_result_cannot_become_measured(self):
        path = self.root / "research/test-measurement.json"
        path.write_text(json.dumps({"data_origin": "synthetic"}))
        self.mutate("research/assessments.json", lambda d: d["assessments"][0].update(
            evidence_stage="fixture_measured", measurement_record={"path": "research/test-measurement.json", "sha256": research.digest(path)}))
        self.assertTrue(any("synthetic data cannot" in e for e in research.validate(self.root)))

    def test_adoption_target_cannot_escape_repository(self):
        self.mutate("research/benchmarks.json", lambda d: d["benchmarks"][0].update(implementation_paths=["../outside.md"]))
        self.assertTrue(any("escapes repository" in e for e in research.validate(self.root)))

    def test_unknown_source_role_is_rejected(self):
        def change(data):
            data["source_roles"][next(iter(data["source_roles"]))] = "unlimited-proof"
        self.mutate("research/protocol.json", change)
        self.assertTrue(any("invalid source role" in e for e in research.validate(self.root)))

    def test_changed_artifact_makes_snapshot_stale(self):
        path = research.read(self.root, "research/protocol.json")["tracked_artifacts"][0]
        with (self.root / path).open("a") as handle:
            handle.write("\n")
        self.assertTrue(any("snapshot.json is stale" in e for e in research.check_outputs(self.root)))

    def test_readme_summary_cannot_disagree_with_records(self):
        path = self.root / "README.md"
        content = path.read_text().replace("| Core sources |", "| Wrong sources |")
        path.write_text(content)
        self.assertTrue(any("README research summary" in e for e in research.check_outputs(self.root)))

    def test_refresh_restores_generated_summary(self):
        path = self.root / "README.md"
        path.write_text(path.read_text().replace("| Core sources |", "| Wrong sources |"))
        research.refresh(self.root)
        self.assertEqual(research.check_outputs(self.root), [])

    def release_fixture(self):
        data = research.read(self.root, "research/releases.json")
        if not data["releases"]:
            assessment = research.read(self.root, "research/assessments.json")["assessments"][0]["id"]
            data["releases"] = [{"version": "test-fixture", "published_at": "2026-10-29T00:00:00Z",
                                 "primary_url": "https://example.invalid/test-only", "release_commit": "a" * 40,
                                 "assessment_ids": [assessment], "test_status": "not_tested", "test_result": None,
                                 "effect_on_research": "Temporary mutation fixture, not a source record."}]
            (self.root / "research/releases.json").write_text(json.dumps(data))

    def test_release_notice_cannot_become_a_test_result(self):
        self.release_fixture()
        self.mutate("research/releases.json", lambda d: d["releases"][0].update(test_result={"passed": True}))
        self.assertTrue(any("not a local test result" in e for e in research.validate(self.root)))

    def test_tested_release_requires_a_fixture_record(self):
        self.release_fixture()
        self.mutate("research/releases.json", lambda d: d["releases"][0].update(test_status="fixture_tested"))
        self.assertTrue(any("hashed fixture record" in e for e in research.validate(self.root)))


if __name__ == "__main__":
    unittest.main()
