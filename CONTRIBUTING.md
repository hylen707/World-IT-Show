# Contributing research

Start from a specific question and identify the evidence that could change the answer. Update the core ledger before strengthening a claim. Keep company descriptions attributed, commercial metrics sourced, and proposed tests distinct from measurements.

## Change workflow

1. Preserve the supplied material and record an exact source location.
2. Update the relevant company case, technology decision and next evidence gate.
3. If a release matters, record its date, immutable version and untested/tested scope.
4. Regenerate analytical outputs through their scripts, rather than editing results.
5. Run the research snapshot refresh, inspect its diff, and update the README narrative when a conclusion changes.
6. Run the complete offline verification before publishing.

    python research.py --write
    python reproduce.py

The refresh updates generated counts and artifact hashes. It does not establish scientific truth or replace a review of changed assumptions. Record substantive technical work in commits. Method references are pinned in [research/benchmarks.json](research/benchmarks.json); do not copy upstream implementation or branding without an appropriate separate review.
