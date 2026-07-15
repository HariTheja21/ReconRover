# Phase 3.5: SLAM Engine - Verification Plan

## Executive Summary
This document delineates the verification parameters for the Phase 3.5 SLAM Engine. The objective is to rigorously audit the decoupling of pure odometry from cumulative spatial drift, validate the mathematical integrity of the `ScanMatcher` (ICP stub), and ensure `LoopClosure` logic operates efficiently without introducing thread deadlocks.

## Verification Objectives
- Validate the separation of raw `RobotPoseUpdated` coordinates from the internal `PoseCorrector` offsets.
- Evaluate the time-complexity and memory scaling of the `LoopClosure` historical path graph.
- Verify thread safety between the 10Hz mathematical SLAM pipeline and random-interval EventBus ingestion.

## Verification Scope
Audit covers all `core/slam/` modules (`slam_engine.py`, `pose_corrector.py`, `loop_closure.py`, etc.). Pure mechanical navigation or path-finding is explicitly out of scope.

## Audit Strategy
1. **Static Analysis:** Examine `threading.RLock()` implementations inside `PoseCorrector` and `LoopClosure` during rapid coordinate injection.
2. **Dynamic Analysis:** Simulate a 50+ node continuous path that returns to origin to force a `LoopClosure` trigger event.

## Architecture Audit
- Verify that SLAM sits purely as an observational correction layer between Odometry (Localization) and World State (Mapping), adhering to the stateless/stateful separation rules.

## Runtime Audit
- Assert that the 10Hz alignment cycle yields appropriately via `asyncio.sleep(0.1)` to avoid starving the primary EventBus.

## Memory Audit
- Measure the growth characteristics of `visited_nodes` inside `LoopClosure`.

## CPU Audit
- Assert that naive Pythagorean distance calculations within the loop closure sweep compute in $O(N)$ time, safely under the 100ms cycle budget.

## Thread Safety Audit
- Validate read/write locks inside the `SLAMManager`'s cached state variables (`raw_pose`, `latest_obstacle`, `grid_snapshot`).

## Async Safety Audit
- Confirm lack of blocking mathematical loops in the main publish routine.

## EventBus Audit
- Verify emission schema for `CorrectedPoseUpdated`, `LoopClosureDetected`, `SLAMMapUpdated`, `SLAMStatisticsUpdated`, and `SLAMHealthUpdated`.

## Internal Test Matrix
1. **Test 1 - Basic Pass-through:** Inject raw pose. Verify output correctly reflects (raw + offset).
2. **Test 2 - Loop Closure:** Inject 51 sequential nodes. Inject a node matching node 0. Expect `LoopClosureDetected` event.

## PASS / FAIL Criteria
- **PASS:** Accurate correction offsets applied linearly. Loop closure correctly detected after minimum node threshold.
- **FAIL:** Dropped coordinate frames, infinite recursion during alignment, or memory overflow in the path graph.

## Risks
- Extreme sensor noise could cause the `ScanMatcher` to generate false-positive alignment scores, heavily shifting the `PoseCorrector` into an invalid spatial dimension.

## Expected Deliverables
- `PHASE-3.5-VERIFICATION-PLAN.md`
- `PHASE-3.5-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
