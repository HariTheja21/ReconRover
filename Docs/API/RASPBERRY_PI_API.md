# Recon Rover V1 — Raspberry Pi Internal API & Modules

**Document Version:** 1.0  
**Status:** Frozen Specification  
**Last Updated:** 2026-06-28  

This document defines the high-level Python software modules running on the Raspberry Pi 3B+. The Pi acts as the cognitive layer. It communicates with the ESP32-S3 via the `serial_manager` and synchronizes internal state via an asynchronous event bus and a shared world model.

## 1. Module Overview & Responsibilities

| Module | Core Responsibility |
|--------|---------------------|
| `main.py` | Bootstraps all modules, manages startup order and graceful shutdown. |
| `config.py` | Loads, validates, and exposes all configuration values (e.g., from `rover.yaml`). |
| `logger.py` | Provides thread-safe structured logging to console and rotating log files. |
| `event_bus.py` | Internal publish/subscribe system for passing events between modules asynchronously. |
| `serial_manager.py` | Owns the USB serial port; reads JSON telemetry, writes JSON commands. |
| `vision_pipeline.py` | Handles OpenCV frame capture, object detection, and tracking in a separate thread. |
| `audio_pipeline.py` | Handles microphone capture, Voice Activity Detection (VAD), and speech-to-text. |
| `sensor_fusion.py` | Merges ESP32 telemetry data into the global world model. |
| `world_model.py` | Thread-safe object storing the rover's real-time spatial and state representation. |
| `ai_engine.py` | High-level decision making and behavioral mode management (e.g., IDLE, PATROL, AVOID). |
| `navigation.py` | Path planning, obstacle avoidance, and high-level movement directives. |
| `motion_planner.py` | Translates navigation directives into specific motor speed/direction targets. |
| `expression_selector.py`| Maps the current AI context to OLED eye expression identifiers. |
| `command_builder.py` | Packs actuator targets into the outgoing JSON command packet. |
| `dashboard_server.py` | WebSocket/HTTP server streaming telemetry to the web dashboard. |

## 2. Core Data Structures & Interfaces

### 2.1 The Event Bus
The `event_bus.py` module acts as the central nervous system. Modules publish events without knowing who consumes them.
* **Topics:** `telemetry_received`, `object_detected`, `voice_command`, `mode_change`, `hardware_fault`.

### 2.2 The World Model
The `world_model.py` contains the authoritative state of the rover.
* **Fields:** `current_mode`, `obstacles` (distance map from sensors), `detected_objects` (from vision), `battery_voltage`, `last_telemetry_ts`.

### 2.3 Command Builder
The `command_builder.py` collects state from `motion_planner.py` (motors, servos), `expression_selector.py` (eyes), and AI Engine (LEDs) to construct the unified JSON command packet defined in `COMMUNICATION_PROTOCOL.md`.

## 3. Concurrency Model
The software uses Python `asyncio` for I/O-bound tasks and threading for CPU/Blocking tasks:
* **asyncio loop:** `serial_manager`, `sensor_fusion`, `ai_engine`, `navigation`, `command_builder`, `dashboard_server`.
* **Threads:** `vision_pipeline` (blocks on OpenCV capture), `audio_pipeline` (blocks on audio stream), `logger` (file I/O).
