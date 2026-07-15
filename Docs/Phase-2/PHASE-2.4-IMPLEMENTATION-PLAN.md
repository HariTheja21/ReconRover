# Phase 2.4: Hardware Abstraction Layer & Event Bridge Implementation Plan

## Goal Description
Build the complete Hardware Abstraction Layer (HAL) for the Recon Rover V2. This layer is the sole interface that communicates with the physical ESP32 via Serial. It isolates all hardware dependencies and communicates with the higher-level architecture strictly through the EventBus.

## Proposed Changes

### 1. Serial and Port Management (`core/hal/`)
[NEW] `serial_port_manager.py`: Scans and auto-connects to the appropriate ESP32 COM/TTY port.
[NEW] `serial_manager.py`: Central orchestrator for the physical layer. Initiates `serial_port_manager` and coordinates readers/writers.
[NEW] `serial_health.py`: Tracks raw serial-level health (connection drops, uptime).
[NEW] `serial_watchdog.py`: Enforces auto-reconnect logic and detects timeout hangs.
[NEW] `serial_statistics.py`: Low-level physical byte statistics (bytes in/out, error counts).

### 2. Packet Pipeline (`core/hal/`)
[NEW] `serial_packet_reader.py`: Async reading of the physical buffer. Uses a sliding window to search for `SYNC_BYTE_1` and `SYNC_BYTE_2` to align packets.
[NEW] `serial_packet_writer.py`: Non-blocking async queue to dispatch outgoing bytes to the serial port.
[NEW] `serial_packet_validator.py`: Handles CRC16 payload validation, packet length verification, and detects corruption or duplicate sequences before routing.

### 3. Event Bridge (`core/hal/`)
[NEW] `event_bridge.py`: Acts as the bi-directional gateway between the HAL and the EventBus.
- **Inbound (From ESP32):** Converts raw validated byte arrays from `serial_packet_reader` into `SerialPacketReceived` events (for consumption by the Phase 2.3 Telemetry Manager).
- **Outbound (To ESP32):** Listens to `OutgoingCommandPacket` on the EventBus, formats them via `telemetry_encoder`, and pushes them to `serial_packet_writer`.

### 4. Documentation
[NEW] `docs/Phase-2/PHASE-2.4-IMPLEMENTATION-PLAN.md` (This document)
[NEW] `docs/Phase-2/PHASE-2.4.md` (Final deliverables)
[MODIFY] `ENGINEERING-CHANGELOG.md` (Update log)

## Verification Plan
### Internal Tests
- Write a test script (`scratch/test_hal.py`) that uses a dummy/mock serial port.
- Push mocked raw bytes with invalid CRCs and verify `serial_packet_validator` drops them and publishes `PacketValidationFailed`.
- Push valid heartbeat bytes and verify `event_bridge` publishes `SerialPacketReceived`.
- Trigger a simulated timeout and ensure `serial_watchdog` initiates the auto-reconnect sequence.

## User Review Required
> [!NOTE]
> Since we do not have a physical ESP32 connected during development, I will use `pyserial` (or `serial_asyncio`) in the code but architect it to gracefully handle `serial.SerialException` (i.e. port not found). The internal tests will use a mocked serial transport stream to validate the sliding-window buffer alignment and CRC logic. Please approve the plan.
