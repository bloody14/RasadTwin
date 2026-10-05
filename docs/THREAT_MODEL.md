# RasadTwin Lightweight Threat Model

## Scope

This model covers the student prototype and experimental repository for RasadTwin. It is not a classified-system threat model or a formal accreditation artifact.

## Assets

- Source code and configuration.
- Synthetic logistics datasets.
- Experimental raw results and figures.
- Reproducibility metadata and Git history.
- Local prototype state and cached map/data fixtures.
- Development credentials, if any are temporarily required.

## Threats and controls

| Threat | Example | Required control |
|---|---|---|
| Secret leakage | API key in Git/log | Environment variables, secret scan, redaction |
| Data leakage | sensitive file copied into fixture | synthetic-only rule, review, git diff |
| Exfiltration | background HTTP upload | network off by default, no telemetry |
| Supply-chain risk | unpinned dependency | pinned versions, review new dependencies |
| Agent drift | agent changes experiment definition | protected files + stop condition |
| Result manipulation | editing CSV to improve chart | immutable raw outputs, provenance |
| Unsafe API | arbitrary file/URL/shell endpoint | strict schemas, no eval, no arbitrary fetch |
| Availability | solver runs indefinitely | time limits, checkpoints, cancellation |
| Misinterpretation | prototype presented as autonomous command | explicit human-in-the-loop boundary |

## Security review questions

Before a security-sensitive phase is accepted, answer:
1. What data enters the component?
2. Can it leave the component?
3. What files can it read/write?
4. What external services can it call?
5. What authentication/authorization boundary exists?
6. What is logged?
7. What happens on failure?
8. What is the offline fallback?

Any unknown answer is an open risk, not an assumption of safety.
