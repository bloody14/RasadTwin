# RasadTwin Project State

## Current phase
P0 — Repository Foundation, Engineering Guardrails & Reproducibility

## Last approved objective
Build RasadTwin as an uncertainty-aware predictive logistics digital twin for synthetic scenarios, covering demand forecasting, stock-out risk/inventory, multi-modal routing, disruption-aware re-optimization, explainability, and an offline-capable human-in-the-loop dashboard.

## Active task
Establishing repository skeleton, Python environment, tooling, test and reproducibility foundations without implementing specific experimental or ML logic.

## Protected decisions
- Official PS: SIH26251, Indian Army — Predictive Logistics & Forward Supply Chain.
- Prototype must be offline-first / air-gapped compatible.
- CPU-only Windows development.
- Synthetic scenarios only unless explicitly approved.
- Human-in-the-loop; no autonomous dispatch.
- Research integrity rules in `docs/PREREG.md` remain authoritative once locked.

## Current known risks
- Keep prototype scope demo-grade.
- Prevent research/prototype requirements from drifting apart.
- Verify any external-data adapter remains optional and offline-capable.

## Last phase verdict
P0 is currently in progress.

## Next action
Complete P0 tasks and report for review.

## Agent instruction
Read this file at the start of every phase and update it only within the phase scope.
