# Phase 4.7: ESP32 UART Integration Layer - Verification Plan

## Executive Summary
This document outlines the verification strategy for Phase 4.7 (ESP32 UART Integration Layer). The objective is to rigorously verify that the C++17 UART pipeline correctly routes incoming bytes into valid Command Packets and routes outgoing Telemetry Packets into bytes without invoking dynamic memory allocation, and while maintaining strict $O(1)$ constant-time execution suitable for FreeRTOS ISRs.

## Verification Objectives
- Validate the $O(1)$ static ring buffer `UartBuffer` correctly wraps pointers via modulo arithmetic and prevents buffer overflow data corruption.
- Ensure the `UartReceiver` state machine recovers from misaligned bytes or corrupted headers without hard resets.
- Verify `UartTransmitter` cleanly buffers outgoing payload data until the RTOS tick is ready to push it to hardware.
- Prove that the `UartManager` architecture correctly separates ISR contexts from task contexts via the callback system.
- Confirm zero dynamic allocation across the entire UART stack.

## Verification Scope
The scope encompasses the `ESP32_ROVER/main/uart/` subsystem. Hardware DMA/FIFO behavior is evaluated architecturally, while logical verification relies on the internal emulator test suite.

## Audit Strategy
1. **Static Architecture Analysis:** Audit C++ templates and arrays to guarantee no heap usage.
2. **Logic Emulation:** Utilize the `test_uart.cpp` internal test suite to emulate FreeRTOS ticks, RX byte injections, and TX byte extractions.
3. **Protocol Resilience:** Intentionally inject framing errors to verify the state machine resets cleanly and catches the next valid packet.

## FreeRTOS Audit
- Ensure that the injected callbacks (used for crossing from UART ISR to Runtime Core) execute non-blocking operations.
- Verify DMA compatibility by asserting that TX chunking (`TickTx`) limits the maximum bytes pushed per cycle, avoiding blocking calls inside `uart_write_bytes`.

## Runtime Audit
- Verify the `UartReceiver` executes $O(1)$ boolean logic per byte received.

## Memory Audit
- Verify that `UartBuffer<256>` allocates exactly 256 bytes plus 6 bytes of structural pointers, avoiding `std::vector` overhead.

## Internal Test Matrix
1. **Packet Framing:** Inject exactly 9 valid bytes, assert 1 complete packet is generated via callback.
2. **Queue Saturation:** Push 256 bytes to TX buffer, assert successful queueing. Push 1 more byte, assert it is gracefully rejected (buffer overflow caught).
3. **Queue Flushing:** Call the tick function, assert exactly the expected chunk of bytes is flushed to the physical layer.
4. **Framing Recovery:** Inject `0xAA`, `0x00`, then a full valid 9-byte packet. Assert the initial false header is dropped and exactly 1 valid packet is generated.

## PASS / FAIL Criteria
- **PASS:** 100% test success, zero heap allocation, sub-microsecond state machine parsing, flawless error recovery.
- **FAIL:** Dynamic memory allocations, buffer overrun memory corruption, or stalling FreeRTOS tasks.

## Expected Deliverables
- `PHASE-4.7-VERIFICATION-PLAN.md`
- `PHASE-4.7-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
