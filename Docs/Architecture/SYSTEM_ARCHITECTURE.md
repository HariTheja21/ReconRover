# Recon Rover V1 — System Architecture

**Document Version:** 1.0  
**Status:** Foundation Draft  
**Last Updated:** 2026-06-28  
**Author:** Lead Robotics Software Architect  
**Classification:** Internal Design Document

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Mission](#2-mission)
3. [System Goals](#3-system-goals)
4. [High-Level Architecture](#4-high-level-architecture)
5. [Hardware Overview](#5-hardware-overview)
6. [Hardware Statistics](#6-hardware-statistics)
7. [Hardware Inventory](#7-hardware-inventory)
8. [ESP32-S3 Responsibilities](#8-esp32-s3-responsibilities)
9. [Raspberry Pi Responsibilities](#9-raspberry-pi-responsibilities)
10. [Data Flow](#10-data-flow)
11. [Communication Philosophy](#11-communication-philosophy)
12. [Telemetry Philosophy](#12-telemetry-philosophy)
13. [Design Principles](#13-design-principles)
14. [Scalability Strategy](#14-scalability-strategy)
15. [Future Expansion Strategy](#15-future-expansion-strategy)
16. [Conclusion](#16-conclusion)

---

## 1. Project Overview

**Recon Rover V1** is an intelligent, ground-based autonomous reconnaissance platform engineered for exploration, environmental sensing, and real-time situational awareness. The rover is designed around a strict two-tier computing architecture: a **Raspberry Pi 3B+** serving as the high-level cognitive brain, and an **ESP32-S3 N16R8** serving as the deterministic real-time hardware controller.

The platform integrates multiple heterogeneous sensors, a USB vision system, expressive OLED eyes, addressable RGB lighting, and a live telemetry dashboard — all unified under a clean, maintainable, modular software architecture intended for long-term development and eventual open-source publication.

Recon Rover V1 is a learning and research platform first, and a capable reconnaissance agent second. Every engineering decision prioritises **clarity, maintainability, and modularity** over premature optimisation.

---

## 2. Mission

> **To build an intelligent autonomous rover capable of perceiving its environment, making real-time navigation decisions, and communicating its findings — while maintaining a clean, professional, and extensible software architecture fit for long-term development.**

The rover must be able to:

- Navigate autonomously in an unstructured indoor environment.
- Detect, classify, and track objects using computer vision.
- Monitor environmental and electrical conditions via an onboard sensor suite.
- Express contextual state visually through animated OLED eye displays and ARGB lighting.
- Stream live telemetry to an external dashboard over a network connection.
- Respond to voice commands through an integrated USB microphone pipeline.

---

## 3. System Goals

### Functional Goals

| ID | Goal | Priority |
|----|------|----------|
| G-01 | Autonomous obstacle avoidance in all four directions | Critical |
| G-02 | Real-time object detection via USB webcam | Critical |
| G-03 | Sensor telemetry streaming to live dashboard | Critical |
| G-04 | Expressive OLED eye animations driven by AI context | High |
| G-05 | ARGB LED status and mood lighting | High |
| G-06 | Voice command recognition via USB microphone | High |
| G-07 | Gas hazard detection via MQ-2 sensor | High |
| G-08 | Battery/power health monitoring via INA219 | Medium |
| G-09 | IMU-assisted navigation and orientation tracking | Medium |
| G-10 | Pan/tilt camera servo control | Medium |

### Non-Functional Goals

| ID | Goal | Description |
|----|------|-------------|
| NF-01 | Modularity | Every subsystem is independently replaceable |
| NF-02 | Separation of Concerns | Hardware layer is strictly isolated from AI/logic layer |
| NF-03 | Reliability | The ESP32 must never block or hang due to high-level failures |
| NF-04 | Observability | All subsystems must emit structured, loggable telemetry |
| NF-05 | Maintainability | Code must be readable and documented for future contributors |
| NF-06 | Extensibility | New sensors and modules can be added without refactoring core code |

---

## 4. High-Level Architecture

The architecture follows a **Hierarchical Dual-Processor Model** with a strict command-and-control boundary between cognitive and reactive layers.

```
+==================================================================+
|                    EXTERNAL SYSTEMS                              |
|         +--------------------------------------+                 |
|         |       Live Dashboard (PC/Web)        |                 |
|         |   Telemetry  .  Logs  .  Controls    |                 |
|         +------------------+-------------------+                 |
+============================|=====================================+
                             | WiFi / WebSocket
+============================v=====================================+
|                   COGNITIVE LAYER                                |
|                  Raspberry Pi 3B+                                |
|                                                                  |
|  +--------------+  +--------------+  +---------------------+    |
|  | Vision       |  | AI / NLP     |  | Navigation &        |    |
|  | Pipeline     |  | Engine       |  | Motion Planning     |    |
|  | (OpenCV)     |  |              |  |                     |    |
|  +--------------+  +--------------+  +---------------------+    |
|  +--------------+  +--------------+  +---------------------+    |
|  | Audio        |  | Sensor       |  | Dashboard           |    |
|  | Processing   |  | Fusion       |  | Communicator        |    |
|  +--------------+  +--------------+  +---------------------+    |
|                                                                  |
|              USB Serial / UART  (JSON Protocol)                  |
+============================|=====================================+
                             |
+============================v=====================================+
|                   REACTIVE LAYER                                 |
|                    ESP32-S3 N16R8                                 |
|                                                                  |
|  +--------------+  +--------------+  +---------------------+    |
|  | Motor        |  | Servo        |  | OLED Eye            |    |
|  | Controller   |  | Controller   |  | Renderer            |    |
|  | (L298N)      |  | (Pan/Tilt)   |  | (SSD1306 x2)        |    |
|  +--------------+  +--------------+  +---------------------+    |
|  +--------------+  +--------------+  +---------------------+    |
|  | Ultrasonic   |  | TOF Sensors  |  | ARGB LED            |    |
|  | Array        |  | (VL53L0X x2) |  | Controller          |    |
|  | (HC-SR04 x4) |  |              |  | (WS2812B x2)        |    |
|  +--------------+  +--------------+  +---------------------+    |
|  +--------------+  +--------------+                             |
|  | IMU          |  | Gas Sensor   |                             |
|  | (MPU6050)    |  | (MQ-2)       |                             |
|  +--------------+  +--------------+                             |
|                                                                  |
+==================================================================+
```

### Layer Summary

| Layer | Processor | Role | Latency Class |
|-------|-----------|------|---------------|
| Cognitive | Raspberry Pi 3B+ | AI, vision, planning, dashboard | 10 ms – 1 s |
| Reactive | ESP32-S3 N16R8 | Hardware I/O, real-time sensing | < 5 ms |

---

## 5. Hardware Overview

Recon Rover V1 is built around two tightly integrated computing systems connected via USB serial communication. The hardware is partitioned by function — sensors and actuators are owned exclusively by the ESP32-S3, while high-level perception and intelligence live on the Raspberry Pi.

### Computing Architecture Diagram

```
Raspberry Pi 3B+
|
+-- USB Port --> ESP32-S3  (Serial JSON Bridge)
+-- USB Port --> USB Webcam
+-- USB Port --> USB Microphone

ESP32-S3 N16R8
|
+-- I2C Bus  (SDA: GPIO13,  SCL: GPIO14)
|   +-- PCA9548A I2C Multiplexer
|       +-- CH0 --> SSD1306 OLED  (Left Eye)
|       +-- CH1 --> SSD1306 OLED  (Right Eye)
|       +-- CH2 --> VL53L0X ToF   (Front)
|       +-- CH3 --> VL53L0X ToF   (Pan)
|
+-- GPIO10 --> MQ-2  (Gas Sensor - Analog)
|
+-- GPIO11 --> SG90 Servo  (Pan)
+-- GPIO12 --> SG90 Servo  (Tilt)
|
+-- Ultrasonic Array (HC-SR04)
|   +-- Front:  TRIG GPIO4  / ECHO GPIO5
|   +-- Left:   TRIG GPIO6  / ECHO GPIO7
|   +-- Right:  TRIG GPIO15 / ECHO GPIO16
|   +-- Rear:   TRIG GPIO17 / ECHO GPIO18
|
+-- L298N Motor Driver --> 4x DC Gear Motors
|
+-- WS2812B ARGB LED Strips x2  (5 LEDs each)
```

---

## 6. Hardware Statistics

| Category | Metric | Value |
|----------|--------|-------|
| Computing | Processors | 2 |
| Computing | Pi RAM | 1 GB LPDDR2 |
| Computing | Pi CPU | ARM Cortex-A53 @ 1.4 GHz (quad-core) |
| Computing | ESP32 RAM | 512 KB SRAM + 8 MB PSRAM |
| Computing | ESP32 Flash | 16 MB |
| Computing | ESP32 CPU | Xtensa LX7 dual-core @ 240 MHz |
| Vision | Cameras | 1 (USB Webcam) |
| Audio | Microphones | 1 (USB Microphone) |
| Sensors | Distance sensors (total) | 6 (4x HC-SR04, 2x VL53L0X) |
| Sensors | IMU | 1 (MPU6050, 6-axis) |
| Sensors | Gas sensors | 1 (MQ-2) |
| Sensors | Power monitors | 1 planned (INA219) |
| Displays | OLED panels | 2 (SSD1306 128x64) |
| Motion | DC motors | 4 |
| Motion | Motor drivers | 1 (L298N, dual H-bridge) |
| Motion | Servos | 2 (SG90 Pan/Tilt) |
| Lighting | ARGB LED strips | 2 (WS2812B, 5 LEDs each) |
| Lighting | Total addressable LEDs | 10 |
| I2C | Multiplexer channels used | 4 of 8 |
| GPIO | I2C pins | 2 (SDA: GPIO13, SCL: GPIO14) |
| GPIO | Ultrasonic pins | 8 (4 TRIG, 4 ECHO) |
| GPIO | Servo pins | 2 (GPIO11, GPIO12) |
| GPIO | Analog sensor pins | 1 (GPIO10) |

---

## 7. Hardware Inventory

### Computing Units

| Component | Model | Qty | Role |
|-----------|-------|-----|------|
| Single Board Computer | Raspberry Pi 3B+ | 1 | Cognitive brain |
| Microcontroller | ESP32-S3 N16R8 | 1 | Reactive hardware controller |

### Vision & Audio

| Component | Interface | Qty | Role |
|-----------|-----------|-----|------|
| USB Webcam | USB | 1 | Object detection & navigation vision |
| USB Microphone | USB | 1 | Voice command input |

### Sensors

| Component | Model | Interface | Qty | Owned By | Purpose |
|-----------|-------|-----------|-----|----------|---------|
| IMU | MPU6050 | I2C (via PCA9548A) | 1 | ESP32-S3 | Orientation, acceleration, gyroscope |
| ToF Distance | VL53L0X | I2C CH2 (Front) | 1 | ESP32-S3 | Precise frontal distance measurement |
| ToF Distance | VL53L0X | I2C CH3 (Pan) | 1 | ESP32-S3 | Pan-axis distance measurement |
| Ultrasonic | HC-SR04 | GPIO | 4 | ESP32-S3 | Omnidirectional obstacle detection |
| Gas Sensor | MQ-2 | Analog GPIO10 | 1 | ESP32-S3 | Smoke / gas hazard detection |
| Power Monitor | INA219 | I2C (planned) | 1 | ESP32-S3 | Battery voltage & current monitoring |

### Displays

| Component | Model | Interface | Qty | OLED Channel | Role |
|-----------|-------|-----------|-----|--------------|------|
| Left Eye Display | SSD1306 | I2C CH0 | 1 | PCA9548A CH0 | Left animated eye |
| Right Eye Display | SSD1306 | I2C CH1 | 1 | PCA9548A CH1 | Right animated eye |

> **Note:** Both OLEDs share the same I2C address (0x3C). The PCA9548A multiplexer allows them to be addressed on separate channels without conflict.

### Motion

| Component | Model | Qty | Interface | Role |
|-----------|-------|-----|-----------|------|
| DC Gear Motor | Generic 6V | 4 | L298N | Drive wheels |
| Motor Driver | L298N | 1 | GPIO | Dual H-bridge motor control |
| Pan Servo | SG90 | 1 | GPIO11 | Camera pan axis |
| Tilt Servo | SG90 | 1 | GPIO12 | Camera tilt axis |

### Lighting

| Component | Model | LEDs | Interface | Qty | Role |
|-----------|-------|------|-----------|-----|------|
| ARGB LED Strip (Left) | WS2812B | 5 | GPIO | 1 | Status & mood lighting |
| ARGB LED Strip (Right) | WS2812B | 5 | GPIO | 1 | Status & mood lighting |

### I2C Infrastructure

| Component | Model | Qty | Channels Used |
|-----------|-------|-----|--------------|
| I2C Multiplexer | PCA9548A | 1 | 4 of 8 |

#### PCA9548A Channel Map

| Channel | Device | Purpose |
|---------|--------|---------|
| CH0 | SSD1306 OLED | Left Eye display |
| CH1 | SSD1306 OLED | Right Eye display |
| CH2 | VL53L0X | Front proximity sensor |
| CH3 | VL53L0X | Pan-axis proximity sensor |
| CH4 – CH7 | *(Reserved)* | Future sensor expansion |

---

## 8. ESP32-S3 Responsibilities

The ESP32-S3 is the **Reactive Layer** of Recon Rover V1. Its sole responsibility is to manage hardware in real time — it never reasons, plans, or makes decisions. All decisions are made by the Raspberry Pi and translated into commands for the ESP32 to execute.

### Core Mandate

> **The ESP32-S3 must never perform AI, computer vision, or high-level decision making. It reads hardware, executes commands, and reports data. Nothing more.**

### Responsibilities

#### 1. Sensor Reading & Management

| Sensor | Task |
|--------|------|
| HC-SR04 x4 | Poll ultrasonic distance for Front, Left, Right, and Rear zones |
| VL53L0X x2 | Read precise ToF distance from Front and Pan channels |
| MPU6050 | Read 6-axis IMU data (acceleration, gyroscope, temperature) |
| MQ-2 | Read analog gas concentration value |
| INA219 *(planned)* | Read bus voltage, current, and power consumption |

#### 2. Motor Control

- Accept speed and direction commands from the Raspberry Pi.
- Drive the L298N motor driver to control all 4 DC gear motors.
- Support movement modes: forward, reverse, turn left, turn right, pivot, stop.
- Apply independent per-motor speed via PWM for accurate differential drive.

#### 3. Servo Control

- Accept pan and tilt angle commands from the Raspberry Pi.
- Drive GPIO11 (Pan Servo) and GPIO12 (Tilt Servo) via PWM.
- Enforce safe angle boundaries to prevent mechanical damage.

#### 4. OLED Eye Rendering

- Receive eye expression identifiers from the Raspberry Pi (e.g., `"expression": "happy"`).
- Render the corresponding pre-defined animation frame on Left Eye (CH0) and Right Eye (CH1) OLEDs via PCA9548A.
- Manage channel switching on the PCA9548A without Pi involvement.

#### 5. ARGB LED Control

- Accept LED colour and pattern commands from the Raspberry Pi.
- Drive Left and Right WS2812B strips with independent control over all 10 LEDs.
- Support modes: solid colour, blink, pulse, status indicator, custom pattern.

#### 6. Telemetry Streaming

- Continuously package all sensor readings into structured JSON telemetry packets.
- Transmit packets to the Raspberry Pi over USB serial at a defined rate (target: 20 Hz).
- Report self-diagnostics (e.g., sensor error flags, I2C failures).

#### 7. Command Reception

- Listen for JSON command packets from the Raspberry Pi on the serial bus.
- Parse and dispatch commands to the appropriate hardware subsystem.
- Send acknowledgement responses where applicable.

### What the ESP32-S3 Must NOT Do

- Run object detection or computer vision.
- Make any navigation or movement decisions independently.
- Perform sensor fusion or data interpretation beyond raw value reporting.
- Communicate directly with the dashboard.
- Store or log data long-term.

---

## 9. Raspberry Pi Responsibilities

The Raspberry Pi 3B+ is the **Cognitive Layer** of Recon Rover V1. It is responsible for all perception, reasoning, planning, and communication. It never directly touches hardware — all hardware interactions are delegated to the ESP32-S3 via the serial bridge.

### Core Mandate

> **The Raspberry Pi decides everything. It observes the world through sensors and cameras, reasons about what to do, and issues commands to the ESP32-S3 for execution.**

### Responsibilities

#### 1. Vision Pipeline

- Capture frames from the USB webcam.
- Run object detection models (e.g., YOLO, MobileNet SSD) using OpenCV.
- Track detected objects across frames.
- Derive spatial context (distance estimation, object class, confidence score).
- Feed detection results into the navigation and decision engine.

#### 2. Audio Processing

- Capture audio from the USB microphone.
- Perform voice activity detection (VAD).
- Run speech-to-text to extract commands.
- Dispatch parsed commands to the appropriate subsystem.

#### 3. Sensor Fusion

- Receive raw telemetry packets from the ESP32-S3.
- Fuse data from ultrasonic sensors, VL53L0X, and IMU into a unified spatial model.
- Maintain a real-time world model for navigation decisions.

#### 4. Navigation & Motion Planning

- Determine the rover's safe movement strategy based on the fused sensor model and vision output.
- Plan paths and generate movement commands.
- Issue motor commands to the ESP32-S3 (speed, direction, duration).
- Issue servo commands for camera pan/tilt based on tracking targets.

#### 5. High-Level Decision Making

- Determine the rover's current behavioural mode (idle, patrol, tracking, hazard response, etc.).
- Select appropriate eye expressions, LED patterns, and behaviours based on context.
- Respond to voice commands by changing modes or performing actions.

#### 6. Eye Expression Selection

- Based on the current AI context (e.g., detecting a person, low battery, error state), select an appropriate eye expression identifier.
- Send the expression command to the ESP32-S3 for OLED rendering.

#### 7. Dashboard Communication

- Maintain a live data stream (WebSocket or similar) to an external dashboard.
- Push structured telemetry: sensor readings, object detections, battery status, system events.
- Receive optional manual control input from the dashboard.
- Serve a local web dashboard if required.

#### 8. System Logging

- Log all significant events to structured log files.
- Include timestamps, event types, sensor values, and decision outcomes.
- Rotate and archive logs to manage storage on the Pi's SD card.

### What the Raspberry Pi Must NOT Do

- Directly read or write GPIO pins that belong to the ESP32's domain.
- Block on hardware I/O that would delay AI or vision processing.
- Expose raw low-level hardware commands without safety validation.

---

## 10. Data Flow

### Sensor Data Flow  (ESP32 --> Raspberry Pi)

```
[Hardware Sensors]
        |
        v
[ESP32-S3 Sensor Polling Loop]
        |   Reads HC-SR04, VL53L0X, MPU6050, MQ-2, INA219
        |
        v
[ESP32-S3 Telemetry Packager]
        |   Packages data into structured JSON telemetry packet
        |
        v
[USB Serial Bus]   (115200 baud or higher, newline-delimited JSON)
        |
        v
[Raspberry Pi Serial Reader]
        |   Receives and deserialises telemetry packet
        |
        v
[Raspberry Pi Sensor Fusion Engine]
        |   Fuses distance, IMU, and gas data into spatial model
        |
        +----> [Navigation Planner]
        +----> [Dashboard Broadcaster]
        +----> [System Logger]
```

### Command Flow  (Raspberry Pi --> ESP32)

```
[Raspberry Pi Decision Engine]
        |   Computes: motion, expression, LED pattern
        |
        v
[Command Builder]
        |   Constructs JSON command packet
        |
        v
[USB Serial Bus]
        |
        v
[ESP32-S3 Command Dispatcher]
        |
        +----> [Motor Controller]     --> L298N --> DC Motors
        +----> [Servo Controller]     --> SG90 Pan / Tilt
        +----> [Eye Renderer]         --> PCA9548A --> SSD1306 x2
        +----> [LED Controller]       --> WS2812B x2
```

### External Telemetry Flow  (Raspberry Pi --> Dashboard)

```
[Raspberry Pi]
        |   Aggregates sensor data + AI detections + system events
        |
        v
[Dashboard Communicator Module]
        |   Serialises structured telemetry to JSON
        |
        v
[WiFi Network]   (WebSocket or HTTP long-poll)
        |
        v
[Live Dashboard]   (PC / Browser)
        |   Displays: sensor graphs, camera feed, event log, battery status
```

---

## 11. Communication Philosophy

### The Serial Bridge Contract

All communication between the Raspberry Pi and the ESP32-S3 travels over a single **USB Serial link**. This is the **only** communication channel between the two processors. There is no SPI, no I2C cross-talk, and no shared memory.

The protocol is:

- **Encoding:** UTF-8 JSON, one packet per line (`\n` delimited).
- **Direction:** Bidirectional — telemetry flows up (ESP32 -> Pi), commands flow down (Pi -> ESP32).
- **Framing:** Each packet is terminated with a newline character for simple line-based parsing.
- **Acknowledgement:** Commands may optionally receive an `ACK` or `NACK` response from the ESP32.

### Design Rationale

| Decision | Rationale |
|----------|-----------|
| JSON over binary | Human-readable, easy to debug, no custom deserialisation library needed |
| USB Serial over WiFi | Low latency, no network dependency, reliable physical link |
| Newline-delimited | Simple to parse with `readline()` on both platforms |
| Unidirectional data streams | Prevents command/telemetry collision and simplifies state management |

### Packet Structure (Illustrative)

**Telemetry Packet  (ESP32 --> Pi)**

```json
{
  "type": "telemetry",
  "ts": 123456789,
  "ultrasonic": { "front": 35, "left": 80, "right": 72, "rear": 120 },
  "tof": { "front": 33, "pan": 77 },
  "imu": { "ax": 0.02, "ay": -0.01, "az": 9.81, "gx": 0.1, "gy": 0.0, "gz": 0.0 },
  "gas": { "raw": 215, "hazard": false },
  "power": { "voltage": 7.4, "current": 1.2 }
}
```

**Command Packet  (Pi --> ESP32)**

```json
{
  "type": "cmd",
  "ts": 123456792,
  "motors": { "fl": 80, "fr": 80, "rl": 80, "rr": 80 },
  "servos": { "pan": 90, "tilt": 45 },
  "eyes": { "expression": "curious" },
  "leds": { "mode": "pulse", "color": [0, 120, 255] }
}
```

> **Note:** The exact packet schema is defined in `Docs/Protocol/`. These samples are illustrative only.

---

## 12. Telemetry Philosophy

Telemetry is a first-class citizen of this project. Every meaningful event in the rover's operation must be observable, logged, and transmittable.

### Principles

| Principle | Description |
|-----------|-------------|
| **Structured, not textual** | All telemetry is machine-parseable JSON — no freeform log strings in data paths |
| **Timestamped** | Every packet carries a monotonic timestamp for ordering and latency analysis |
| **Push-based** | The ESP32 pushes telemetry continuously; the Pi does not poll |
| **Layered** | Hardware telemetry (ESP32 -> Pi) and system telemetry (Pi -> Dashboard) are separate concerns |
| **Non-blocking** | Telemetry transmission must never block the main sensing or control loops |
| **Lossy-tolerant** | Occasional dropped telemetry packets are acceptable; correctness is not sacrificed for delivery |

### Telemetry Data Categories

| Category | Source | Destination | Contents |
|----------|--------|-------------|----------|
| Sensor Telemetry | ESP32-S3 | Raspberry Pi | Distance, IMU, gas, power readings |
| Vision Telemetry | Raspberry Pi | Dashboard | Detected objects, bounding boxes, class confidence |
| System Events | Raspberry Pi | Dashboard + Logs | Mode changes, errors, warnings, command outcomes |
| Performance Metrics | Raspberry Pi | Dashboard + Logs | Loop rates, inference latency, CPU/memory usage |

### Target Telemetry Rates

| Stream | Target Rate | Notes |
|--------|-------------|-------|
| ESP32 --> Pi (sensor) | 20 Hz | Full sensor suite snapshot |
| Pi --> Dashboard (live) | 10 Hz | Aggregated and enriched |
| Pi --> Dashboard (events) | On-change | Immediate push for state events |
| Pi --> Log files | Per-event | Persistent structured logs |

---

## 13. Design Principles

These principles govern every architectural decision in Recon Rover V1. They are not aspirational — they are mandatory constraints.

### P-01: Separation of Cognition and Reaction

The boundary between the Raspberry Pi and the ESP32-S3 is sacred. The ESP32 reads hardware and executes commands. The Raspberry Pi reasons and decides. These roles must never bleed into each other.

### P-02: The Hardware Layer Is Dumb By Design

The ESP32-S3 should require no understanding of the rover's mission, environment, or state. It reacts to inputs and commands, nothing more. All intelligence lives above the serial bridge.

### P-03: Modularity Over Monoliths

Every subsystem — vision, audio, navigation, telemetry, LED control — is an independent module with a defined interface. Modules communicate through structured data, not shared state.

### P-04: Failure Isolation

A failure in the vision pipeline must not crash the navigation stack. A serial communication timeout must not freeze the motor controller. Each subsystem must fail gracefully and independently.

### P-05: Observability By Default

Every module emits structured logs and telemetry. No silent failures. No invisible state. Every action is observable, every error is reportable.

### P-06: No Premature Optimisation

Write clear, readable code first. Optimise only where measured profiling identifies a genuine bottleneck. Clever code that is hard to maintain is not acceptable.

### P-07: Configuration Over Hardcoding

All tunable parameters (sensor thresholds, speeds, loop rates, serial port paths, pin assignments) are defined in configuration files, not buried in source code.

### P-08: Deterministic Hardware Control

The ESP32's control loops must be deterministic and predictable. Avoid dynamic memory allocation, blocking calls, or non-deterministic delays in real-time control paths.

---

## 14. Scalability Strategy

Recon Rover V1 is intentionally designed to grow. The following strategies ensure the platform can scale without architectural rework.

### I2C Expansion (ESP32)

The PCA9548A multiplexer provides 8 I2C channels, of which only 4 are currently used. Channels CH4–CH7 are reserved for future I2C devices (e.g., additional ToF sensors, barometric pressure sensor, additional displays).

### GPIO Expansion (ESP32)

The ESP32-S3 N16R8 has abundant GPIO capacity beyond current usage. Future peripherals (e.g., additional LED strips, encoders, actuators) can be mapped to available pins without hardware changes to the core board.

### Software Module Expansion (Raspberry Pi)

The Raspberry Pi software stack is organised as independent modules. Adding a new capability (e.g., SLAM, thermal camera, LiDAR integration) requires writing a new module and registering it with the sensor fusion and telemetry pipeline — no modifications to existing modules required.

### Protocol Versioning

The JSON serial protocol includes a `type` field for packet classification and is designed to be versioned in future iterations. New packet types can be added without breaking existing parsers, as unknown types are silently ignored.

### Dashboard Extensibility

The dashboard data contract is defined by the telemetry schema, not by the dashboard implementation. A new dashboard (e.g., mobile app, 3D visualiser) can be built to consume the same telemetry stream without modifying the rover's software.

---

## 15. Future Expansion Strategy

The following enhancements are anticipated in future versions of Recon Rover and are accounted for in this architecture's design decisions.

### Planned for V1.x

| Feature | Description | Impact |
|---------|-------------|--------|
| INA219 Power Monitor | Full battery voltage, current, and power monitoring | ESP32 sensor module addition |
| SLAM / Mapping | Simultaneous Localisation and Mapping using sensor fusion | New Pi module; no hardware changes |
| Voice Command Expansion | Extended NLP command vocabulary | Pi audio module update |
| Motor Encoder Feedback | Closed-loop wheel odometry for dead reckoning | ESP32 GPIO + Pi sensor fusion update |

### Planned for V2+

| Feature | Description | Impact |
|---------|-------------|--------|
| LiDAR Integration | 360-degree spatial scanning for advanced mapping | New sensor module + Pi integration |
| Thermal Imaging | Heat signature detection and tracking | New Pi vision module |
| Remote Operation Mode | Full teleoperation over WiFi from dashboard | Dashboard + Pi command mode |
| Multi-Rover Coordination | Swarm communication between multiple rovers | New Pi networking module |
| Cloud Telemetry | Push telemetry to a cloud backend for historical analysis | Dashboard communicator extension |

### Architecture Headroom

| Resource | Current Usage | Maximum | Headroom |
|----------|--------------|---------|----------|
| PCA9548A I2C Channels | 4 | 8 | 4 channels free |
| ESP32-S3 GPIO | ~15 | 45 | ~30 pins available |
| Serial Protocol Packet Types | 2 | Unlimited | Extensible by design |
| Pi USB Ports | 3 of 4 | 4 | 1 port free |

---

## 16. Conclusion

Recon Rover V1 is architected as a professional-grade, modular, and scalable robotics platform. Every design decision — from the strict separation of the Raspberry Pi and ESP32-S3 responsibilities, to the structured JSON telemetry protocol, to the PCA9548A I2C multiplexer strategy — has been made with long-term maintainability and extensibility as the primary constraint.

The **Hierarchical Dual-Processor Model** ensures that:

- Real-time hardware control is always deterministic, responsive, and isolated from cognitive failures.
- High-level intelligence, vision, and planning can evolve freely without impacting the hardware layer.
- The system remains fully observable through structured telemetry at every layer.
- New hardware, sensors, or capabilities can be integrated without refactoring the core architecture.

This document establishes the **canonical reference** for all future software, firmware, and protocol decisions on the Recon Rover V1 platform. All implementation work must align with the principles and boundaries defined here.

---

*End of Document*

---

> **Document Control**
>
> | Version | Date | Author | Notes |
> |---------|------|--------|-------|
> | 1.0 | 2026-06-28 | Lead Architect | Initial foundation draft |
