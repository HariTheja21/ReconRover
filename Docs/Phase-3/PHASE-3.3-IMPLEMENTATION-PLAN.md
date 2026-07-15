# Phase 3.3: Localization Engine - Implementation Plan

## Executive Summary
Recon Rover V2's Phase 3.3 establishes the Localization Engine, granting the robot awareness of its own position in space. By consuming fused telemetry (IMU, distance approximations), the engine calculates and maintains a historical sliding window of the robot's $X$, $Y$, and $\Theta$ pose.

## Objectives
- Isolate Localization mathematics from Mapping (SLAM) entirely.
- Implement robust `Odometry`, `OrientationTracker`, and `VelocityEstimator` modules.
- Aggregate positional components via the `PoseEstimator`.
- Expose the unified `RobotPoseUpdated` event to the EventBus at a stable 20Hz.

## Architecture
- `localization_manager.py`: Connects logic to the EventBus.
- `localization_engine.py`: Orchestrates internal modules.
- `pose_estimator.py`: Fuses dead-reckoning and orientation.
- `odometry.py`: Integrates velocity vectors mathematically over time.
- `orientation_tracker.py`: Translates raw IMU yaw degrees into standardized radians ($\Theta$).
- `velocity_estimator.py`: Heuristically derives linear velocity from time-deltas of fused obstacle distance (acting as a placeholder for wheel encoders).
- `pose_history.py`: A `collections.deque` maintaining the last 1000 known coordinates.

## EventBus Integration
**Consumes:** `IMUUpdated`, `FusedDistance`
**Publishes:** `RobotPoseUpdated`, `VelocityUpdated`, `LocalizationUpdated`, `LocalizationHealthUpdated`

## Risks
- **Dead-Reckoning Drift:** Pure mathematical integration of velocity without external anchor correction (SLAM) will drift over time.
- **Mitigation:** The `PoseEstimator` decays its own confidence value continuously to flag down-stream modules about drifting precision.

## Migration
Zero structural migrations. Plugs directly into the runtime orchestrator as a standalone daemon.
