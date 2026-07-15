# Phase 3.8: Dynamic Obstacle Avoidance - Implementation Plan

## Executive Summary
Phase 3.8 implements the Dynamic Obstacle Avoidance Engine. Unlike the Path Planning Engine (which calculates static, global routes), this module acts as a high-speed local reactive system. It continuously monitors a configurable "Safety Bubble" around the robot, overriding global trajectories with evasive maneuvers or emergency stops if unexpected objects (e.g. humans, moving pets) violate the perimeter.

## Objectives
- Deploy an independent `AvoidanceManager` running at a high frequency (20Hz).
- Implement a `SafetyBubble` with two tiers: Warning Zone (triggering evasion) and Critical Zone (triggering E-Stop).
- Construct a `CollisionChecker` to project the robot's current vector against dynamic sensor data.
- Stub a `TrajectoryGenerator` ready to accept advanced algorithms like DWA (Dynamic Window Approach) or APF (Artificial Potential Fields).

## Architecture
- `avoidance_manager.py`: Core 20Hz safety daemon.
- `avoidance_engine.py`: Evaluates immediate threats against current trajectories.
- `safety_bubble.py`: Manages radial proximity rules.
- `collision_checker.py`: Intersects predicted motion against incoming `FusedObstacle` data.
- `trajectory_generator.py`: Generates short-term spatial splines to safely route around immediate threats.
- `local_planner.py`: Interface for future modular algorithm injection.

## EventBus Integration
**Consumes:** `PathGenerated`, `CorrectedPoseUpdated`, `FusedObstacle`
**Publishes:** `SafeTrajectoryGenerated`, `CollisionPredicted`, `EmergencyStopRequired`, `AvoidanceHealthUpdated`

## Risks
- **False Positives:** If sensor noise triggers a phantom obstacle inside the Critical Zone, the robot will lock into a permanent E-Stop loop.
- **Mitigation:** The Sensor Fusion engine (Phase 3.2) actively filters low-confidence sensor noise, ensuring only high-confidence obstacles reach the Avoidance Engine.

## Migration
Zero structural migrations. Ready to serve as the final spatial intelligence layer before Phase 4 (Locomotion & Hardware Execution).
