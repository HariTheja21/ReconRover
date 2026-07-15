# Phase 3.4: Mapping Engine - Verification Plan

## Executive Summary
This document outlines the verification criteria for Phase 3.4 (Mapping Engine). The objective is to ensure that the probabilistic sparse grid accurately resolves relative obstacles into absolute space, prevents memory leaks through dynamic garbage collection, and properly isolates from the localization loop.

## Verification Objectives
- Validate the $O(1)$ scaling properties of the sparse dictionary occupancy grid.
- Prove mathematical correctness of the trigonometric transformations inside `MapBuilder`.
- Ensure thread-safe ingestion of asynchronous `FusedObstacle` and `RobotPoseUpdated` events.
- Verify memory stability through the `MapOptimizer` pruning routines.

## Verification Scope
Scope encompasses all `core/mapping/` components. Interactions with actual sensor hardware, true pathfinding (A*), or AI modules are explicitly out of scope.

## Audit Strategy
1. **Static Analysis:** Examine `threading.RLock()` boundaries within the dictionary mutations.
2. **Dynamic Analysis:** Simulate grid projection from coordinate (0,0) with varying angular alignments to prove trigonometric reliability.

## Architecture Audit
- Verify that `MappingManager` successfully decouples the high-speed EventBus ingestion from the slower 5Hz optimization and publication loop.

## Runtime Audit
- Assert that asynchronous yields (`asyncio.sleep(0.2)`) prevent the mapping process from starving the CPU.

## Memory Audit
- Verify the pruning of strictly $0.5$ (unknown) probability cells, guaranteeing memory reflects only explored space, not theoretical maximum space.

## CPU Audit
- Evaluate the computational cost of extracting `occupied_cells` and `free_cells` snapshots from the sparse dictionary structure during the 5Hz tick.

## Thread Safety Audit
- Validate read/write locks inside `OccupancyGrid` during simultaneous EventBus projections and `MappingManager` snapshot extraction.

## Async Safety Audit
- Confirm lack of blocking I/O during the `MapStorage.save()` stub implementations, ensuring the event loop remains unhindered.

## EventBus Audit
- Verify emission schema for `MapUpdated`, `OccupancyGridUpdated`, `MapStatisticsUpdated`, and `MappingHealthUpdated`.

## Internal Test Matrix
1. **Test 1 - Raycasting Projection:** Inject Robot Pose (0,0, $\Theta=0$) and Obstacle at 50cm. Expected: Cell (5,0) occupied, Origin (0,0) free.

## PASS / FAIL Criteria
- **PASS:** Accurate translation of obstacles to absolute grid frames. Memory bounds remain intact. No deadlocks.
- **FAIL:** `KeyError` exceptions, overlapping free/occupied paradoxes, or unbounded dictionary growth.

## Risks
- Rapid rotation while moving could hypothetically smear the occupancy map if the timestamp deltas between pose updates and obstacle detections are too large.

## Expected Deliverables
- `PHASE-3.4-VERIFICATION-PLAN.md`
- `PHASE-3.4-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
