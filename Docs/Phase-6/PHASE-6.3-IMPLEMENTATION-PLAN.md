# Phase 6.3: Live Camera Streaming - Implementation Plan

## Executive Summary
Phase 6.3 implements a low-latency, real-time video streaming architecture bridging the Raspberry Pi camera subsystem to the browser dashboard. By avoiding the overhead of WebRTC and relying on a highly optimized MJPEG-over-WebSocket pipeline, the system prioritizes minimal latency and predictability over maximum resolution, satisfying the strict requirements for remote teleoperation.

## Objectives
- Implement Backend `CameraStreamManager` to interface seamlessly with the existing `CameraFrameEvent` published by the Camera Pipeline.
- Implement Backend `FrameEncoder` utilizing OpenCV (`cv2.imencode`) to compress raw numpy arrays into target JPEG resolutions on the fly.
- Implement Backend `StreamSessionManager` to track active viewers and automatically pause encoding if no clients are connected, saving crucial CPU cycles.
- Implement Frontend HTML5 Canvas (`<canvas>`) rendering pipeline to ingest binary WebSocket frames and paint them instantly.
- Implement Frontend `StreamStatistics` to calculate real-time FPS, bandwidth (kbps), and estimated network latency.

## Architecture
- `WEB_UI/backend/frame_encoder.py`: Handles the synchronous CPU-bound task of image compression.
- `WEB_UI/backend/stream_engine.py`: Orchestrates the flow from raw frame $\to$ compression $\to$ websocket broadcast.
- `WEB_UI/frontend/js/stream_renderer.js`: Converts binary Blobs into `Image` objects and paints them via `canvas.drawImage`, avoiding the memory leaks associated with continuously updating `<img>` `src` attributes.

## Performance Constraints
- **Encoding Latency:** The `FrameEncoder` must execute in < 20ms to sustain 30FPS.
- **Garbage Collection:** The frontend `StreamRenderer` must explicitly call `URL.revokeObjectURL(img.src)` after every frame to prevent catastrophic browser memory leaks during extended operation.
- **Network Degradation:** The frontend allows operators to select Quality profiles (High/Medium/Low). The backend dynamically adjusts the `cv2.IMWRITE_JPEG_QUALITY` and resolution parameters based on this feedback.
