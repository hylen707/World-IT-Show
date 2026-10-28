# From graphene properties to appliance evidence

## Research abstract

This retrospective audit examines a user-supplied Graphene Square company report associated with EC4. It asks whether claims about an ideal material justify conclusions about manufactured films, cooking performance, and consumer safety. The complete text export was preserved and mapped to eleven located observations and ten claim records. A primary-paper cross-check identifies a specific-area mismatch; other issues concern attribution, manufacturing quality, endpoint definition, and overbroad safety wording. Two transparent calculations quantify the area discrepancy and the dependence of task energy on heat capture. They are analytical models, not appliance tests. The contribution of this repository is an inspectable chain from source statement to bounded conclusion, with counterarguments and a proposed validation protocol. The original author's identity, the student's personal contribution, and activity dates remain unverified.

## 한국어 설명

이 자료의 강점은 그래핀을 ‘꿈의 소재’로 소개하는 데서 한 단계 더 나아가, **소재의 특성 → 실제 제조 품질 → 기기 성능 → 안전성** 사이에 어떤 증거가 필요한지 따지는 데 있다. 원문을 지우거나 더 그럴듯하게 고치는 대신, 원문을 보존하고 주장별 근거·반론·한계를 연결했다. 이 분석은 2026년 10월 28일에 추가한 사후 검토이며, 학생이 과거에 실험하거나 논문을 검증했다고 서술하지 않는다.

## Scope and method

The unit of analysis is one falsifiable or materially consequential statement, not one company or product. S01 is the original 43-line text; S02–S04 are research-paper abstracts, S05–S06 are current manufacturer pages, and S07 is the publicly available scope of a safety guide. The audit does not assume that today's product page describes the product version behind the original report. All source records and exact locations are in [evidence.json](../evidence.json).

The review prioritizes statements where an error would materially change the argument: numbers and units; universal language; priority; mechanism; comparative performance; and absence-of-harm claims. Broader descriptions of strength, thermal conductivity, incorporation, and supply-chain strategy are retained as **reported, not independently validated** where no targeted verification was performed. Selection is risk-based and not an exhaustive materials review.

## Source-specific corrections

| Claim | Original location | Audit result | Defensible replacement / remaining evidence |
| --- | --- | --- | --- |
| C02: specific area | S01 L14–15 | 7,140 versus S02's 2,630 m²/g reference | Use the ideal-sheet convention explicitly; justify a different material/measurement if intended. |
| C03: universal perfection | S01 L30 | Method name is insufficient quality evidence; S04 provides a relevant counterexample | Require spatial quality maps, sample coverage, defect definitions, and yield criteria. |
| C04: corporate priority | S01 L29; L21–22 | S03 is from 2010; the report gives company formation as 2012 | Separate research lineage, licensing, company identity, and the particular production advance. Priority remains unresolved. |
| C05: cooker efficiency | S01 L35 | No matched-outcome energy dataset | Specify comparator, load, endpoint, wall-plug energy, repeats, and uncertainty. |
| C06: no-burn inference | S01 L38 | A temperature alone does not establish no contact harm; S07 requires context | Identify surfaces, access, duration, construction, and independent assessment; do not claim certification. |
| C07: display mechanism | S01 L39 | S05 describes an optical assembly combined with heating | Attribute the visual effect to the reported assembly; no optical performance is established here. |
| C08: industrial integration | S01 L43 | Outlook without a located contract or shipment record | Retain as source-reported strategy, not achieved deployment or impact. |

Primary references: [S02 / Stoller 2008](https://pubmed.ncbi.nlm.nih.gov/18788793/), [S03 / Bae 2010](https://www.nature.com/articles/nnano.2010.132), [S04 / Yu 2011](https://www.nature.com/articles/nmat3010), [S05 / radiator](https://www.graphenesq.co.kr/product_en/product01_03.php), [S06 / cooker](https://www.graphenesq.co.kr/product_en/product01_02.php), [S07 / ASTM scope](https://store.astm.org/standards/c1055). Abstracts and manufacturer statements have different evidentiary roles; neither establishes this student's experimental results.

## Reproducible numerical checks

Run `python tools/analyze.py`. The exact generated output is [results.json](results.json); assumptions are [model-inputs.json](model-inputs.json).

### Area conventions

The source-to-reference ratio is `7140 / 2630 = 2.714829`, an excess of approximately **171.48%** relative to the cited ideal-sheet value. If the reference counts two accessible faces, a corresponding one-face convention is 1,315 m²/g; that convention makes the discrepancy larger. The audit does not treat a soccer-field analogy as measurement, nor infer where the number originated. A theoretical benchmark also does not establish experimentally accessible surface area after stacking or transfer.

### Task energy and heat capture

For an illustrative 0.5 kg water-equivalent load heated by 60 K, choosing `c = 4180 J/(kg·K)` gives useful heat `Q = mcΔT = 125,400 J = 34.833 Wh`. This is a deliberately simplified assumed load, not food data or a specific cooker specification.

Let `η_task = Q_useful / E_wall`. This combines all losses into one effective parameter. For the same endpoint, `E_wall = Q_useful / η_task`. With an illustrative baseline `η_task = 0.50`, changing the modeled value to 0.40, 0.60, or 0.80 produces energy changes of **−25%, +16.67%, or +37.5% savings**, respectively. Negative savings means increased consumption. No modeled value is assigned to a Graphene Square device.

These scenarios make the central inference explicit: material conductivity does not determine the missing device-level parameter. At equal task efficiency a 600 W and a 1,200 W assumed heater use the same modeled energy, while idealized heating times differ. Real losses vary with time and temperature; the calculation is a sensitivity tool, not a prediction or a measurement. For purely resistive elements, heating is Joule dissipation; potential appliance gains must be located in task coupling, thermal mass, geometry, control, or losses rather than presumed from a material label.

## Strongest counterarguments

An original text export may omit diagrams or supplementary measurements. A founder's pre-incorporation research may legitimately explain technology lineage. A high-quality manufacturing process may outperform older research samples. A later product version may differ from the report. Real energy savings may exist despite incomplete public methodology. These alternatives limit the conclusion to **what is presently supported by the inspected evidence**, rather than declaring the technology ineffective or the company misleading.

## What would change the conclusion?

| Open issue | Decisive next evidence | Effect on argument |
| --- | --- | --- |
| Area value | Definition, mass basis, sample type, original numerical source | Correct error or explain a genuinely different quantity |
| Film quality | Spatially representative quality dataset with acceptance criteria | Replace a universal adjective with a measured quality/yield statement |
| Efficiency | Matched-endpoint wall-energy measurements and uncertainty | Quantify an appliance benefit within the tested task |
| Safety | Applicable version-specific independent assessment | Bound a safety claim to evaluated surfaces and conditions |
| Personal agency | Student-owned drafts, notes, decisions, and explanation | Permit specific contribution claims in a portfolio |

The technical package is inspectable now. The next student contribution should be a defensible choice—correcting a number, narrowing a claim, or executing a feasible protocol—not merely endorsing the report.

## Company and technology research extension

The [company brief](../research/COMPANY_BRIEF.md) connects the technical findings to commercialization questions without introducing unsupported financial metrics. [Technology decisions](../research/assessments.json) identify the evidence stage and next gate for each material/device question. [Method benchmarking](../research/BENCHMARKS.md) records the exact external practices adopted. Run `python reproduce.py` from the repository root to verify the integrated package.
