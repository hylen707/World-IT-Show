#!/usr/bin/env python3
"""Validate research records and keep the public overview synchronized."""
import argparse
import ast
import hashlib
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
START = "<!-- research-snapshot:start -->"
END = "<!-- research-snapshot:end -->"


def read(root, path):
    def invalid(value):
        raise ValueError("Nonfinite JSON value: " + value)
    return json.loads((root / path).read_text(encoding="utf-8"), parse_constant=invalid)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local(root, path):
    if not isinstance(path, str) or not path:
        raise ValueError("A nonempty local path is required")
    target = (root / path).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("Path escapes repository: " + path)
    return target


def validate(root=ROOT):
    errors = []
    def check(ok, message):
        if not ok:
            errors.append(message)
    def text(value):
        return isinstance(value, str) and bool(value.strip())
    def records(value, label):
        if not isinstance(value, list) or not value:
            errors.append(label + ": a nonempty array is required")
            return []
        if any(not isinstance(item, dict) for item in value):
            errors.append(label + ": records must be objects")
        return [item for item in value if isinstance(item, dict)]
    def indexed(items, label):
        identifiers = [item.get("id") for item in items]
        check(all(text(x) for x in identifiers), label + ": nonempty IDs required")
        safe = [x for x in identifiers if text(x)]
        check(len(safe) == len(set(safe)), label + ": duplicate IDs")
        return {item["id"]: item for item in items if text(item.get("id"))}
    def refs(values, known, label, allow_empty=False):
        if not isinstance(values, list):
            errors.append(label + ": references must be an array")
            return []
        check(allow_empty or bool(values), label + ": evidence references required")
        safe = [x for x in values if text(x)]
        check(len(safe) == len(values), label + ": references must be strings")
        check(len(safe) == len(set(safe)), label + ": duplicate references")
        for value in safe:
            check(value in known, label + ": unknown reference " + value)
        return safe
    try:
        evidence = read(root, "evidence.json")
        protocol = read(root, "research/protocol.json")
        companies = records(read(root, "research/entities.json")["entities"], "entities")
        decisions = records(read(root, "research/assessments.json")["assessments"], "assessments")
        benchmark_data = read(root, "research/benchmarks.json")
        benchmarks = records(benchmark_data["benchmarks"], "benchmarks")
        releases = read(root, "research/releases.json")
        sm = {item["id"]: item for item in evidence["sources"]}
        om = {item["id"]: item for item in evidence["observations"]}
        cm = {item["id"]: item for item in evidence["claims"]}
        em = indexed(companies, "entities")
        dm = indexed(decisions, "assessments")
        indexed(benchmarks, "benchmarks")
        roles = protocol["source_roles"]
        check(isinstance(roles, dict) and set(roles) == set(sm), "protocol: source roles must cover the exact core source set")
        if not isinstance(roles, dict):
            return errors
        allowed_roles = {"supplied_report", "supplied_slides", "research_abstract", "vendor_primary",
                         "standard", "standard_scope", "government_guidance", "synthetic",
                         "regulatory_filing", "independent_measurement", "student_record"}
        check(all(isinstance(v, str) and v in allowed_roles for v in roles.values()), "protocol: invalid source role")
        date.fromisoformat(protocol["reviewed_on"])
        check(protocol["result_type"] in {"analytical_scenarios", "synthetic_scenarios"}, "protocol: invalid result type")
        covered = set()
        independent = {"regulatory_filing", "independent_measurement"}
        for entity in companies:
            name = entity.get("id", "entity")
            check(text(entity.get("name")) and text(entity.get("research_question")), name + ": name and question required")
            refs(entity.get("source_ids"), sm, name)
            covered.update(refs(entity.get("claim_ids"), cm, name))
            check(entity.get("identity_status") == "source_reported", name + ": legal identity is not independently established")
            facts = records(entity.get("reported_offerings"), name + " offerings")
            for fact in facts:
                check(text(fact.get("description")), name + ": offering description required")
                refs(fact.get("source_ids"), sm, name + " offering")
                check(fact.get("status") == "source_reported", name + ": an offering description must retain attribution")
            metrics = entity.get("commercial_evidence")
            check(isinstance(metrics, dict), name + ": commercial evidence must be an object")
            if isinstance(metrics, dict):
                for key in ("revenue", "funding", "customer_deployments"):
                    check(key in metrics, name + ": missing commercial evidence field " + key)
                    value = metrics.get(key)
                    if value is not None:
                        if not isinstance(value, dict):
                            errors.append(name + ": commercial metric requires a located evidence record")
                            continue
                        ids = refs(value.get("observation_ids"), om, name + " commercial metric")
                        check(text(value.get("as_of")) and text(value.get("unit")), name + ": metric date and unit required")
                        check(bool(ids) and all(roles.get(om[i]["source_id"]) in independent for i in ids if i in om),
                              name + ": commercial metric lacks independent evidence")
        for item in decisions:
            name = item.get("id", "assessment")
            for field in ("technology", "rationale", "limitation"):
                check(text(item.get(field)), name + ": missing " + field)
            refs(item.get("entity_ids"), em, name)
            covered.update(refs(item.get("claim_ids"), cm, name))
            check(item.get("disposition") in {"investigate", "design_test", "replicate", "pause"}, name + ": invalid disposition")
            check(item.get("evidence_stage") in {"reported", "literature_checked", "synthetic_only", "fixture_measured"},
                  name + ": unsupported evidence stage")
            gate = item.get("next_gate")
            check(isinstance(gate, dict), name + ": next evidence gate required")
            if isinstance(gate, dict):
                for field in ("question", "required_record", "acceptance_condition"):
                    check(text(gate.get(field)), name + ": incomplete next gate")
            if item.get("evidence_stage") == "fixture_measured":
                record = item.get("measurement_record")
                if not isinstance(record, dict):
                    errors.append(name + ": measured stage requires a hashed measurement record")
                else:
                    target = local(root, record.get("path"))
                    check(target.is_file(), name + ": measurement file missing")
                    if target.is_file():
                        check(digest(target) == record.get("sha256"), name + ": measurement hash mismatch")
                        check(read(root, record["path"]).get("data_origin") == "measured",
                              name + ": synthetic data cannot support a measured stage")
        expected = {key for key, value in cm.items() if value["kind"] != "proposal"}
        check(expected <= covered, "research: an existing analytical claim has no company or technology route")
        for item in benchmarks:
            name = item.get("id", "benchmark")
            check(bool(re.fullmatch(r"[0-9a-f]{40}", str(item.get("commit_sha", "")))), name + ": exact upstream commit required")
            check(item.get("endorsement") is False, name + ": benchmarking is not endorsement")
            check(text(item.get("practice")) and text(item.get("license_note")), name + ": practice and license context required")
            supporting = item.get("supporting_files", [])
            check(isinstance(supporting, list), name + ": supporting sources must be an array")
            inspected = [item.get("inspected_file")] + (supporting if isinstance(supporting, list) else [])
            for source in inspected:
                if not isinstance(source, dict):
                    errors.append(name + ": inspected source file required")
                    continue
                check(text(source.get("path")), name + ": inspected source path required")
                start, end = source.get("line_start"), source.get("line_end")
                valid = type(start) is int and type(end) is int and 0 < start <= end
                check(valid, name + ": invalid upstream line range")
                expected_url = "https://github.com/{}/blob/{}/{}#L{}-L{}".format(
                    item.get("repository"), item.get("commit_sha"), source.get("path"), start, end)
                check(source.get("url") == expected_url, name + ": source URL is not pinned to the inspected commit")
                check(bool(re.fullmatch(r"[0-9a-f]{40}", str(source.get("blob_sha", "")))), name + ": source blob SHA required")
            targets = item.get("implementation_paths")
            check(isinstance(targets, list) and bool(targets), name + ": implementation paths required")
            if isinstance(targets, list):
                for path in targets:
                    check(local(root, path).is_file() or path in {"research/STATUS.md", "research/snapshot.json"},
                          name + ": adoption target missing")
        check(isinstance(releases.get("releases"), list), "releases: expected an array")
        for item in releases.get("releases", []):
            refs(item.get("assessment_ids"), dm, "release")
            check(item.get("test_status") in {"not_tested", "fixture_tested"}, "release: invalid test status")
            if item.get("test_status") == "not_tested":
                check(item.get("test_result") is None, "release: a release notice is not a local test result")
            elif item.get("test_status") == "fixture_tested":
                record = item.get("test_result")
                if not isinstance(record, dict):
                    errors.append("release: tested status requires a hashed fixture record")
                else:
                    target = local(root, record.get("path"))
                    check(target.is_file(), "release: fixture result file missing")
                    if target.is_file():
                        check(digest(target) == record.get("sha256"), "release: fixture result hash mismatch")
                        measurement = read(root, record["path"])
                        check(measurement.get("data_origin") == "measured", "release: fixture result must be measured")
                        check(isinstance(measurement.get("configuration"), dict) and bool(measurement["configuration"]),
                              "release: complete fixture configuration required")
                        check(isinstance(measurement.get("negative_controls"), list) and bool(measurement["negative_controls"]),
                              "release: negative controls required")
            check(bool(re.fullmatch(r"[0-9a-f]{40}", str(item.get("release_commit", "")))), "release: immutable release commit required")
            for field in ("version", "published_at", "primary_url", "effect_on_research"):
                check(text(item.get(field)), "release: missing " + field)
        for path in protocol["tracked_artifacts"]:
            check(local(root, path).is_file(), "snapshot input missing: " + path)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        errors.append("research input: " + str(exc))
    return errors


