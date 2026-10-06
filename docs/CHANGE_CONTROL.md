# CHANGE CONTROL POLICY

**WHEN AN ADR IS REQUIRED:**
- Introducing a new database engine or framework.
- Altering the security, offline, or data governance paradigms.
- Changing the primary architecture layer boundaries.

**WHEN AN API CHANGE IS REQUIRED:**
- API contracts must be documented in OpenAPI/Swagger before breaking endpoints.
- Breaking changes require versioning or explicit coordination with UI updates.

**WHEN A SCHEMA MIGRATION IS REQUIRED:**
- Any change to the PostgreSQL/SQLite relational structure must be captured in a migration script (e.g., Alembic). Do not manually alter tables in production.

**WHEN A DATASET PROVENANCE ENTRY IS REQUIRED:**
- The moment any new real public data (OSM, SRTM, Weather) or synthetic scenario dataset is ingested.

**WHEN EXPERIMENT PREREGISTRATION MUST REMAIN UNTOUCHED:**
- Always. E1 and other completed research artifacts are locked. Modifying them invalidates the research integrity.

**WHEN A UI-ONLY CHANGE IS ACCEPTABLE:**
- Visual layout adjustments, Tailwind class modifications, or client-side filtering changes that do not alter the underlying business logic or data payload structure.
