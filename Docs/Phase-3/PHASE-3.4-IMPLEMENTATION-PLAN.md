# Phase 3.4: Mapping Engine - Implementation Plan

## Executive Summary
Recon Rover V2's Phase 3.4 establishes the Mapping Engine, providing the robot with a spatial memory of its environment. By combining the `RobotPoseUpdated` data (Localization) with `FusedObstacle` data (Perception), the engine projects sensory collisions into a global 2D `OccupancyGrid`. 

## Objectives
- Implement a memory-efficient sparse 2D Occupancy Grid representing the world.
- Project forward-facing sensor collisions into the absolute world frame.
- Safely manage the robot's spatial memory footprint using garbage collection/optimization rules.
- Publish `OccupancyGridUpdated` events to the EventBus without blocking the 10Hz perception cycles.

## Architecture
- `mapping_manager.py`: Thread-safe asynchronous daemon binding the grid to the EventBus.
- `mapping_engine.py`: Orchestrates the builder, optimizer, and storage pipelines.
- `occupancy_grid.py`: Core mathematical dictionary storing `(gx, gy) -> probability`.
- `map_builder.py`: Trigonometric translation of relative sensor distance to absolute grid coordinates.
- `map_storage.py`: Basic JSON serialization for saving the map state to disk.
- `map_history.py`: A `deque` tracking chronological map diffs.
- `map_optimizer.py`: Prunes 0.5 probability (unknown) cells from the dictionary to cap RAM usage.

## EventBus Integration
**Consumes:** `RobotPoseUpdated`, `FusedObstacle`
**Publishes:** `MapUpdated`, `OccupancyGridUpdated`, `MapStatisticsUpdated`, `MappingHealthUpdated`

## Risks
- **RAM Exhaustion:** A massive open-world space could overload the dictionary if not pruned.
- **Mitigation:** The `MapOptimizer` aggressively culls any cell that reverts to an exact 0.5 probability, maintaining a sparse footprint.

## Migration
Zero structural migrations. The SLAM puzzle is now ready for closure.
