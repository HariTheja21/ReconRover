# Recon Rover V1 — ESP32-S3 Pinout & Allocation

**Document Version:** 1.0  
**Status:** Frozen Specification  
**Last Updated:** 2026-06-28  

This document details the complete GPIO mapping for the ESP32-S3 N16R8 microcontroller on Recon Rover V1. All sensors and actuators interface exclusively with the ESP32-S3.

> **Note:** The ESP32-S3 logic level is 3.3V. All 5V inputs (such as HC-SR04 ECHO lines) must be stepped down via a logic level shifter or voltage divider.

## GPIO Allocation Table

| GPIO | Peripheral | Direction | Interface | Purpose / Notes |
|------|-----------|-----------|-----------|----------------|
| **GPIO4** | HC-SR04 Front — TRIG | Output | Digital | 10 µs pulse |
| **GPIO5** | HC-SR04 Front — ECHO | Input | Digital | 5V->3.3V level shift required |
| **GPIO6** | HC-SR04 Left — TRIG | Output | Digital | 10 µs pulse |
| **GPIO7** | HC-SR04 Left — ECHO | Input | Digital | 5V->3.3V level shift required |
| **GPIO10** | MQ-2 Gas Sensor | Input | Analog (ADC) | Read gas concentration |
| **GPIO11** | SG90 Servo — Pan | Output | PWM (LEDC) | 50 Hz, 1–2 ms pulse width |
| **GPIO12** | SG90 Servo — Tilt | Output | PWM (LEDC) | 50 Hz, 1–2 ms pulse width |
| **GPIO13** | I2C SDA | Bidirectional | I2C | PCA9548A & direct I2C devices |
| **GPIO14** | I2C SCL | Output | I2C | I2C Clock |
| **GPIO15** | HC-SR04 Right — TRIG | Output | Digital | 10 µs pulse |
| **GPIO16** | HC-SR04 Right — ECHO | Input | Digital | 5V->3.3V level shift required |
| **GPIO17** | HC-SR04 Rear — TRIG | Output | Digital | 10 µs pulse |
| **GPIO18** | HC-SR04 Rear — ECHO | Input | Digital | 5V->3.3V level shift required |
| **USB D+** | USB Serial Bridge | Bidirectional | USB CDC | JSON serial link to Raspberry Pi |
| **USB D-** | USB Serial Bridge | Bidirectional | USB CDC | JSON serial link to Raspberry Pi |
| *TBD* | L298N IN1 | Output | Digital | Motor direction — Left side A |
| *TBD* | L298N IN2 | Output | Digital | Motor direction — Left side B |
| *TBD* | L298N IN3 | Output | Digital | Motor direction — Right side A |
| *TBD* | L298N IN4 | Output | Digital | Motor direction — Right side B |
| *TBD* | L298N ENA | Output | PWM (LEDC) | Motor speed — Left side |
| *TBD* | L298N ENB | Output | PWM (LEDC) | Motor speed — Right side |
| *TBD* | WS2812B Data — Left | Output | Digital (1-Wire)| ARGB LED strip Left (x5 LEDs) |
| *TBD* | WS2812B Data — Right| Output | Digital (1-Wire)| ARGB LED strip Right (x5 LEDs)|

## PCA9548A I2C Multiplexer Channels
Connected to GPIO13 (SDA) and GPIO14 (SCL).

| Channel | I2C Address | Device | Purpose |
|---------|-------------|--------|---------|
| **CH0** | 0x3C | SSD1306 OLED | Left Eye display |
| **CH1** | 0x3C | SSD1306 OLED | Right Eye display |
| **CH2** | 0x29 | VL53L0X | Front proximity sensor |
| **CH3** | 0x29 | VL53L0X | Pan-axis proximity sensor |
| CH4-7 | — | — | *Reserved for future expansion* |

## Power Considerations
* **Input Voltage:** The ESP32-S3 must be powered by the dedicated 5V Buck Converter (#2) in production, stepping down the battery voltage.
* **Internal LDO:** The 5V input is stepped down to 3.3V internally for the ESP32 logic. Do not pull high current from the ESP32 3.3V output pin.
