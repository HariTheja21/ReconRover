# Phase 3.7: Path Planning Engine - Implementation Plan

## Executive Summary
Phase 3.7 introduces the Path Planning Engine, fulfilling the requirement for intelligent spatial traversal. By consuming the Navigation Core's goal and evaluating it against the Mapping Engine's occupancy grid, this module generates safe, collision-free paths. Crucially, the architecture is designed as a modular interface, allowing algorithmic flexibility (e.g., swapping A* for D* Lite or RRT) without altering downstream APIs.

## Objectives
- Deploy a decoupled `PathPlanner` interface.
- Implement $A^*$ (A-Star) as the default resolution-based planning algorithm.
- Build a robust `PathValidator` to prevent stale-cache collisions when the environment changes.
- Implement a `PathCache` to dramatically reduce CPU spikes on static objectives.
- Seamlessly ingest `CorrectedPoseUpdated` and `GoalUpdated` via the EventBus.

## Architecture
- `planner_manager.py`: Connects the 2Hz conditional planning cycle to the EventBus.
- `planner_engine.py`: Central pipeline orchestrator (Cache $\rightarrow$ Plan $\rightarrow$ Optimize $\rightarrow$ Validate).
- `astar_planner.py`: Standard graph-search implementation.
- `path_optimizer.py`: Stubbed hook for future curve-smoothing (B-splines).
- `path_validator.py`: Real-time collision detection mapping coordinates to the sparse `OccupancyGrid`.
- `path_cache.py`: High-speed memory retrieval for identical unblocked routes.

## EventBus Integration
**Consumes:** `CorrectedPoseUpdated`, `OccupancyGridUpdated`, `GoalUpdated`
**Publishes:** `PathGenerated`, `PathInvalidated`, `PathUpdated`, `PlannerStatisticsUpdated`, `PlannerHealthUpdated`

## Risks
- **Grid Resolution Overhead:** Running $A^*$ over massive distances at 1cm resolution can stall the CPU. 
- **Mitigation:** The planner utilizes a 10cm grid block resolution, keeping the open-set array small and solving most rooms in milliseconds.

## Migration
Zero structural migrations. Ready to inject optimal paths directly into the final Local Planner / Obstacle Avoidance layer in Phase 4.
