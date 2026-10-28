# World IT Show · From graphene claims to engineering evidence

**When does a remarkable material become a demonstrably better product?**

This project examines the chain from a Graphene Square company report to manufactured film quality, heating performance and commercial evidence. It separates what the source says from what literature supports, what analytical assumptions imply, and what a device-level measurement would still need to establish.

The result is an inspectable company and technology study: a preserved source, located claims and counterarguments, quantitative checks, explicit research decisions and reproducible outputs.

기업의 소재·제품 설명을 검증 가능한 질문으로 좁혔다. 그래핀 수치와 제조 품질을 검토하고, 실제 제품 우위를 말하려면 필요한 에너지·안전·고객 적용 근거를 구분했다.

[Company brief](research/COMPANY_BRIEF.md) · [Technical report](analysis/REPORT.md) · [Research workspace](research/README.md)

<!-- research-snapshot:start -->
| Core sources | Located observations | Claims | Company cases | Technology questions | Method references | Test cases |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 7 | 11 | 10 | 1 | 4 | 3 | 41 |
<!-- research-snapshot:end -->

## Findings and their consequence

| Finding | Consequence for the company and technology argument |
| --- | --- |
| The reported 7,140 m²/g is **2.714829 times** the cited ideal two-face reference of 2,630 m²/g | Define the physical quantity and mass/face convention before using the analogy. A theoretical area is not an accessible-area measurement. |
| At fixed assumed task efficiency, the modeled 600 W and 1,200 W heaters both use **69.667 Wh** | Heating rate and energy per completed task are different endpoints. No modeled efficiency is assigned to a product. |
| CVD alone does not establish a universally defect-free film | Quality needs a process version, sampling, acceptance criteria and yield evidence. |
| Safety, optical performance and corporate priority remain version- or scope-dependent | Require the corresponding assessment, optical endpoint and attributable research lineage. Preserve unresolved questions. |

These checks narrow the claims that the inspected material supports. They do not measure a commercial appliance or establish that an advantage cannot exist.

## The research system

| Layer | What it contributes |
| --- | --- |
| [Company case](research/entities.json) | Attributed offerings, commercial questions and explicitly unknown financial/deployment metrics |
| [Technology decisions](research/assessments.json) | Evidence stage, research action and the next record that could change the conclusion |
| [Source and claim audit](evidence.json) | Located observations, reasoning, counterarguments and limitations |
| [Analytical model](tools/analyze.py) | Reproducible area conventions and task-energy sensitivity; [inputs](analysis/model-inputs.json) and [results](analysis/results.json) |
| [Measurement design](analysis/METHOD.md) | A matched-task protocol, conditions and uncertainty requirements for proposed follow-up |
| [Method benchmark](research/BENCHMARKS.md) | Exact upstream references and the practices adopted locally |

The investigation progressed from source preservation to claim reconstruction, primary-reference checks, analytical sensitivity and bounded evidence gates. The [research status](research/STATUS.md) and this overview share a generated summary, so changed records cannot silently leave the headline counts stale.

## Reproduce

Python 3.11+ and the standard library are sufficient:

```bash
python reproduce.py
```

This checks source bytes, evidence links, deterministic results, company/technology records, pinned method references, documentation consistency and the complete test suite. [Contribution guidance](CONTRIBUTING.md) describes how a changed result reaches the report and README.

## Open evidence gates

The most decisive next evidence is a version-specific matched-task wall-energy dataset, representative film-quality measurements, and an exact source for the disputed area quantity. Revenue, funding, customer deployments and a financial valuation are not established here. Physical tests remain proposed, separate from the completed literature audit and analytical calculations.

[Source register](evidence/SOURCE_REGISTER.md) · [Validation details](docs/VALIDATION.md) · [Methods and provenance](attribution.md)

[Research change record](CHANGELOG.md)
