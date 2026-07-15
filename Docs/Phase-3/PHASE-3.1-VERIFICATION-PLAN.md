# Phase 3.1: World Model Engine - Verification Plan

## Executive Summary
This verification plan ensures that the Phase 3.1 World Model Engine functions correctly as an isolated, scalable, and memory-safe spatial database. It dictates the testing strategy for the 12 core modules that manage deterministic state, semantic entities, and sensor confidence tracking.

## Verification Objectives
- Validate that the composite memory model (`WorldDatabase`) accurately and safely structures incoming semantic abstractions.
- Confirm thread-safety constraints against concurrent EventBus injections.
- Verify robust lifecycle hooks, specifically tracking Time-To-Live (TTL) garbage collection and linear confidence decay algorithms.

## Verification Scope
The scope encompasses all 12 modules implemented in `core/world/*`, including Entity lifecycle logic, Confidence calculations, Occupancy structures, and the cyclic `WorldManager` publication loops. SLAM calculations and Vision processing logic are entirely out of scope.

## Audit Strategy
1. Perform static analysis on the synchronization primitives (`threading.RLock`) utilized inside `EntityManager`, `ObstacleManager`, `LandmarkManager`, and `OccupancyManager`.
2. Run internal integration tests via `test_world.py` to confirm accurate EventBus serialization and mathematical bounds.

## Architecture Audit
- Verify encapsulation boundaries: Does `WorldManager` properly hide `WorldDatabase` from the broader system logic?
- Ensure semantic inputs decouple perfectly from hardware schemas.

## Runtime Audit
- Assert that the 10Hz publication task `_publish_loop` functions deterministically via `asyncio.sleep` without blocking concurrent EventBus callbacks.

## Memory Audit
- Verify TTL sweep mechanisms execute in bounds and effectively cap infinite memory expansion for long uptimes.
- Verify garbage collection for nested dynamic data types inside `EntityManager`.

## CPU Audit
- Analyze dictionary time-complexity on inserts and deletes. Verify $O(1)$ operations strictly enforced.

## Thread Safety Audit
- Validate read/write race condition protections on high-velocity state variables like `BatteryUpdated`.

## Async Safety Audit
- Ensure task isolation within the `WorldManager`.

## EventBus Audit
- Verify the publishing schemas of `WorldUpdated`, `ObstacleMapUpdated`, `LandmarkUpdated`, and `RobotStateUpdated`.

## Internal Test Matrix
1. **Robot State Injection:** Verify structural integrity of `world_state.py` updates.
2. **Obstacle Registration:** Test concurrent threshold violations.
3. **Occupancy Mutation:** Map mock targets and ensure aggregation totals update linearly.

## PASS / FAIL Criteria
- **PASS:** Zero memory leaks during TTL sweeps. Perfect correlation between injected test events and the resulting 10Hz summary snapshots.
- **FAIL:** Python `AttributeError` parsing event properties, race-condition exceptions, blocking loops, or exponential memory growth.

## Risks
- Rapidly vacillating Confidence levels from poor sensors causing event spam. (Mitigated via linear decay in `ConfidenceManager`).

## Expected Deliverables
- `PHASE-3.1-VERIFICATION-PLAN.md`
- `PHASE-3.1-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
