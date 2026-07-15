# Phase 2.9: Sensor & IMU Subsystem Bridge - Implementation Plan

## Goal Description
Build the Sensor & IMU Subsystem Bridge for Recon Rover V2. This layer acts as the inbound equivalent to the Actuation Layer (Phase 2.8). It is responsible for intercepting raw `TelemetryPacket` bytes from the Hardware Abstraction Layer (HAL) and dynamically unpacking, scaling, and publishing them as high-level, semantic `EventBus` events (e.g., `IMUUpdated`, `ObstacleDetected`, `BatteryUpdated`). 

This architecture maintains strict isolation: NO SLAM, AI, or decision-making occurs here. It is purely an abstraction mechanism designed to convert structured C-style bytes into Pythonic, application-ready events.

## Proposed Changes

### 1. Sensor Events (`core/sensors/`)
[NEW] `sensor_events.py`:
- Consumes: `TelemetryPacket` (raw bytes from HAL) and `ConfigurationUpdated`.
- Publishes: `IMUUpdated`, `OrientationUpdated`, `AccelerationUpdated`, `GyroscopeUpdated`, `ObstacleDetected`, `DistanceUpdated`, `BatteryUpdated`, `SensorHealthUpdated`, `SensorStatisticsUpdated`.

### 2. Sensor Managers (`core/sensors/`)
[NEW] `imu_manager.py`: Unpacks MPU6050 packets (Acceleration/Gyro/Orientation), applies configurable offsets, and publishes `IMUUpdated`/`OrientationUpdated`.
[NEW] `ultrasonic_manager.py`: Unpacks HC-SR04 ping responses, tracks time-of-flight distances, and publishes `DistanceUpdated` or `ObstacleDetected` based on configurable thresholds.
[NEW] `lidar_manager.py`: Unpacks VL53L0X time-of-flight payloads, providing high-accuracy mm distance reporting.
[NEW] `battery_manager.py`: Unpacks ADC voltages and maps them to standard battery percentage/health metrics.

### 3. Pipeline & Routing (`core/sensors/`)
[NEW] `sensor_router.py`: Inspects the `TelemetryPacket.sensor_id` (or similar packet type byte) and routes the binary payload to the correct downstream manager (IMU, Ultrasonic, Lidar, Battery). Rejects malformed or incomplete packets safely.
[NEW] `sensor_manager.py`: The top-level orchestrator. Subscribes to the EventBus for `TelemetryPacket` and `ConfigurationUpdated` events, manages the router, and controls lifecycle state.

### 4. Telemetry & Health (`core/sensors/`)
[NEW] `sensor_health.py`: Continuously evaluates the data rate of sensors. If a sensor goes dark (no packets for X seconds), it updates the system health flags.
[NEW] `sensor_statistics.py`: Thread-safe tracking of packets decoded per second.

### 5. Documentation
[NEW] `docs/Phase-2/PHASE-2.9-IMPLEMENTATION-PLAN.md` (This file natively)
[NEW] `docs/Phase-2/PHASE-2.9.md`
[MODIFY] `ENGINEERING-CHANGELOG.md`

## Verification Plan
### Internal Tests
- Write `scratch/test_sensors.py`.
- Mock a `ConfigurationUpdated` event to load limits (e.g. `ultrasonic_obstacle_threshold_cm = 15`).
- Inject raw `TelemetryPacket` bytes corresponding to IMU data (`[AccX, AccY, AccZ, Gyro...]`) and ensure an `IMUUpdated` event is precisely fired with floating point translations.
- Inject raw `TelemetryPacket` bytes for Ultrasonic data indicating `10cm`. Verify that BOTH `DistanceUpdated` and `ObstacleDetected` events fire.
- Verify `SensorStatistics` gracefully tracks thousands of simulated high-frequency inbound telemetry frames per second.

## User Review Required
> [!IMPORTANT]  
> Following the strict documentation policy, this custom plan is bypassing the deprecated artifacts. Once approved, I will implement all 9 modules in `core/sensors/` and verify structural routing with a dedicated test script before generating the final implementation report.
