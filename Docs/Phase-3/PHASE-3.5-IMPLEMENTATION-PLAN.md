# Phase 3.5: SLAM Engine - Implementation Plan

## Executive Summary
Phase 3.5 closes the loop on spatial cognition by deploying the SLAM Engine. This module addresses the fundamental flaw of dead-reckoning localization: drift. By continuously aligning the robot's perceived position against the global `OccupancyGrid` using scan matching and loop closure detection, it provides a stable, "corrected" spatial truth to the rest of the system.

## Objectives
- Ingest `RobotPoseUpdated` (drifting odometry).
- Ingest `OccupancyGridUpdated` and `FusedObstacle` (environmental structure).
- Apply a `ScanMatcher` (ICP-style) to calculate micro-drift offsets.
- Deploy a `LoopClosure` detector to resolve macro-drift (e.g., returning to the start after a long circle).
- Maintain an internal `PoseCorrector` mathematically isolating drift vectors.

## Architecture
- `slam_manager.py`: Connects the 10Hz alignment cycle to the EventBus.
- `slam_engine.py`: Central pipeline orchestrator.
- `scan_matcher.py`: Correlates new obstacle scans against the known grid to detect coordinate drift.
- `pose_corrector.py`: Stores continuous mathematical offsets (`dx`, `dy`, `dtheta`).
- `loop_closure.py`: Tracks historical visited nodes to identify return-trips.
- `landmark_associator.py`: Supports discrete semantic anchors.
- `map_alignment.py`: Applies warp adjustments to the map upon loop closure.

## EventBus Integration
**Consumes:** `RobotPoseUpdated`, `OccupancyGridUpdated`, `FusedObstacle`
**Publishes:** `CorrectedPoseUpdated`, `SLAMMapUpdated`, `LoopClosureDetected`, `SLAMStatisticsUpdated`, `SLAMHealthUpdated`

## Risks
- **False Loop Closures:** Incorrectly identifying a symmetrical room as a previously visited node can permanently warp the map.
- **Mitigation:** The loop closure threshold is highly conservative and relies on a minimum historical node buffer before trusting spatial overlaps.

## Migration
Zero structural migrations. The system now fully achieves Simultaneous Localization and Mapping.
