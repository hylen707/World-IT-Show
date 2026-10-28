# Claim audit and proposed engineering method

## Completed in this repository

The source text was read; its high-consequence claims were located; primary references were checked within the recorded scopes; and explicit analytical calculations were run. These are retrospective repository tasks. There is no physical measurement, product certification, company interview, or independently confirmed student experiment.

## Codebook

| Field | Rule |
| --- | --- |
| `source_observation` | Describes what a source states; does not endorse the statement |
| `retrospective_analysis` | Adds reasoning now, with premises and a rival explanation |
| `proposal` | Work not executed; cannot be counted as completed impact |
| `supported` | Evidence supports the carefully bounded claim text, not every underlying vendor claim |
| `contested` | A material alternative or attribution remains unresolved |
| `draft` | Evidence or reasoning incomplete |
| `withdrawn` | Retain history but do not reuse the claim |

Evidence quality is categorical: author-reported research result, manufacturer statement, original report assertion, or public standard scope. No numerical evidence score is manufactured from these labels. Missing data stay missing; zero is reserved for an observed count of zero.

## Proposed matched-task comparison — not executed

**Question:** Under a predeclared task, does a transparent planar-heater appliance require less wall-plug energy than a specified comparator?

Record exact product version, vessel geometry, load mass, initial and final temperatures, ambient conditions, lid/vent state, measurement boundary, instrument resolution/calibration, completion criterion, cooldown accounting, and run order. Predeclare repeats based on available equipment; distinguish a pilot from confirmatory runs. If repeated runs are not independent, do not treat them as independent samples.

For each valid run compute integrated energy `E = ∫P(t)dt` in Wh. Compare only runs reaching the same predefined endpoint. Record unsuccessful runs and exclusions with reasons. Report mean, range, and instrument uncertainty; do not present a small convenience sample as a universal product ranking. Choose an uncertainty method after defining the sampling design; repeated readings from the same run are not extra trials.

Keep heater power and energy distinct. For an actual cooking task, water-equivalent heat is an approximation and cannot replace texture, safety, evaporation, or doneness endpoints. Battery losses must be included if the comparison boundary is wall energy, and excluded only under an explicitly different boundary.

Use only commercially safe operation within manufacturer instructions and an appropriate supervised setting. Do not synthesize graphene, open mains-powered appliances, expose people to heated surfaces, or run burn experiments. If safe equipment access is unavailable, retain the literature audit as the completed scope.

## Proposed film-quality inquiry — not executed

Request a public quality-control example rather than infer perfection from CVD. Define sampling positions and area coverage, layer-count indicators, Raman setup, sheet-resistance distribution, transfer-induced defects, acceptance threshold, and lot-to-lot yield. A few favorable spectra cannot establish entire-film uniformity. Proprietary data may remain unavailable; that becomes an explicit limit.

## Reproducibility and disagreement

Two readers can independently code a subset of statements and compare category/location disagreements. Record the number reviewed and the reconciliation notes only if this actually happens. Do not invent inter-rater agreement statistics. A future reviewer should be able to reject one inference without losing the raw original or the rest of the argument.
