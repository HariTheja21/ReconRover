# Phase 2.6: Remote Control & Gamepad Bridge - Implementation Plan

## Goal Description
Build the Remote Control & Gamepad Bridge for the Recon Rover V2. This layer serves as the universal input abstraction layer. It will ingest raw human input (from physical remotes, future USB gamepads, keyboards, etc.), normalize the signals (including dead-zone filtering), map them to semantic intents, and publish those intents to the EventBus. It strictly isolates hardware input devices from the command layer.

## Proposed Changes

### 1. Input Events (`core/input/`)
[NEW] `input_events.py`:
- Defines raw input events: `RawJoystickMoved`, `RawButtonPressed`.
- Imports and re-uses semantic intents from Phase 2.5 (`MoveIntent`, `StopIntent`, etc.), plus adds any new semantic intents required (`TurnIntent`, `SpeedIntent`, `MenuNavigationIntent`).

### 2. Normalization & Validation (`core/input/`)
[NEW] `joystick_mapper.py`: Translates raw joystick axes (-1.0 to 1.0) into proper PWM ranges (-255 to 255), applying dead-zone filtering and scaling curves (linear or exponential) for precise control.
[NEW] `button_mapper.py`: Maps physical button codes (e.g., Button 0, Button 1) to semantic actions (e.g., Mode Switch, Servo Action, E-Stop).
[NEW] `input_validator.py`: Ensures raw inputs are within physically possible bounds before mapping prevents corrupt input signals from cascading.

### 3. Managers & Input Handlers (`core/input/`)
[NEW] `gamepad_manager.py`: Connects to standard OS-level gamepads (e.g., `pygame.joystick` or similar generic USB HID polling).
[NEW] `remote_manager.py`: Acts as the orchestrator. Subscribes to raw input events, routes them through the mappers and validators, and publishes the final `*Intent` objects onto the EventBus.

### 4. Health & Statistics (`core/input/`)
[NEW] `input_statistics.py`: Thread-safe tracking of total inputs processed, dropped (in dead-zone), and mapped.
[NEW] `input_health.py`: Evaluates the gamepad/remote connection status and publishes health updates periodically.

### 5. Documentation
[NEW] `docs/Phase-2/PHASE-2.6-IMPLEMENTATION-PLAN.md` (This document)
[NEW] `docs/Phase-2/PHASE-2.6.md`
[MODIFY] `ENGINEERING-CHANGELOG.md`

## Verification Plan
### Internal Tests
- Write a mock script (`scratch/test_input.py`).
- Simulate a raw joystick movement inside the dead-zone and verify `MoveIntent` is **not** published.
- Simulate a raw joystick movement at max forward (1.0) and verify a `MoveIntent(left=255, right=255)` is published.
- Simulate an emergency button press and verify `EmergencyStopIntent` is published immediately.

## User Review Required
> [!NOTE]
> Per the mandatory documentation policy, I have strictly avoided using the default `implementation_plan.md` artifact. This plan serves as the official blueprint. Since we don't have physical hardware, `gamepad_manager.py` will be structured dynamically to optionally use a standard library like `pygame` or `inputs`, but will fail gracefully if no physical controller is attached. Please approve this plan to begin execution.
