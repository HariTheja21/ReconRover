# Phase 6.2: Browser Remote Teleoperation - Verification Plan

## Executive Summary
This document outlines the verification strategy for Phase 6.2 (Browser Remote Teleoperation). The goal is to audit the bidirectional control pipeline, ensuring that human operator intent captured in the browser is securely validated, rate-limited, and routed to the robot's physical hardware via the EventBus without compromising safety or system stability.

## Verification Objectives
- Validate the `CommandRouter` and `InputValidator` aggressively reject malformed, out-of-bounds, or unauthorized WebSocket payloads.
- Ensure the `RateLimiter` enforces the 20Hz cap to prevent UART buffer overruns.
- Prove the Frontend `ControlStateManager` properly enforces mutual exclusivity between Keyboard, Gamepad, and Virtual Joystick input modes.
- Verify the Hardware `EMERGENCY_STOP` bypasses all queues and ownership checks.
- Confirm the automatic Deadman Switch triggers an E-Stop if the active WebSocket connection drops.

## Verification Scope
The scope encompasses the `WEB_UI/backend/` control logic (`control_manager.py`, `command_router.py`, etc.) and the `WEB_UI/frontend/js/` input controllers. It verifies the upward command flow from the operator's input device to the `OperatorCommandEvent`.

## Audit Strategy
1. **Security Audit:** Inject malformed JSON commands (e.g., `throttle: 500`, `command: "EXPLODE"`) into the `CommandRouter` and verify they are dropped.
2. **Safety Audit:** Simulate an active control session, then forcefully drop the client connection. Verify the `EmergencyStopEvent` is emitted to the EventBus.
3. **Concurrency Emulation:** Emulate two users attempting to drive simultaneously. Verify `active_controller_id` locks out the second user.

## Runtime Audit
- Verify the backend `ControlManager` does not block the main AsyncIO loop while parsing incoming JSON strings.

## Memory Audit
- Confirm that disconnected clients are fully expunged from the `ControlManager`'s tracking structures to prevent memory leaks over time.

## Internal Test Matrix
1. **Keyboard/Gamepad Integration:** Verify WS payload format matches the schema expected by `InputValidator`.
2. **Rate Limiting:** Fire 100 commands instantly; verify exactly 20 are routed and 80 are dropped.
3. **Emergency Stop Bypass:** Verify E-Stop routes instantly even if the rate limit is currently exhausted.

## PASS / FAIL Criteria
- **PASS:** 100% test success, strict ownership enforcement, immediate E-Stop on disconnect, zero memory leaks.
- **FAIL:** Unvalidated inputs reaching the EventBus, missing Deadman Switch, multiple clients driving simultaneously.

## Expected Deliverables
- `PHASE-6.2-VERIFICATION-PLAN.md`
- `PHASE-6.2-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
