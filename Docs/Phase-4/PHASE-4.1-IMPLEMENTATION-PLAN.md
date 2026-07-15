# Phase 4.1: Differential Drive Kinematics Engine - Implementation Plan

## Executive Summary
Phase 4.1 establishes the Differential Drive Kinematics Engine. This module accepts safe, bounded, normalized `MotionRequest` events from Phase 4.0 and performs the rigid mathematical translation required to convert abstract linear ($v$) and angular ($\omega$) velocities into specific left ($v_l$) and right ($v_r$) wheel speeds.

## Objectives
- Deploy a `KinematicsManager` operating at a 20Hz cadence to ingest normalized motion intents.
- Implement a strict `DifferentialDrive` mathematical model:
  - $v_l = v - \omega$
  - $v_r = v + \omega$
- Implement a `KinematicsValidator` to prevent malformed or out-of-bounds $[-1.0, 1.0]$ signals from inducing mathematical errors.
- Ensure velocity saturation preserves the intended turning arc.

## Architecture
- `kinematics_manager.py`: Core 20Hz orchestration daemon mapping EventBus to the Engine.
- `kinematics_engine.py`: Orchestrates validation and mathematical translation.
- `wheel_model.py`: Polymorphic base interface to support future swerve/Mecanum upgrades.
- `differential_drive.py`: Concrete implementation of the standard 2WD/4WD skid-steer algorithm.
- `kinematics_validator.py`: Structural data integrity checks.

## EventBus Integration
**Consumes:** `MotionRequest`, `MotionStopped`, `MotionPaused`, `EmergencyStopRequired`
**Publishes:** `WheelVelocityRequest`, `KinematicsUpdated`, `KinematicsHealthUpdated`

## Risks
- **Velocity Saturation Loss of Arc:** If $v_l$ or $v_r$ exceeds maximum bounds (e.g., $1.2$), merely capping it at $1.0$ would distort the requested turning radius.
- **Mitigation:** The `DifferentialDrive` module will implement proportional saturation. If $\max(|v_l|, |v_r|) > 1.0$, both velocities are divided by the maximum, scaling down absolute speed while perfectly preserving the $\omega$ ratio.

## Migration
The cognitive intelligence (Phase 3) and safety bounds (Phase 4.0) are completely insulated from these mathematical realities. The output (`WheelVelocityRequest`) is fully prepped for ingestion by the upcoming hardware PWM drivers.
