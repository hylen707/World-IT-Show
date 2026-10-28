# Evidence, authorship, and dates

This repository separates four kinds of work:

1. **Source observation** — what a cited original artifact actually says or shows, with a location.
2. **Retrospective analysis** — reasoning added while organizing the repository; it is not presented as contemporaneous student work.
3. **Proposed follow-up** — a protocol or experiment that has not been executed unless a dated result is linked.
4. **Student-verified statement** — a statement the student has reviewed and can explain, supported by evidence.

An exhibition visit, interview, experiment, participant count, working hours, leadership role, award, deployment, or measured impact must not be inferred from the exhibition name or a repository commit. Missing facts remain `null` or explicitly pending.

## Repository history

Commits record when documentation and tools were actually created. They do not establish when an activity occurred or how many weeks a student spent on it. Logical commit boundaries are for review and reproducibility; dates and authors are never rewritten to simulate an earlier research timeline.

## Contribution review

Repository materials do not establish that the student designed or performed the analyses. Before using any material in an application, the student must correct the wording, confirm personal contribution, attach original evidence, and explain each technical argument independently.

## Public evidence

Linking an original document establishes a reference, not proof that the document was read or that the student authored it. Do not publish personal information, identifiable participants, private student records, access tokens, or unrestricted copies of third-party materials. Use minimal paraphrases and precise references where full republication is unnecessary.

## Submission gate

`python tools/validate.py --submission` is a conservative repository readiness check. Passing it does not guarantee accuracy, admission, or compliance with every school's instructions. A pending result is a useful finding: it identifies the exact evidence needed before a claim can be used.
