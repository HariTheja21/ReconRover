# Phase 4.6: ESP32 Hardware Telemetry System - Implementation Plan

## Executive Summary
Phase 4.6 implements the upward transmission pathway of the ESP32 firmware architecture. The Hardware Telemetry System is responsible for querying the physical states of motors, servos, IMUs, and batteries, packaging this data into the standard 9-byte binary `0xAA55` protocol, and dispatching it to the UART transport layer. This enables the Raspberry Pi to maintain real-time situational awareness of the physical robot.

## Objectives
- Implement `TelemetryScheduler` to regulate the transmission frequency of various data types (e.g., Heartbeat at 1Hz, Motor Status at 10Hz).
- Implement `TelemetryEncoder` to securely serialize C++ structs into Big-Endian binary payloads.
- Implement `TelemetryPacketBuilder` to encapsulate the encoded payloads with headers (`0xAA55`), sequence numbers, and CRC8 checksums.
- Implement `TelemetryEngine` and `TelemetryManager` as the FreeRTOS-compatible polling loops to aggregate data across all hardware domains without blocking execution.

## Architecture
- `ESP32_ROVER/main/telemetry/telemetry_events.h`: Defines abstract status structs matching the Python backend.
- `ESP32_ROVER/main/telemetry/telemetry_scheduler.cpp`: Decouples transmission rates from the main loop speed.
- `ESP32_ROVER/main/telemetry/telemetry_encoder.cpp`: Big-Endian byte packing logic.
- `ESP32_ROVER/main/telemetry/telemetry_packet_builder.cpp`: Frame assembly and CRC calculation.
- `ESP32_ROVER/main/telemetry/telemetry_engine.cpp`: State collection hub.
- `ESP32_ROVER/main/telemetry/telemetry_manager.cpp`: High-level RTOS orchestrator.

## FreeRTOS Considerations
- **Non-Blocking:** The scheduler uses non-blocking millisecond deltas (`current_time_ms - last_publish_ms`) rather than `vTaskDelay` to allow a single hardware-monitoring task to interleave smoothly.
- **Zero Allocation:** The entire telemetry building pipeline operates on statically allocated stack buffers (maximum 16 bytes), entirely eliminating heap usage and fragmentation risks.
- **Callback Injection:** The engine relies on an abstract `UartTransmitCallback` rather than hardcoding ESP-IDF UART drivers, allowing safe cross-thread queuing later.

## Telemetry Flow
1. `TelemetryManager::Tick()` checks `TelemetryScheduler`.
2. Scheduler flags `ShouldSendHeartbeat()` or `ShouldSendMotorStatus()`.
3. Engine queries the Driver layer for current physical states.
4. Engine delegates the state struct to `TelemetryPacketBuilder`.
5. Builder uses `TelemetryEncoder` to pack the 4-byte payload.
6. Builder appends headers, increments sequence, calculates CRC8, and fires the UART callback.
