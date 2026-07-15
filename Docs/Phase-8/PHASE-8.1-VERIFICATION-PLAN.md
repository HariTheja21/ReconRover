# Phase 8.1: Vision Model Integration - Verification Plan

## Executive Summary
This document establishes the verification strategy for Phase 8.1. The objective is to validate that the Vision Runtime flawlessly loads, executes, and unloads physical ML models. The pipeline must demonstrate complete abstraction—allowing hot-swapping between YOLO (object detection) and Depth Anything (depth estimation) without altering the high-level EventBus interface.

## Verification Objectives
- Validate `VisionLoader` successfully initializes weights using both `ONNXProvider` and `TorchProvider` without memory overlaps.
- Confirm `VisionInference` correctly threads inputs through `VisionPreprocessor` and `VisionPostprocessor`.
- Verify `VisionRegistry` safely restricts unsupported model initializations.
- Prove hot-swapping capabilities: Load YOLO -> Execute -> Unload YOLO -> Load Depth Anything -> Execute.
- Ensure `VisionBridge` serializes parsed `VisionResults` into standardized JSON payloads (`ObjectDetectionUpdated`).

## Verification Scope
The scope encompasses all 20 vision integration modules located in `MAIN CODE/RASPBERRY_PI/core/ai/runtime/vision/` and the integration script `scratch/test_vision_models.py`.

## Audit Strategy
1. **Model Registration Audit:** Check `VisionRegistry` for the exact presence of `yolo11`, `rt-detr`, `fastsam`, and `depth_anything` provider classes.
2. **Pipeline Abstraction Audit:** Execute an inference call. Verify the engine receives a generic `VisionResults` dataclass rather than raw ONNX/PyTorch tensors.
3. **Hot-Swap Memory Audit:** Instruct `VisionLoader` to unload a model. Verify the dictionary reference is deleted, signaling the Python garbage collector to free the RAM/VRAM.
4. **Latency Measurement Audit:** Check if `VisionInference.execute()` accurately wraps the forward pass with a `time.time()` block, appending the elapsed milliseconds to the result.
5. **Event Routing Audit:** Monitor the MockEventBus for the exact presence of `ObjectDetectionUpdated` after a successful YOLO inference.

## Runtime Audit
- Verify the `VisionScheduler` utilizes non-blocking `asyncio.sleep()` routines to regulate FPS, preventing the camera polling loop from starving the CPU.

## Memory Audit
- Verify the system only permits one heavy vision model (e.g., Depth Anything) to occupy VRAM at a time during standard execution, explicitly unloading previous models via `VisionLoader.unload_model()`.

## Internal Test Matrix
1. **Valid Initialization:** Run `test_vision_models.py`. (Expect Success).
2. **Provider Loading (ONNX):** Load YOLO. (Expect True).
3. **Inference (Detection):** Execute YOLO. (Expect BBox generation).
4. **Model Unloading:** Unload YOLO. (Expect RAM released).
5. **Provider Loading (Torch):** Load Depth Anything. (Expect True).
6. **Inference (Depth):** Execute Depth Anything. (Expect Depth Map generation).

## PASS / FAIL Criteria
- **PASS:** The Vision Runtime flawlessly abstracts underlying frameworks. Models load, execute, and unload on command. Telemetry is serialized successfully to the EventBus.
- **FAIL:** Provider specific tensors leak out of the postprocessor. The `VisionLoader` fails to clear memory during hot-swaps. The scheduler blocks the async thread.

## Expected Deliverables
- `PHASE-8.1-VERIFICATION-PLAN.md`
- `PHASE-8.1-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
