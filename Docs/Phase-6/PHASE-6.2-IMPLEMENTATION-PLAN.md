# Phase 6.2: Browser Remote Teleoperation - Implementation Plan

## Executive Summary
Phase 6.2 implements the bidirectional control loop, allowing the operator to command the physical robot directly from the browser. It introduces the `ControlManager` backend to rigorously validate, rate-limit, and safely route incoming WebSocket commands to the internal `EventBus`. On the frontend, it provides a unified `teleoperation.js` architecture supporting Keyboard, Gamepad, and Virtual Joystick inputs. 

## Objectives
- Implement Backend `CommandRouter` and `InputValidator` to ensure malformed or dangerous commands (e.g., `speed = 5000`) never reach the physical hardware.
- Implement Backend `RateLimiter` to prevent the browser from overwhelming the 115200 baud UART link with high-frequency joystick polling.
- Implement Frontend `KeyboardController`, `GamepadController`, and `VirtualJoystick` to capture diverse operator input methods.
- Implement Frontend `ControlStateManager` to ensure only one control methodology is active at a time to prevent input conflict.
- Implement critical safety interlocks: A hardware-level Emergency Stop bypass, and automatic disconnect halting.

## Architecture
- `WEB_UI/backend/command_router.py`: Validates and limits incoming commands before publishing to the `EventBus`.
- `WEB_UI/frontend/js/control_state_manager.js`: Handles mututally exclusive toggling between input devices.
- `WEB_UI/frontend/js/command_sender.js`: Packages UI intent into strictly formatted JSON payloads.

## Rate Limiting & Safety
The `RateLimiter` ensures that the browser cannot flood the backend with more than 20 commands per second. However, the `EMERGENCY_STOP` command is granted a hardcoded bypass, ensuring it jumps the queue and executes instantly regardless of the rate limit. 
If the active controlling WebSocket disconnects (e.g., the tablet loses Wi-Fi), the `ControlManager` catches the exception and immediately injects an `EmergencyStopEvent` into the EventBus, preventing a runaway rover scenario.
