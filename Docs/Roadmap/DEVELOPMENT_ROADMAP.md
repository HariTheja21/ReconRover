# Recon Rover V1 — Development Roadmap & Project Phases

**Document Version:** 1.0  
**Status:** Frozen Specification  
**Last Updated:** 2026-06-28  

This document outlines the structured phases for the software and firmware implementation of Recon Rover V1, following the completion of the Architectural Documentation Freeze.

## Phase 1: Hardware Bench Verification
**Goal:** Prove the electrical design before writing complex code.
* Assemble power rails (Battery, BMS, Buck converters).
* Verify 5V and 3.3V stability under mock load.
* Connect ESP32-S3 and Raspberry Pi 3B+ to verify basic boot.
* Basic I2C scanner test for address resolution.

## Phase 2: Reactive Firmware (ESP32-S3) Foundations
**Goal:** Implement the L1/L2 drivers and FreeRTOS task skeleton.
* Initialize FreeRTOS tasks with stubbed loops.
* Implement UART CDC serial driver (bidirectional string echo).
* Implement L298N PWM motor drivers.
* Implement WS2812B LED sequences.
* Implement Sensor reading (HC-SR04, VL53L0X, MPU6050).

## Phase 3: Protocol Integration
**Goal:** Establish the strict dual-processor serial boundary.
* ESP32-S3: Implement JSON `telemetry_builder` and transmit at 20Hz.
* ESP32-S3: Implement JSON `command_parser`.
* Raspberry Pi: Implement `serial_manager.py` to ingest telemetry and emit dummy commands.
* **Milestone:** The Pi can see the world through the ESP32 and manually drive the motors over serial.

## Phase 4: Cognitive Software (Raspberry Pi)
**Goal:** Give the rover awareness.
* Implement `world_model.py` and `sensor_fusion.py`.
* Implement `vision_pipeline.py` (Object detection).
* Implement `navigation.py` (Obstacle avoidance based on HC-SR04/VL53L0X).
* Implement `ai_engine.py` (Mode switching: IDLE, PATROL, AVOID).

## Phase 5: Autonomous Integration
**Goal:** Full closed-loop autonomy.
* Pi makes navigation decisions based on combined vision and telemetry.
* ESP32 correctly displays OLED eyes matching the Pi's AI context.
* LEDs reflect operational status (e.g., Green for tracking, Red for Hazard).
* **Milestone:** Rover can autonomously patrol a room without colliding and react to its environment.
