# Validation and readiness

## Automated checks

`tools/validate.py` implements the schema keywords used in the published project/evidence schemas: local `$ref`, `type`, `required`, `properties`, `items`, `const`, `enum`, `minLength`, `pattern`, and `minimum`. It is a project validator, not a general JSON Schema engine. It additionally checks ID uniqueness, source/observation references, exact claim locators, readable-source requirements, original-source line bounds, project/source agreement, exact original bytes, and the normalized derivative.

Non-null personal facts need located observation references. Submission mode additionally requires a student-record source for authorship/contribution verification. These checks cannot authenticate a student's signature or decide whether a scientific inference is true; human source review remains necessary.

`tools/analyze.py --check` compares a fresh deterministic calculation with the tracked result. Tests mutate inputs to ensure unbacked findings, false evidence links, fabricated metadata, corrupted originals, and completed-work labels for proposals are rejected. Model tests exercise zero/invalid efficiency and a negative savings case.

## Expected current results

| Command | Expected result | Meaning |
| --- | --- | --- |
| `python tools/validate.py` | Exit 0 | Draft structure, located evidence, and source integrity are consistent |
| `python tools/analyze.py --check` | Exit 0 | Model output matches code and assumptions |
| `python -m unittest discover -s tests -v` | Exit 0 | Rejection paths and model boundaries pass |
| `python tools/validate.py --submission` | Exit 1 | Personal contribution and activity verification remain pending |

Current submission blockers: `student_verification=pending`, `artifact_state=draft`, no located student contribution verification, and `activity_dates`, `hours`, and `role` are `null`. Impact also remains unknown; it is not a mandatory claim and must not be manufactured to pass a check.

## Manual technical review

Check the original claim against its location. Confirm the external source is primary and that its inspected scope supports only the stated conclusion. Inspect the strongest alternative explanation. Re-run the calculation and state what is assumed rather than measured. Keep company-reported current product details separate from an undated original report. Review student ownership separately from technical correctness.
