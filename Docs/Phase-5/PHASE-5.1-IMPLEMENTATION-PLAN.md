# Phase 5.1: Real-World Hardware Integration & Calibration - Implementation Plan

## Executive Summary
Phase 5.1 focuses entirely on the physical hardware integration of Recon Rover V2. While previous phases built theoretically robust software, this phase grounds that software in the physical world. It implements the Linux device mapping (`udev` rules simulation) to guarantee the software always finds the correct hardware ports, and establishes a comprehensive calibration pipeline for the ESP32 (Motors, Servos, IMU, Battery) and the Raspberry Pi (Camera). The output of this layer is a reusable `recon_rover_calibration.json` profile.

## Objectives
- Implement `CalibrationManager` and `CalibrationEngine` to orchestrate a sequenced discovery and calibration routine.
- Implement `DeviceMapper` to define and simulate `udev` rules that map physical USB ports to static logical symlinks (`/dev/esp32`, `/dev/camera`, `/dev/lidar`).
- Implement independent calibrators (`SerialCalibrator`, `CameraCalibrator`, `ImuCalibrator`, `MotorCalibrator`, `ServoCalibrator`, `BatteryCalibrator`).
- Implement `SystemValidator` to ensure all calibrations passed before exporting the final profile.

## Architecture
- `MAIN CODE/RASPBERRY_PI/core/calibration/calibration_manager.py`: External API for triggering the routine.
- `MAIN CODE/RASPBERRY_PI/core/calibration/device_mapper.py`: Linux symlink management.
- `MAIN CODE/RASPBERRY_PI/core/calibration/*_calibrator.py`: Modular classes dedicated to testing individual hardware components.
- `MAIN CODE/RASPBERRY_PI/core/calibration/system_validator.py`: Profile compliance checker.

## Hardware Discovery via Udev
Without `udev` rules, Linux may arbitrarily assign `/dev/ttyUSB0` or `/dev/ttyUSB1` based on boot order. The `DeviceMapper` defines the static rules matching `idVendor` and `idProduct` so the Rover's software configuration can rely blindly on `/dev/esp32`.

## Calibration Workflow
1. **Device Mapping:** `DeviceMapper` confirms symlinks are active.
2. **Serial Ping:** `SerialCalibrator` verifies round-trip latency to the ESP32.
3. **Camera Init:** `CameraCalibrator` verifies the video4linux interface.
4. **IMU Bias:** `ImuCalibrator` measures stationary offsets for X/Y/Z.
5. **Motor Polarity:** `MotorCalibrator` validates wiring.
6. **Servo Centering:** `ServoCalibrator` validates PWM theoretical centers against physical linkages.
7. **Battery Scaling:** `BatteryCalibrator` generates ADC multipliers.
8. **Export:** Resulting data is dumped to `/tmp/recon_rover_calibration.json`.

## Error Handling
If any calibrator throws an exception (e.g., motor overcurrent, UART timeout, camera unreadable), the `CalibrationEngine` immediately halts, firing a `CalibrationFailedEvent` and rejecting the profile generation.
