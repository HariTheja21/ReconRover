# Phase 3.1: World Model Engine - Implementation Plan

## Executive Summary
Recon Rover V2 is entering the cognitive domain. Phase 3.1 establishes the "World Model Engine," an in-memory spatial database designed to aggregate, timestamp, and store semantic events (IMU, distance, obstacles, orientation, battery) fired by the Sensor Bridge. It maintains a centralized world state, tracks dynamic entities, and calculates sensory confidence decay.

## Objectives
- Build a thread-safe, timestamped, semantic world database (`world_database.py`).
- Implement decoupled modules for tracking the internal Robot State, Obstacles, Landmarks, Occupancy grids, and Entities.
- Introduce `confidence_manager.py` to decay sensor confidence linearly over time.
- Guarantee constant $O(1)$ read/write capabilities for future mapping nodes to poll securely.

## Repository Analysis
The `SystemOrchestrator` guarantees robust runtime lifecycle management. Phase 3.1 operates seamlessly within this supervised architecture.

## Current Architecture
The system currently generates telemetry but possesses zero contextual memory. Events evaporate upon consumption.

## Technical Debt
None.

## Proposed Architecture
The `WorldManager` consumes asynchronous events, piping them directly into the `WorldDatabase`.
- `world_state.py`: Tracks internal physical parameters (battery, IMU pose).
- `entity_manager.py`: Tracks specific physical entities (via `entity.py`) with semantic classes and confidence scalars.
- `obstacle_manager.py`: Aggregates dynamic sensor proximity data into collision threats.
- `landmark_manager.py`: Anchors vision-detected targets in local space.
- `occupancy_manager.py`: Exposes a discrete spatial grid.

## Folder Structure
```
core/world/
  ├── world_manager.py
  ├── world_state.py
  ├── world_database.py
  ├── entity_manager.py
  ├── entity.py
  ├── obstacle_manager.py
  ├── landmark_manager.py
  ├── occupancy_manager.py
  ├── confidence_manager.py
  ├── world_events.py
  ├── world_health.py
  └── world_statistics.py
```

## Public APIs
The `WorldManager` acts as the daemon, publishing 4 main payloads to the EventBus at fixed cyclic intervals (10Hz): `WorldUpdated`, `ObstacleMapUpdated`, `LandmarkUpdated`, `RobotStateUpdated`.

## EventBus Integration
**Consumes:** `IMUUpdated`, `DistanceUpdated`, `ObstacleDetected`, `BatteryUpdated`, `CameraFrameAvailable`
**Publishes:** `WorldUpdated`, `ObstacleMapUpdated`, `LandmarkUpdated`, `RobotStateUpdated`, `WorldHealthUpdated`

## Dependencies
None outside of standard core events.

## Runtime Design
A central aggregator loop driven by `asyncio.sleep(0.1)`. All incoming events use ultra-fast `threading.RLock()` to write to the `world_database.py`. The 10Hz sweep task extracts snapshots and purges old observations using Time-To-Live limits.

## Memory Strategy
Strict memory boundaries. Obsolete obstacles and entities are flushed dynamically.

## CPU Strategy
State updates are $O(1)$ dictionary overrides. No expensive map computations occur here.

## Risks
Stale Data: Resolved natively via Time-To-Live (TTL) timestamps and linear `confidence_manager.py` decay.

## Migration Strategy
No structural migrations needed. 

## Deliverables
Implementation of 12 files inside `core/world/`.
Internal Test script validation.
Standard documentation and changelogs.

## Engineering Recommendation
Proceed immediately. The World Database isolates the mapping math from the state storage, enabling perfect separation of concerns for the incoming SLAM modules.
