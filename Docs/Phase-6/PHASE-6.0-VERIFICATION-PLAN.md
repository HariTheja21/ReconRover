# Phase 6.0: Ground Station & Web Dashboard Framework - Verification Plan

## Executive Summary
This document defines the verification strategy for Phase 6.0 (Ground Station & Web Dashboard Framework). The goal is to audit the foundational backend architecture that serves the web UI, ensuring that REST APIs, WebSocket routing, and operator sessions function securely and deterministically without blocking the core robotic control loops.

## Verification Objectives
- Validate the `DashboardManager` and `DashboardEngine` structure for managing FastAPI/Uvicorn lifecycles.
- Ensure the `SessionManager` securely issues and times-out token-based sessions.
- Verify that the `WebsocketManager` handles concurrent client connections safely and routes commands properly.
- Prove that the `TelemetryBridge` successfully ingests high-frequency EventBus data and formats it for broadcast.
- Confirm that unauthorized REST/WebSocket access is aggressively rejected by the `ApiServer` and `Authentication` modules.

## Verification Scope
The scope encompasses the `WEB_UI/backend/` directory on the Raspberry Pi. This audit checks the logic that manages network connections and bridges internal software architectures to external HTTP/WS protocols. It does not include frontend UI rendering (Phase 6.1).

## Audit Strategy
1. **Security Audit:** Trace the authentication flow from `LoginAttemptEvent` to token generation and subsequent API access to ensure no endpoints are exposed without validation.
2. **Concurrency Emulation:** Review `test_dashboard.py` execution to verify that asynchronous methods properly decouple external network latency from internal EventBus propagation.
3. **Data Integrity:** Verify that telemetry data bridged via `WebsocketBroadcast` matches the exact schema emitted by the underlying hardware modules.

## AsyncIO Audit
- Ensure that `await` calls in `WebsocketManager.broadcast()` and `route_incoming_message()` yield correctly, allowing the backend to service multiple browsers simultaneously.

## Runtime Audit
- Verify the `DashboardEngine` spins up cleanly and establishes communication pathways without causing race conditions during boot.

## Memory Audit
- Confirm that disconnected WebSockets and expired sessions are properly garbage collected by the `SessionManager` and `WebsocketManager`, preventing memory leaks over extended operation.

## Internal Test Matrix
1. **Authentication Success/Failure:** Verify valid credentials yield tokens and invalid ones do not.
2. **Session Persistence:** Verify token-based REST queries succeed, and invalid token queries return `{"error": "Unauthorized"}`.
3. **WebSocket Routing:** Verify incoming WS messages are wrapped and fired as `CommandReceivedEvent`s.
4. **Telemetry Bridging:** Verify `EventBus` payloads are formatted and emitted as `WebsocketBroadcast` events.

## PASS / FAIL Criteria
- **PASS:** 100% test success, strict session enforcement, non-blocking WS routing, zero memory leaks on disconnect.
- **FAIL:** Unauthenticated API access, dropped telemetry packets, thread-blocking network calls, memory growth on client disconnect.

## Expected Deliverables
- `PHASE-6.0-VERIFICATION-PLAN.md`
- `PHASE-6.0-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
