# RasadTwin Agent Decision Policy

## Goal
Prevent long-running agent sessions from silently changing project direction.

## Decision classes

### Class A — Autonomous
Agent may decide without asking:
- formatting;
- variable names;
- local refactors with identical behavior;
- additional unit tests;
- internal helper extraction;
- bug fixes that directly satisfy an already-approved requirement.

### Class B — Report and continue
Agent may implement, but must document:
- a minor implementation choice that has no impact on research metrics, security, API contract, or scope;
- equivalent library API changes that preserve behavior.

### Class C — Stop for human decision
Agent must stop coding and report before proceeding if the decision affects:
- research hypothesis or primary metric;
- baseline definition;
- train/calibration/test split;
- statistical test or correction;
- synthetic-world assumptions;
- public vs restricted data boundary;
- network connectivity;
- security controls;
- protected file content;
- public API contract;
- major architecture choice;
- dependency set;
- experimental result schema;
- project scope or milestone;
- autonomous behavior.

## Anti-drift rule

When the agent discovers a “better” idea, it must not silently implement it. It must write:
1. Current approved behavior
2. Proposed alternative
3. Why it may be better
4. Risk / compatibility impact
5. Smallest experiment or validation needed
6. Human decision required

## Conflict rule

Never resolve a governance conflict by guessing. Preserve the existing behavior until the human decides.

## Completion rule

“Done” means the requested acceptance criteria passed. It does not mean the agent is free to expand scope.
