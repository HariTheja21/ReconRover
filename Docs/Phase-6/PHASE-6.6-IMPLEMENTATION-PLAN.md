# Phase 6.6: Diagnostics & Log Viewer - Implementation Plan

## Executive Summary
Phase 6.6 delivers the Diagnostics & Log Viewer Framework. This phase constructs the system observability layer, granting operators real-time insight into the rover's internal state. It features live log streaming, subsystem health monitoring, hardware performance metrics (CPU, RAM, Temp), and diagnostic report generation.

## Objectives
- Implement `LogManager` and `LogStorage` to persistently record system events with daily rotation.
- Implement `HealthMonitor` and `PerformanceMonitor` to ingest and aggregate EventBus metrics into a unified state.
- Develop `diagnostics.html` to provide a triple-pane view: Subsystem Health Grid, Live Log Terminal, and Performance Dashboard.
- Implement `ReportGenerator` to serialize the current diagnostic state into downloadable JSON reports.

## Architecture
- **Log Pipeline:** The rover's subsystems publish `LogEvent` payloads to the EventBus. `LogManager` captures these, writes them to `data/logs/system_YYYY-MM-DD.log`, and bridges them to the frontend via WebSockets.
- **Health & Performance:** Dedicated monitors aggregate `HealthStatusEvent` and `PerformanceMetricsEvent` objects. This decoupled approach ensures that high-frequency telemetry doesn't overwhelm the logging system.
- **Frontend Observability:** The UI employs `LogViewer` to render terminal-like logs with regex/level filtering, and `HealthDashboard` to render dynamic status badges (OK, WARNING, ERROR, OFFLINE).

## Safety & Constraints
- **Failsafe Logging:** `LogStorage` wraps file I/O in strict `try/except` blocks. If the disk is full or read-only, the logger silently drops events rather than crashing the overarching EventBus.
- **Memory Bounding:** The frontend `LogViewer` maintains a strict FIFO buffer (`maxLogs = 1000`) to prevent the browser tab from crashing due to DOM bloating during extended missions.
