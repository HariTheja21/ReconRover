# Phase 4.3: Serial Transport Layer - Verification Plan

## Executive Summary
This document defines the verification parameters for Phase 4.3 (Serial Transport Layer). The goal is to conclusively verify that the Raspberry Pi can manage physical UART connections without blocking, properly frame incoming byte streams despite fragmentation, and successfully transmit serialized commands to downstream microcontrollers.

## Verification Objectives
- Validate the $50$Hz asynchronous transmission loop inside `SerialTransportManager`.
- Ensure `SerialPort` handles connection drops safely without crashing the Python interpreter.
- Verify `PacketSender` properly caps queue sizes and forces `HardwareStopPacket` to the front of the queue.
- Prove `PacketReceiver` and `PacketFramer` can ingest fragmented byte streams and reassemble 9-byte payloads aligned to the `0xAA55` header.
- Confirm seamless EventBus integration for both Tx and Rx paths.

## Verification Scope
The scope is constrained to the `core/serial_transport/` package. It verifies logic against a mocked internal loopback adapter. Validating physical electrical characteristics (e.g., UART noise, baud rate drift on actual hardware) is outside the scope of software verification and will occur during Phase 5 (Hardware Bringup).

## Audit Strategy
1. **Architecture Audit:** Ensure strict isolation of hardware-specific `pyserial` dependencies inside the Engine/Port classes.
2. **Dynamic Testing:** Flood the transport layer with partial byte chunks and verify flawless reassembly.
3. **Fault Injection:** Force connection drops to verify the automatic 1.0s backoff and recovery cycle.

## Architecture Audit
- Verify the `queue.Queue` handles multi-threaded race conditions between EventBus injection and the asyncio reading loop.

## Runtime Audit
- Assert the engine maintains a stable $50$Hz cycle.

## Memory Audit
- Verify that `PacketBuffer` and `PacketSender` apply strict limits (4096 bytes and 100 packets, respectively) to prevent OOM errors on dead links.

## CPU Audit
- Profile the `pyserial` `read(in_waiting)` call to ensure the zero-timeout configuration behaves entirely non-blocking.

## Thread Safety Audit
- Validate `threading.RLock()` across all stateful buffers (Buffer, Stats, Sender).

## Async Safety Audit
- Ensure that the primary transport loop uses `asyncio.sleep()` correctly to yield control to the broader system.

## Internal Test Matrix
1. **Auto-Connect:** Spin up manager, verify `SerialConnected` event.
2. **Loopback Transmit:** Send an artificial `HardwareCommandPacket`, assert a perfectly matching `SerialPacketReceived` event is generated.
3. **Queue Override:** Flood the queue with velocity commands. Inject an E-Stop. Assert the E-Stop is the very next packet dequeued and transmitted.
4. **Fragmented Framing:** Feed `\xAA`, wait, then feed `\x55\x01\x05...`. Assert the framer holds state and reconstructs the packet perfectly.
5. **Disconnect/Reconnect:** Force close the mock port. Assert `SerialDisconnected`. Wait 1.2s. Assert `SerialConnected`.

## PASS / FAIL Criteria
- **PASS:** 100% test matrix success. Stable memory profile. Instantaneous E-Stop processing.
- **FAIL:** Buffer leaks, blocking IO calls freezing the event loop, or dropped packets under nominal conditions.

## Expected Deliverables
- `PHASE-4.3-VERIFICATION-PLAN.md`
- `PHASE-4.3-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
