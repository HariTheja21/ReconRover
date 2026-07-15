# Phase 4.4: ESP32 Runtime Core & Command Dispatcher - Implementation Plan

## Executive Summary
Phase 4.4 transitions development from the central Raspberry Pi orchestrator into the ESP32 firmware domain. The goal of this phase is to establish a robust, C++17 FreeRTOS-compatible Runtime Core. This core is responsible for receiving serial UART data, extracting `0xAA55` payloads, validating their integrity, and routing validated commands to the physical hardware execution tasks via an abstract Event Dispatcher. No actual motor or sensor hardware drivers will be instantiated in this phase.

## Objectives
- Implement `PacketReceiver` to manage a ring buffer of raw incoming UART streams, mitigating fragmentation.
- Implement `PacketValidator` to check header bytes, verify CRC8 checksums, and silently reject duplicated packets (sequence tracking).
- Implement `CommandRouter` to decode the binary format and emit type-safe `RuntimeEvent` structs.
- Implement `CommandDispatcher` as an abstract interface, allowing future hardware tasks to subscribe to specific queues.
- Implement `RuntimeManager` as the top-level orchestration class, ready for invocation within a FreeRTOS `xTaskCreate` loop.

## Architecture
- `ESP32_ROVER/main/runtime/runtime_events.h`: Defines memory-aligned unions for hardware commands.
- `ESP32_ROVER/main/runtime/packet_receiver.cpp`: Circular buffer with sliding window frame extraction.
- `ESP32_ROVER/main/runtime/packet_validator.cpp`: Protocol integrity assertions.
- `ESP32_ROVER/main/runtime/command_router.cpp`: Protocol to C++ struct mapping.
- `ESP32_ROVER/main/runtime/runtime_manager.cpp`: Loop control and health monitoring.

## FreeRTOS Considerations
- **No Dynamic Allocation:** All buffers and queues are statically allocated `O(1)` memory. No `malloc` or `new` inside the runtime loop to guarantee immunity from heap fragmentation.
- **ISR Safety:** The architecture is designed such that the UART Interrupt Service Routine (ISR) only pushes bytes to the `RuntimeManager::OnUartData()`, while the main FreeRTOS task handles the `ProcessIncomingBytes()` decoding.
- **Deterministic Latency:** The `PacketReceiver` uses a fast circular buffer without memory shifting operations to extract frames, ensuring sub-millisecond dispatching.

## Event Dispatching Schema
- **MotorCommandEvent:** Extracted from Command ID `0x01`.
- **RuntimeHealthEvent:** Emitted periodically or upon UART timeout.

## Error Handling
1. **Invalid CRC:** Silently dropped, statistics incremented.
2. **Duplicated Sequence:** The system tracks the last known sequence ID. Exact repeats (common in noisy UART auto-resends) are dropped without dispatching to hardware.
3. **Buffer Exhaustion:** If junk data fills the buffer without a valid `0xAA55` header, the receiver drops a single byte and continues searching, preventing deadlock.
