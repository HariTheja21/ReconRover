# Phase 8.4: RAG & Semantic Retrieval Engine - Verification Plan

## Executive Summary
This document outlines the verification strategy for Phase 8.4. The objective is to validate that the Retrieval-Augmented Generation (RAG) subsystem accurately chunks, embeds, indexes, and retrieves semantic information without blocking the primary asyncio event loop.

## Verification Objectives
- Validate `ChunkManager` correctly splits raw text with appropriate overlaps to preserve semantic continuity.
- Confirm `DocumentIndexer` synchronously writes embeddings to the abstract `VectorDatabase` and raw text to the `DocumentStore`.
- Verify `RetrievalEngine` accurately executes the semantic pipeline: query optimization, vector search, and reranking.
- Prove `ContextBuilder` formats retrieved JSON chunks into a strict string suitable for LLM injection.
- Ensure `RAGScheduler` processes all indexing and retrieval tasks asynchronously.
- Validate `RAGBridge` correctly routes telemetry (e.g., `RetrievalCompleted`) to the EventBus.

## Verification Scope
The scope encompasses all 26 RAG modules located in `MAIN CODE/RASPBERRY_PI/core/ai/runtime/rag/` and the integration script `scratch/test_rag_runtime.py`.

## Audit Strategy
1. **Ingestion Audit:** Pass a mock document into the `DocumentLoader`. Verify the `ChunkManager` splits it and the `DocumentIndexer` updates both the `DocumentStore` and the mock `ChromaDBProvider`.
2. **Retrieval Audit:** Execute a mock query via `RetrievalEngine.retrieve()`. Verify the `QueryOptimizer`, `SemanticSearch`, and `Reranker` functions are called in sequence.
3. **Specialized Search Audit:** Verify `KnowledgeRetriever` and `MemoryRetriever` apply the correct prepended context strings to the base query.
4. **Context Building Audit:** Pass the retrieved results to the `ContextBuilder` and verify the output string aggregates all text blocks seamlessly.
5. **Event Routing Audit:** Monitor the MockEventBus for the exact presence of `RetrievalCompleted` and `ContextBuilt` JSON payloads.

## Runtime Audit
- Ensure that `RAGScheduler` utilizes an `asyncio.Queue` so that dense vector calculations (which can spike CPU usage) do not starve the robot's main control loops.

## Memory Audit
- Verify the mock vector databases (`ChromaDBProvider`, `FAISSProvider`) operate strictly in-memory or bounded SQLite modes to prevent unbounded RAM bloat.

## Internal Test Matrix
1. **Valid Initialization:** Run `test_rag_runtime.py`. (Expect Success).
2. **Chunking & Indexing:** Load mock doc. (Expect `DocumentStore` size > 0).
3. **Retrieval:** Query the engine. (Expect mock results with scores).
4. **Memory Retrieval:** Query the memory API. (Expect targeted episodic results).
5. **Context Construction:** Pass results to builder. (Expect formatted string).
6. **Telemetry:** Check stdout. (Expect EventBus logs).

## PASS / FAIL Criteria
- **PASS:** The RAG Runtime abstracts the database and embedding layers perfectly. Retrieval is fast, non-blocking, and cleanly formatted for LLM consumption.
- **FAIL:** The system blocks the main thread during embedding generation. Context building drops data. The EventBus receives malformed telemetry.

## Expected Deliverables
- `PHASE-8.4-VERIFICATION-PLAN.md`
- `PHASE-8.4-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
