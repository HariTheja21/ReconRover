# Phase 7.1: Vision AI Engine - Verification Plan

## Executive Summary
This document defines the verification strategy for Phase 7.1. The objective is to validate the architectural integrity, real-time performance, and logical correctness of the Vision AI Engine, ensuring the `VisionPipeline` successfully processes frames, tracks objects, and emits high-fidelity semantic telemetry without memory leaks or Event Loop blocking.

## Verification Objectives
- Validate `VisionRuntime` initialization and model loading lifecycle via `ModelLoader`.
- Confirm `VisionScheduler` successfully drops frames when its internal queue (`maxsize=5`) overflows during artificial processing spikes.
- Verify `DetectionFilter` correctly drops unmapped classes and `ConfidenceFilter` correctly rejects sub-threshold bounding boxes.
- Prove `ObjectTracker` correctly assigns monotonically increasing tracking IDs across sequential frames.
- Validate `VisionBridge` publishes structured `DetectionEvent` objects to the `vision.detections` topic.

## Verification Scope
The scope covers all 19 Vision modules located in `MAIN CODE/RASPBERRY_PI/core/ai/vision/` and the scratch test `scratch/test_vision_runtime.py`.

## Audit Strategy
1. **Pipeline Execution Audit:** Inject a mock frame into the `VisionPipeline`. Hardcode the `ObjectDetector` to return 3 objects: Person (0.9 conf), Car (0.8 conf), and Laptop (0.4 conf). Set `ConfidenceFilter` to 0.5. Verify only the Person and Car proceed. Set `DetectionFilter` allowed classes to "person" and "laptop". Verify only the Person survives the full pipeline.
2. **Scheduler Stress Audit:** Set `VisionScheduler` maxsize to 2. Rapidly inject 10 frames. Verify `stats.frames_dropped` equals 8, proving the system prioritizes latency over backlog.
3. **Tracking Audit:** Pass identical mock detections into `ObjectTracker` over 3 frames. Verify the assigned `tracking_id` persists rather than randomly regenerating.
4. **Event Routing Audit:** Trigger the `InferenceWorker`. Verify `VisionBridge` splits `VisionInferenceEvent` (latency data) to `telemetry.vision` and `DetectionEvent` to `vision.detections`.

## Runtime Audit
- Ensure NumPy array manipulations inside `FramePreprocessor` and `VisionOverlay` do not introduce hidden GIL locks that block the asyncio loop.

## Memory Audit
- Verify the internal queue of `VisionScheduler` explicitly drops references to discarded frame matrices, allowing Python's GC to reclaim memory.

## Internal Test Matrix
1. **Valid Initialization:** Run `test_vision_runtime.py`. (Expect Success).
2. **Queue Saturation:** Inject 20 frames instantly. (Expect Drops).
3. **Threshold Filtering:** Filter high vs low confidence targets. (Expect Accuracy).
4. **Invalid Model Path:** Attempt to load a non-existent ONNX file. (Expect Graceful Failure).

## PASS / FAIL Criteria
- **PASS:** The pipeline accurately filters targets, assigns tracking IDs, routes events correctly, and drops frames predictably under load.
- **FAIL:** The queue backlogs infinitely. Tracking IDs rotate every frame. NumPy blocks the event loop.

## Expected Deliverables
- `PHASE-7.1-VERIFICATION-PLAN.md`
- `PHASE-7.1-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
