# Phase 6.3: Live Camera Streaming - Verification Plan

## Executive Summary
This document outlines the verification strategy for Phase 6.3 (Live Camera Streaming). The goal is to audit the entire video pipeline from EventBus ingestion to browser rendering, ensuring low-latency transport, memory stability, and efficient CPU utilization across both the backend encoder and frontend canvas renderer.

## Verification Objectives
- Validate the `StreamEngine` completely halts OpenCV processing when zero clients are actively viewing.
- Ensure the `FrameEncoder` sustains < 20ms encoding latency for 640x480 MJPEG frames.
- Prove the Frontend `StreamRenderer` successfully garbage collects Blob object URLs, preventing browser memory leaks.
- Verify the `StreamRouter` efficiently broadcasts `FrameBroadcastEvent`s to all connected WebSocket clients.
- Confirm the On-Screen Display (OSD) accurately reports FPS, bandwidth, and estimated latency.

## Verification Scope
The scope encompasses the `WEB_UI/backend/` streaming modules (`camera_stream_manager.py`, `stream_engine.py`, `frame_encoder.py`) and the `WEB_UI/frontend/js/` rendering scripts. It focuses on video transport efficiency, latency, and memory safety.

## Audit Strategy
1. **CPU Efficiency Audit:** Monitor Raspberry Pi simulated CPU load with 0, 1, and 5 connected clients to verify dynamic encoding suspension.
2. **Memory Leak Audit:** Run the frontend simulated stream at 30 FPS for 10 minutes. Profile the browser heap to confirm `URL.revokeObjectURL` prevents unbounded growth.
3. **Latency Emulation:** Inject a simulated timestamp in the mock backend and measure the delta inside `stream_renderer.js` to ensure the end-to-end pipeline operates under 100ms.

## Runtime Audit
- Verify the `CameraStreamManager` cleanly ingests numpy arrays from the EventBus without blocking other subscribers.

## Memory Audit
- Strict verification of frontend Image/Blob garbage collection. A missed revocation will crash a field tablet within minutes.

## Internal Test Matrix
1. **Zero-Viewer Optimization:** Verify `encode()` is not called when `sessions.has_viewers() == False`.
2. **Quality Switching:** Verify dynamic resolution and compression adjustments apply instantly without dropping the WebSocket.
3. **Canvas Drawing:** Verify the `<canvas>` dynamically resizes if the incoming frame dimensions change.

## PASS / FAIL Criteria
- **PASS:** Stable memory profile, <100ms simulated latency, zero-viewer CPU suspension working, accurate OSD.
- **FAIL:** Browser memory leak, heavy CPU load with no viewers, UI thread blocking, latency >200ms.

## Expected Deliverables
- `PHASE-6.3-VERIFICATION-PLAN.md`
- `PHASE-6.3-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
