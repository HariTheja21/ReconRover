# Recon Rover V1 — Documentation Index

This directory contains the authoritative engineering documentation for Recon Rover V1. All software and hardware design decisions are governed by these documents.

## Directory Structure

* **`/Architecture`**
  * `SYSTEM_ARCHITECTURE.md` - High-level system goals, dual-processor separation.
  * `HARDWARE_ARCHITECTURE.md` - Hardware topology, module allocation.
  * `SOFTWARE_ARCHITECTURE.md` - High-level software component interactions.
  * `FIRMWARE_ARCHITECTURE.md` - ESP32-S3 FreeRTOS design and constraints.
* **`/API`**
  * `ESP32_API.md` - Internal firmware queues and FreeRTOS task responsibilities.
  * `RASPBERRY_PI_API.md` - Internal Python modules, asyncio loops, world model.
* **`/Hardware`**
  * `POWER_DISTRIBUTION.md` - Dual-rail 5V logic and unregulated motor power.
  * `HARDWARE_COMPONENTS.md` - Master Bill of Materials (BOM).
* **`/Pinout`**
  * `ESP32S3_PINOUT.md` - ESP32-S3 GPIO mappings.
  * `RASPBERRY_PI_CONNECTIONS.md` - Pi USB, network, and power connections.
* **`/Protocol`**
  * `COMMUNICATION_PROTOCOL.md` - JSON payload specifications for the serial bridge.
* **`/Roadmap`**
  * `DEVELOPMENT_ROADMAP.md` - Step-by-step implementation phases.
* **`/Tests`**
  * `TESTING_PROCEDURES.md` - Subsystem bench tests and integration tests.
* **`SETUP_GUIDE.md`** - How to setup ESP-IDF and Python environments.
