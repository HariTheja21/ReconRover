# Phase 4.2: Hardware Execution Bridge - Implementation Plan

## Executive Summary
Phase 4.2 institutes the final software layer of the Raspberry Pi stack: The Hardware Execution Bridge. This module encapsulates all low-level communication packet construction. It translates normalized kinematic output into protocol-compliant binary structures, guaranteeing that any downstream microcontrollers (e.g., ESP32) receive validated, sequenced, and checksum-verified payloads.

## Objectives
- Deploy a `HardwareBridgeManager` running at a 20Hz polling interval to ingest `WheelVelocityRequest` events.
- Implement a `CommandEncoder` to scale $[-1.0, 1.0]$ floating-point constraints into $[-32767, 32767]$ 16-bit signed integer representations.
- Implement a `PacketBuilder` to pack the binary structure, append sequence numbers, and compute standard XOR CRC8 signatures.
- Emit finalized `HardwareCommandPacket` events containing literal byte arrays for transmission.

## Architecture
- `hardware_bridge_manager.py`: Core asynchronous orchestration layer.
- `hardware_bridge_engine.py`: Encapsulates encoding and validation logic.
- `packet_validator.py`: Asserts structural boundaries before serialization.
- `command_encoder.py`: Floating-point mapping algorithms.
- `packet_builder.py`: Python `struct` manipulation mapping to the `SHARED` protocol spec.

## SHARED Protocol Specification Compliance
**Format:** `[HEADER_1] [HEADER_2] [CMD_TYPE] [SEQ_NUM] [LEFT_H] [LEFT_L] [RIGHT_H] [RIGHT_L] [CRC8]`
**Byte Count:** 9 bytes total.
- `HEADER`: `0xAA 0x55`
- `CMD_TYPE`: `0x01` (Velocity Command)
- `SEQ_NUM`: 8-bit wrap-around unsigned integer.
- `PAYLOAD`: Dual 16-bit signed integers (Big-Endian).

## EventBus Integration
**Consumes:** `WheelVelocityRequest`, `MotionStopped`, `EmergencyStopRequired`
**Publishes:** `HardwareCommandPacket`, `HardwareStopPacket`, `HardwareBridgeUpdated`, `HardwareBridgeHealthUpdated`

## Emergency Overrides
Unlike standard velocity requests which await the 20Hz timing loop, an `EmergencyStopRequired` event instantly overrides the engine. It forces immediate generation of a $0.0, 0.0$ `HardwareStopPacket`, entirely bypassing the queue to ensure zero communication latency during hardware failures.
