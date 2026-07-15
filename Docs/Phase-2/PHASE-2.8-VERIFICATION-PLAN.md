# Phase 2.8: Actuation Layer & Hardware Control Bridge - Verification Plan

## 1. Verification Objectives
To perform a complete engineering verification of the Actuation Layer & Hardware Control Bridge built in Phase 2.8. Ensure that the layer provides strict decoupling between cognitive commands and raw hardware execution via robust configuration-driven clamping and parsing.

## 2. Audit Strategy
The audit will cover all 10 modules constructed in Phase 2.8:
- `ActuationManager`
- `MotorController`, `ServoController`, `OLEDController`, `RGBController`, `BuzzerController`
- `HardwareRouter`
- `HardwareHealth`
- `HardwareStatistics`
- EventBus Integration

We will mathematically verify struct unpacking boundaries, ConfigurationUpdated real-time cascading limits, and EmergencyStopActivated lockout mechanisms.

## 3. Runtime Test Matrix
- **Motor Decoding:** Assert that an `OutgoingCommandPacket` with `0x10` and `Left=255, Right=255` correctly unpacks to `MotorCommandRequest(255, 255)`.
- **Config Constraints:** Assert that setting `max_pwm=150` clamps outbound requests to `150`. Assert `invert_left=True` forces `-150`.
- **Servo Decoding:** Assert that `0x20` parses `servo_id` and `angle`.
- **RGB Decoding:** Assert that `0x50` unpacks four 8-bit bytes seamlessly into R, G, B, Brightness.
- **E-Stop Safety Loop:** Assert that `EmergencyStopActivated` fires an instant 0 PWM command and drops all subsequent `OutgoingCommandPacket` events.

## 4. PASS/FAIL Criteria
- **PASS:** Zero dependency violations, robust parsing of memory-safe `bytes`, configuration correctly clamps physical limits, E-Stop permanently locks the router.
- **FAIL:** Memory leaks on byte unpacking, failure to apply config updates asynchronously, thread-locking during high-frequency throughput.

## 5. Risks
- Python `struct` unpack exceptions crashing the router if malformed bytes are injected (partially mitigated by length checks).
- `HardwareStatistics` lock contention if commands exceed 10,000/sec (mitigated by `RLock` and 1-second interval smoothing).

## 6. Expected Deliverables
- `PHASE-2.8-VERIFICATION-PLAN.md`
- `PHASE-2.8-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
