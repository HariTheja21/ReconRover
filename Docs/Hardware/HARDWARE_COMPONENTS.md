# Recon Rover V1 — Hardware Components (BOM)

**Document Version:** 1.0  
**Status:** Frozen Specification  
**Last Updated:** 2026-06-28  

This document serves as the master Bill of Materials (BOM) and component specification sheet for Recon Rover V1.

## 1. Computing Subsystem

| Component | Qty | Role | Key Specifications |
|-----------|-----|------|--------------------|
| **Raspberry Pi 3B+** | 1 | Cognitive Processor | 1.4 GHz ARM Cortex-A53, 1GB RAM, WiFi/BLE, 4x USB 2.0 |
| **ESP32-S3 N16R8** | 1 | Reactive Processor | Dual-core 240 MHz Xtensa, 16MB Flash, 8MB PSRAM, USB CDC |

## 2. Sensor Suite

| Component | Qty | Role | Key Specifications |
|-----------|-----|------|--------------------|
| **USB Webcam** | 1 | Primary Vision | 720p or 480p, 30fps, standard UVC driver |
| **USB Microphone** | 1 | Audio Input | Standard USB audio class |
| **VL53L0X** | 2 | High-Precision ToF Proximity | Range: up to 2m, Interface: I2C (0x29) |
| **HC-SR04** | 4 | Perimeter Sonar Proximity | Range: 2cm - 400cm, Interface: Digital IO (5V logic) |
| **MPU6050** | 1 | Inertial Measurement Unit (IMU) | 6-axis (Accel+Gyro), Interface: I2C (0x68) |
| **MQ-2** | 1 | Gas/Smoke Hazard Detection | Interface: Analog (ADC) |
| **INA219** *(Planned)*| 1 | Power Monitoring | Measures voltage/current. Interface: I2C |

## 3. Motion & Actuation

| Component | Qty | Role | Key Specifications |
|-----------|-----|------|--------------------|
| **DC Gear Motor** | 4 | Chassis Drive (4WD) | "Yellow" TT Motors, 3-6V |
| **L298N** | 1 | Dual H-Bridge Motor Driver | Drives left and right motor banks. PWM speed control |
| **SG90 Servo** | 2 | Camera Pan & Tilt Bracket | 0°-180° range, 50Hz PWM control |

## 4. Displays & Indicators

| Component | Qty | Role | Key Specifications |
|-----------|-----|------|--------------------|
| **SSD1306 OLED** | 2 | Animated Eye Displays | 0.96", 128x64px, Interface: I2C (0x3C) |
| **WS2812B Strip**| 2 | Status Indication & Illumination | 5 LEDs per strip, Addressable ARGB, 5V |

## 5. Power & Infrastructure

| Component | Qty | Role | Key Specifications |
|-----------|-----|------|--------------------|
| **PCA9548A** | 1 | I2C Multiplexer | Resolves address collisions (OLEDs, ToF). Interface: I2C (0x70) |
| **Buck Converter** | 2 | 5V Voltage Regulation | Steps down battery voltage to 5V. Must be low ripple. |
| **Li-Po Battery** | 1 | Main Power Supply | 2S (7.4V nominal) recommended. Minimum 2000mAh |
| **BMS Module** | 1 | Battery Protection | Over-discharge, overcharge, and overcurrent cutoff |
| **Logic Shifters** | 4+ | 5V to 3.3V Conversion | For HC-SR04 ECHO signals to protect ESP32-S3 |
