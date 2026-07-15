# Phase 4.0: Motion Controller - Implementation Plan

## Executive Summary
Phase 4.0 marks the beginning of the Physical Execution Layer. The Motion Controller acts as the crucial translation boundary between abstract spatial intentions (e.g., "dodge left", "navigate to waypoint") and normalized kinetic requests. It receives intent from the cognitive subsystems, filters it through rigorous safety constraints (velocity/acceleration caps, E-stops), and outputs normalized `MotionRequest` events. Crucially, it contains absolutely no hardware-specific logic, PID loops, or PWM generation.

## Objectives
- Deploy a `MotionManager` executing a 20Hz evaluation loop.
- Implement `MotionLimits` to bound instantaneous velocities and enforce acceleration stepping (preventing mechanical shear).
- Stub a `MotionProfile` module for future integration of non-linear jerk smoothing (S-curves).
- Create a `MotionContext` dictionary to latch systemic state variables (`estop`, `paused`, `mission_active`).

## Architecture
- `motion_manager.py`: Core 20Hz safety and translation daemon.
- `motion_engine.py`: Orchestrates the filtering pipeline.
- `motion_limits.py`: Enforces mathematical bounds on target velocities relative to current velocities.
- `motion_profile.py`: Prepares abstract inputs for mechanical realization.
- `motion_validator.py`: Asserts data integrity of incoming float vectors.

## EventBus Integration
**Consumes:** `SafeTrajectoryGenerated`, `MissionStarted`, `MissionPaused`, `MissionCancelled`, `EmergencyStopRequired`
**Publishes:** `MotionRequest`, `MotionStateUpdated`, `MotionStopped`, `MotionPaused`, `MotionResumed`, `MotionHealthUpdated`

## Risks
- **Control Loop Desync:** If the Motion Controller generates requests faster than the downstream PID loop can consume them, queues could overflow or induce latency.
- **Mitigation:** The 20Hz rate is explicitly chosen as an industry standard for smooth DC motor PID integration without saturating standard serial links.

## Migration
Phase 3 is entirely preserved. The system now publishes `MotionRequest` payloads on the EventBus, perfectly staging the codebase for Phase 4.1 (Kinematics & Hardware Abstraction).
