# Phase 4.4: ESP32 Runtime Core & Command Dispatcher - Verification Plan

## Executive Summary
This document outlines the verification strategy for Phase 4.4 (ESP32 Runtime Core & Command Dispatcher). The objective is to rigorously prove that the C++17 foundation correctly identifies, parses, validates, and dispatches incoming physical byte streams while remaining strictly compliant with FreeRTOS memory constraints.

## Verification Objectives
- Validate the `PacketReceiver` correctly buffers and extracts 9-byte frames without memory shifting overhead.
- Ensure the `PacketValidator` correctly implements the matching CRC8 XOR algorithm and blocks corrupted payloads.
- Verify that `PacketValidator` effectively rejects duplicate sequences to prevent mechanical stutter from serial retries.
- Prove that `CommandRouter` correctly maps Big-Endian bytes into `MotorCommandEvent` payloads.
- Confirm that the `RuntimeManager` handles byte ingestion in an ISR-safe manner.

## Verification Scope
The scope is constrained to the `ESP32_ROVER/main/runtime/` package. FreeRTOS specific integration (like creating the actual queues and tasks) is deferred to Phase 4.5. 

## Audit Strategy
1. **Static Analysis:** Examine the C++ code to guarantee $O(1)$ dynamic memory allocations (no `new` or `malloc`).
2. **Structural Audit:** Ensure type safety using C++ structs for event payloads instead of raw byte pointers.
3. **Logic Emulation:** Run the internal test suite to emulate UART injection.

## Architecture Audit
- Verify the abstract boundary of `CommandDispatcher`, ensuring hardware drivers will not be tightly coupled to the parsing logic.

## FreeRTOS Audit
- Assert that no blocking IO calls exist within the packet processing loop.

## Runtime Audit
- Assert that processing a single packet takes bounded, constant time $O(1)$.

## Memory Audit
- Verify the `PacketReceiver` circular buffer strictly operates within its 256-byte static limit, dropping bytes properly when exhausted.

## CPU Audit
- Profile the sliding-window buffer logic. Assert that `Peek()` operations are mathematically inexpensive modulo divisions.

## Internal Test Matrix
1. **Valid Packet:** Inject perfectly structured bytes. Assert `MotorCommandEvent` fires with exact values.
2. **Invalid CRC:** Flip a single bit in the payload. Assert silent rejection.
3. **Duplicate Sequence:** Send identical sequence numbers consecutively. Assert the second is dropped.
4. **Fragmented Stream:** Feed bytes byte-by-byte. Assert it still fires exactly one event when the 9th byte arrives.
5. **Health Timeout:** Starve the manager for >1000ms. Assert `IsHealthy()` goes false.

## PASS / FAIL Criteria
- **PASS:** 100% test success, zero heap allocation, constant-time processing.
- **FAIL:** Logic blocking, pointer mismanagement, heap usage, or invalid endian conversion.

## Expected Deliverables
- `PHASE-4.4-VERIFICATION-PLAN.md`
- `PHASE-4.4-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
