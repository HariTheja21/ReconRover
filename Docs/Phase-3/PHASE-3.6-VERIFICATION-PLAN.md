# Phase 3.6: Navigation Core - Verification Plan

## Executive Summary
This document delineates the verification parameters for the Phase 3.6 Navigation Core. The primary objective is to prove that the state machine cleanly abstracts Goal and Waypoint tracking without entangling itself in path generation or low-level robotic motor control.

## Verification Objectives
- Validate discrete state transitions (`IDLE` $\rightarrow$ `NAVIGATING` $\rightarrow$ `REACHED`).
- Ensure the `WaypointManager` correctly advances sub-goals based on purely mathematical `math.hypot()` distance triggers against the SLAM pose.
- Verify thread safety of the `NavigationContext` when ingesting rapid SLAM updates.

## Verification Scope
Scope encompasses all `core/navigation/` components (`navigation_manager.py`, `navigation_engine.py`, `goal_manager.py`, `waypoint_manager.py`, etc.). Pure mechanical navigation, motor control, or path-finding (e.g. A*) are explicitly out of scope.

## Audit Strategy
1. **Static Analysis:** Examine `threading.RLock()` boundaries within the state machine mutations and context updates.
2. **Dynamic Analysis:** Simulate goal ingestion and force SLAM coordinate teleportation to verify the exact frame the `GoalReached` payload is published.

## Architecture Audit
- Verify that `NavigationEngine` operates purely as a cognitive state-evaluator, retaining zero knowledge of how to physically reach the goal.

## Runtime Audit
- Assert that the 10Hz calculation loop does not freeze while waiting for fresh SLAM data (i.e. handles stale poses gracefully).

## Memory Audit
- Verify that `WaypointManager` consumes strictly $O(W)$ memory (where $W$ is the number of waypoints).

## CPU Audit
- Assert that Pythagorean hypotenuse checks compute in minimal time, ensuring no CPU spikes during navigation.

## Thread Safety Audit
- Validate read/write race condition protections on high-velocity state variables like `CorrectedPoseUpdated`.

## Async Safety Audit
- Confirm lack of blocking mathematical loops in the main EventBus evaluation routine.

## EventBus Audit
- Verify emission schema for `NavigationStateUpdated`, `GoalReached`, `WaypointReached`, and `NavigationHealthUpdated`.

## Internal Test Matrix
1. **Test 1 - State Progression:** Emit `GoalUpdated`. Verify `NAVIGATING` state. Emit `CorrectedPoseUpdated` matching goal coordinate. Verify `REACHED` state and `GoalReached` event.

## PASS / FAIL Criteria
- **PASS:** State machine transitions accurately based on distance. Thread locks prevent state corruption.
- **FAIL:** Infinite loops around Waypoints (missing radius checks), state desynchronization, or blocking the EventBus.

## Risks
- Rapidly changing goals could theoretically cause race conditions if the state machine isn't fully locked during transition evaluations.

## Expected Deliverables
- `PHASE-3.6-VERIFICATION-PLAN.md`
- `PHASE-3.6-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
