# Phase 2.7: Local Camera Pipeline & Vision Node - Implementation Plan

## Goal Description
Build the foundational Local Camera Pipeline for Recon Rover V2. This phase is strictly focused on image acquisition, buffering, and distribution. No AI or object detection will be performed. The objective is to decouple camera hardware streams into standardized, asynchronous `EventBus` payloads so future cognitive scripts can seamlessly subscribe to `FrameAvailable` events. 

## Proposed Changes

### 1. Vision Events (`core/vision/`)
[NEW] `vision_events.py`:
- Publishes: `CameraStarted`, `CameraStopped`, `FrameCaptured`, `FrameDropped`, `FrameAvailable`, `CameraHealthUpdated`, `CameraStatisticsUpdated`.
- Consumes: `CameraStartRequest`, `CameraStopRequest`, `CameraConfigurationUpdate`.

### 2. Capture & Buffering (`core/vision/`)
[NEW] `camera_capture.py`: Interfaces natively with USB/CSI cameras (e.g., using `cv2.VideoCapture`). Will use a mock or safe-fail interface if no hardware is present during testing.
[NEW] `frame_buffer.py`: Implements a fast Ring Buffer for raw frames. Ensures memory is strictly capped and older frames are natively dropped under high load to prevent memory leaks.
[NEW] `frame_distributor.py`: Extracts the latest frames from the buffer and pushes `FrameAvailable` metadata/payloads onto the EventBus.

### 3. Pipeline & Management (`core/vision/`)
[NEW] `camera_pipeline.py`: Orchestrates the raw data flow: Capture $\rightarrow$ Validate $\rightarrow$ Timestamp $\rightarrow$ Buffer $\rightarrow$ Distributor.
[NEW] `camera_manager.py`: Top-level node controller. Subscribes to start/stop intents on the EventBus and manages the lifecycle of the `camera_pipeline`.
[NEW] `camera_stream.py`: Future-proofing stub for web/IP stream syndication.

### 4. Telemetry (`core/vision/`)
[NEW] `camera_statistics.py`: Thread-safe tracking of FPS, frame counts, and drops.
[NEW] `camera_health.py`: Periodic broadcasts of camera health, verifying capture loop latency.

### 5. Documentation
[NEW] `docs/Phase-2/PHASE-2.7-IMPLEMENTATION-PLAN.md` (This file natively)
[NEW] `docs/Phase-2/PHASE-2.7.md`
[MODIFY] `ENGINEERING-CHANGELOG.md`

## Verification Plan
### Internal Tests
- Write `scratch/test_vision.py`.
- Verify `CameraManager` starts the pipeline gracefully.
- Inject a mock image frame into `camera_capture.py` and trace it through the `frame_buffer.py`.
- Verify `FrameAvailable` is successfully broadcast to the EventBus.
- Verify Ring Buffer explicitly drops the oldest frame if a burst of 100 frames is injected.

## User Review Required
> [!NOTE]
> Following the strict mandatory documentation policy, I have bypassed the deprecated default artifacts and crafted this custom implementation plan. To ensure our tests pass perfectly in a CI/headless environment, `camera_capture.py` will have a robust fallback to generate synthetic numpy array frames if no physical `/dev/video0` USB camera is present. Please approve this plan to begin execution.
