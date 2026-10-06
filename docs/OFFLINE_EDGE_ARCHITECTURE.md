# OFFLINE / EDGE ARCHITECTURE

## 1. CONNECTIVITY STATES

### ONLINE
- **Data Source**: Central PostgreSQL via REST/GraphQL API.
- **Local Compute**: Minimal. Client renders data directly from API responses.
- **Queue**: Empty.
- **Sync**: Real-time WebSocket or polling updates keeping the Digital Twin perfectly in sync with HQ.

### WEAK NETWORK (Degraded)
- **Data Source**: API prioritized, but falls back to SQLite cache on timeout.
- **Local Compute**: UI utilizes cached state; heavy simulations (What-If) are still routed to HQ API if possible.
- **Queue**: Decisions made by the Commander are sent immediately but mirrored in a local retry queue.
- **Sync**: Throttled polling. Large data assets (images, heavy geometries) are deferred.

### OFFLINE (Air-gapped)
- **Data Source**: Local SQLite database only.
- **Local Compute**: The Edge device runs a localized, lightweight version of the forecasting and routing engines.
- **Queue**: All `HITL` actions (Approvals, Overrides) and local inventory changes are appended to a robust local SQLite transaction queue.
- **Sync**: Suspended. 
- **Conflict Handling**: When network is restored, the Edge queue is flushed to HQ. Time-stamped CRDTs (Conflict-Free Replicated Data Types) or strict "Commander Override Wins" policies reconcile conflicting inventory or route states.

## 2. DEPLOYMENT REALITY
*Note: The current synthetic prototype demonstrates offline capability visually via the UI `offline` flag and local SQLite audit log. True bidirectional synchronization and conflict resolution are architectural targets, not yet implemented in production.*
