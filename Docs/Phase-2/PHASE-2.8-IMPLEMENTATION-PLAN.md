# Phase 2.8: Actuation Layer & Hardware Control Bridge - Implementation Plan

## Goal Description
Build the Actuation Layer & Hardware Control Bridge for Recon Rover V2. This layer is the strict translator between logical, validated commands (`OutgoingCommandPacket`) and the explicit hardware actuation requests (`MotorCommandRequest`, etc.). It acts as a safety bottleneck, enforcing hardware constraints stored centrally in the `ConfigurationManager` (such as maximum PWM, inverted polarity, and servo limits) before physical routing. No direct GPIO or Serial commands will be executed here; it purely routes abstracted requests via the EventBus for the HAL (Phase 2.4) to consume.

## Proposed Changes

### 1. Actuation Events (`core/actuation/`)
[NEW] `actuation_events.py`:
- Consumes: `OutgoingCommandPacket` (from Phase 2.5), `EmergencyStopActivated`, `ConfigurationUpdated`.
- Publishes: `MotorCommandRequest`, `ServoCommandRequest`, `OLEDCommandRequest`, `RGBCommandRequest`, `BuzzerCommandRequest`, `HardwareHealthUpdated`, `HardwareStatisticsUpdated`.

### 2. Hardware Controllers (`core/actuation/`)
[NEW] `motor_controller.py`: Reads motor polarity/limits from ConfigManager and applies transforms to PWM values.
[NEW] `servo_controller.py`: Constrains servo angles based on physical hardware limits from configuration.
[NEW] `oled_controller.py`: Manages display requests and brightness settings.
[NEW] `rgb_controller.py`: Formats RGB color arrays and brightness.
[NEW] `buzzer_controller.py`: Handles tone and duration requests.

### 3. Pipeline & Routing (`core/actuation/`)
[NEW] `hardware_router.py`: Parses the `command_id` and payload from an `OutgoingCommandPacket` and routes the request to the appropriate sub-controller.
[NEW] `actuation_manager.py`: Top-level orchestrator. Subscribes to the EventBus, handles configuration state fetching (via ConfigManager requests if needed, or by tracking `ConfigUpdated` events), and locks the router upon `EmergencyStopActivated`.

### 4. Telemetry (`core/actuation/`)
[NEW] `hardware_health.py`: Monitors the operational status of the controllers and broadcasts health summaries.
[NEW] `hardware_statistics.py`: Thread-safe tracking of actuation requests routed per second.

### 5. Documentation
[NEW] `docs/Phase-2/PHASE-2.8-IMPLEMENTATION-PLAN.md` (This file natively)
[NEW] `docs/Phase-2/PHASE-2.8.md`
[MODIFY] `ENGINEERING-CHANGELOG.md`

## Verification Plan
### Internal Tests
- Write `scratch/test_actuation.py`.
- Mock a `ConfigurationUpdated` event to load limits (e.g. `max_pwm = 200`, `left_motor_inverted = true`).
- Inject an `OutgoingCommandPacket` containing a drive command (e.g. `Left=255, Right=255`).
- Verify the router triggers the `motor_controller` which clamps `255 -> 200` and applies inversion (`-200, 200`), ultimately publishing a `MotorCommandRequest(-200, 200)`.
- Inject an `EmergencyStopActivated` event and verify subsequent packets are aggressively blocked by the `hardware_router`.

## User Review Required
> [!IMPORTANT]  
> Following the strict documentation policy, this custom plan is bypassing the deprecated artifacts. Once approved, I will implement all 10 modules in `core/actuation/` and prove full config-driven routing via an internal test script.
