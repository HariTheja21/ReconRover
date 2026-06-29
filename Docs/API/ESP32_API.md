# Recon Rover V1 — ESP32-S3 Internal API & Modules

**Document Version:** 1.0  
**Status:** Frozen Specification  
**Last Updated:** 2026-06-28  

This document outlines the internal firmware interfaces (Layer 3) for the ESP32-S3. All modules communicate strictly via FreeRTOS queues and event groups, enforcing a decoupled, reactive architecture.

## 1. Module Overview

| Module / Task | Core | Priority | Responsibility |
|---------------|------|----------|----------------|
| `watchdog` | 0 | 5 (CRITICAL) | Monitors task heartbeats; triggers safe mode on hang |
| `sensor_manager` | 0 | 4 (HIGH) | Polls HC-SR04, I2C sensors, MQ-2. Pushes to Sensor Queue |
| `motor_controller` | 1 | 4 (HIGH) | Subscribes to Motor Queue. Sets L298N PWM and direction |
| `serial_handler` | 1 | 4 (HIGH) | Handles USB CDC RX/TX. Enqueues to Command Queue |
| `telemetry_builder` | 0 | 3 (NORMAL) | Reads Sensor Queue, packs JSON, pushes to TX Queue |
| `command_parser` | 1 | 3 (NORMAL) | Parses JSON from Command Queue, dispatches to Actuator Queues |
| `servo_controller` | 1 | 3 (NORMAL) | Subscribes to Servo Queue. Sets SG90 PWM |
| `oled_renderer` | 1 | 2 (LOW) | Subscribes to Eye Queue. Draws bitmaps to SSD1306 |
| `led_controller` | 1 | 2 (LOW) | Subscribes to LED Queue. Animates WS2812B |
| `health_monitor` | 0 | 2 (LOW) | Evaluates sensor flags. Pushes to Fault Queue if error |
| `fault_manager` | Any | 3 (NORMAL)| Reads Fault Queue, triggers safe mode, queues fault packets |

## 2. Inter-Task Queue Specifications

### `Sensor Queue`
* **Producer:** `sensor_manager`
* **Consumer:** `telemetry_builder`
* **Payload:** `sensor_data_t` struct (contains distances, IMU floats, gas raw, health flags).

### `Command Queue`
* **Producer:** `serial_handler`
* **Consumer:** `command_parser`
* **Payload:** `raw_packet_t` (Null-terminated JSON string up to 256 bytes).

### `Motor Queue`
* **Producer:** `command_parser`
* **Consumer:** `motor_controller`
* **Payload:** `motor_cmd_t` (FL, FR, RL, RR speeds: -100 to +100).

### `Servo Queue`
* **Producer:** `command_parser`
* **Consumer:** `servo_controller`
* **Payload:** `servo_cmd_t` (Pan and Tilt angles: 0 to 180 degrees).

### `Eye Queue`
* **Producer:** `command_parser`
* **Consumer:** `oled_renderer`
* **Payload:** `eye_cmd_t` (Expression ID string, e.g., "happy", "alert").

### `LED Queue`
* **Producer:** `command_parser`
* **Consumer:** `led_controller`
* **Payload:** `led_cmd_t` (Mode ID string, target RGB color).

### `TX Queue`
* **Producer:** `telemetry_builder`, `fault_manager`
* **Consumer:** `serial_handler` (TX path)
* **Payload:** `tx_packet_t` (JSON string up to 512 bytes, Priority flag).

## 3. Hardware Abstraction Layer (HAL) Requirements
The Subsystem Layer (above) must never write directly to ESP32 registers. All hardware access goes through the L1/L2 Driver layers:
* `hal_gpio` / `driver_hcsr04`
* `hal_i2c` / `driver_pca9548a`
* `hal_ledc` / `driver_l298n` / `driver_sg90`
* `hal_adc` / `driver_mq2`
* `hal_rmt` / `driver_ws2812b`
