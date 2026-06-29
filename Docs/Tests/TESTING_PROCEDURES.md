# Recon Rover V1 — Testing Procedures

**Document Version:** 1.0  
**Status:** Frozen Specification  
**Last Updated:** 2026-06-28  

This document outlines the testing strategy for Recon Rover V1, ensuring that both the Cognitive Layer (Raspberry Pi) and Reactive Layer (ESP32-S3) function independently before full system integration.

## 1. Hardware Bench Testing

Before any firmware is deployed to the assembled rover, individual subsystems must be verified on the bench.
* **Power:** Verify 5V Buck Converters output stable 5.0V-5.2V before connecting the Pi or ESP32.
* **I2C Bus:** Flash an I2C scanner sketch to the ESP32 to verify that the PCA9548A responds at `0x70` and that all routed sensors respond on their assigned channels.
* **Motors:** Apply a temporary 3V source to each L298N output to verify wheel rotation direction matches `HARDWARE_ARCHITECTURE.md` conventions.

## 2. Firmware (ESP32-S3) Testing

* **Serial Telemetry Mock:** Without the Pi connected, connect the ESP32 to a PC via USB. Open a serial monitor (115200 or 921600 baud). Verify that the `ready` packet is sent on boot, followed by `telemetry` JSON packets at 20 Hz.
* **Actuator Injection:** Send manual JSON `cmd` packets via the serial monitor (e.g., `{"proto":1,"type":"cmd","ts":0,"seq":1,"motors":{"fl":50,"fr":50,"rl":50,"rr":50}}`) and verify motor spin.
* **Fault Injection:** Manually disconnect a sensor (e.g., MPU6050) and verify that the `health` block in the telemetry reflects the failure and a `fault` packet is transmitted.

## 3. Software (Raspberry Pi) Testing

* **Hardware-In-The-Loop Mocking:** Connect the Pi to a mock ESP32 or PC script that emits dummy telemetry JSON packets over serial.
* **Vision Pipeline:** Run the vision pipeline standalone with the webcam. Verify object detection framerates and bounding box outputs without requiring motor movement.
* **Integration Tests:** Use `pytest` to validate internal logic (e.g., the `motion_planner.py` translates an AVOID directive into the correct motor outputs).

## 4. Full System Integration

1. **Safety Block:** Place the rover on a block so wheels can spin freely.
2. **Boot Sequence:** Power on. Verify Pi boots, ESP32 transmits `ready`, and Pi transitions from IDLE to PATROL (if commanded).
3. **Sensor Fusion:** Move objects in front of the HC-SR04 and VL53L0X sensors. Observe the dashboard to verify the `world_model` updates accurately.
4. **Closed Loop Check:** Allow the AI Engine to generate motor commands based on the sensor fusion data. Verify the wheels spin in the correct direction to avoid the obstacle.
