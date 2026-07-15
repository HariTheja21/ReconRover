# Phase 4.1: Differential Drive Kinematics Engine - Verification Plan

## Executive Summary
This document delineates the verification protocols for the Phase 4.1 Differential Drive Kinematics Engine. The primary objective is to prove that the module correctly and safely translates normalized velocity vectors from the Motion Controller into discrete, mechanically viable left and right wheel speeds without distorting intended navigation arcs.

## Verification Objectives
- Validate the $20$Hz EventBus evaluation cycle inside `KinematicsManager`.
- Ensure `DifferentialDrive` correctly scales out-of-bound rotational requests using proportional saturation mathematics.
- Verify that `KinematicsValidator` traps structural payload anomalies.
- Confirm that `EmergencyStopRequired` cascades instantly to the kinematic level, zeroing wheel speeds regardless of incoming velocity targets.

## Verification Scope
Scope encompasses all `core/kinematics/` modules. Direct hardware PWM generation, ESP32 serial communication, and closed-loop motor PID control are explicitly deferred to Phase 4.2.

## Audit Strategy
1. **Static Analysis:** Examine the polymorphic boundaries established by `WheelModel`. Verify read/write synchronization within `KinematicsState`.
2. **Dynamic Analysis:** Simulate combined linear/angular vectors (arcs) through the EventBus and mathematically assert the resulting left/right differential speeds.

## Architecture Audit
- Verify the structural separation between the `KinematicsManager` (Event orchestration) and the `KinematicsEngine` (math encapsulation).

## Runtime Audit
- Assert that the engine sustains its 20Hz pipeline asynchronously without blocking EventBus ingestion.

## Memory Audit
- Verify $O(1)$ memory allocation by confirming all state tracking variables are pre-allocated floating-point scalars.

## CPU Audit
- Profile the `DifferentialDrive.compute()` matrix logic to ensure negligible scalar overhead.

## Thread Safety Audit
- Validate `threading.RLock()` usage within the engine state to prevent torn reads during parallel EventBus dispatches.

## Async Safety Audit
- Confirm that `asyncio.sleep(0.05)` correctly yields thread execution in the `KinematicsManager` daemon loop.

## EventBus Audit
- Verify emission schema for `WheelVelocityRequest`, ensuring output bounds remain strictly within $[-1.0, 1.0]$.

## Internal Test Matrix
1. **Test 1 - Straight-line:** Emit $(v=0.8, \omega=0.0)$. Expect $(v_l=0.8, v_r=0.8)$.
2. **Test 2 - Pivot:** Emit $(v=0.0, \omega=0.5)$. Expect $(v_l=-0.5, v_r=0.5)$.
3. **Test 3 - Arc Saturation:** Emit $(v=0.8, \omega=0.4)$. Raw right equals $1.2$. Expect proportional scaling to $(v_l=0.33, v_r=1.0)$, preserving the arc.
4. **Test 4 - E-Stop Cascade:** Trigger E-Stop mid-motion. Expect zeroed wheel request regardless of incoming `MotionRequest` payloads.

## PASS / FAIL Criteria
- **PASS:** Computes correct differential speeds, scales velocity out-of-bounds proportionally, and respects systemic emergency halts.
- **FAIL:** Clips velocity asymmetrically (distorting the turn), blocks the event loop, or drops kinematic updates under load.

## Expected Deliverables
- `PHASE-4.1-VERIFICATION-PLAN.md`
- `PHASE-4.1-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