def snapshot(root=ROOT):
    evidence = read(root, "evidence.json")
    protocol = read(root, "research/protocol.json")
    tests = sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")
                for path in (root / "tests").glob("test_*.py") for node in ast.walk(ast.parse(path.read_text())))
    return {"schema_version": "1.0", "reviewed_on": protocol["reviewed_on"],
            "result_type": protocol["result_type"],
            "counts": {"sources": len(evidence["sources"]), "observations": len(evidence["observations"]),
                       "claims": len(evidence["claims"]),
                       "entities": len(read(root, "research/entities.json")["entities"]),
                       "assessments": len(read(root, "research/assessments.json")["assessments"]),
                       "benchmarks": len(read(root, "research/benchmarks.json")["benchmarks"]),
                       "test_definitions": tests},
            "artifact_sha256": {path: digest(local(root, path)) for path in sorted(protocol["tracked_artifacts"])}}


def overview(data):
    c = data["counts"]
    return "\n".join([START, "| Core sources | Located observations | Claims | Company cases | Technology questions | Method references | Test cases |",
                      "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
                      "| {sources} | {observations} | {claims} | {entities} | {assessments} | {benchmarks} | {test_definitions} |".format(**c),
                      END])


def status(root, data):
    entities = read(root, "research/entities.json")["entities"]
    assessments = read(root, "research/assessments.json")["assessments"]
    lines = ["# Research status", "", "Evidence review: **" + data["reviewed_on"] + "**.",
             "Generated from versioned research records. Counts describe this repository, not external market coverage.",
             "", overview(data), "", "## Company questions", ""]
    for item in entities:
        lines += ["- **" + item["name"] + "**: " + item["research_question"]]
    lines += ["", "## Technology decisions", "", "| Technology | Evidence stage | Next action | Required next evidence |",
              "| --- | --- | --- | --- |"]
    for item in assessments:
        values = [item["technology"], item["evidence_stage"], item["disposition"], item["next_gate"]["required_record"]]
        lines.append("| " + " | ".join(value.replace("|", "/") for value in values) + " |")
    lines += ["", "These are research actions, not production-readiness ratings or vendor rankings.",
              "See [assessments](assessments.json), [company cases](entities.json), and [benchmark adoption](BENCHMARKS.md).", ""]
    return "\n".join(lines)


