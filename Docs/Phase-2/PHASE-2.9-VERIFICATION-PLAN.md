# Phase 2.9: Sensor & IMU Subsystem Bridge - Verification Plan

## 1. Verification Objectives
To perform a complete engineering verification of the Sensor & IMU Subsystem Bridge built in Phase 2.9. Ensure that the layer provides strict decoupling between raw binary telemetry from the hardware and semantic EventBus events for the higher-level autonomy/navigation nodes.

## 2. Audit Strategy
The audit will cover all 9 modules constructed in Phase 2.9:
- `SensorManager`
- `IMUManager`, `UltrasonicManager`, `LidarManager`, `BatteryManager`
- `SensorRouter`
- `SensorHealth`
- `SensorStatistics`
- EventBus Integration

We will mathematically verify struct unpacking boundaries, ConfigurationUpdated real-time cascading limits, and the correct emission of context-aware alerts (e.g. `ObstacleDetected` vs standard `DistanceUpdated`).

## 3. Runtime Test Matrix
- **IMU Decoding:** Inject raw `0x01` struct packets and assert that `IMUUpdated` fires precisely with scaled physical bounds applied.
- **Ultrasonic Obstacle Avoidance:** Inject `0x02` bytes reporting distance. Assert that crossing the `obstacle_threshold_cm` limit dynamically fires a `CRITICAL` `ObstacleDetected` event while still firing `DistanceUpdated`.
- **LiDAR Processing:** Inject `0x03` bytes indicating safe distance, verify only `DistanceUpdated` fires.
- **Battery Calculation:** Inject `0x04` bytes with raw analog voltage and verify standard mapping to 0-100% telemetry values and charging state.
- **Config Constraints:** Assert that setting new limits dynamically applies to the routers on-the-fly without requiring IO restarts.

## 4. PASS/FAIL Criteria
- **PASS:** Zero dependency violations, robust parsing of memory-safe `bytes`, configuration correctly overrides default physical thresholds, precise event publication.
- **FAIL:** Float precision loss causing runaway math, blocking/hanging threads during high-frequency throughput.

## 5. Risks
- Python `struct` unpack exceptions crashing the router if malformed bytes are injected (mitigated by strict length checks).

## 6. Expected Deliverables
- `PHASE-2.9-VERIFICATION-PLAN.md`
- `PHASE-2.9-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
