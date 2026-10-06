# ADR-001: Synthetic Operational Data Policy

## Context
RasadTwin requires logistics data to demonstrate predictive capability and network resilience. However, defense logistics data is highly sensitive.

## Decision
All operational military logistics data (node positions, inventory, demand, fleet availability, and scenarios) must remain strictly synthetic. Public geographical and environmental data may be used as a backdrop.

## Rationale
Prevents accidental spillage or exposure of classified/sensitive material while maintaining a realistic demonstration of system capabilities.

## Consequences
- Requires fictional study regions or intentionally offset coordinates.
- Validates the system's logic without tying it to real-world operational vulnerabilities.

## Status
ACCEPTED
