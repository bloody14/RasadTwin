# ADR-005: Optional pgvector RAG Layer

## Context
Commanders may need to reference Standard Operating Procedures (SOPs), manuals, and doctrines alongside active disruptions.

## Decision
Implement an optional Knowledge/RAG layer using the `pgvector` extension in PostgreSQL to store and query document embeddings.

## Rationale
Keeps semantic retrieval inside the existing relational database ecosystem, reducing architectural complexity compared to standing up a standalone vector database.

## Consequences
- Extends the core database payload.
- Serves strictly as a retrieval tool, not as part of the core relational digital twin state.

## Status
PROPOSED
