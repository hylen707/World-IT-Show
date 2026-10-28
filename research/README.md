# Research workspace

| Route | Inspectable artifact |
| --- | --- |
| Current coverage and actions | [Research status](STATUS.md) |
| Company proposition and evidence gaps | [Company brief](COMPANY_BRIEF.md) · [typed cases](entities.json) |
| Technology decisions and next gates | [Assessments](assessments.json) |
| External method comparison | [Benchmark adoption](BENCHMARKS.md) · [immutable source register](benchmarks.json) |
| Evidence classes and comparison rules | [Protocol](protocol.json) |
| Dated release context | [Release watch](releases.json) |
| Technical and contribution review | [Review record](../docs/review/REVIEW_GUIDE.md) |
| Design rationale | [Research decisions](DECISIONS.md) |
| Reproduction inputs and hashes | [Snapshot](snapshot.json) |

The core evidence ledger remains the source for technical claims. Method references and release notices are separate research context; they are not added to the core claim-source count or treated as experiments.

Run the full offline verification from the repository root:

    python reproduce.py

After reviewing changed research inputs, refresh the generated status and README summary:

    python research.py --write

Review narrative conclusions separately. The refresh synchronizes metadata and hashes; it does not write the scientific interpretation.
