# Phase 7.1: Vision AI Engine - Implementation Plan

## Executive Summary
Phase 7.1 integrates the Vision AI Engine into the Phase 7.0 AI Runtime Framework. This module is responsible for real-time camera frame ingestion, object detection, multi-object tracking, and semantic event generation. It acts entirely as a perception layer—converting pixel data into structured metadata—without encroaching on the autonomy or navigation stacks.

## Objectives
- Build `VisionRuntime` and `VisionManager` as the core orchestration layers, exposing a clean API for loading ONNX models (e.g., YOLOv11).
- Implement a rigorous 7-stage `VisionPipeline` (Detect -> Map Classes -> Filter Confidence -> Filter Allowed -> Format BBoxes -> Track -> Overlay).
- Create strict filtering classes (`ConfidenceFilter`, `DetectionFilter`) to drop low-certainty or irrelevant objects before they consume downstream resources.
- Construct the `InferenceWorker` to execute the pipeline asynchronously and publish `VisionInferenceEvent` and `DetectionEvent` payloads.
- Utilize a `VisionScheduler` with bounded queues (`asyncio.Queue(maxsize=5)`) to drop frames if the model cannot maintain real-time throughput, prioritizing low latency over 100% frame processing.

## Architecture
- **Inference Pipeline:** Raw Frame -> `FramePreprocessor` -> `ObjectDetector` -> `FramePostprocessor`.
- **Metadata Pipeline:** Raw Detections -> `ClassMapper` -> `ConfidenceFilter` -> `DetectionFilter` -> `BoundingBoxManager` -> `ObjectTracker`.
- **Event Routing:** The `VisionBridge` intercepts raw detections. Standard telemetry (latency, frame counts) is routed to `telemetry.vision`. High-priority semantic detections (e.g., "Person detected at [x,y]") are routed to `vision.detections` for eventual autonomy consumption.

## Safety & Constraints
- **Frame Dropping:** To prevent memory leaks and massive latency lag, the `VisionScheduler` utilizes a hard cap on its intake queue. If the AI is overwhelmed, old frames are discarded.
- **Thread Safety:** The Vision Engine operates entirely asynchronously, utilizing NumPy arrays safely within the Python `asyncio` event loop.
