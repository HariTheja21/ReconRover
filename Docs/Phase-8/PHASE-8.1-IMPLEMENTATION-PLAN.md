# Phase 8.1: Vision Model Integration - Implementation Plan

## Executive Summary
Phase 8.1 introduces the Vision Model Integration layer to Recon Rover V2. Building on top of the Phase 8.0 AI Environment Runtime, this phase implements the specific inference pipelines for computer vision. It abstracts away the complexities of running YOLO11, RT-DETR, FastSAM, and Depth Anything models behind unified interfaces, allowing the rover's Multi-Agent framework to seamlessly switch vision capabilities on the fly without dealing with the underlying PyTorch or ONNX runtimes.

## Objectives
- Build `VisionRuntime`, `VisionRegistry`, and `VisionLoader` to handle dynamic model injection and lifecycle management.
- Implement `BaseProvider`, `ONNXProvider`, and `TorchProvider` to abstract backend execution.
- Create specific model implementations: `YOLOProvider`, `RTDETRProvider`, `FastSAMProvider`, and `DepthAnythingProvider`.
- Develop `VisionPreprocessor` (image normalization, resizing) and `VisionPostprocessor` (NMS, formatting) to standardize I/O across heterogeneous models.
- Construct `VisionInference` engine to execute the end-to-end forward pass and record latency.
- Integrate `VisionScheduler` to process camera frames asynchronously at a target FPS.
- Wire `VisionBridge` to broadcast standard events (`ObjectDetectionUpdated`, `SegmentationUpdated`) to the EventBus.

## Architecture
- **Initialization:** `VisionRuntime` registers the available vision models into the `VisionRegistry`.
- **Loading:** `VisionLoader` initializes the requested model, assigning it either an ONNX or Torch provider backend.
- **Execution Loop:** `VisionScheduler` grabs frames and calls `VisionInference.execute()`.
- **Inference Pipeline:** Frame -> `VisionPreprocessor` -> Provider `infer()` -> `VisionPostprocessor` -> `VisionResults`.
- **Event Routing:** `VisionBridge` publishes the parsed results to `vision.perception`.

## Safety & Constraints
- **Model Agnosticism:** Upper layers (like the Vision Agent) never import ONNX or PyTorch directly. They only consume standard `VisionResults` objects.
- **Memory Bounding:** Models are unloaded dynamically when switching tasks to preserve the constrained RAM of the host device.
