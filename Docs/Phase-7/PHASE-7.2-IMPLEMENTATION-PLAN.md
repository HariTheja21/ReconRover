# Phase 7.2: Perception Engine - Implementation Plan

## Executive Summary
Phase 7.2 introduces the Perception Engine. This layer acts as the bridge between raw Vision AI and high-level autonomy. It ingests 2D bounding boxes and raw SLAM/depth data, and outputs a structured 3D Scene Graph containing object permanence, spatial coordinates, and semantic relationships. No autonomous decisions are made here; it solely constructs the world model.

## Objectives
- Build `PerceptionRuntime` and `PerceptionManager` as the core orchestration layers for the perception pipeline.
- Implement the `SceneAnalyzer` which fuses multiple data streams into a cohesive environmental understanding.
- Develop `ObjectCorrelator` and `DistanceEstimator` to project 2D vision detections into estimated 3D spatial coordinates using Depth/SLAM data.
- Construct `EntityTracker` and `VisibilityManager` to maintain object permanence (e.g., remembering a chair exists even if temporarily occluded).
- Create `SpatialReasoner` to calculate predicates (e.g., "next_to", "approaching") between tracked entities.
- Assemble the `SceneGraph` to maintain the live structured state of the environment.

## Architecture
- **Perception Pipeline:** Raw Detections + Depth + Pose -> `ObjectCorrelator` -> `WorldProjection` -> `ConfidenceFusion` -> `SemanticFilter` -> `EntityTracker` -> `SpatialReasoner` -> `SceneGraph` -> `EnvironmentClassifier`.
- **Event Routing:** The `PerceptionBridge` emits `perception.objects` (individual 3D objects) and `perception.scene` (entire scene graph snapshot).

## Safety & Constraints
- **Asynchronous Scheduler:** Similar to Vision AI, the `PerceptionScheduler` uses a bounded `asyncio.Queue` (maxsize=10) to drop older states if the perception math lags behind real-time.
- **Thread Safety:** Operations on the `SceneGraph` are strictly synchronous within the async worker loop, avoiding race conditions during graph updates.
