# Method benchmark and adoption record

Reviewed on **2026-10-29**. Selection favors identifiable maintainers, inspectable method, versioned artifacts and a relevant research practice.
Popularity is not a quality score. These references inform repository design; they do not endorse this project or verify its findings.

| Reference | Inspected practice | Local implementation |
| --- | --- | --- |
| [OpenBB / OpenBQ](https://github.com/openbq-org/OpenBB/blob/7df7d0c5592bf25be88e87e130a05c71e243d2d8/openbb_platform/README.md#L3-L19) | Typed provider boundaries distinguish data sources from analysis. | [research/entities.json](../research/entities.json), [research/protocol.json](../research/protocol.json) |
| [Thoughtworks Build Your Own Radar](https://github.com/thoughtworks/build-your-own-radar/blob/3379de7db36ce86af7b2607429be0b5f888c8120/README.md#L19-L40) | Structured entries carry an explicit assessment and rationale. | [research/assessments.json](../research/assessments.json), [research/STATUS.md](../research/STATUS.md) |
| [MLCommons MLPerf Inference](https://github.com/mlcommons/inference/blob/3fbc329939999c13d0a7b5e67fb2092287e06047/README.md#L168-L173) | Reproduction identifies an exact version and workload. | [research/protocol.json](../research/protocol.json), [reproduce.py](../reproduce.py), [research/snapshot.json](../research/snapshot.json) |

## What was deliberately not adopted

- No financial data API, credential requirement or investment recommendation.
- No imported radar rating or unsupported technology-readiness score.
- No external benchmark result, certification or performance badge.
- No upstream source code, branding or assets were copied. License context and immutable source locators remain in [benchmarks.json](benchmarks.json).

## Transfer into this research

Company records retain source attribution and keep commercial metrics unknown without independent evidence. Technology records carry a bounded evidence stage, an action and a falsifiable next gate. The experiment keeps configuration and result files together; a generated snapshot and one-command verification detect stale documentation.

## Implementation inspection

[OpenBB / OpenBQ implementation](https://github.com/openbq-org/OpenBB/blob/7df7d0c5592bf25be88e87e130a05c71e243d2d8/openbb_platform/core/openbb_core/provider/abstract/fetcher.py#L35-L56), [Thoughtworks Build Your Own Radar implementation](https://github.com/thoughtworks/build-your-own-radar/blob/3379de7db36ce86af7b2607429be0b5f888c8120/src/util/factory.js#L40-L53), [MLCommons MLPerf Inference implementation](https://github.com/mlcommons/inference/blob/3fbc329939999c13d0a7b5e67fb2092287e06047/loadgen/test_settings.h#L109-L120). These pinned files expose adapter, input-validation, scenario-setting or version-matrix boundaries. They informed original local checks; no upstream code was copied or executed.