def check_outputs(root=ROOT):
    errors = []
    data = snapshot(root)
    if read(root, "research/snapshot.json") != data:
        errors.append("research/snapshot.json is stale; inspect changes and run python research.py --write")
    expected = overview(data)
    content = (root / "README.md").read_text()
    if content.count(START) != 1 or content.count(END) != 1 or expected not in content:
        errors.append("README research summary is stale or missing")
    if (root / "research/STATUS.md").read_text() != status(root, data):
        errors.append("research/STATUS.md is stale")
    for path in root.rglob("*.md"):
        if any(part in {".git", "__pycache__"} for part in path.relative_to(root).parts):
            continue
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            if target and not (path.parent / target).exists():
                errors.append("broken documentation link: " + str(path.relative_to(root)) + " -> " + target)
    return errors


def refresh(root=ROOT):
    data = snapshot(root)
    path = root / "README.md"
    content = path.read_text()
    if content.count(START) != 1 or content.count(END) != 1:
        raise ValueError("README requires exactly one research summary marker pair")
    content = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda match: overview(data), content, flags=re.DOTALL)
    path.write_text(content, encoding="utf-8")
    (root / "research/snapshot.json").write_text(json.dumps(data, indent=2) + "\n")
    (root / "research/STATUS.md").write_text(status(root, data), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Refresh the reviewed snapshot and README summary")
    parser.add_argument("--check", action="store_true", help="Check without modifying tracked files (default)")
    args = parser.parse_args()
    errors = validate()
    if not errors:
        try:
            if args.write:
                refresh()
            errors += check_outputs()
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append("generated research record: " + str(exc))
    if errors:
        print("\n".join("FAIL: " + error for error in errors))
        return 1
    print("PASS: pinned methods, company/technology evidence, source hashes, README and research status")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
