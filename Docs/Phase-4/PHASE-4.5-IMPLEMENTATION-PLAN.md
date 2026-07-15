# Phase 4.5: ESP32 Hardware Driver Layer - Implementation Plan

## Executive Summary
Phase 4.5 establishes the bottom-level Hardware Driver Layer for the ESP32. This module directly interfaces with the microcontroller's physical peripherals (LEDC, I2C, RMT) to actuate motors, servos, and indicators based on the logical commands issued by the Phase 4.4 Runtime Core. It provides strict hardware isolation without introducing any high-level robotic intelligence.

## Objectives
- Implement `MotorDriver` using LEDC PWM to control a TB6612/L298 motor controller.
- Implement `ServoDriver` using 50Hz LEDC signals to control SG90 pan/tilt mechanisms.
- Implement `OLEDDriver` via I2C to display system status.
- Implement `RGBDriver` via the RMT peripheral to control WS2812 status LEDs.
- Implement `BuzzerDriver` for audible alerts and diagnostic feedback.
- Implement `DriverManager` to map `RuntimeEvent` structs securely to their respective physical drivers.

## Architecture
- `ESP32_ROVER/main/drivers/driver_manager.cpp`: The central hub binding events to peripherals.
- `ESP32_ROVER/main/drivers/motor_driver.cpp`: Directional pins + PWM scaling.
- `ESP32_ROVER/main/drivers/servo_driver.cpp`: Angle bounding and PWM translation.
- `ESP32_ROVER/main/drivers/oled_driver.cpp`: State display logic.
- `ESP32_ROVER/main/drivers/rgb_driver.cpp`: LED color indexing.
- `ESP32_ROVER/main/drivers/buzzer_driver.cpp`: Frequency generation.

## FreeRTOS Considerations
- **ISR Safety:** Operations that may block (like I2C transfers for OLED) will not be called from an ISR.
- **Thread Safety:** The abstract drivers currently represent stateless hardware wrappers. State mutations are protected by ensuring execution happens sequentially within the main hardware execution FreeRTOS task.
- **No Dynamic Allocation:** All driver classes and tracking structs are statically allocated.

## Hardware Operations
- **PWM Scaling:** The motor driver converts the theoretical $\pm 32767$ velocity requests into bounded $0-255$ 8-bit LEDC duty cycles.
- **Angle Limiting:** The servo driver rigidly clamps abstract angle requests to $[0, 180]$ to prevent mechanical binding of the pan/tilt system.
- **Emergency Stop:** E-Stop injection bypasses abstract command queues and immediately forces `MotorDriver` to zero, flashes the `RGBDriver` red, and sounds the `BuzzerDriver`.
