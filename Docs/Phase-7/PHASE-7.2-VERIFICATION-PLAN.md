# Phase 7.2: Perception Engine - Verification Plan

## Executive Summary
This document defines the verification strategy for Phase 7.2. The primary objective is to validate that the Perception Engine accurately transforms raw 2D bounding boxes and depth/SLAM data into a robust, 3D semantic `SceneGraph` without introducing memory leaks, thread locks, or event loop blocking.

## Verification Objectives
- Validate `PerceptionRuntime` initialization and pipeline orchestration.
- Confirm `ObjectCorrelator` correctly extracts depth medians from mock depth matrices using `DistanceEstimator`.
- Verify `WorldProjection` accurately translates 2D+Depth into `[x, y, z]` world coordinates using mock robot odometry.
- Prove `EntityTracker` successfully maintains object permanence across sequential frames, and `VisibilityManager` correctly decays occluded objects.
- Validate `SpatialReasoner` calculates accurate geometric predicates (e.g., "near").
- Confirm `PerceptionBridge` serializes the highly-nested `SceneGraph` dictionary into JSON for the EventBus.

## Verification Scope
The scope encompasses all 20 modules created within `MAIN CODE/RASPBERRY_PI/core/ai/perception/` and the scratch test `scratch/test_perception_runtime.py`.

## Audit Strategy
1. **Spatial Projection Audit:** Pass a bounding box `[100, 100, 50, 150]` with a mock depth map of `np.ones * 2.5` and a robot pose of `x=10.0, y=5.0`. Verify the resulting `world_coords` are geometrically consistent (e.g., `x = 12.5`).
2. **Object Permanence Audit:** Inject a "person" (tracking_id=1). In the next frame, omit the person. Verify the entity still exists in `EntityTracker.entities` but its `visibility` score drops from 1.0 to 0.9.
3. **Graph Assembly Audit:** Inject a "person" and a "table". Verify the `SceneGraph` correctly catalogs both nodes and that the `SpatialReasoner` populates the edges array with a relationship predicate.
4. **Queue Saturation Audit:** Rapidly push 20 states into the `PerceptionScheduler` (maxsize=10). Verify the oldest states are gracefully discarded.

## Runtime Audit
- Ensure that the heavy NumPy median operations within `DistanceEstimator` execute quickly enough to prevent starving the Python `asyncio` loop.

## Memory Audit
- Verify the `SceneGraph` and `EntityTracker` do not balloon infinitely. Test the `VisibilityManager` pruning logic to ensure objects with visibility <= 0 are completely deleted from memory.

## Internal Test Matrix
1. **Valid Initialization:** Run `test_perception_runtime.py`. (Expect Success).
2. **Depth Correlation:** Extract median from a simulated noisy depth array. (Expect accurate distance).
3. **Ghost Object Purge:** Run visibility decay until an object hits 0.0. (Expect dict key deletion).
4. **Event Serialization:** Trigger `SceneUpdated`. (Expect valid JSON strings).

## PASS / FAIL Criteria
- **PASS:** The pipeline accurately correlates depth, maps world coordinates, tracks entities across frames, and publishes valid JSON without blocking.
- **FAIL:** NumPy operations lock the GIL. The entity dictionary grows infinitely. World coordinates calculate incorrectly.

## Expected Deliverables
- `PHASE-7.2-VERIFICATION-PLAN.md`
- `PHASE-7.2-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
