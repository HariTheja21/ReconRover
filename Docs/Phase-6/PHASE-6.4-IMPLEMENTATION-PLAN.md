# Phase 6.4: Mission Planning Interface - Implementation Plan

## Executive Summary
Phase 6.4 introduces the Mission Planning Interface, empowering operators to design, validate, store, and execute autonomous waypoint-based routines. The frontend leverages Leaflet.js for lightweight interactive mapping, allowing drag-and-drop waypoint creation. The backend handles secure JSON storage, mission validation, and bridging execution intents into the rover's core `EventBus`.

## Objectives
- Implement `MissionManager` and `MissionEngine` to orchestrate backend storage, validation, and execution.
- Implement `MissionStorage` to persist mission configurations as JSON files to the disk (`data/missions/`).
- Implement `MissionValidator` to enforce structural integrity (e.g., minimum waypoints, valid lat/lng constraints) before saving or executing.
- Implement a responsive UI (`missions.html`) using Leaflet.js for interactive mapping (`mission_map.js`).
- Implement `MissionEditor` logic to handle UI state transitions (Add, Edit, Save, Execute).

## Architecture
- **Storage:** Missions are stored as individual JSON files to prevent database overhead and ensure easy import/export capabilities.
- **Frontend Map:** `Leaflet.js` is utilized via a CDN. It acts as the interactive canvas, emitting latitude/longitude coordinates to the `MissionEditor` upon clicks or marker drags.
- **Backend Bridge:** The `MissionScheduler` does not drive the rover directly. It loads the verified JSON, emits a `MissionStatusEvent`, and relies on the Phase 3 Navigation Engine to consume the waypoints via the `EventBus`.

## Constraints & Edge Cases
- **Validation:** Missions without names or zero waypoints are rejected instantly by both the frontend and backend.
- **Execution Locks:** Only one mission can run at a time. The `MissionScheduler` tracks `active_mission_id` and rejects concurrent execution requests.
