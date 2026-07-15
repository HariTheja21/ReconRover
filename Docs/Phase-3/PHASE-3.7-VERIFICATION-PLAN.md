# Phase 3.7: Path Planning Engine - Verification Plan

## Executive Summary
This document delineates the verification parameters for the Phase 3.7 Path Planning Engine. The primary objective is to prove that the engine calculates mathematically optimal collision-free routes across the `OccupancyGrid`, respects cache invalidation when obstacles appear, and operates within safe memory and CPU thresholds on ARM architecture.

## Verification Objectives
- Validate the $A^*$ (A-Star) graph search implementation for path optimality (shortest possible Euclidean distance around obstacles).
- Ensure the `PathValidator` accurately correlates absolute path coordinates back to grid coordinates to detect dynamic collisions.
- Verify thread safety of the EventBus ingestion while `heapq` is actively calculating routes.

## Verification Scope
Scope encompasses all `core/path_planning/` components. Interactions with mechanical steering, PID loops, or direct sensor hardware are explicitly out of scope.

## Audit Strategy
1. **Static Analysis:** Examine `AStarPlanner` heuristics and queue handling. Ensure Python's `heapq` is utilized safely across thread boundaries.
2. **Dynamic Analysis:** Simulate grid barriers and execute generation ticks. Verify the generated node lists route around the barriers rather than penetrating them.

## Architecture Audit
- Verify that `PlannerEngine` successfully wraps the $A^*$ implementation behind the `BasePathPlanner` interface, proving structural polymorphism for future D* or RRT upgrades.

## Runtime Audit
- Assert that the 2Hz asynchronous evaluation cycle handles the "dirty flag" logic accurately, preventing runaway compute cycles on identical ticks.

## Memory Audit
- Profile the open-set queue size inside $A^*$ to ensure memory growth bounds remain strictly tied to exploration space ($O(E)$).

## CPU Audit
- Assert that cache hits evaluate in $O(1)$ time, entirely skipping the $A^*$ queue.
- Assert that cache misses compute rapidly enough to not block the primary Python asyncio loop.

## Thread Safety Audit
- Validate read/write locks inside the `PathCache` and `PlannerState` modules.

## Async Safety Audit
- Confirm that the `PlannerManager` delegates the heavy $A^*$ compute cleanly without locking out `CorrectedPoseUpdated` ingestion.

## EventBus Audit
- Verify emission schema for `PathGenerated`, `PathInvalidated`, and `PlannerHealthUpdated`.

## Internal Test Matrix
1. **Test 1 - Optimal Straight Line:** Provide an empty occupancy grid. Request target at (50, 0). Expect straight line nodes.
2. **Test 2 - Obstacle Avoidance:** Inject an occupied block across the direct path. Expect the algorithm to deflect around the block via an alternate axis.

## PASS / FAIL Criteria
- **PASS:** Generates collision-free paths. `PathValidator` rejects stale cached paths when new obstacles appear on the line.
- **FAIL:** `PathValidator` allows collision paths. Unbounded memory growth in `heapq`.

## Risks
- Extreme grid resolution (e.g. 1mm cells) would exponentially multiply the node graph, locking the CPU.
- **Mitigation:** The system uses 10cm grid block scaling.

## Expected Deliverables
- `PHASE-3.7-VERIFICATION-PLAN.md`
- `PHASE-3.7-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
