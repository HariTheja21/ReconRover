# Phase 7.5: Semantic Mapping Engine - Verification Plan

## Executive Summary
This document defines the verification strategy for Phase 7.5. The objective is to validate that the Semantic Mapping Engine accurately converts short-term spatial object detections into persistent, long-term spatial memory without database locks, infinite graph growth, or event loop starvation.

## Verification Objectives
- Validate `SemanticRuntime` properly manages the lifecycle of the SQLite database connection.
- Confirm `PersistentStorage` and `SemanticDatabase` correctly write and read objects to/from the local disk.
- Verify `EntityLinker` deduplicates objects, preventing identical entities from spawning infinitely in the database.
- Prove `RoomClassifier` correctly applies semantic labels (e.g., "bedroom") to geographic zones based on the objects within them.
- Validate `KnowledgeGraph` correctly tracks relationships between objects and landmarks.
- Confirm `SemanticBridge` properly serializes semantic data and routes it to the EventBus.

## Verification Scope
The scope encompasses all 19 semantic modules situated in `MAIN CODE/RASPBERRY_PI/core/ai/semantic/` and the scratch test `scratch/test_semantic_runtime.py`.

## Audit Strategy
1. **Persistent Storage Audit:** Insert 10 mock objects into `SemanticDatabase`. Close the connection. Re-initialize the runtime and query for the objects. Verify the objects persist across power cycles.
2. **Entity Deduplication Audit:** Inject the exact same mock object dictionary into the `SemanticEngine` twice. Verify that `EntityLinker` merges the entries and that the database row count only increases by 1.
3. **Semantic Classification Audit:** Inject an object classed as "sofa" into the engine. Verify the `RoomClassifier` returns "living_room" with a high confidence score.
4. **Queue & Thread Safety Audit:** Rapidly inject 50 scene updates into the `SemanticScheduler`. Verify the asynchronous queue drops overflowing frames safely and that SQLite `check_same_thread=False` does not yield locking exceptions during concurrent ingestion.

## Runtime Audit
- Ensure that the SQLite query execution time remains <50ms even when the `objects` table exceeds 10,000 rows.

## Memory Audit
- Verify the `KnowledgeGraph` and `ObjectMemory` in-memory caches do not consume excessive RAM by ensuring `MemoryOptimizer` has bounded limits on graph nodes.

## Internal Test Matrix
1. **Valid Initialization:** Run `test_semantic_runtime.py`. (Expect Success).
2. **Entity Linking:** Pass identical object twice. (Expect 1 row).
3. **Room Classification:** Pass "bed". (Expect "bedroom").
4. **Graph Statistics:** Add 5 objects. (Expect 5 graph nodes).

## PASS / FAIL Criteria
- **PASS:** The engine accurately persists objects, correctly labels rooms, deduplicates entities over time, and publishes semantic JSON payloads without blocking the `asyncio` event loop.
- **FAIL:** SQLite locks due to cross-thread writes. The database grows infinitely with duplicate objects. The knowledge graph consumes >100MB of RAM.

## Expected Deliverables
- `PHASE-7.5-VERIFICATION-PLAN.md`
- `PHASE-7.5-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
