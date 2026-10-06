# ADR-008: Multi-Modal Routing

## Context
Logistics networks rely on multiple transport modes, not just roads. Each mode has distinct vulnerabilities.

## Decision
Implement distinct routing constraints for Road, Mule, Helicopter, and Drone assets.

## Rationale
A "Heavy Snow" disruption might close a Road but allow a Drone to pass, while "High Wind" grounds the Drone but leaves the Road unaffected. This proves the value of a predictive digital twin.

## Consequences
- Routing algorithms must weigh mode-specific parameters (speed, range, weather vulnerability).

## Status
ACCEPTED
