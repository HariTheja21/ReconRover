# Phase 3.6: Navigation Core - Implementation Plan

## Executive Summary
Phase 3.6 lays the architectural foundation for autonomous movement by establishing the Navigation Core. This module acts as the state machine that decides *what* the robot is trying to do (e.g., reaching a waypoint) based on where the robot currently is (SLAM Pose). It strictly avoids path planning (A*) and hardware manipulation, serving solely as the cognitive executive for spatial goals.

## Objectives
- Implement a rigid state machine (`IDLE`, `NAVIGATING`, `REACHED`, `FAILED`).
- Provide discrete `GoalManager` and `WaypointManager` hierarchies.
- Maintain a thread-safe `NavigationContext` containing the latest SLAM coordinates and Mapping constraints.
- Publish state transitions dynamically via `NavigationStateUpdated`.

## Architecture
- `navigation_manager.py`: Core EventBus daemon running at 10Hz.
- `navigation_engine.py`: Orchestrates state transitions based on distance heuristics.
- `navigation_state.py`: Thread-safe enum wrapping the active state.
- `goal_manager.py`: Stores the ultimate target coordinate ($X, Y$).
- `waypoint_manager.py`: Stores the sub-targets needed to reach the goal.
- `navigation_context.py`: Thread-safe cache of SLAM maps and SLAM poses.
- `navigation_validator.py`: A stub for future map-bounding collision checks.

## EventBus Integration
**Consumes:** `CorrectedPoseUpdated`, `SLAMMapUpdated`, `GoalUpdated`
**Publishes:** `NavigationStateUpdated`, `GoalReached`, `WaypointReached`, `NavigationHealthUpdated`

## Risks
- **Waypoint Overshoot:** If the robot moves too quickly, the 10Hz tick might miss the exact moment the robot enters the 10cm "reached" radius, causing the robot to orbit the waypoint indefinitely.
- **Mitigation:** The 10cm radius is sufficiently large for a 10Hz tick cycle at the robot's expected physical velocities (e.g., < 0.5m/s).

## Migration
Zero structural migrations. Ready to serve as the foundation for the Phase 3.7 Path Planner.
