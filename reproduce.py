#!/usr/bin/env python3
"""Run all offline evidence, research, reproduction and test checks."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(*args):
    subprocess.run([sys.executable, *map(str, args)], cwd=ROOT, check=True)


def main():
    project = json.loads((ROOT / "project.json").read_text())
    if project["ec_id"] == "EC4":
        run("tools/validate.py")
        run("tools/analyze.py", "--check")
    elif project["ec_id"] == "EC5":
        run("scripts/validate_project.py")
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            run("scripts/ingest_pptx.py", "sources/original.pptx", temp / "slides.json")
            run("scripts/migration_model.py", "--output", temp / "scenarios.json")
            pairs = [(temp / "slides.json", ROOT / "sources/slides.json"),
                     (temp / "scenarios.json", ROOT / "results/migration_scenarios.json")]
            for actual, expected in pairs:
                if json.loads(actual.read_text()) != json.loads(expected.read_text()):
                    raise ValueError("Generated JSON differs: " + str(expected.relative_to(ROOT)))
            if (temp / "scenarios.csv").read_bytes() != (ROOT / "results/migration_scenarios.csv").read_bytes():
                raise ValueError("Generated scenario CSV differs")
    else:
        raise ValueError("Unsupported research project")
    run("research.py", "--check")
    run("-m", "unittest", "discover", "-s", "tests", "-v")
    print("PASS: complete offline research verification")


if __name__ == "__main__":
    main()
