# RASADTWIN AGENT GOVERNANCE

## 1. PROJECT PURPOSE
RasadTwin is a defense-oriented Predictive Logistics Digital Twin demonstrator. It integrates forecasting (E1), multi-modal routing, and Human-In-The-Loop (HITL) auditing to simulate network resilience against disruptions.

## 2. AUTHORITATIVE RULES DIRECTORY
All future agents must read the relevant `.agents/rules/*.md` files before modifying any domain.

## 3. ARCHITECTURE AUTHORITY ORDER
1. Explicit user instruction
2. AGENTS.md
3. .agents/rules/
4. Approved ADRs
5. Target architecture
6. Current architecture
7. Reports/evidence
8. README
*(Do not treat old chat messages as authoritative over repository governance).*

## 4. SECURITY BOUNDARIES & SYNTHETIC DATA POLICY
- **NEVER** use real operational military positions or classified coordinates.
- **NEVER** expose targeting, weapons, or live surveillance data.
- **ALLOWED**: Public weather, public terrain/roads (OSM/SRTM), and 100% synthetic fictional logistics data.

## 5. E1 PROTECTION
E1 is a locked, validated research artifact. Do not rerun, rewrite, alter seeds, or tune on held-out test data.

## 6. CHANGE CONTROL & TESTING EXPECTATIONS
- Tests must verify: ACTION → API → STATE CHANGE → VISIBLE RESULT.
- Architectural changes require an ADR. 
- Small, logical Git commits only. No force pushes or committing generated junk.
