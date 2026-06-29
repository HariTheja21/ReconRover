# Recon Rover V1 — Software Architecture

**Document Version:** 1.0  
**Status:** Foundation Draft  
**Last Updated:** 2026-06-28  
**Author:** Lead Robotics Software Architect  
**Classification:** Internal Design Document  
**References:**
- `SYSTEM_ARCHITECTURE.md` — System-level architecture, design principles, communication philosophy
- `HARDWARE_ARCHITECTURE.md` — Hardware topology, GPIO map, power architecture, sensor placement

---

## Table of Contents

1. [Software Philosophy](#1-software-philosophy)
2. [Software Layers](#2-software-layers)
3. [Complete Software Stack](#3-complete-software-stack)
4. [Raspberry Pi Software Architecture](#4-raspberry-pi-software-architecture)
5. [ESP32 Software Architecture](#5-esp32-software-architecture)
6. [Shared Components](#6-shared-components)
7. [Module Responsibilities](#7-module-responsibilities)
8. [Boot Sequence](#8-boot-sequence)
9. [Runtime Sequence](#9-runtime-sequence)
10. [Communication Architecture](#10-communication-architecture)
11. [Thread Architecture](#11-thread-architecture)
12. [Task Scheduler](#12-task-scheduler)
13. [Data Flow](#13-data-flow)
14. [Telemetry Flow](#14-telemetry-flow)
15. [Command Flow](#15-command-flow)
16. [AI Pipeline](#16-ai-pipeline)
17. [Vision Pipeline](#17-vision-pipeline)
18. [Audio Pipeline](#18-audio-pipeline)
19. [Navigation Pipeline](#19-navigation-pipeline)
20. [Sensor Fusion Pipeline](#20-sensor-fusion-pipeline)
21. [OLED Rendering Pipeline](#21-oled-rendering-pipeline)
22. [LED Pipeline](#22-led-pipeline)
23. [Motor Control Pipeline](#23-motor-control-pipeline)
24. [Error Handling](#24-error-handling)
25. [Logging Strategy](#25-logging-strategy)
26. [Configuration Strategy](#26-configuration-strategy)
27. [Scalability Strategy](#27-scalability-strategy)
28. [Future Modules](#28-future-modules)
29. [Folder Responsibility Table](#29-folder-responsibility-table)
30. [Conclusion](#30-conclusion)

---

## 1. Software Philosophy

### The Governing Principle

> **The software architecture is a direct expression of the hardware architecture. The boundary that physically separates the Raspberry Pi from the ESP32-S3 in hardware is replicated exactly in software — two independent codebases, one serial protocol, zero shared state.**

The Recon Rover V1 software is not a monolith. It is a collection of purpose-bound modules, each with a clearly defined responsibility, a stable interface, and no hidden dependencies on the internals of its neighbours. Any module can be replaced, upgraded, or disabled without rewriting anything else.

### Core Software Tenets

| Tenet | Statement |
|-------|-----------|
| **Separation of Concerns** | Every module does exactly one thing. Vision does not navigate. Navigation does not render eyes. |
| **No Shared State Across the Serial Bridge** | The Raspberry Pi and ESP32 never share memory. All cross-processor state is serialised as JSON. |
| **Fail Independently** | A failure in any module must not propagate to other modules or crash the system. |
| **Structured Communication** | All inter-module and inter-processor messages are structured, typed, and timestamped. |
| **Observable by Default** | Every module emits logs and telemetry. No state is invisible. |
| **Configuration Over Hardcoding** | All tunable values live in configuration files, never in source code. |
| **Readable Over Clever** | Code is written for the next developer, not for the compiler. |

### What This Document Covers

This document describes the complete software architecture of Recon Rover V1. It covers both the Raspberry Pi (Python, Linux) codebase and the ESP32-S3 (C++, FreeRTOS) firmware, as well as the shared protocol specification and tooling layer.

This document does **not** contain application code, pseudocode, or implementation details. It defines architecture, module responsibilities, data flows, and design decisions.

---

## 2. Software Layers

The software stack consists of four distinct layers. Each layer communicates only with its immediate neighbours through defined interfaces.

```
+==================================================================+
|  LAYER 4 — EXTERNAL SYSTEMS                                      |
|  Live Dashboard  |  Remote Control  |  Log Viewer                |
|  (Browser / PC — communicates with Pi over WiFi)                 |
+==================================================================+
                             |
                    WebSocket / HTTP
                             |
+==================================================================+
|  LAYER 3 — COGNITIVE SOFTWARE  (Raspberry Pi 3B+)               |
|                                                                  |
|  AI Engine  |  Vision Pipeline  |  Audio Pipeline               |
|  Navigation |  Sensor Fusion    |  Dashboard Server              |
|  Decision Engine  |  Command Builder  |  Serial Manager          |
+==================================================================+
                             |
                  USB Serial — JSON Protocol
                             |
+==================================================================+
|  LAYER 2 — REACTIVE FIRMWARE  (ESP32-S3 N16R8 / FreeRTOS)       |
|                                                                  |
|  Sensor Manager  |  Motor Controller  |  Servo Controller        |
|  OLED Renderer   |  LED Controller    |  Telemetry Builder       |
|  Command Parser  |  Watchdog          |  Health Monitor          |
+==================================================================+
                             |
                   Hardware Abstraction
                             |
+==================================================================+
|  LAYER 1 — HARDWARE                                              |
|  HC-SR04 x4  |  VL53L0X x2  |  MPU6050  |  MQ-2  |  INA219     |
|  SSD1306 x2  |  SG90 x2     |  L298N    |  WS2812B x2           |
|  USB Webcam  |  USB Microphone                                   |
+==================================================================+
```

### Layer Responsibilities

| Layer | Processor | Language / Runtime | Responsibility |
|-------|-----------|--------------------|----------------|
| L4 — External | PC / Browser | Any | Display, monitor, optionally control |
| L3 — Cognitive | Raspberry Pi 3B+ | Python 3 / Linux | Intelligence, perception, planning, communication |
| L2 — Reactive | ESP32-S3 N16R8 | C++ / FreeRTOS | Real-time hardware I/O, actuation, telemetry |
| L1 — Hardware | Physical devices | — | Raw sensor signals and actuator response |

---

## 3. Complete Software Stack

### Raspberry Pi Software Stack

```
+------------------------------------------------------------------+
|  APPLICATION LAYER                                               |
|  main.py — Entry point, module orchestration, graceful shutdown  |
+------------------------------------------------------------------+
|  INTELLIGENCE LAYER                                              |
|  ai_engine.py       Decision making, mode management            |
|  vision_pipeline.py Object detection, tracking (OpenCV)         |
|  audio_pipeline.py  Voice capture, VAD, speech-to-text          |
+------------------------------------------------------------------+
|  PLANNING LAYER                                                  |
|  navigation.py      Path planning, obstacle avoidance            |
|  motion_planner.py  Motor command generation                     |
|  expression_selector.py  Eye expression logic                    |
+------------------------------------------------------------------+
|  FUSION LAYER                                                    |
|  sensor_fusion.py   Integrates all inbound telemetry data        |
|  world_model.py     Real-time spatial state representation       |
+------------------------------------------------------------------+
|  COMMUNICATION LAYER                                             |
|  serial_manager.py  USB serial read/write, JSON framing          |
|  dashboard_server.py WebSocket / HTTP server for dashboard       |
|  command_builder.py  Constructs and validates command packets    |
+------------------------------------------------------------------+
|  INFRASTRUCTURE LAYER                                            |
|  config.py          Loads and validates configuration            |
|  logger.py          Structured logging to file and console       |
|  event_bus.py       Internal pub/sub for inter-module events     |
+------------------------------------------------------------------+
|  RUNTIME PLATFORM                                                |
|  Python 3.x  |  asyncio  |  OpenCV  |  TFLite  |  Linux OS      |
+------------------------------------------------------------------+
```

### ESP32-S3 Firmware Stack

```
+------------------------------------------------------------------+
|  APPLICATION LAYER                                               |
|  main.cpp — Entry point, task spawning, system initialisation   |
+------------------------------------------------------------------+
|  SUBSYSTEM LAYER                                                 |
|  sensor_manager.cpp  Polls all sensors on schedule              |
|  motor_controller.cpp  L298N PWM drive, direction logic         |
|  servo_controller.cpp  LEDC PWM, angle validation               |
|  oled_renderer.cpp     PCA9548A channel switching, SSD1306 draw |
|  led_controller.cpp    WS2812B strip management                  |
+------------------------------------------------------------------+
|  COMMUNICATION LAYER                                             |
|  serial_handler.cpp  USB CDC read/write, line framing           |
|  telemetry_builder.cpp  Packs sensor data to JSON               |
|  command_parser.cpp   Validates and dispatches command packets  |
+------------------------------------------------------------------+
|  DRIVER LAYER                                                    |
|  driver_hcsr04.cpp   Ultrasonic pulse timing                    |
|  driver_vl53l0x.cpp  VL53L0X I2C driver wrapper                |
|  driver_mpu6050.cpp  MPU6050 register interface                 |
|  driver_mq2.cpp      ADC read, voltage conversion               |
|  driver_ina219.cpp   INA219 I2C driver (planned)                |
|  driver_pca9548a.cpp PCA9548A channel selector                  |
+------------------------------------------------------------------+
|  INFRASTRUCTURE LAYER                                            |
|  config.h            Compile-time and runtime configuration     |
|  watchdog.cpp        FreeRTOS task watchdog, reboot guard       |
|  health_monitor.cpp  Sensor fault detection and reporting       |
+------------------------------------------------------------------+
|  RUNTIME PLATFORM                                                |
|  FreeRTOS  |  ESP-IDF  |  C++17  |  LEDC  |  I2C  |  ADC       |
+------------------------------------------------------------------+
```

### PC / Dashboard Stack

```
+------------------------------------------------------------------+
|  PRESENTATION LAYER                                              |
|  Live sensor graphs  |  Camera feed  |  Event log  |  Controls  |
+------------------------------------------------------------------+
|  DATA LAYER                                                      |
|  WebSocket client  |  JSON telemetry parser                     |
+------------------------------------------------------------------+
|  RUNTIME PLATFORM                                                |
|  Browser / Electron / Python  (implementation defined in V1.x)  |
+------------------------------------------------------------------+
```

---

## 4. Raspberry Pi Software Architecture

The Raspberry Pi software runs on Linux as a set of concurrent Python modules coordinated by an asynchronous event loop. Modules are loosely coupled through an internal event bus and communicate with the ESP32-S3 exclusively through the serial manager.

### Module Map

```
+------------------------------------------------------------------+
|  main.py                                                         |
|  Bootstraps all modules. Manages startup order and shutdown.     |
|         |                                                        |
|   +-----+-----+--------+----------+----------+-----------+      |
|   |           |        |          |          |           |      |
| [Vision]  [Audio]  [Serial]  [Sensor   [AI        [Dashboard]  |
| Pipeline  Pipeline  Manager  Fusion]   Engine]    Server]      |
|   |           |        |          |          |           |      |
|   |           |        v          v          |           |      |
|   |           |   [Telemetry  [World     [Decision      |      |
|   |           |    Receiver]   Model]     Engine]       |      |
|   |           |                   |          |          |      |
|   +-----------+-------------------+----------+          |      |
|                          |                              |      |
|                  [Navigation /              [Command    |      |
|                   Motion Planner]            Builder]   |      |
|                          |                      |       |      |
|                          +----------+-----------+       |      |
|                                     |                   |      |
|                             [Serial Manager] ----------+      |
|                             (sends commands to ESP32)         |
+------------------------------------------------------------------+
```

### Module Dependency Graph

```
main.py
  |-- config.py              (no dependencies)
  |-- logger.py              (no dependencies)
  |-- event_bus.py           (no dependencies)
  |-- serial_manager.py      (config, logger, event_bus)
  |-- vision_pipeline.py     (config, logger, event_bus)
  |-- audio_pipeline.py      (config, logger, event_bus)
  |-- sensor_fusion.py       (config, logger, event_bus, world_model)
  |-- world_model.py         (config, logger)
  |-- ai_engine.py           (config, logger, event_bus, world_model)
  |-- navigation.py          (config, logger, event_bus, world_model)
  |-- motion_planner.py      (config, logger, event_bus)
  |-- expression_selector.py (config, logger, event_bus, ai_engine)
  |-- command_builder.py     (config, logger)
  |-- dashboard_server.py    (config, logger, event_bus)
```

### Asynchronous Execution Model

The Raspberry Pi software is built on Python `asyncio`. Each functional module runs as a coroutine or a concurrent thread that feeds events into the shared event bus. This prevents any single module from blocking the others, which is critical given the concurrent demands of vision inference, audio processing, serial I/O, and dashboard streaming.

| Module | Execution Model | Reason |
|--------|----------------|--------|
| vision_pipeline | Thread (blocking OpenCV) | OpenCV frame capture is blocking |
| audio_pipeline | Thread (blocking audio stream) | Audio capture is blocking |
| serial_manager | asyncio coroutine | Async serial read/write |
| sensor_fusion | asyncio coroutine | Event-driven, non-blocking |
| ai_engine | asyncio coroutine | Event-driven decision making |
| navigation | asyncio coroutine | Reacts to world model updates |
| dashboard_server | asyncio coroutine | WebSocket async I/O |
| logger | Thread-safe queue | Must never block callers |

---

## 5. ESP32 Software Architecture

The ESP32-S3 firmware runs on FreeRTOS. Each subsystem is implemented as an independent FreeRTOS task pinned to a specific CPU core. Tasks communicate through FreeRTOS queues and semaphores. No shared global variables are used between tasks.

### Task Map

```
+------------------------------------------------------------------+
|  ESP32-S3 FreeRTOS Task Layout                                   |
|                                                                  |
|  Core 0                          Core 1                         |
|  +--------------------------+    +---------------------------+   |
|  | Task: sensor_manager     |    | Task: serial_handler      |  |
|  | Priority: HIGH           |    | Priority: HIGH            |  |
|  | Period: 50 ms (20 Hz)    |    | Mode: Event-driven        |  |
|  +--------------------------+    +---------------------------+   |
|  | Task: telemetry_builder  |    | Task: command_parser      |  |
|  | Priority: NORMAL         |    | Priority: NORMAL          |  |
|  | Triggered by sensor task |    | Triggered by serial task  |  |
|  +--------------------------+    +---------------------------+   |
|  | Task: health_monitor     |    | Task: motor_controller    |  |
|  | Priority: LOW            |    | Priority: HIGH            |  |
|  | Period: 1000 ms (1 Hz)   |    | Mode: Command-driven      |  |
|  +--------------------------+    +---------------------------+   |
|  | Task: watchdog           |    | Task: servo_controller    |  |
|  | Priority: HIGHEST        |    | Priority: NORMAL          |  |
|  | Period: 100 ms           |    | Mode: Command-driven      |  |
|  +--------------------------+    +---------------------------+   |
|                                  | Task: oled_renderer       |  |
|                                  | Priority: LOW             |  |
|                                  | Mode: Command-driven      |  |
|                                  +---------------------------+   |
|                                  | Task: led_controller      |  |
|                                  | Priority: LOW             |  |
|                                  | Mode: Command-driven      |  |
|                                  +---------------------------+   |
+------------------------------------------------------------------+
```

### Inter-Task Communication

```
sensor_manager
    |-- [Sensor Queue] --> telemetry_builder --> [TX Queue] --> serial_handler
    |-- [Health Queue] --> health_monitor

serial_handler (RX)
    |-- [Command Queue] --> command_parser
                               |-- [Motor Queue]  --> motor_controller
                               |-- [Servo Queue]  --> servo_controller
                               |-- [Eye Queue]    --> oled_renderer
                               |-- [LED Queue]    --> led_controller

watchdog
    |-- Monitors all task heartbeats
    |-- Triggers safe stop if any critical task misses its deadline
```

### FreeRTOS Task Priority Levels

| Priority Level | Tasks | Rationale |
|---------------|-------|-----------|
| HIGHEST (5) | Watchdog | Must always run; safety-critical |
| HIGH (4) | sensor_manager, serial_handler, motor_controller | Real-time I/O |
| NORMAL (3) | telemetry_builder, command_parser, servo_controller | Processing tasks |
| LOW (2) | oled_renderer, led_controller, health_monitor | Non-critical output |
| IDLE (1) | FreeRTOS idle task | Background cleanup |

---

## 6. Shared Components

The `SHARED/` folder contains assets and specifications that are owned by neither the Pi nor the ESP32 exclusively, but are required by both.

### Shared Protocol Specification

The JSON serial protocol schema is the contract between the Raspberry Pi and the ESP32-S3. It is the single most critical shared component. Any change to the protocol must be reflected in both codebases simultaneously.

**See Section 10 — Communication Architecture for full packet specifications.**

### Shared Configuration Schema

While each processor maintains its own configuration file, the protocol-level field names and telemetry key names are shared. These are documented in `SHARED/` and must not be changed unilaterally.

### Shared Expression Registry

The OLED eye expression identifiers (e.g., `"idle"`, `"happy"`, `"alert"`) must be consistent between:

- The Raspberry Pi's `expression_selector.py` (which chooses the ID).
- The ESP32-S3's `oled_renderer.cpp` (which looks up the bitmap).

The canonical list of valid expression IDs is maintained in `SHARED/`.

### Shared Folder Contents

| Item | Description |
|------|-------------|
| `protocol_spec.md` | Canonical JSON packet schema for telemetry and commands |
| `expression_registry.md` | Complete list of valid OLED eye expression identifiers |
| `error_codes.md` | Shared error code registry used in telemetry health fields |
| `led_modes.md` | Canonical LED mode identifier list |

---

## 7. Module Responsibilities

### Raspberry Pi Modules

| Module | File | Single Responsibility |
|--------|------|-----------------------|
| Main | `main.py` | Bootstraps all modules, manages startup order and graceful shutdown |
| Config | `config.py` | Loads, validates, and exposes all configuration values |
| Logger | `logger.py` | Thread-safe structured logging to console and rotating log files |
| Event Bus | `event_bus.py` | Internal publish/subscribe system for inter-module event passing |
| Serial Manager | `serial_manager.py` | Owns the USB serial port; reads telemetry, writes commands |
| Vision Pipeline | `vision_pipeline.py` | Frame capture, object detection, object tracking |
| Audio Pipeline | `audio_pipeline.py` | Microphone capture, VAD, speech-to-text, command dispatch |
| Sensor Fusion | `sensor_fusion.py` | Integrates ESP32 telemetry into the world model |
| World Model | `world_model.py` | Thread-safe spatial state object accessed by all modules |
| AI Engine | `ai_engine.py` | High-level decision making, behavioural mode management |
| Navigation | `navigation.py` | Obstacle avoidance, path selection, motor command generation |
| Motion Planner | `motion_planner.py` | Translates navigation intent into motor speed and direction values |
| Expression Selector | `expression_selector.py` | Maps AI context to OLED eye expression identifiers |
| Command Builder | `command_builder.py` | Constructs and validates outgoing JSON command packets |
| Dashboard Server | `dashboard_server.py` | WebSocket/HTTP server; streams telemetry to the dashboard |

### ESP32-S3 Modules

| Module | File | Single Responsibility |
|--------|------|-----------------------|
| Main | `main.cpp` | Initialises hardware, spawns all FreeRTOS tasks |
| Sensor Manager | `sensor_manager.cpp` | Periodically reads all sensors; deposits data to sensor queue |
| Telemetry Builder | `telemetry_builder.cpp` | Serialises sensor data to JSON telemetry packet |
| Serial Handler | `serial_handler.cpp` | Owns USB CDC; reads command packets, writes telemetry packets |
| Command Parser | `command_parser.cpp` | Validates incoming JSON; dispatches to per-subsystem queues |
| Motor Controller | `motor_controller.cpp` | Translates motor commands to L298N PWM and direction signals |
| Servo Controller | `servo_controller.cpp` | Translates servo angle commands to LEDC PWM pulse widths |
| OLED Renderer | `oled_renderer.cpp` | Manages PCA9548A channel switching; renders eye bitmaps to SSD1306 |
| LED Controller | `led_controller.cpp` | Drives WS2812B strips with mode-based colour and pattern logic |
| Health Monitor | `health_monitor.cpp` | Detects sensor faults; updates health flags in telemetry |
| Watchdog | `watchdog.cpp` | Monitors critical task heartbeats; triggers safe stop on timeout |
| Driver: HC-SR04 | `driver_hcsr04.cpp` | GPIO TRIG/ECHO timing, distance calculation |
| Driver: VL53L0X | `driver_vl53l0x.cpp` | I2C read via PCA9548A channel, distance extraction |
| Driver: MPU6050 | `driver_mpu6050.cpp` | I2C register read, raw IMU data conversion |
| Driver: MQ-2 | `driver_mq2.cpp` | ADC read, voltage-to-concentration conversion |
| Driver: INA219 | `driver_ina219.cpp` | I2C read, voltage/current extraction (planned) |
| Driver: PCA9548A | `driver_pca9548a.cpp` | I2C channel select/deselect logic |

---

## 8. Boot Sequence

### Raspberry Pi Boot Sequence

```
POWER ON
    |
    v
[Linux OS Boots]
    |
    v
[main.py starts]
    |
    +---> [1] Load config.py
    |         Read rover.yaml
    |         Validate all required fields
    |         Abort if critical fields missing
    |
    +---> [2] Initialise logger.py
    |         Open log file with timestamp
    |         Set log level from config
    |
    +---> [3] Initialise event_bus.py
    |         Register all topic channels
    |
    +---> [4] Initialise serial_manager.py
    |         Open USB serial port (from config)
    |         Wait for ESP32 READY packet (timeout: 10s)
    |         If timeout: log CRITICAL, retry or exit
    |
    +---> [5] Initialise sensor_fusion.py + world_model.py
    |         Reset spatial state to defaults
    |
    +---> [6] Initialise vision_pipeline.py
    |         Open USB webcam (from config)
    |         Load detection model weights
    |         Start frame capture thread
    |
    +---> [7] Initialise audio_pipeline.py
    |         Open USB microphone (from config)
    |         Start audio capture thread
    |
    +---> [8] Initialise ai_engine.py
    |         Set initial mode: IDLE
    |         Subscribe to events: detection, telemetry, voice_command
    |
    +---> [9] Initialise navigation.py + motion_planner.py
    |         Set movement state: STOPPED
    |
    +---> [10] Initialise dashboard_server.py
    |          Start WebSocket server on configured port
    |          Begin broadcasting telemetry
    |
    +---> [11] Send BOOT_COMPLETE event on event_bus
    |
    v
[RUNNING STATE — asyncio event loop active]
```

### ESP32-S3 Boot Sequence

```
POWER ON
    |
    v
[ESP32 Reset Vector]
    |
    v
[FreeRTOS Scheduler Starts]
    |
    v
[main.cpp app_main()]
    |
    +---> [1] Initialise NVS (non-volatile storage)
    |
    +---> [2] Load config.h constants
    |
    +---> [3] Initialise I2C bus
    |         GPIO13 (SDA), GPIO14 (SCL) at 400 kHz
    |
    +---> [4] Initialise PCA9548A driver
    |         Deselect all channels (write 0x00)
    |         Verify I2C acknowledge from 0x70
    |
    +---> [5] Initialise all sensors (sequential)
    |         MPU6050: configure, self-test
    |         VL53L0X (CH2): configure ranging mode
    |         VL53L0X (CH3): configure ranging mode
    |         HC-SR04: configure GPIO pins
    |         MQ-2: configure ADC channel
    |
    +---> [6] Initialise OLEDs
    |         CH0 -> SSD1306 Left: clear, display boot animation
    |         CH1 -> SSD1306 Right: clear, display boot animation
    |
    +---> [7] Initialise WS2812B LED strips
    |         Play startup sweep animation
    |
    +---> [8] Initialise motor controller
    |         Set all motors to STOP (brake state)
    |
    +---> [9] Initialise servo controller
    |         Move Pan to centre (90 deg)
    |         Move Tilt to neutral (90 deg)
    |
    +---> [10] Initialise USB serial (CDC)
    |          Open CDC UART at configured baud
    |
    +---> [11] Spawn FreeRTOS tasks
    |          watchdog         Core 0, Priority 5
    |          sensor_manager   Core 0, Priority 4
    |          serial_handler   Core 1, Priority 4
    |          motor_controller Core 1, Priority 4
    |          telemetry_builder Core 0, Priority 3
    |          command_parser   Core 1, Priority 3
    |          servo_controller Core 1, Priority 3
    |          oled_renderer    Core 1, Priority 2
    |          led_controller   Core 1, Priority 2
    |          health_monitor   Core 0, Priority 2
    |
    +---> [12] Transmit READY packet over serial
    |
    v
[RUNNING STATE — FreeRTOS scheduler owns execution]
```

---

## 9. Runtime Sequence

### Steady-State Runtime Loop

Once both processors are running, the system operates in continuous interleaved loops:

```
ESP32-S3 (Reactive Loop — 20 Hz)          Raspberry Pi (Cognitive Loop — 10 Hz)
-----------------------------------------  ----------------------------------------
sensor_manager polls all sensors           serial_manager reads incoming telemetry
    |                                          |
    v                                          v
telemetry_builder packs JSON               sensor_fusion updates world_model
    |                                          |
    v                                          v
serial_handler transmits packet  --------> vision_pipeline processes latest frame
                                               |
                                               v
command_parser receives packet  <--------- ai_engine evaluates world state
    |                                          |
    v                                          v
motor/servo/oled/led controllers act       navigation generates motor commands
                                               |
                                               v
                                           command_builder builds JSON packet
                                               |
                                               v
                                           serial_manager transmits command
                                               |
                                               v
                                           dashboard_server broadcasts telemetry
```

### Behavioural Mode State Machine

The AI engine manages the rover's top-level behavioural mode. Mode transitions drive expression and LED selections.

```
              [BOOT]
                |
                v
+----------> [IDLE] <----------+
|               |              |
|    voice:patrol or auto      |
|               v              |
|         [PATROLLING]         |
|          |       |           |
|   obstacle    object         |
|   detected    detected       |
|       v           v          |
|  [AVOIDING]   [TRACKING]     |
|       |           |          |
| clear path   object lost     |
|       |           |          |
+-------+    [SEARCHING]       |
                 |             |
           timeout/clear       |
                 |             |
                 +-------------+
                 
  [HAZARD] can interrupt any state
  [ERROR]  can interrupt any state
  [SHUTDOWN] terminates all states
```

---

## 10. Communication Architecture

### The Serial Bridge Contract

All cross-processor communication is via a single USB serial link. This is the **only** data channel between the Raspberry Pi and the ESP32-S3. See `SYSTEM_ARCHITECTURE.md` Section 11 for the full design rationale.

```
Raspberry Pi                          ESP32-S3
    |                                     |
    |   Telemetry packet (ESP32->Pi)      |
    | <-----------------------------------+
    |                                     |
    |   Command packet (Pi->ESP32)        |
    +-----------------------------------> |
    |                                     |
    | (packets are newline-delimited JSON)|
```

### Telemetry Packet Structure (ESP32 -> Pi)

```
{
  "type": "telemetry",
  "ts": <uint32 milliseconds since ESP32 boot>,
  "ultrasonic": {
    "front": <int cm>,
    "left":  <int cm>,
    "right": <int cm>,
    "rear":  <int cm>
  },
  "tof": {
    "front": <int mm>,
    "pan":   <int mm>
  },
  "imu": {
    "ax": <float m/s2>,
    "ay": <float m/s2>,
    "az": <float m/s2>,
    "gx": <float deg/s>,
    "gy": <float deg/s>,
    "gz": <float deg/s>
  },
  "gas": {
    "raw":    <int ADC counts>,
    "hazard": <bool>
  },
  "power": {
    "voltage": <float V>,
    "current": <float A>
  },
  "health": {
    "imu_ok":   <bool>,
    "tof_f_ok": <bool>,
    "tof_p_ok": <bool>,
    "gas_ok":   <bool>,
    "pwr_ok":   <bool>
  }
}
```

### Command Packet Structure (Pi -> ESP32)

```
{
  "type": "cmd",
  "ts": <uint32 milliseconds since Pi boot>,
  "motors": {
    "fl": <int -100 to 100>,
    "fr": <int -100 to 100>,
    "rl": <int -100 to 100>,
    "rr": <int -100 to 100>
  },
  "servos": {
    "pan":  <int 0-180 degrees>,
    "tilt": <int 0-180 degrees>
  },
  "eyes": {
    "expression": <string — see SHARED/expression_registry.md>
  },
  "leds": {
    "mode":  <string — see SHARED/led_modes.md>,
    "color": [<int R>, <int G>, <int B>]
  }
}
```

### Acknowledgement Packet Structure (ESP32 -> Pi)

```
{
  "type": "ack",
  "ts":  <uint32>,
  "ref_ts": <uint32 — echoes the command ts>,
  "status": "ok" | "err",
  "msg": <string — optional error description>
}
```

### Special Packets

| Packet Type | Direction | Purpose |
|------------|-----------|---------|
| `"ready"` | ESP32 -> Pi | Sent once after ESP32 boot completes |
| `"heartbeat"` | Bidirectional | Sent every 1 s; proves link is alive |
| `"fault"` | ESP32 -> Pi | Immediate alert for critical hardware event |
| `"shutdown"` | Pi -> ESP32 | Graceful stop all actuators |

### Serial Protocol Rules

| Rule | Detail |
|------|--------|
| Encoding | UTF-8 JSON |
| Framing | One JSON object per line, terminated with `\n` |
| Baud rate | 115200 minimum; 921600 preferred |
| Max packet size | 512 bytes (telemetry), 256 bytes (command) |
| Unknown packet type | Silently ignored by receiver |
| Malformed packet | Logged and discarded; no exception propagation |

### Dashboard Communication (Pi -> Browser)

The Raspberry Pi hosts a WebSocket server on a configurable port (default: 8765). The dashboard connects as a client and receives a continuous stream of enriched telemetry at 10 Hz, plus event notifications on state changes.

| Topic | Rate | Content |
|-------|------|---------|
| `telemetry` | 10 Hz | Merged sensor data + vision detections |
| `event` | On-change | Mode transitions, faults, voice commands |
| `log` | On-write | Selected log entries for dashboard log panel |
| `video` | Optional | MJPEG or WebRTC frame stream from webcam |

---

## 11. Thread Architecture

### Raspberry Pi Thread Map

```
PROCESS: rover_main
    |
    +--- [Main Thread] asyncio event loop
    |       Runs: serial_manager, sensor_fusion, ai_engine,
    |             navigation, command_builder, dashboard_server
    |
    +--- [Thread: vision_capture]
    |       Blocking OpenCV VideoCapture.read()
    |       Posts frames to vision queue
    |       Thread-safe frame buffer (latest-frame pattern)
    |
    +--- [Thread: vision_inference]
    |       Consumes frames from vision queue
    |       Runs object detection model
    |       Posts detection results to event_bus
    |
    +--- [Thread: audio_capture]
    |       Blocking microphone stream read
    |       Posts audio chunks to audio queue
    |
    +--- [Thread: audio_inference]
    |       Consumes audio chunks
    |       Runs VAD + STT
    |       Posts voice commands to event_bus
    |
    +--- [Thread: file_logger]
    |       Consumes from log queue
    |       Writes to rotating log files
    |       Never blocks callers
    |
    +--- [Thread: dashboard_ws]
            WebSocket server coroutine pool
            Handles client connections
```

### ESP32-S3 Task Map

```
RTOS SCHEDULER
    |
    +--- Core 0
    |       [watchdog]          Priority 5 — 100 ms
    |       [sensor_manager]    Priority 4 — 50 ms
    |       [telemetry_builder] Priority 3 — triggered by sensor_manager
    |       [health_monitor]    Priority 2 — 1000 ms
    |
    +--- Core 1
            [serial_handler]    Priority 4 — event-driven
            [motor_controller]  Priority 4 — event-driven (queue)
            [command_parser]    Priority 3 — event-driven
            [servo_controller]  Priority 3 — event-driven (queue)
            [oled_renderer]     Priority 2 — event-driven (queue)
            [led_controller]    Priority 2 — event-driven (queue)
```

### Thread Safety Rules

| Rule | Applies To |
|------|-----------|
| All shared data structures are protected by asyncio locks or threading.Lock | Raspberry Pi |
| The world_model object uses a read/write lock pattern | Raspberry Pi |
| All inter-task communication uses FreeRTOS queues — no shared globals | ESP32-S3 |
| Sensor data is double-buffered — one buffer for write, one for read | ESP32-S3 |
| The serial TX path uses a dedicated FreeRTOS queue to prevent concurrent writes | ESP32-S3 |

---

## 12. Task Scheduler

### Raspberry Pi Scheduling Model

The Raspberry Pi uses Python `asyncio` as its cooperative scheduler for non-blocking tasks, supplemented by `threading.Thread` for blocking I/O. The asyncio loop runs at full speed; coroutines yield control with `await`.

| Scheduled Task | Trigger | Target Rate |
|---------------|---------|------------|
| serial_manager.read_loop | asyncio — continuous | As fast as data arrives |
| sensor_fusion.process | event_bus: telemetry_received | 20 Hz (driven by ESP32) |
| ai_engine.evaluate | event_bus: world_model_updated | 10 Hz |
| navigation.compute | event_bus: ai_decision | 10 Hz |
| dashboard_server.broadcast | asyncio — periodic | 10 Hz |
| vision_pipeline (capture thread) | Thread — continuous | Camera frame rate |
| vision_pipeline (inference thread) | Thread — continuous | Model throughput |
| audio_pipeline (capture thread) | Thread — continuous | Audio sample rate |
| audio_pipeline (inference thread) | Thread — on VAD trigger | On speech detection |

### ESP32-S3 Scheduling Model

The ESP32-S3 uses FreeRTOS tick-based preemptive scheduling. Each task runs at a fixed period or is event-driven via queue.

| Task | Core | Priority | Period | Mode |
|------|------|----------|--------|------|
| watchdog | 0 | 5 | 100 ms | Periodic |
| sensor_manager | 0 | 4 | 50 ms | Periodic |
| serial_handler | 1 | 4 | — | Event (CDC RX interrupt) |
| motor_controller | 1 | 4 | — | Event (queue) |
| telemetry_builder | 0 | 3 | — | Triggered by sensor_manager |
| command_parser | 1 | 3 | — | Event (queue from serial) |
| servo_controller | 1 | 3 | — | Event (queue) |
| oled_renderer | 1 | 2 | — | Event (queue) |
| led_controller | 1 | 2 | — | Event (queue) |
| health_monitor | 0 | 2 | 1000 ms | Periodic |

### HC-SR04 Time-Multiplexed Firing Schedule

The four HC-SR04 sensors are fired sequentially — never simultaneously — to prevent acoustic crosstalk. The sensor_manager fires each sensor in round-robin order with a 10 ms inter-sensor delay.

```
t=0ms    Fire FRONT  HC-SR04 -> wait for ECHO
t=10ms   Fire LEFT   HC-SR04 -> wait for ECHO
t=20ms   Fire RIGHT  HC-SR04 -> wait for ECHO
t=30ms   Fire REAR   HC-SR04 -> wait for ECHO
t=40ms   All four readings complete -> pack telemetry
t=50ms   Cycle repeats (20 Hz)
```

---

## 13. Data Flow

### Complete Data Flow Diagram

```
HARDWARE (Layer 1)
    HC-SR04 x4       VL53L0X x2      MPU6050     MQ-2     INA219
        |                 |              |           |         |
        +--------+--------+--------------+-----------+---------+
                 |
        [sensor_manager — ESP32, 20 Hz]
                 |
        [telemetry_builder — ESP32]
         Pack all readings into JSON telemetry packet
                 |
        [serial_handler TX — ESP32]
         Transmit over USB Serial
                 |
                 |  USB Serial (physical)
                 |
        [serial_manager RX — Raspberry Pi]
         Receive and deserialise JSON packet
                 |
        [sensor_fusion — Raspberry Pi]
         Validate + integrate into world model
                 |
        [world_model — Raspberry Pi]
         Thread-safe spatial state object
                 |
         +-------+-------+----------+
         |               |          |
   [navigation]    [ai_engine]  [dashboard_server]
   Obstacle         Decision     Broadcast to
   avoidance        making       dashboard
         |               |
   [motion_planner] [expression_selector]
   Motor speeds      Eye expression ID
         |               |
   [command_builder] builds unified JSON command packet
                 |
        [serial_manager TX — Raspberry Pi]
         Transmit command over USB Serial
                 |
        [serial_handler RX — ESP32]
         Receive and deserialise command packet
                 |
        [command_parser — ESP32]
         Dispatch to subsystem queues
                 |
    +------+------+------+------+
    |      |      |      |      |
[motor] [servo] [oled] [led] (future subsystems)
    |      |      |      |
 L298N   SG90  SSD1306  WS2812B
(motors)(servos)(eyes)  (strips)

USB Webcam --> [vision_pipeline] --> event_bus --> [ai_engine]
USB Mic    --> [audio_pipeline]  --> event_bus --> [ai_engine]
```

---

## 14. Telemetry Flow

### ESP32 to Raspberry Pi (Hardware Telemetry)

```
[sensor_manager polls at 20 Hz]
    |
    | HC-SR04: front=35cm, left=80cm, right=72cm, rear=120cm
    | VL53L0X: front=33mm, pan=77mm
    | MPU6050: ax=0.02, ay=-0.01, az=9.81, gx=0.1 gy=0.0, gz=0.0
    | MQ-2: raw=215, hazard=false
    | health: all_ok=true
    |
    v
[telemetry_builder serialises to JSON]
    |
    v
[serial_handler writes line to USB CDC TX buffer]
    |
    v
[USB Serial cable — physical transmission]
    |
    v
[serial_manager.read_loop — Raspberry Pi receives line]
    |
    v
[JSON deserialised to Python dict]
    |
    v
[Event published on event_bus: topic="telemetry_received", data=packet]
    |
    v
[sensor_fusion.process() consumes event]
    |  Validates all fields
    |  Updates world_model distances, orientation, gas level
    |  Timestamps the update
    |
    v
[Event published: topic="world_model_updated"]
    |
    +---> [navigation] re-evaluates safe movement
    +---> [ai_engine]  re-evaluates behavioural mode
    +---> [dashboard_server] queues for next broadcast
```

### Raspberry Pi to Dashboard (Enriched Telemetry)

```
[dashboard_server periodic broadcast — 10 Hz]
    |
    | Collects from world_model:  sensor distances, IMU, gas, power
    | Collects from ai_engine:    current mode, last decision
    | Collects from vision:       latest detection list
    | Collects from audio:        last voice command (if recent)
    |
    v
[Merged telemetry dict serialised to JSON]
    |
    v
[WebSocket broadcast to all connected dashboard clients]
    |
    v
[Dashboard renders: sensor graphs, map overlay, camera feed, event log]
```

---

## 15. Command Flow

### Raspberry Pi to ESP32 (Command)

```
[ai_engine determines action needed]
    |
    | Decision: rover should move forward at 70% speed
    | Decision: camera should pan 15 degrees right
    | Decision: eyes should show "curious" expression
    | Decision: LEDs should pulse yellow (tracking mode)
    |
    v
[navigation -> motion_planner]
    Converts intent to motor values:
    fl=70, fr=70, rl=70, rr=70
    |
    v
[expression_selector]
    AI context -> "curious" expression ID
    |
    v
[command_builder]
    Assembles all fields into unified command packet
    Validates all values are in safe ranges
    Adds timestamp
    |
    v
[serial_manager.write()]
    Serialises dict to JSON string
    Appends newline
    Writes to USB serial TX buffer
    |
    v
[USB Serial — physical transmission]
    |
    v
[serial_handler.read_loop — ESP32]
    Receives complete line (newline-terminated)
    |
    v
[command_parser]
    JSON deserialised
    Packet type validated as "cmd"
    All fields range-checked
    |
    +-- motors: {fl:70, fr:70, rl:70, rr:70}
    |       -> enqueued to [motor_controller queue]
    |
    +-- servos: {pan:105, tilt:90}
    |       -> enqueued to [servo_controller queue]
    |
    +-- eyes: {expression:"curious"}
    |       -> enqueued to [oled_renderer queue]
    |
    +-- leds: {mode:"pulse", color:[255,200,0]}
            -> enqueued to [led_controller queue]
    |
    v
[ACK packet sent to Pi]
    {type:"ack", ref_ts:<command_ts>, status:"ok"}
```

---

## 16. AI Pipeline

The AI engine is the central decision-making component of the Raspberry Pi. It consumes observations from the world model, vision pipeline, and audio pipeline, and produces behavioural decisions.

### AI Engine Inputs

| Input Source | Data | Rate |
|-------------|------|------|
| world_model | Obstacle distances, IMU orientation, gas level, power | 20 Hz |
| vision_pipeline | Object detections (class, confidence, bounding box, depth) | Camera fps |
| audio_pipeline | Voice command strings | On detection |
| dashboard | Manual override commands (optional) | On user input |

### AI Engine Outputs

| Output | Consumer | Examples |
|--------|---------|---------|
| Behavioural mode | navigation, expression_selector, LED mode | IDLE, PATROLLING, TRACKING, HAZARD |
| Navigation intent | navigation | Move forward, turn left, stop |
| Eye expression ID | expression_selector -> command_builder | idle, curious, happy, alert |
| LED mode | command_builder | patrol, tracking, hazard, error |

### Decision Logic Flow

```
[world_model_updated event]
    |
    v
[ai_engine.evaluate()]
    |
    +---> Check gas hazard flag
    |       If true -> transition to HAZARD mode
    |       Emit: stop motors, hazard LED, eyes=hazard
    |
    +---> Check obstacle distances
    |       If front < safety_threshold -> obstacle avoidance needed
    |       Emit: avoidance intent to navigation
    |
    +---> Check vision detections
    |       If target class detected (e.g., person)
    |         -> transition to TRACKING mode
    |         -> emit: track target, eyes=curious, LEDs=tracking
    |       Else if no detections
    |         -> remain PATROLLING or IDLE
    |
    +---> Check voice commands (from event_bus)
    |       "patrol"   -> transition to PATROLLING
    |       "stop"     -> transition to IDLE
    |       "come here" -> transition to APPROACH
    |
    +---> Check power level (from world_model)
    |       If voltage < warning_threshold -> emit low battery event
    |
    v
[Emit decision event on event_bus]
    topic="ai_decision"
    data={mode, intent, expression, led_mode}
```

---

## 17. Vision Pipeline

The vision pipeline runs entirely on the Raspberry Pi. It is responsible for continuous frame capture, object detection, and object tracking.

### Pipeline Stages

```
[USB Webcam — hardware]
    |
    v
[STAGE 1: Frame Capture Thread]
    OpenCV VideoCapture.read()
    Captures raw BGR frame
    Resizes to inference resolution (e.g., 320x240)
    Deposits to latest-frame buffer (thread-safe overwrite)
    Rate: camera frame rate (target 15-30 fps)
    |
    v
[STAGE 2: Pre-Processing]
    Normalise pixel values
    Convert colour space if required by model
    Apply any undistortion (future)
    |
    v
[STAGE 3: Object Detection (Inference Thread)]
    Run detection model (TFLite / YOLO / MobileNet SSD)
    Output: list of {class_id, confidence, bbox [x, y, w, h]}
    Filter by confidence threshold (from config)
    Rate: model-dependent (target 5-15 fps on Pi 3B+)
    |
    v
[STAGE 4: Depth Estimation]
    For each detection, estimate distance using:
      - Pan ToF reading (if detection is near camera centre)
      - Bounding box area heuristic (fallback)
    Annotate each detection with estimated depth
    |
    v
[STAGE 5: Object Tracking]
    Assign tracker IDs to detections (simple centroid or CSRT)
    Maintain track history for continuity between inference frames
    |
    v
[STAGE 6: Result Publication]
    Publish event: topic="detections_updated"
    data = list of TrackedObject records
    Consumed by: ai_engine, dashboard_server, expression_selector
```

### Object Detection Model Strategy

| Strategy | Model | Use Case |
|----------|-------|---------|
| V1 baseline | MobileNet SSD (TFLite, COCO) | General object detection, low latency |
| V1 upgrade | YOLOv5n (TFLite) | Better accuracy, similar latency |
| V2 option | YOLOv8n (TFLite) | Best balance of accuracy and speed |

Model selection is configuration-driven. Swapping models requires only a config change and model file replacement.

---

## 18. Audio Pipeline

The audio pipeline runs on the Raspberry Pi. It is responsible for capturing microphone audio, detecting speech, and transcribing voice commands.

### Pipeline Stages

```
[USB Microphone — hardware]
    |
    v
[STAGE 1: Audio Capture Thread]
    PyAudio or sounddevice stream
    Captures raw PCM chunks (e.g., 16 kHz, 16-bit mono)
    Deposits to audio queue (ring buffer)
    |
    v
[STAGE 2: Voice Activity Detection (VAD)]
    Analyse energy level / spectral features
    Trigger: if speech energy exceeds threshold
    Pass speech segments to STT stage
    Discard silence segments
    |
    v
[STAGE 3: Speech-to-Text (STT)]
    Run STT engine on speech segment
    Options: Vosk (offline), Whisper (offline), Google STT (online)
    Output: transcript string
    |
    v
[STAGE 4: Command Parsing]
    Match transcript against known command vocabulary
    Example vocabulary:
      "patrol"   -> CMD_PATROL
      "stop"     -> CMD_STOP
      "come here"-> CMD_APPROACH
      "scan"     -> CMD_SCAN
    Unrecognised transcripts -> logged, discarded
    |
    v
[STAGE 5: Command Publication]
    Publish event: topic="voice_command"
    data = {command: CMD_PATROL, raw_text: "patrol"}
    Consumed by: ai_engine
```

### STT Engine Selection

| Engine | Mode | Latency | Accuracy | Network |
|--------|------|---------|---------|---------|
| Vosk | Offline | ~200 ms | Good | None required |
| Whisper (tiny) | Offline | ~500 ms | Very good | None required |
| Google STT | Online | ~300 ms | Excellent | WiFi required |

Engine selection is configuration-driven.

---

## 19. Navigation Pipeline

The navigation pipeline computes movement decisions based on the current world model and AI intent.

### Pipeline Stages

```
[world_model_updated event]
    |
    v
[STAGE 1: Spatial Assessment]
    Read current distances from world_model:
      front, left, right, rear (HC-SR04)
      tof_front (VL53L0X — precise)
    Read current IMU heading from world_model
    |
    v
[STAGE 2: Obstacle Zone Classification]
    For each direction:
      distance > clear_threshold    -> CLEAR
      safety_threshold < d < clear  -> CAUTION
      d <= safety_threshold         -> BLOCKED
    Build 4-direction zone map
    |
    v
[STAGE 3: Intent Integration]
    Read current AI intent from ai_engine
    (e.g., move forward, track left, approach target)
    |
    v
[STAGE 4: Movement Decision]
    Apply obstacle avoidance rules:
      If FRONT=BLOCKED and intent=FORWARD:
        Evaluate LEFT and RIGHT zones
        If LEFT=CLEAR -> intent=TURN_LEFT
        If RIGHT=CLEAR -> intent=TURN_RIGHT
        If both BLOCKED -> intent=REVERSE
      If FRONT=CLEAR -> execute AI intent
    |
    v
[STAGE 5: Motion Planning]
    Translate movement decision to motor values
    Apply speed ramp (acceleration limiter)
    Compute servo angles if tracking a target
    |
    v
[STAGE 6: Command Generation]
    Send motor values to command_builder
    Send servo angles to command_builder
```

### Navigation Thresholds (Configuration-Driven)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `safety_threshold_cm` | 20 | Distance below which a zone is BLOCKED |
| `caution_threshold_cm` | 50 | Distance below which speed is reduced |
| `clear_threshold_cm` | 80 | Distance above which a zone is fully CLEAR |
| `max_speed_pct` | 80 | Maximum motor speed percentage (0-100) |
| `caution_speed_pct` | 40 | Motor speed in CAUTION zone |

---

## 20. Sensor Fusion Pipeline

The sensor fusion module integrates all incoming sensor data from the ESP32-S3 into a coherent, consistent world model.

### Fusion Process

```
[telemetry_received event — 20 Hz]
    |
    v
[STAGE 1: Packet Validation]
    Check all required keys are present
    Check timestamp is advancing (detect stale packets)
    Check values are in physically plausible ranges
    Flag any sensor with out-of-range reading as FAULT
    |
    v
[STAGE 2: Distance Data Integration]
    HC-SR04 readings -> direction proximity zones
    VL53L0X front -> overrides HC-SR04 front if range <= 1200mm
    VL53L0X pan -> depth context for camera tracking
    |
    v
[STAGE 3: IMU Integration]
    Accelerometer -> compute pitch and roll
    Gyroscope -> integrate for yaw rate
    Apply simple complementary filter:
      angle = alpha * (angle + gyro * dt) + (1-alpha) * accel_angle
    Update world_model: pitch, roll, yaw_rate
    |
    v
[STAGE 4: Gas Hazard Integration]
    If gas.hazard == true -> set world_model.gas_hazard = true
    Publish event: topic="hazard_detected"
    |
    v
[STAGE 5: Power Integration]
    Update world_model: battery_voltage, current_draw
    If voltage < warning_threshold -> publish low_battery event
    |
    v
[STAGE 6: Health Flag Integration]
    Update world_model sensor health flags
    For any health.xxx_ok == false:
      Publish event: topic="sensor_fault", data={sensor_name}
    |
    v
[world_model updated — publish world_model_updated event]
```

### World Model State Object

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `dist_front` | int cm | HC-SR04 | Frontal distance |
| `dist_left` | int cm | HC-SR04 | Left lateral distance |
| `dist_right` | int cm | HC-SR04 | Right lateral distance |
| `dist_rear` | int cm | HC-SR04 | Rear distance |
| `tof_front` | int mm | VL53L0X | Precise frontal distance |
| `tof_pan` | int mm | VL53L0X | Camera axis distance |
| `pitch` | float deg | MPU6050 | Chassis pitch angle |
| `roll` | float deg | MPU6050 | Chassis roll angle |
| `yaw_rate` | float deg/s | MPU6050 | Turn rate |
| `gas_hazard` | bool | MQ-2 | Gas threshold exceeded |
| `battery_voltage` | float V | INA219 | Battery voltage |
| `current_draw` | float A | INA219 | System current |
| `sensor_health` | dict | health flags | Per-sensor fault flags |
| `detections` | list | Vision | Current object detections |
| `mode` | string | AI engine | Current behavioural mode |
| `last_updated` | float | System clock | Timestamp of last update |

---

## 21. OLED Rendering Pipeline

The OLED rendering pipeline runs entirely on the ESP32-S3. The Raspberry Pi never sends pixel data — only expression identifiers.

### Pipeline Stages

```
[Command received from Pi: eyes.expression="curious"]
    |
    v
[command_parser dispatches to oled_renderer queue]
    |
    v
[oled_renderer task wakes on queue item]
    |
    v
[STAGE 1: Expression Lookup]
    Look up expression ID in local flash asset table
    Retrieve: left_eye_bitmap[], right_eye_bitmap[]
    Retrieve: animation_frames[], frame_delay_ms
    |
    v
[STAGE 2: Left Eye Render]
    PCA9548A: select CH0 (Left Eye)
    SSD1306: clear display buffer
    SSD1306: blit bitmap frame to buffer
    SSD1306: transfer buffer to display
    PCA9548A: deselect CH0
    |
    v
[STAGE 3: Right Eye Render]
    PCA9548A: select CH1 (Right Eye)
    SSD1306: clear display buffer
    SSD1306: blit bitmap frame to buffer
    SSD1306: transfer buffer to display
    PCA9548A: deselect CH1
    |
    v
[STAGE 4: Animation Loop]
    If expression has multiple frames:
      Advance to next frame
      Wait frame_delay_ms (FreeRTOS vTaskDelay)
      Repeat STAGE 2-3 for next frame
      Loop until new expression command received or timeout
```

### Expression Asset Storage

| Asset | Location | Format |
|-------|----------|--------|
| Bitmap arrays | ESP32-S3 Flash (PROGMEM) | 128x64 monochrome, 1 bit per pixel |
| Animation frame sequences | Flash | Array of bitmap pointers + frame delay |
| Expression lookup table | Flash | String key -> asset struct |

### Blink Behaviour

The OLED renderer implements autonomous idle blinking. When the active expression is `idle` or any other non-alert expression, the renderer periodically replaces the open-eye bitmap with a closed-eye bitmap (for approximately 150 ms) at a randomised interval (3–6 seconds) to simulate natural blinking. This runs locally without any Pi instruction.

---

## 22. LED Pipeline

The LED pipeline runs on the ESP32-S3. The Raspberry Pi sends a mode identifier and optional colour; the ESP32 runs the full animation locally.

### Pipeline Stages

```
[Command received from Pi: leds.mode="pulse", leds.color=[0,200,255]]
    |
    v
[command_parser dispatches to led_controller queue]
    |
    v
[led_controller task wakes on queue item]
    |
    v
[STAGE 1: Mode Selection]
    Look up mode string in mode table
    Load corresponding animation function pointer
    Store target colour
    |
    v
[STAGE 2: Animation Execution]
    Execute mode animation on both strips:
    |
    +-- "solid"   -> Set all LEDs to color, hold
    +-- "pulse"   -> Sine-wave brightness on target color, loop
    +-- "blink"   -> Toggle all LEDs on/off at set interval
    +-- "sweep"   -> Fill LEDs progressively left-to-right
    +-- "strobe"  -> Rapid on/off at high frequency
    +-- "chase"   -> Single LED travels across strip, loop
    +-- "off"     -> Set all LEDs to 0,0,0
    |
    v
[STAGE 3: WS2812B Write]
    Encode colour data as WS2812B NZR bit stream
    Write Left strip (5 LEDs)
    Write Right strip (5 LEDs)
    |
    v
[Loop — repeat animation until new command or power-down]
```

---

## 23. Motor Control Pipeline

The motor control pipeline runs on the ESP32-S3. It translates abstract speed values (-100 to +100 per motor) into L298N GPIO and PWM signals.

### Pipeline Stages

```
[Command received: motors.fl=70, fr=70, rl=70, rr=70]
    |
    v
[command_parser dispatches to motor_controller queue]
    |
    v
[motor_controller task wakes on queue item]
    |
    v
[STAGE 1: Value Validation]
    Clamp all values to valid range [-100, 100]
    Check for emergency stop conditions (watchdog fault, etc.)
    |
    v
[STAGE 2: Direction Decode]
    For each motor:
      value > 0  -> FORWARD  (IN1=HIGH, IN2=LOW)
      value < 0  -> REVERSE  (IN1=LOW,  IN2=HIGH)
      value == 0 -> BRAKE    (IN1=HIGH, IN2=HIGH)
    |
    v
[STAGE 3: Speed Mapping]
    Map abs(value) 0-100 to PWM duty cycle 0-255 (or 0-1023)
    Apply: duty = (abs(value) / 100.0) * MAX_DUTY
    |
    v
[STAGE 4: L298N Signal Output]
    Left side (FL + RL):
      Set GPIO: IN1, IN2 for direction
      Set LEDC duty: ENA for speed
    Right side (FR + RR):
      Set GPIO: IN3, IN4 for direction
      Set LEDC duty: ENB for speed
    |
    v
[Motors respond within 1 PWM cycle (~1 ms at 1 kHz PWM)]
```

### Motor Safety Rules

| Rule | Implementation |
|------|---------------|
| Maximum speed is configuration-limited | Commanded value is capped at config max_speed |
| Watchdog timeout triggers motor stop | Watchdog task writes STOP to motor queue on timeout |
| Serial link loss triggers motor stop | serial_handler publishes link_lost event -> motors stop |
| No sudden full-speed reversals | Speed ramp enforced in motion_planner on Pi side |

---

## 24. Error Handling

### Error Classification

| Class | Severity | Examples | Response |
|-------|---------|---------|---------|
| CRITICAL | Fatal | Serial port not found, camera not found on boot | Log, abort startup, notify |
| ERROR | Subsystem fault | Sensor I2C failure, serial packet corrupt | Log, disable subsystem, continue |
| WARNING | Degraded | Sensor reading out of range, low battery | Log, flag in telemetry, continue |
| INFO | Operational | Mode change, detection event, command sent | Log at INFO level |
| DEBUG | Development | Packet contents, loop timing | Log at DEBUG level (disabled in production) |

### Raspberry Pi Error Strategy

```
[Exception raised in any module]
    |
    +-- Is it CRITICAL?
    |     YES -> Log at CRITICAL level
    |          -> Attempt graceful shutdown
    |          -> Send shutdown command to ESP32
    |          -> Exit with non-zero code
    |
    +-- Is it a subsystem ERROR?
          YES -> Log at ERROR level
              -> Disable the affected module
              -> Publish fault event on event_bus
              -> Continue with reduced capability
              -> Dashboard receives fault notification
              -> Other modules degrade gracefully
```

### ESP32-S3 Error Strategy

```
[Sensor read fails]
    |
    +-- Set health flag: sensor_name_ok = false
    +-- Use last good reading with age timestamp
    +-- After N consecutive failures:
          -> Disable sensor from telemetry
          -> Send fault packet to Pi
    
[I2C bus error (PCA9548A unreachable)]
    |
    +-- Log fault
    +-- Disable all PCA-dependent devices (OLEDs, VL53Ls)
    +-- Continue with HC-SR04, MPU6050, MQ-2
    +-- Send fault telemetry packet to Pi
    
[Serial link idle for > 2 seconds]
    |
    +-- Watchdog: publish link_lost event
    +-- motor_controller: immediately STOP all motors
    +-- servo_controller: hold current position
    +-- oled_renderer: switch to error expression
    +-- led_controller: switch to error LED pattern
    +-- Continue attempting serial read (do not reboot)
    
[Watchdog: critical task misses heartbeat]
    |
    +-- Log fault to serial TX buffer
    +-- Stop all actuators (safety-first)
    +-- Attempt task restart
    +-- If restart fails -> ESP32 soft reboot
```

---

## 25. Logging Strategy

### Raspberry Pi Logging

All Raspberry Pi modules log through a single centralised `logger.py` module. Logs are written to both the console and a rotating log file.

| Parameter | Value |
|-----------|-------|
| Log format | JSON-structured line per entry |
| Fields | timestamp, level, module, event, data |
| File location | `Logs/rover_YYYYMMDD_HHMMSS.log` |
| Rotation | New file per run; optional size-based rotation |
| Console level | Configurable (default: INFO) |
| File level | Configurable (default: DEBUG) |
| Thread safety | Log queue + dedicated logger thread |

### Log Entry Format

```
{
  "ts": "2026-06-28T10:30:00.123Z",
  "level": "INFO",
  "module": "navigation",
  "event": "obstacle_avoidance_triggered",
  "data": {
    "front_cm": 18,
    "action": "TURN_LEFT",
    "reason": "front_blocked"
  }
}
```

### Log Events by Module

| Module | Key Events Logged |
|--------|-----------------|
| serial_manager | Port open, port close, parse error, link lost |
| sensor_fusion | Sensor fault detected, world model reset |
| vision_pipeline | Camera open, camera error, model loaded, detection |
| audio_pipeline | Microphone open, VAD triggered, command recognised |
| ai_engine | Mode transition, decision taken, hazard detected |
| navigation | Avoidance triggered, path clear, movement command |
| dashboard_server | Client connected, client disconnected, broadcast error |

### ESP32-S3 Logging

The ESP32-S3 does not have a file system for persistent logging. All diagnostic output is:

1. Transmitted to the Raspberry Pi via the telemetry health fields.
2. Emitted on the UART debug port (USB CDC secondary channel, or JTAG) for development use.
3. Included in `fault` packet payloads when a serious error occurs.

---

## 26. Configuration Strategy

### Raspberry Pi Configuration

All Raspberry Pi runtime parameters are stored in a single YAML configuration file: `RASPBERRY PI/config/rover.yaml`.

The `config.py` module loads this file at startup, validates all required fields, and exposes values as a typed configuration object consumed by all modules.

**No module may use a hardcoded numeric value that should be configurable.**

### Configuration File Structure

```yaml
serial:
  port: "/dev/ttyUSB0"
  baud: 921600
  timeout_s: 2.0
  link_watchdog_s: 2.0

vision:
  device_index: 0
  width: 640
  height: 480
  fps: 30
  model_path: "models/ssd_mobilenet_v2.tflite"
  confidence_threshold: 0.55
  target_classes: [0, 15, 16, 63]

audio:
  device_index: 1
  sample_rate: 16000
  chunk_size: 1024
  vad_threshold: 0.5
  stt_engine: "vosk"
  model_path: "models/vosk-model-small-en"

navigation:
  safety_threshold_cm: 20
  caution_threshold_cm: 50
  clear_threshold_cm: 80
  max_speed_pct: 80
  caution_speed_pct: 40
  ramp_step: 5

power:
  low_battery_v: 7.0
  critical_battery_v: 6.5

dashboard:
  host: "0.0.0.0"
  port: 8765
  broadcast_hz: 10

logging:
  console_level: "INFO"
  file_level: "DEBUG"
  log_dir: "Logs/"
```

### ESP32-S3 Configuration

ESP32-S3 configuration is split between:

1. **Compile-time constants** in `config.h` — pin assignments, I2C addresses, PWM channels. These rarely change.
2. **Runtime constants** in NVS (Non-Volatile Storage) — values that may need adjustment without recompilation (baud rate, sensor thresholds).

```
config.h (compile-time)
  PIN_SDA = 13
  PIN_SCL = 14
  PIN_MQ2 = 10
  PIN_SERVO_PAN = 11
  PIN_SERVO_TILT = 12
  PIN_HCSR04_FRONT_TRIG = 4
  PIN_HCSR04_FRONT_ECHO = 5
  PIN_HCSR04_LEFT_TRIG = 6
  PIN_HCSR04_LEFT_ECHO = 7
  PIN_HCSR04_RIGHT_TRIG = 15
  PIN_HCSR04_RIGHT_ECHO = 16
  PIN_HCSR04_REAR_TRIG = 17
  PIN_HCSR04_REAR_ECHO = 18
  I2C_ADDR_PCA9548A = 0x70
  I2C_ADDR_MPU6050 = 0x68
  TELEMETRY_RATE_HZ = 20
  WATCHDOG_TIMEOUT_MS = 2000
  SERVO_PAN_MIN_DEG = 0
  SERVO_PAN_MAX_DEG = 180
  SERVO_TILT_MIN_DEG = 45
  SERVO_TILT_MAX_DEG = 135
  MOTOR_MAX_DUTY = 255
```

---

## 27. Scalability Strategy

### Adding a New Sensor (ESP32 Side)

1. Write a new driver in `ESP32S3/drivers/driver_newdevice.cpp`.
2. Add a read call in `sensor_manager.cpp` poll loop.
3. Add the new field to the telemetry JSON packet in `telemetry_builder.cpp`.
4. Update the protocol spec in `SHARED/protocol_spec.md`.
5. Add the new field to the Pi `sensor_fusion.py` and `world_model.py`.
6. No other module changes required.

### Adding a New Actuator (ESP32 Side)

1. Write a new controller in `ESP32S3/controller_newactuator.cpp`.
2. Add a new queue and dispatch case in `command_parser.cpp`.
3. Add the new command field to the JSON command packet schema in `SHARED/protocol_spec.md`.
4. Add the new field to `command_builder.py` on the Pi.
5. No other module changes required.

### Adding a New AI Behaviour (Pi Side)

1. Add a new mode constant in `ai_engine.py`.
2. Implement the behaviour logic in `ai_engine.evaluate()`.
3. Add the corresponding navigation intent handler in `navigation.py` if needed.
4. Add the corresponding expression ID in `expression_selector.py`.
5. No ESP32 changes required (unless new hardware is involved).

### Adding a New Voice Command (Pi Side)

1. Add the command string to the vocabulary in `audio_pipeline.py`.
2. Add the command handler in `ai_engine.py`.
3. No other changes required.

### Adding a New Dashboard View

1. The dashboard consumes the existing WebSocket telemetry stream.
2. New dashboard views require only frontend changes.
3. If new data fields are needed, add them to the telemetry broadcast in `dashboard_server.py`.
4. No ESP32 changes required unless the new view needs new sensor data.

---

## 28. Future Modules

The following modules are planned for future versions and are accounted for in the current architecture's design decisions.

### Planned for V1.x

| Module | Location | Purpose | Dependencies |
|--------|----------|---------|-------------|
| `driver_ina219.cpp` | ESP32S3/ | INA219 power monitor driver | I2C bus, PCA9548A or direct |
| `power_monitor.py` | RASPBERRY PI/ | Power event handling, low battery alerts | sensor_fusion, world_model |
| `slam_module.py` | RASPBERRY PI/ | Simultaneous Localisation and Mapping | world_model, sensor_fusion |
| `motor_encoder.cpp` | ESP32S3/ | Wheel encoder reading for odometry | New GPIO pins |
| `odometry.py` | RASPBERRY PI/ | Dead reckoning from encoder telemetry | world_model |

### Planned for V2+

| Module | Location | Purpose |
|--------|----------|---------|
| `lidar_driver.cpp` | ESP32S3/ or RASPBERRY PI/ | LiDAR integration for 360° mapping |
| `thermal_pipeline.py` | RASPBERRY PI/ | Thermal camera frame processing |
| `remote_control.py` | RASPBERRY PI/ | Full teleoperation mode from dashboard |
| `cloud_telemetry.py` | RASPBERRY PI/ | Push telemetry to cloud backend |
| `fleet_manager.py` | PC AI/ | Multi-rover coordination |

### PC AI Folder

The `PC AI/` folder is reserved for offboard computation tools — AI model training scripts, data analysis notebooks, and simulation harnesses that run on a development PC rather than onboard the rover.

| Tool | Purpose |
|------|---------|
| Model training scripts | Train and export custom TFLite detection models |
| Dataset utilities | Collect, label, and augment training data from rover logs |
| Simulation harness | Replay rover logs for testing navigation logic offline |
| Dashboard application | Primary dashboard client implementation |

---

## 29. Folder Responsibility Table

The `MAIN CODE/` directory structure is fixed and must not be modified. Each folder has a precisely defined ownership boundary.

```
MAIN CODE/
    |
    +-- ESP32S3/          Firmware for the ESP32-S3 N16R8
    |                     Language: C++ (ESP-IDF / Arduino framework)
    |                     Runtime: FreeRTOS
    |                     Owns: All hardware I/O, sensors, actuators
    |
    +-- RASPBERRY PI/     Software for the Raspberry Pi 3B+
    |                     Language: Python 3
    |                     Runtime: Linux / asyncio
    |                     Owns: AI, vision, audio, navigation, dashboard
    |
    +-- PC AI/            Offboard tools (runs on development PC)
    |                     Language: Python 3
    |                     Owns: Model training, simulation, data analysis
    |
    +-- SHARED/           Protocol specifications and shared registries
    |                     Language: Markdown, JSON Schema, YAML
    |                     Owns: JSON protocol spec, expression registry,
    |                           LED mode registry, error codes
    |
    +-- TOOLS/            Development and deployment utilities
                          Language: Python 3, Shell
                          Owns: Deployment scripts, log viewers,
                                serial monitor, calibration tools
```

### Folder Responsibility Table

| Folder | Language | Runtime | Processor Target | Contents |
|--------|----------|---------|-----------------|---------|
| `ESP32S3/` | C++ | FreeRTOS / ESP-IDF | ESP32-S3 N16R8 | Firmware: drivers, tasks, controllers |
| `RASPBERRY PI/` | Python 3 | Linux / asyncio | Raspberry Pi 3B+ | Software: AI, vision, audio, navigation |
| `PC AI/` | Python 3 | PC / Linux | Development machine | Model training, simulation, dashboard app |
| `SHARED/` | Markdown / YAML | — | Both | Protocol spec, expression registry, error codes |
| `TOOLS/` | Python 3 / Shell | PC / Pi | Development use | Scripts, calibration, monitoring utilities |

### Module-to-Folder Mapping

| Module | Folder | File |
|--------|--------|------|
| Main entry point (Pi) | RASPBERRY PI/ | main.py |
| Config loader (Pi) | RASPBERRY PI/config/ | rover.yaml, config.py |
| Logger (Pi) | RASPBERRY PI/ | logger.py |
| Event bus (Pi) | RASPBERRY PI/ | event_bus.py |
| Serial manager (Pi) | RASPBERRY PI/ | serial_manager.py |
| Vision pipeline (Pi) | RASPBERRY PI/ | vision_pipeline.py |
| Audio pipeline (Pi) | RASPBERRY PI/ | audio_pipeline.py |
| Sensor fusion (Pi) | RASPBERRY PI/ | sensor_fusion.py |
| World model (Pi) | RASPBERRY PI/ | world_model.py |
| AI engine (Pi) | RASPBERRY PI/ | ai_engine.py |
| Navigation (Pi) | RASPBERRY PI/ | navigation.py |
| Motion planner (Pi) | RASPBERRY PI/ | motion_planner.py |
| Expression selector (Pi) | RASPBERRY PI/ | expression_selector.py |
| Command builder (Pi) | RASPBERRY PI/ | command_builder.py |
| Dashboard server (Pi) | RASPBERRY PI/ | dashboard_server.py |
| Main entry point (ESP32) | ESP32S3/ | main.cpp |
| Sensor manager | ESP32S3/ | sensor_manager.cpp |
| Telemetry builder | ESP32S3/ | telemetry_builder.cpp |
| Serial handler | ESP32S3/ | serial_handler.cpp |
| Command parser | ESP32S3/ | command_parser.cpp |
| Motor controller | ESP32S3/ | motor_controller.cpp |
| Servo controller | ESP32S3/ | servo_controller.cpp |
| OLED renderer | ESP32S3/ | oled_renderer.cpp |
| LED controller | ESP32S3/ | led_controller.cpp |
| Watchdog | ESP32S3/ | watchdog.cpp |
| Health monitor | ESP32S3/ | health_monitor.cpp |
| HC-SR04 driver | ESP32S3/drivers/ | driver_hcsr04.cpp |
| VL53L0X driver | ESP32S3/drivers/ | driver_vl53l0x.cpp |
| MPU6050 driver | ESP32S3/drivers/ | driver_mpu6050.cpp |
| MQ-2 driver | ESP32S3/drivers/ | driver_mq2.cpp |
| PCA9548A driver | ESP32S3/drivers/ | driver_pca9548a.cpp |
| INA219 driver (planned) | ESP32S3/drivers/ | driver_ina219.cpp |
| Protocol specification | SHARED/ | protocol_spec.md |
| Expression registry | SHARED/ | expression_registry.md |
| LED mode registry | SHARED/ | led_modes.md |
| Error codes | SHARED/ | error_codes.md |
| ESP32 config constants | ESP32S3/include/ | config.h |
| Deployment scripts | TOOLS/ | deploy.sh / deploy.py |
| Serial monitor | TOOLS/ | serial_monitor.py |
| Log viewer | TOOLS/ | log_viewer.py |
| Dashboard app | PC AI/ | dashboard/ |

---

## 30. Conclusion

The Recon Rover V1 software architecture is a direct and faithful software expression of the physical and philosophical principles established in `SYSTEM_ARCHITECTURE.md` and `HARDWARE_ARCHITECTURE.md`.

### What This Architecture Achieves

**Strict boundary enforcement.** The ESP32-S3 firmware and the Raspberry Pi software are entirely separate codebases. They share nothing except the JSON protocol contract defined in `SHARED/`. The serial link is the only crossing point, and every byte that crosses it is typed, structured, and timestamped.

**Modularity at every level.** On the Raspberry Pi, each Python module has one job. On the ESP32-S3, each FreeRTOS task has one job. Replacing, upgrading, or disabling any module requires touching only that module's file, not the rest of the system.

**Independent failure.** A vision pipeline crash does not stop the motors. A serial timeout does not crash the Pi. An OLED I2C failure does not stop sensor polling. Every subsystem is isolated behind event-driven interfaces and fault flags.

**Observability.** Every module logs. Every sensor has a health flag. Every mode transition is a named event. Nothing is silent. The dashboard provides a live, structured window into the rover's complete operational state.

**Scalability.** Adding a new sensor requires changes in exactly three places: the ESP32 driver, the telemetry packet, and the Pi's sensor fusion module. Adding a new behaviour requires changes in exactly two places: the AI engine and the navigation module. The architecture is designed to accommodate V2's planned features — SLAM, LiDAR, cloud telemetry, multi-rover coordination — without refactoring the core.

### The Single Most Important Rule

> **The Raspberry Pi decides. The ESP32 executes. The serial bridge carries the conversation. Nothing else crosses the boundary.**

Every future contribution to this codebase must honour this rule. Any code that attempts to perform AI on the ESP32, or directly control hardware from the Pi, is architecturally wrong and must be rejected.

This document is the official software architecture reference for Recon Rover V1. All source code, firmware, configuration files, and future modules must align with the architecture defined here.

---

*End of Document*

---

> **Document Control**
>
> | Version | Date | Author | Notes |
> |---------|------|--------|-------|
> | 1.0 | 2026-06-28 | Lead Software Architect | Initial foundation draft |
