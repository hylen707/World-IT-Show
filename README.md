# World IT Show · Graphene Claims to Engineering Evidence

**What evidence connects an exceptional material to a better appliance?**

Graphene's material properties make it a compelling platform for thermal devices. Establishing a useful product advantage also requires evidence about manufactured film quality, heat transfer, task energy, and operating conditions. This project investigates that chain through a close audit of a Graphene Square company report.

The work develops the original company research into a traceable engineering argument: preserve the source, isolate consequential claims, compare primary references, quantify the assumptions, and specify the measurements that would resolve remaining questions. Its central result is a clearer boundary between a material property, a manufacturing claim, and demonstrated device performance.

기업 조사에서 출발해 그래핀의 소재 특성이 실제 제품 성능을 뒷받침하려면 어떤 증거가 필요한지 분석했다. 수치·단위·제조 품질·에너지·안전 주장을 각각 검토하고, 재현 가능한 계산과 후속 검증 설계로 연결했다.

[Read the research report](analysis/REPORT.md) · [Inspect the evidence ledger](evidence.json) · [View automated checks](https://github.com/hylen707/World-IT-Show/actions/workflows/validate.yml)

## Findings that changed the argument

| Question | Result | Engineering implication |
| --- | --- | --- |
| What does “1 gram covers 7,140 m²” mean? | The reported value is **2.714829 times** the cited ideal two-face benchmark of **2,630 m²/g**. A corresponding one-face convention is 1,315 m²/g. | Define the surface convention and mass basis before using an area analogy. Theoretical area also differs from accessible area after stacking or transfer. |
| Does high thermal conductivity establish lower cooking energy? | In the model, a 600 W and a 1,200 W heater both require **69.667 Wh** at the same assumed task efficiency; idealized heating times differ. | Separate heating rate from energy per completed task. Device-level heat capture and losses remain necessary inputs. |
| Does a process name establish a defect-free film? | The inspected literature does not justify universal perfection from CVD alone. | Require spatial sampling, defect definitions, acceptance criteria, and yield evidence. |
| Do temperature and product descriptions establish safety or optical performance? | The available evidence leaves surface conditions, contact duration, product version, and optical assembly performance unresolved. | Bound conclusions to evaluated conditions and identify the missing assessment. |

The area calculation is a reference comparison. The thermal calculation is an illustrative sensitivity model: **none of its efficiencies or energy values is a product measurement**. The audit leaves corporate priority unresolved where research lineage and company attribution require further evidence.

## How the inquiry developed

| Stage | Completed work | Inspectable record |
| --- | --- | --- |
| Source preservation | Original 43-line report, exact bytes, numbered derivative, and export checksum | [Source register](evidence/SOURCE_REGISTER.md) |
| Claim reconstruction | **7 sources, 11 located observations, 8 bounded findings, and 2 proposals** with reasoning, counterarguments, and limitations | [Evidence ledger](evidence.json) |
| Technical review | Targeted checks of area, CVD quality, priority, energy, safety, and display claims | [Research report](analysis/REPORT.md) |
| Quantitative analysis | Explicit area conventions, task-energy assumptions, efficiency sensitivity, and power comparison | [Inputs](analysis/model-inputs.json) · [Code](tools/analyze.py) · [Results](analysis/results.json) |
| Validation design | Matched-endpoint energy protocol and film-quality inquiry, with measurement boundaries and uncertainty requirements | [Method](analysis/METHOD.md) |
| Reproducibility | Source-integrity checks, evidence-link validation, and **23 mutation and model-boundary tests** | [Validator](tools/validate.py) · [Tests](tests/test_evidence.py) |

## What remains open

The technical audit and analytical calculations are complete within the inspected sources. Physical appliance measurements and film-quality tests remain proposed work. Current manufacturer descriptions may concern a different product version from the original report, and paper abstracts have narrower evidentiary scope than complete experimental records.

The next decisive evidence would be a version-specific, matched-task wall-energy dataset, representative film-quality measurements, or a precise definition and source for the area claim. These would permit stronger conclusions while retaining the original source and the reasoning that preceded them.

## Reproduce the analysis

Python 3.10+ and the standard library are sufficient. Run from the repository root:

```bash
python tools/validate.py
python tools/analyze.py --check
python -m unittest discover -s tests -v
```

`python tools/analyze.py` regenerates the tracked numerical output. Validation checks source integrity and evidence consistency; the tests exercise corrupted sources, broken evidence links, invalid inputs, and model boundaries. Scientific interpretation still requires reading the cited evidence and assumptions.

[Validation details](docs/VALIDATION.md) · [Methods and provenance](attribution.md)
