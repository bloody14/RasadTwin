# Agent Bootstrap Acknowledgement

## Official Problem Statement (PS)
The official Problem Statement is SIH26251, Indian Army — Predictive Logistics & Forward Supply Chain, comprising four main pillars: AI/ML-based demand forecasting, GIS-enabled logistics planning, IoT-based inventory tracking, and an integrated predictive logistics management system.

## Project Goal
The primary objective is to build a credible, reproducible, CPU-only, Windows-compatible prototype and experimental codebase that addresses the official problem statement through predictive logistics decision support for synthetic scenarios.

## Security Boundary
The default security posture is an offline-first, air-gapped environment execution. Network access and external dependencies are OFF by default. The system will use only synthetic or explicitly approved public datasets; no real, sensitive, classified, or operational military data will be processed. The system operates entirely under human-in-the-loop review and must never perform autonomous dispatch.

## Allowed Autonomous Decisions
I am authorized to autonomously decide low-risk implementation details (Class A), including variable and function naming, internal module organization within the approved scope, formatting, local refactors that preserve behavior, test structure, and extracting deterministic helper utilities.

## Decisions Requiring Human Approval
Human approval is required before changing the official problem interpretation, research hypotheses, metrics, baselines, test-set policy, data classification, security/data restrictions, dependencies, or protected formula/algorithm definitions. I must also seek approval before adding external network services, handling non-public/sensitive data, or making any changes that impact project scope, public APIs, or autonomous behavior.

## Current Phase/State
The current phase and active task are TBD, awaiting the phase prompt from the human Technical Lead.

## Protected Files
I consider the following files to be governance-controlled and protected from unauthorized modification:
- `docs/PREREG.md`
- `docs/ASSUMPTIONS.md`
- `docs/SECURITY_POLICY.md`
- `docs/DECISION_POLICY.md`
- `docs/CHANGE_CONTROL.md`
- `docs/STATE.md`
- `docs/CHANGELOG.md`
- `config/experiments/*.yaml`

## Statement on Research Integrity
I will follow strict evidence discipline and will never invent results. I will not falsify experiment outputs, and every reported number will trace back to a logged run with exact reproducibility metadata. When uncertain, I will report the question and wait for human instruction rather than guessing.
