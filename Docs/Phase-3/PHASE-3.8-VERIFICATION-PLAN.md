# Phase 3.8: Dynamic Obstacle Avoidance - Verification Plan

## Executive Summary
This document outlines the verification protocols for the Phase 3.8 Dynamic Obstacle Avoidance Engine. The primary objective is to prove that the engine successfully evaluates collision threats against a tiered Safety Bubble at 20Hz, overriding global trajectories safely without mutating the global state.

## Verification Objectives
- Validate the $20$Hz EventBus evaluation cycle inside `AvoidanceManager`.
- Ensure the `CollisionChecker` mathematically correlates incoming dynamic radar/sonar telemetry with the robot's current pose.
- Verify that the two-tier `SafetyBubble` correctly triggers distinct outcomes (trajectory evasion vs. emergency stop).
- Confirm the architectural integrity of the `BaseLocalPlanner` interface for future DWA substitution.

## Verification Scope
Scope encompasses all `core/obstacle_avoidance/` modules. Actuation of physical DC motors or servo steering systems is out of scope. 

## Audit Strategy
1. **Static Analysis:** Examine `SafetyBubble` logic and state machine transitions in `AvoidanceEngine`.
2. **Dynamic Analysis:** Simulate dynamic obstacles via the EventBus at varying distances and assert that the correct events (`SafeTrajectoryGenerated` vs `EmergencyStopRequired`) are fired.

## Architecture Audit
- Verify the structural separation between the global `PathPlanner` (Phase 3.7) and the `AvoidanceEngine` (Phase 3.8). 

## Runtime Audit
- Assert that the high-frequency evaluation loop operates asynchronously without inducing jitter on the EventBus.

## Memory Audit
- Verify that the Engine caches only the absolute newest sensor frame, preventing memory leaks during sustained runtime.

## CPU Audit
- Profile the trigonometric collision calculation to ensure sub-millisecond execution.

## Thread Safety Audit
- Validate read/write locks inside `AvoidanceManager` state dictionaries (`latest_pose`, `latest_obstacle`).

## Async Safety Audit
- Confirm that high-frequency sensory updates (e.g. 50Hz LiDAR) do not overload the 20Hz `_avoidance_loop`.

## EventBus Audit
- Verify emission schema for `SafeTrajectoryGenerated`, `CollisionPredicted`, and `EmergencyStopRequired`.

## Internal Test Matrix
1. **Test 1 - Safe Distance:** Obstacle far outside the 40cm Warning Zone. Expect normal operation.
2. **Test 2 - Warning Zone:** Obstacle at 30cm. Expect `CollisionPredicted` and `SafeTrajectoryGenerated`.
3. **Test 3 - Critical Zone:** Obstacle at 15cm. Expect `EmergencyStopRequired`.

## PASS / FAIL Criteria
- **PASS:** Triggers evasive trajectories at the warning perimeter. Triggers E-Stop at the critical perimeter.
- **FAIL:** Fails to trigger an E-stop. Misses warning zones. Memory buffer grows indefinitely.

## Risks
- A bug in the trigonometry inside `CollisionChecker` could project the obstacle backward instead of forward.
- **Mitigation:** The unit test logic verifies absolute distance bounds relative to the front quadrant.

## Expected Deliverables
- `PHASE-3.8-VERIFICATION-PLAN.md`
- `PHASE-3.8-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
