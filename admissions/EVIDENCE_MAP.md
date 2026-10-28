# Student review and application evidence map

## Neutral factual compression — not a submission response

**English:** The supplied Graphene Square report covers graphene properties, CVD production, and heating appliances. This repository adds a retrospective evidence audit, an area-convention check, and an illustrative task-energy model. Student authorship, original activity context, and independent technical understanding require verification before any personal accomplishment is described.

**한국어:** 공유된 그래핀스퀘어 기업 보고서를 바탕으로 소재 특성과 기기 성능 사이의 논증을 검토하고, 비표면적 수치와 가정에 따른 에너지 모델을 정리한 저장소다. 원문 작성자·실제 활동 맥락·학생의 독립적인 이해는 아직 확인 전이다. 이 정리 작업 자체를 학생의 과거 활동으로 쓰지 않는다.

## What a reviewer can inspect

| Potential quality | Existing evidence | Current personal-claim limit |
| --- | --- | --- |
| Focused inquiry | [Research report](../analysis/REPORT.md) and source-specific questions | The audit question was developed retrospectively with AI assistance |
| Source criticism | [Claim ledger](../evidence.json), C02–C08 | Do not say the student performed these checks without verification |
| Quantitative reasoning | [Inputs](../analysis/model-inputs.json), [code](../tools/analyze.py), [results](../analysis/results.json) | Illustrative calculation, not experimental performance |
| Reproducibility | [Validator](../tools/validate.py), [mutation tests](../tests/test_evidence.py) | Tool execution is distinct from original activity ownership |
| Personal agency | No located student-verification record yet | No role, hours, leadership, award, or impact claim |
| Reflection | Student responses not supplied | No invented change of belief |

## Prompts for the student's own writing

1. 원문에서 본인이 직접 작성한 부분은 어디이며, 작성 당시 어떤 자료를 실제로 읽었는가?
2. 그래핀에 대한 최초의 생각과 지금의 생각이 다르다면, 어느 근거 때문에 달라졌는가? 실제로 그런 변화가 없었다면 만들지 않는다.
3. Why does a material's thermal conductivity fail to determine an appliance's task energy? Explain without reading the report.
4. What would distinguish a numerical error from a change in area convention? Reproduce the ratio and explain its limits.
5. Which counterargument to this audit is strongest? What evidence would change the conclusion?
6. Which part of the follow-up protocol would the student personally choose and carry out, given real access and constraints?

After answering, select only personally true facts, write independently in the student's own voice, and follow each institution's current authorship instructions. Do not convert a proposal into a completed experiment, modeled savings into measured savings, or commit count into time spent.

## Verification record to add later

Create a dated, student-owned review note containing original artifact links, actual dates/hours and their basis, exact contribution boundaries, corrections to this package, and explanations of the models. Remove private identifiers before publication. Link located observations from that record in `project.json` via `verification_evidence_ids` and `personal_field_evidence`. Flags alone are insufficient; `--submission` requires evidence linkage.
