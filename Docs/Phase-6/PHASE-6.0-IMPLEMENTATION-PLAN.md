# Phase 6.0: Ground Station & Web Dashboard Framework - Implementation Plan

## Executive Summary
Phase 6.0 implements the architectural foundation for the Ground Station Web UI. Rather than a native application, Recon Rover V2 utilizes a browser-based dashboard served directly from the Raspberry Pi. This phase constructs the backend Python framework (designed for FastAPI) that handles HTTP sessions, user authentication, REST APIs, and most importantly, the high-speed bidirectional WebSocket bridge connecting the browser to the robot's internal EventBus.

## Objectives
- Implement `DashboardManager` and `DashboardEngine` to serve as the unified entry point for the web backend.
- Implement `ApiServer` to provide REST endpoints (`/api/status`, `/api/config`) for polling data.
- Implement `SessionManager` and `Authentication` to secure the robot from unauthorized access.
- Implement `WebsocketManager` to handle persistent full-duplex connections to operator browsers.
- Implement `TelemetryBridge` to route internal `EventBus` topics (hardware state, SLAM data) securely to connected WebSocket clients.
- Scaffold the `WEB_UI/frontend/` directory and index page.

## Architecture
- `WEB_UI/backend/dashboard_manager.py`: High-level entry point.
- `WEB_UI/backend/dashboard_engine.py`: Core routing and event generation.
- `WEB_UI/backend/session_manager.py`: Token-based session tracking.
- `WEB_UI/backend/telemetry_bridge.py`: The critical link converting EventBus structs into JSON WebSocket payloads.
- `WEB_UI/backend/api_server.py`: REST routes.
- `WEB_UI/backend/websocket_manager.py`: AsyncIO socket handling.

## Security & Concurrency
The framework enforces a basic token-based session layer. Commands incoming from the WebSocket (e.g., `DRIVE_FORWARD`) are verified and cleanly injected into the internal `EventBus` via `CommandReceivedEvent`. The system is designed to use Python's `asyncio` natively to handle multiple simultaneous browser connections (e.g., a pilot and an observer) without blocking the control loop.
