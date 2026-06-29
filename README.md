# Recon Rover V1

![Status](https://img.shields.io/badge/Status-Architecture%20Phase-blue)
![Architecture](https://img.shields.io/badge/Architecture-Dual--Processor-orange)
![License](https://img.shields.io/badge/License-MIT-green)

**Recon Rover V1** is a modular, intelligent reconnaissance rover built on a strict dual-processor architecture. It separates high-level cognition from low-level reactive hardware control, ensuring real-time responsiveness and system stability.

## 🚀 The Architecture

Recon Rover V1 employs a dual-processor design connected exclusively via a high-speed JSON-over-USB-Serial bridge.

### 🧠 Cognitive Layer: Raspberry Pi 3B+
The brain of the rover. Written in Python 3.
* **Vision & AI:** Object detection via OpenCV/TFLite and a USB webcam.
* **Audio:** Voice command processing (VAD, Speech-to-Text).
* **Navigation:** Spatial world mapping and obstacle avoidance logic.
* **Dashboard:** Hosts a WebSocket server to stream telemetry to a web client.
* *It does not touch GPIO pins.*

### ⚡ Reactive Layer: ESP32-S3 (N16R8)
The spinal cord of the rover. Written in C++ on FreeRTOS.
* **Sensors:** Polls HC-SR04 ultrasonic, VL53L0X ToF, MPU6050 IMU, and MQ-2 Gas sensors.
* **Actuators:** Drives 4x DC Motors via L298N and controls SG90 Pan/Tilt servos.
* **Displays:** Renders animated expressions to 2x SSD1306 OLED screens and drives WS2812B LEDs.
* **Safety:** Hardware watchdog ensures immediate shutdown of motors on fault or Pi disconnect.
* *It does not make decisions; it simply executes commands and reports telemetry.*

## 📚 Documentation

The architecture is fully documented. Please refer to the `Docs/` folder before contributing.

* **[Architecture Index](Docs/README.md)** - Start here for a full list of engineering documents.
* **[System Architecture](Docs/Architecture/SYSTEM_ARCHITECTURE.md)** - The philosophy and design of the dual-processor split.
* **[Communication Protocol](Docs/Protocol/COMMUNICATION_PROTOCOL.md)** - The JSON serial contract between the Pi and ESP32.
* **[Setup Guide](Docs/SETUP_GUIDE.md)** - How to configure your environment for ESP-IDF and Python.

## 🛠️ Hardware Requirements

* Raspberry Pi 3B+
* ESP32-S3 N16R8
* L298N Motor Driver + 4x DC Gear Motors
* PCA9548A I2C Multiplexer
* Sensors: 4x HC-SR04, 2x VL53L0X, MPU6050, MQ-2
* Visuals: 2x 0.96" SSD1306 OLED, 2x WS2812B LED Strips
* Vision/Audio: USB Webcam, USB Microphone
* Power: 2S Li-Po Battery, 2x 5V Buck Converters (Isolating logic from motors)

*See [HARDWARE_COMPONENTS.md](Docs/Hardware/HARDWARE_COMPONENTS.md) for the complete BOM.*

## 📄 License

This project is licensed under the MIT License.
