# Phase 7.4: Autonomous Exploration Engine - Verification Plan

## Executive Summary
This document defines the verification strategy for Phase 7.4. The objective is to validate that the Autonomous Exploration Engine correctly translates raw OccupancyGrid maps into prioritized, safe, and geometrically optimal exploration missions without starving the central event loop or consuming excessive memory.

## Verification Objectives
- Validate `ExplorationRuntime` initialization and state machine transitions.
- Confirm `FrontierDetector` and `FrontierCluster` accurately extract edges from unknown/known space within the map grid.
- Verify `FrontierRanker` and `GoalSelector` prioritize the safest and nearest exploration targets.
- Prove `CoverageTracker` accurately calculates the total explored area in square meters.
- Validate `DeadlockDetector` correctly flags prolonged physical stagnation.
- Confirm `RecoveryManager` safely overrides the exploration goal with an escape maneuver.
- Ensure `ExplorationBridge` effectively serializes mission coordinates and routes them to the EventBus.

## Verification Scope
The scope encompasses all 19 exploration modules situated in `MAIN CODE/RASPBERRY_PI/core/ai/exploration/` and the scratch test `scratch/test_exploration_runtime.py`.

## Audit Strategy
1. **Frontier Extraction Audit:** Inject a simulated 100x100 `numpy.ndarray` occupancy grid containing a distinct boundary between known (0) and unknown (-1) space. Verify `FrontierDetector` successfully flags the boundary array indices.
2. **Goal Ranking Audit:** Supply two clusters. Cluster A is 1m away with size 5. Cluster B is 10m away with size 5. Verify the `FrontierRanker` assigns a mathematically higher score to Cluster A.
3. **Deadlock Recovery Audit:** Repeatedly update the robot pose with identical `[x,y]` coordinates while in the `EXPLORING` state. Verify `DeadlockDetector` triggers and shifts the state to `RECOVERING`.
4. **Queue Saturation Audit:** Rapidly inject 20 large occupancy grids into the `ExplorationScheduler` (maxsize=10). Verify that the oldest grids are discarded cleanly via `asyncio.QueueFull` exception handling.

## Runtime Audit
- Ensure that processing heavy `numpy.ndarray` operations (e.g., frontier edge detection) does not exceed 100ms to prevent starving the Python `asyncio` event loop.

## Memory Audit
- Verify the `CoverageMap` does not leak memory. Ensure `ExplorationOptimizer` restricts the size of its `past_goals` list to avoid infinite array growth over prolonged missions.

## Internal Test Matrix
1. **Valid Initialization:** Run `test_exploration_runtime.py`. (Expect Success).
2. **Coverage Calculation:** Input a grid with 400 known cells at 0.05m resolution. (Expect exactly 1.0 m^2 coverage).
3. **Stagnation Trigger:** Hold pose constant for simulated 30 seconds. (Expect DeadlockEvent).
4. **Event Serialization:** Trigger `ExplorationMissionGenerated`. (Expect valid JSON).

## PASS / FAIL Criteria
- **PASS:** The engine transitions states correctly, calculates coverage accurately, extracts frontiers, ranks them by distance/size, handles deadlocks, and publishes valid JSON without blocking.
- **FAIL:** NumPy operations lock the GIL for >100ms. The `past_goals` array grows infinitely. Target selection math causes division-by-zero errors.

## Expected Deliverables
- `PHASE-7.4-VERIFICATION-PLAN.md`
- `PHASE-7.4-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
