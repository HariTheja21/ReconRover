# Phase 2.5: Command Builder & Protocol Encoding Implementation Plan

## Goal Description
Build the complete outbound command pipeline for Recon Rover V2. The Command Builder will act as the single source of truth for all outbound logic, converting high-level cognitive intents (e.g., `MoveIntent`) into validated protocol packets. It integrates cleanly with the EventBus, validates against the central `StateManager`, and uses an internal priority queue before routing commands down to the Hardware Abstraction Layer (HAL).

## Proposed Changes

### 1. Events Definitions
[NEW] `core/command/command_events.py`
- Define incoming intent dataclasses: `MoveIntent`, `StopIntent`, `ServoIntent`, `ModeChangeIntent`, `MissionChangeIntent`, `EmergencyStopIntent`.
- Define outbound notification dataclasses: `OutgoingCommandPacket`, `CommandValidated`, `CommandRejected`, `CommandQueued`, `CommandSent`, `CommandStatisticsUpdated`.

### 2. Validation & Encoding (`core/command/`)
[NEW] `command_validator.py`: A stateless engine that queries the `StateManager` (from Phase 2.2) to ensure commands are legal (e.g., rejecting `MoveIntent` if the `SafetyState` is `EMERGENCY_STOP` or if we are in `STANDBY` mode).
[NEW] `command_encoder.py`: Responsible for packaging the validated intent into the Shared Command Packet structure (e.g., `MotionCommand` from `SHARED/python/packets.py`) and serializing it to binary.

### 3. Queuing & Scheduling (`core/command/`)
[NEW] `command_queue.py`: An `asyncio.PriorityQueue` wrapping incoming packets, prioritizing `CRITICAL` (E-Stops), `HIGH` (Motion), `NORMAL` (State changes), and `LOW` (Pings).
[NEW] `command_scheduler.py`: A background asyncio task that pulls from `command_queue`, applies rate-limiting if necessary, and ultimately publishes `OutgoingCommandPacket` to the EventBus.

### 4. Orchestration & Health (`core/command/`)
[NEW] `command_health.py` & `command_statistics.py`: Thread-safe tracking of total commands processed, rejected, and sent.
[NEW] `command_builder.py`: The central manager that subscribes to all `*Intent` events, runs them through the `command_validator`, drops them into the `command_queue`, and owns the scheduler lifecycle.

### 5. Documentation
[NEW] `docs/Phase-2/PHASE-2.5-IMPLEMENTATION-PLAN.md` (This document)
[NEW] `docs/Phase-2/PHASE-2.5.md` (Final deliverables)
[MODIFY] `ENGINEERING-CHANGELOG.md` (Update log)

## Verification Plan
### Internal Tests
- Write a script (`scratch/test_commands.py`) to simulate `MoveIntent`.
- Test validation behavior: verify `MoveIntent` is rejected when the `StateManager` is mocked to be in `EMERGENCY_STOP`.
- Test priority queuing: Enqueue a `LOW` priority intent, then a `CRITICAL` intent, and ensure the scheduler emits the `CRITICAL` intent first via the EventBus.

## User Review Required
> [!NOTE]
> The prompt implies moving encoding logic out of the telemetry layer and into the Command Builder layer. I will create `command_encoder.py` to handle the final translation of Python intent objects to binary bytes, which perfectly bridges the cognitive domain to the HAL's EventBridge. Please approve to proceed.
