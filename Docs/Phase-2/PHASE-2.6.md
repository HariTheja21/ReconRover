# Phase 2.6: Remote Control & Gamepad Bridge

## 1. Executive Summary
Phase 2.6 introduces the Input Abstraction Layer. This subsystem natively isolates raw, physical human input (such as joysticks and buttons) from the cognitive layer of the Recon Rover V2. By bridging OS-level hardware drivers to the semantic EventBus, we eliminate hard-coded robotic behaviors. Now, physical remote input dynamically triggers the exact same semantic `MoveIntent` or `EmergencyStopIntent` that an autonomous AI script would use.

## 2. Files Created
- `MAIN CODE/RASPBERRY_PI/core/input/input_events.py`
- `MAIN CODE/RASPBERRY_PI/core/input/input_validator.py`
- `MAIN CODE/RASPBERRY_PI/core/input/joystick_mapper.py`
- `MAIN CODE/RASPBERRY_PI/core/input/button_mapper.py`
- `MAIN CODE/RASPBERRY_PI/core/input/gamepad_manager.py`
- `MAIN CODE/RASPBERRY_PI/core/input/input_statistics.py`
- `MAIN CODE/RASPBERRY_PI/core/input/input_health.py`
- `MAIN CODE/RASPBERRY_PI/core/input/remote_manager.py`
- `scratch/test_input.py`
- `docs/Phase-2/PHASE-2.6-IMPLEMENTATION-PLAN.md`
- `docs/Phase-2/PHASE-2.6.md`

## 3. Files Modified
- `ENGINEERING-CHANGELOG.md`

## 4. Input Pipeline
1. **Raw Poll:** `GamepadManager` reads native OS HID events (e.g., Pygame joysticks).
2. **Normalize & Validate:** Inputs cascade to `InputValidator` to ensure axes do not miraculously exceed physics (e.g. -1.0 to 1.0).
3. **Map:** Valid events strike the `JoystickMapper` (which mathematically translates X/Y geometry into tank drive PWM) or the `ButtonMapper` (which statically maps button IDs to cognitive intents).
4. **Publish:** The final intent (e.g., `EmergencyStopIntent`) is pushed securely onto the internal `EventBus`.

## 5. Mapping Architecture
The mapping layer isolates physical layouts from internal operations. If we switch from an Xbox controller to a generic RC controller, we only change the dictionary inside `ButtonMapper`. The `JoystickMapper` successfully incorporates dead-zone filtering so that joystick hardware drifting does not translate into autonomous `MoveIntent` micro-stutters. Furthermore, caching identical frames prevents spamming the EventBus with `MoveIntent(0,0)` continuously.

## 6. EventBus Integration
- **Consumes (from HW driver):** Raw callbacks for axes and buttons.
- **Publishes (to cognitive layer):** `MoveIntent`, `ModeChangeIntent`, `EmergencyStopIntent`, `InputHealthUpdated`.

## 7. Internal Tests
A full `asyncio` test suite verified:
- Correct application of a 0.15 deadzone resulting in no events published.
- Valid maximum forward bounds natively mapped to `MoveIntent(255, 255)`.
- Valid hard left bounds mapped to `MoveIntent(-255, 255)`.
- Button 7 safely mapped and broadcasted as `EmergencyStopIntent`.
- Button 3 mapped to `ModeChangeIntent(1)`.

## 8. Memory Analysis
Intents are dynamically generated and instantly passed to the EventBus. If the mapped parameters have not fundamentally changed from the previous poll frame (e.g. holding a joystick completely still), no object is instantiated and no Event is pushed, drastically saving memory.

## 9. CPU Analysis
The `RemoteManager` utilizes `asyncio.sleep(0.02)` enabling a fixed 50Hz polling loop. It sits identically within the EventBus thread layout without occupying locking resources or blocking I/O bound pipelines.

## 10. Production Readiness
The Input Abstraction Layer is successfully verified. Physical hardware inputs can now fluidly drive the system through cognitive intents. Ready for Phase 2.7.
