# Recon Rover V1 — Hardware Architecture

**Document Version:** 1.0  
**Status:** Foundation Draft  
**Last Updated:** 2026-06-28  
**Author:** Lead Robotics Hardware Architect  
**Classification:** Internal Design Document  
**Reference:** See `SYSTEM_ARCHITECTURE.md` for system-level context, layer responsibilities, and software philosophy.

---

## Table of Contents

1. [Hardware Design Philosophy](#1-hardware-design-philosophy)
2. [Complete Hardware Block Diagram](#2-complete-hardware-block-diagram)
3. [Power Architecture](#3-power-architecture)
4. [Electrical Architecture](#4-electrical-architecture)
5. [I2C Architecture](#5-i2c-architecture)
6. [GPIO Allocation Table](#6-gpio-allocation-table)
7. [Sensor Placement](#7-sensor-placement)
8. [Camera System](#8-camera-system)
9. [OLED Eye System](#9-oled-eye-system)
10. [Motion System](#10-motion-system)
11. [Lighting System](#11-lighting-system)
12. [Expansion Capability](#12-expansion-capability)
13. [Hardware Failure Strategy](#13-hardware-failure-strategy)
14. [Hardware Design Decisions](#14-hardware-design-decisions)
15. [Conclusion](#15-conclusion)

---

## 1. Hardware Design Philosophy

### The Fundamental Split

Recon Rover V1 is built on a single, inviolable hardware principle:

> **Cognition and reaction are physically separated. No single processor is responsible for both.**

The Raspberry Pi 3B+ handles everything that requires reasoning — vision, AI inference, navigation logic, dashboard communication, and audio processing. The ESP32-S3 handles everything that requires determinism — sensor sampling, motor control, servo positioning, display rendering, and LED output.

This split is not merely a software convention. It is enforced at the hardware level through a single USB serial link that acts as the only bridge between the two processors. There is no shared I2C bus, no shared SPI bus, and no shared GPIO. The boundary is physical.

### Why This Matters for Hardware Design

A Linux-based single board computer like the Raspberry Pi is not suited for real-time hardware control. Its operating system introduces scheduling jitter, USB latency, and non-deterministic interrupt handling. If the Pi were responsible for driving motors directly, a CPU spike from an OpenCV inference cycle could cause a missed PWM pulse, resulting in erratic motor behaviour.

Conversely, the ESP32-S3 — a bare-metal microcontroller running at 240 MHz with deterministic task scheduling via FreeRTOS — is not suited for AI inference, file I/O, or network communication. Its role is precisely bounded: react to hardware in real time.

### Design Constraints This Philosophy Imposes

| Constraint | Consequence |
|------------|-------------|
| All sensors belong to the ESP32 | The Pi never reads GPIO directly |
| All actuators belong to the ESP32 | The Pi never drives PWM or motor pins |
| All USB peripherals belong to the Pi | USB webcam and microphone plug into the Pi only |
| The serial link is the only bridge | Any new cross-processor data must flow through JSON packets |
| Hardware must fail independently | A camera disconnect must not affect motor control |

---

## 2. Complete Hardware Block Diagram

The following diagram represents the complete physical hardware topology of Recon Rover V1, from power input to every connected peripheral.

```
+------------------------------------------------------------------+
|                        POWER SYSTEM                              |
|                                                                  |
|  [Li-Ion / Li-Po Battery Pack]                                   |
|         |  (7.4V - 12V nominal, depending on cell count)         |
|         |                                                        |
|         +--------> [BMS]  (overcharge / overdischarge protect)   |
|                       |                                          |
|         +-------------+-------------+-------------+             |
|         |                           |             |             |
|   [5V Buck #1]              [5V Buck #2]    [Raw VBAT]          |
|   Raspberry Pi                ESP32-S3       L298N ENA           |
|   USB Webcam                  Servos         DC Motors           |
|   USB Microphone              OLEDs                              |
|                               ARGB LEDs                          |
+------------------------------------------------------------------+
                 |                          |
+================v===========+  +===========v====================+
|   COGNITIVE LAYER          |  |  REACTIVE LAYER               |
|   Raspberry Pi 3B+         |  |  ESP32-S3 N16R8               |
|                            |  |                               |
|  [USB Port 1]              |  |  [I2C Bus]                    |
|    --> USB Webcam          |  |  SDA: GPIO13 / SCL: GPIO14    |
|                            |  |    |                          |
|  [USB Port 2]              |  |  [PCA9548A Multiplexer]       |
|    --> USB Microphone      |  |    |                          |
|                            |  |    +-- CH0 --> SSD1306 (L Eye)|
|  [USB Port 3]              |  |    +-- CH1 --> SSD1306 (R Eye)|
|    --> ESP32-S3 (Serial)   |  |    +-- CH2 --> VL53L0X (Front)|
|                            |  |    +-- CH3 --> VL53L0X (Pan)  |
|  [WiFi]                    |  |    +-- CH4-7  (Reserved)      |
|    --> Dashboard (PC/Web)  |  |                               |
|                            |  |  [Analog Input]               |
+============================+  |  GPIO10 --> MQ-2              |
         |                      |                               |
         | USB Serial           |  [PWM Output]                 |
         | (JSON Protocol)      |  GPIO11 --> SG90 Pan Servo    |
         |                      |  GPIO12 --> SG90 Tilt Servo   |
+========v===================+  |                               |
|   SERIAL JSON BRIDGE       |  |  [Digital I/O - Ultrasonic]  |
|   Bidirectional            |  |  GPIO4/5   HC-SR04 Front     |
|   Telemetry (ESP32->Pi)    |  |  GPIO6/7   HC-SR04 Left      |
|   Commands (Pi->ESP32)     |  |  GPIO15/16 HC-SR04 Right     |
+============================+  |  GPIO17/18 HC-SR04 Rear      |
                                |                               |
                                |  [Motor Driver]               |
                                |  L298N                        |
                                |  --> Motor FL (Front Left)    |
                                |  --> Motor FR (Front Right)   |
                                |  --> Motor RL (Rear Left)     |
                                |  --> Motor RR (Rear Right)    |
                                |                               |
                                |  [ARGB LED Output]            |
                                |  --> WS2812B Left  (x5 LEDs) |
                                |  --> WS2812B Right (x5 LEDs) |
                                |                               |
                                |  [I2C - Future]               |
                                |  INA219 Power Monitor         |
                                |  (planned, via PCA or direct) |
                                +===============================+
```

---

## 3. Power Architecture

### Battery

The rover is powered by a rechargeable lithium-based battery pack. The exact cell configuration depends on chassis and runtime requirements, but the design assumes the following general parameters:

| Parameter | Target Value |
|-----------|-------------|
| Chemistry | Li-Ion or Li-Po |
| Nominal Voltage | 7.4 V (2S) or 11.1 V (3S) |
| Capacity | 2000 mAh – 5000 mAh |
| Discharge Rating | 10C minimum |
| Connector | XT60 or equivalent high-current connector |

A 2S Li-Po (7.4V nominal, 8.4V fully charged, 6.0V cutoff) is the primary recommendation for V1. It provides sufficient voltage for the L298N motor driver while keeping weight and size manageable.

### Battery Management System (BMS)

A Battery Management System (BMS) is mandatory. It must provide:

- **Overcharge protection** — prevents charging above 4.2V per cell.
- **Over-discharge protection** — cuts off load below 3.0V per cell (6.0V for 2S).
- **Overcurrent protection** — disconnects load if current exceeds rated limit.
- **Short-circuit protection** — immediate cutoff on dead short.

The BMS sits between the battery and all downstream power rails. No load should be connected directly to the battery without BMS protection.

### Power Rails

| Rail | Voltage | Source | Consumers | Notes |
|------|---------|--------|-----------|-------|
| 5V Rail A | 5.0 V | Buck Converter #1 | Raspberry Pi 3B+, USB Webcam, USB Microphone | High-quality, low-ripple converter required |
| 5V Rail B | 5.0 V | Buck Converter #2 | ESP32-S3, SSD1306 OLEDs, SG90 Servos, WS2812B LEDs | Separate from Pi rail to prevent noise coupling |
| VBAT Rail | Raw battery voltage | BMS output | L298N motor driver logic supply | Direct battery feed |
| Motor Rail | Raw battery voltage | BMS output | L298N output stage, DC gear motors | High current; rated for motor stall current |

### Why Two 5V Rails?

Separating the Raspberry Pi power from the ESP32 power serves two purposes:

1. **Noise isolation.** Servo PWM signals and WS2812B data lines introduce switching noise on their 5V supply. This noise must not propagate to the Pi's supply, as it can cause SD card corruption or USB instability.
2. **Current headroom.** The Pi requires a stable 2.5 A supply under load. Servos under load, combined with LEDs and the ESP32, can draw additional current that would otherwise cause voltage sag on a shared rail.

### Voltage Requirements by Component

| Component | Supply Voltage | Typical Current | Peak Current |
|-----------|---------------|-----------------|-------------|
| Raspberry Pi 3B+ | 5.0 V | 600 mA (idle) | 1.2 A (load) |
| USB Webcam | 5.0 V (USB) | 200 mA | 400 mA |
| USB Microphone | 5.0 V (USB) | 50 mA | 100 mA |
| ESP32-S3 N16R8 | 3.3 V (internal LDO from 5V) | 100 mA | 350 mA |
| SSD1306 OLED x2 | 3.3 V – 5.0 V | 10 mA each | 20 mA each |
| SG90 Servo x2 | 4.8 V – 6.0 V | 100 mA each (idle) | 700 mA each (stall) |
| WS2812B x10 LEDs | 5.0 V | 60 mA (all white) | 600 mA (full white) |
| L298N Logic | 5.0 V | 20 mA | 50 mA |
| DC Gear Motor x4 | VBAT | 200 mA each (free run) | 1.5 A each (stall) |
| MPU6050 | 3.3 V | 3.9 mA | 5 mA |
| VL53L0X x2 | 2.8 V – 3.3 V | 10 mA each | 40 mA each |
| HC-SR04 x4 | 5.0 V | 15 mA each | 15 mA each |
| MQ-2 | 5.0 V | 150 mA (heater) | 200 mA |
| PCA9548A | 3.3 V | 1 mA | 2 mA |

> **Logic Level Warning:** The ESP32-S3 GPIO pins operate at 3.3V and are **not** 5V-tolerant. HC-SR04 ECHO lines output 5V. A resistor voltage divider (e.g., 1 kΩ / 2 kΩ) or a dedicated logic level shifter must be placed on every HC-SR04 ECHO line.

### INA219 Placement (Future)

The INA219 current/voltage sensor will be placed on the main battery output line, between the BMS output and the power distribution node. This allows it to measure total system current draw and battery voltage in real time. It connects to the ESP32-S3 via the I2C bus, either directly (if no address conflict) or via an available PCA9548A channel.

---

## 4. Electrical Architecture

### Interface Summary

| Interface | Used For | Controller |
|-----------|----------|------------|
| USB (Host) | Webcam, Microphone, ESP32 serial bridge | Raspberry Pi |
| USB (Device/Serial) | Serial JSON bridge to Pi | ESP32-S3 |
| I2C | OLED displays, ToF sensors, IMU, power monitor | ESP32-S3 |
| PWM (output) | Servo control, motor speed via L298N ENA/ENB | ESP32-S3 |
| GPIO (digital output) | Motor direction pins (L298N IN1-IN4), WS2812B data | ESP32-S3 |
| GPIO (digital I/O) | HC-SR04 TRIG (output) and ECHO (input) | ESP32-S3 |
| ADC (analog input) | MQ-2 gas sensor | ESP32-S3 |
| WiFi (802.11 b/g/n) | Dashboard telemetry, remote control | Raspberry Pi |

### I2C

The I2C bus runs at 400 kHz (Fast Mode) to support the real-time polling demands of two VL53L0X sensors and the MPU6050. The bus is managed entirely by the ESP32-S3. The Raspberry Pi has no connection to this bus.

**Why I2C was chosen:** I2C allows multiple devices to share two wires (SDA, SCL) using unique 7-bit addresses. This is ideal for a sensor-dense platform where GPIO pins are a limited resource. The PCA9548A multiplexer resolves the address collision problem introduced by using two identical SSD1306 OLEDs.

### UART / USB Serial

The only cross-processor communication channel is a UART-over-USB link between the Raspberry Pi (USB host) and the ESP32-S3 (USB device / CDC serial). Target baud rate: 115200 or higher. The physical USB cable serves as both the data link and a power source for the ESP32 during development; in production the ESP32 should be powered by its dedicated 5V rail.

**Why USB Serial was chosen:** USB CDC serial is universally supported on Linux (Pi) and ESP-IDF/Arduino (ESP32). It requires no additional hardware, provides a reliable framed byte stream, and is trivially debuggable with a serial monitor.

### PWM

PWM is used for:

- **Servo control:** Standard 50 Hz PWM, 1 ms – 2 ms pulse width for SG90 (0°–180°). Driven on GPIO11 (pan) and GPIO12 (tilt) using the ESP32 LEDC peripheral.
- **Motor speed control:** The L298N ENA and ENB pins accept PWM to modulate motor speed. The ESP32 LEDC peripheral provides the required signals.

**Why PWM was chosen:** PWM is the industry standard for servo and DC motor speed control. It is supported natively by the ESP32 LEDC hardware timer, allowing precise frequency and duty cycle control without CPU overhead.

### Analog Input

The MQ-2 gas sensor provides an analog voltage output proportional to gas concentration. This is read via the ESP32-S3 onboard ADC on GPIO10.

> **ADC Note:** The ESP32-S3 ADC has known non-linearity above approximately 3.1 V. The MQ-2 output should be conditioned with a voltage divider if its output range exceeds the ADC reference. Calibration offsets must be applied in firmware.

### Digital I/O — HC-SR04 Ultrasonic

Each HC-SR04 requires a dedicated TRIG (output) and ECHO (input) GPIO pair. The TRIG signal is a 10 µs active-high pulse. The ECHO line returns a high pulse whose width corresponds to the round-trip time of the ultrasonic ping.

A voltage divider or logic level shifter must be placed on every ECHO line (HC-SR04 outputs 5V; ESP32 accepts 3.3V).

---

## 5. I2C Architecture

### Bus Configuration

| Parameter | Value |
|-----------|-------|
| SDA Pin | GPIO13 |
| SCL Pin | GPIO14 |
| Bus Speed | 400 kHz (Fast Mode) |
| Controller | ESP32-S3 (master only) |
| Multiplexer | PCA9548A (TCA9548A compatible) |
| Multiplexer I2C Address | 0x70 (default, A0/A1/A2 tied to GND) |

### The Address Collision Problem

| Device | Default I2C Address | Qty | Conflict? |
|--------|-------------------|-----|-----------|
| SSD1306 OLED | 0x3C | 2 | YES — both OLEDs share the same address |
| VL53L0X | 0x29 | 2 | YES — both ToF sensors share the same address |
| MPU6050 | 0x68 | 1 | No conflict |
| INA219 (planned) | 0x40 | 1 | No conflict |
| PCA9548A | 0x70 | 1 | No conflict |

Without a multiplexer, both OLEDs and both VL53L0X sensors would respond simultaneously to every bus transaction, making independent control impossible. The PCA9548A places each conflicting device on its own isolated channel.

### PCA9548A Channel Map

| Channel | I2C Address on Channel | Device | Purpose | Status |
|---------|----------------------|--------|---------|--------|
| CH0 | 0x3C | SSD1306 OLED | Left Eye display | Active |
| CH1 | 0x3C | SSD1306 OLED | Right Eye display | Active |
| CH2 | 0x29 | VL53L0X | Front proximity sensor | Active |
| CH3 | 0x29 | VL53L0X | Pan-axis proximity sensor | Active |
| CH4 | — | *(Reserved)* | Future sensor | Available |
| CH5 | — | *(Reserved)* | Future sensor | Available |
| CH6 | — | *(Reserved)* | Future sensor | Available |
| CH7 | — | *(Reserved)* | Future sensor | Available |

> **Note:** The MPU6050 (0x68) does not conflict with any other device and may be connected directly to the main I2C bus without routing through the PCA9548A, reducing channel-switching overhead during high-frequency IMU polling.

### Channel Switching Protocol

The ESP32-S3 firmware must write a channel-select byte to the PCA9548A before communicating with any device behind it. Only one channel should be active at any time. After completing transactions on a given channel, the firmware should deselect all channels (write 0x00 to the PCA9548A) to prevent bus contention.

### I2C Pull-up Resistors

| Parameter | Recommended Value |
|-----------|------------------|
| Pull-up resistor (SDA) | 2.2 kΩ – 4.7 kΩ |
| Pull-up resistor (SCL) | 2.2 kΩ – 4.7 kΩ |
| Pull-up reference voltage | 3.3 V |

Many breakout boards include onboard pull-ups. Verify that the combined parallel resistance of all onboard pull-ups does not fall below 1 kΩ, which would over-drive the bus.

---

## 6. GPIO Allocation Table

All GPIOs listed below belong to the **ESP32-S3 N16R8**. The Raspberry Pi has no direct GPIO connections to sensors or actuators.

| GPIO | Peripheral | Direction | Interface | Purpose | Notes |
|------|-----------|-----------|-----------|---------|-------|
| GPIO4 | HC-SR04 Front — TRIG | Output | Digital | Trigger ultrasonic ping, Front | 10 µs pulse |
| GPIO5 | HC-SR04 Front — ECHO | Input | Digital | Receive echo return, Front | 5V->3.3V level shift required |
| GPIO6 | HC-SR04 Left — TRIG | Output | Digital | Trigger ultrasonic ping, Left | 10 µs pulse |
| GPIO7 | HC-SR04 Left — ECHO | Input | Digital | Receive echo return, Left | 5V->3.3V level shift required |
| GPIO10 | MQ-2 Gas Sensor | Input | Analog (ADC) | Read gas concentration voltage | Voltage divider if output > 3.1V |
| GPIO11 | SG90 Servo — Pan | Output | PWM (LEDC) | Pan axis position command | 50 Hz, 1–2 ms pulse width |
| GPIO12 | SG90 Servo — Tilt | Output | PWM (LEDC) | Tilt axis position command | 50 Hz, 1–2 ms pulse width |
| GPIO13 | I2C SDA | Bidirectional | I2C | I2C data line to PCA9548A + devices | 2.2–4.7 kΩ pull-up to 3.3V |
| GPIO14 | I2C SCL | Output | I2C | I2C clock line | 2.2–4.7 kΩ pull-up to 3.3V |
| GPIO15 | HC-SR04 Right — TRIG | Output | Digital | Trigger ultrasonic ping, Right | 10 µs pulse |
| GPIO16 | HC-SR04 Right — ECHO | Input | Digital | Receive echo return, Right | 5V->3.3V level shift required |
| GPIO17 | HC-SR04 Rear — TRIG | Output | Digital | Trigger ultrasonic ping, Rear | 10 µs pulse |
| GPIO18 | HC-SR04 Rear — ECHO | Input | Digital | Receive echo return, Rear | 5V->3.3V level shift required |
| TBD | L298N IN1 | Output | Digital | Motor direction — Left side A | Finalised during wiring |
| TBD | L298N IN2 | Output | Digital | Motor direction — Left side B | Finalised during wiring |
| TBD | L298N IN3 | Output | Digital | Motor direction — Right side A | Finalised during wiring |
| TBD | L298N IN4 | Output | Digital | Motor direction — Right side B | Finalised during wiring |
| TBD | L298N ENA | Output | PWM (LEDC) | Motor speed — Left side | Finalised during wiring |
| TBD | L298N ENB | Output | PWM (LEDC) | Motor speed — Right side | Finalised during wiring |
| TBD | WS2812B Data — Left | Output | Digital (1-Wire) | ARGB LED strip Left | Finalised during wiring |
| TBD | WS2812B Data — Right | Output | Digital (1-Wire) | ARGB LED strip Right | Finalised during wiring |
| USB D+/D- | USB Serial Bridge | Bidirectional | USB CDC | Serial JSON link to Raspberry Pi | Onboard USB connector |

> **TBD pins** will be finalised during physical wiring and recorded in `Docs/Pinout/`. This table must be updated upon finalisation.

---

## 7. Sensor Placement

Physical sensor placement is critical for accurate, collision-free navigation and reliable environmental monitoring.

### HC-SR04 Ultrasonic Sensors

| Sensor | Mounting Position | Facing Direction | Coverage Zone | Mounting Height |
|--------|-----------------|-----------------|---------------|-----------------|
| Front | Front face of chassis, horizontally centred | Forward | 15° cone, 2 cm – 400 cm | ~10 cm AGL |
| Left | Left side of chassis, horizontally centred | Outward left | 15° cone, 2 cm – 400 cm | ~10 cm AGL |
| Right | Right side of chassis, horizontally centred | Outward right | 15° cone, 2 cm – 400 cm | ~10 cm AGL |
| Rear | Rear face of chassis, horizontally centred | Backward | 15° cone, 2 cm – 400 cm | ~10 cm AGL |

> AGL = Above Ground Level. Sensors should be mounted at a height that captures obstacles relevant to the rover body (walls, chair legs, furniture) without pointing at ground clutter.

The four HC-SR04 sensors provide a 360° proximity perimeter. Their placement should minimise acoustic crosstalk between adjacent sensors. Sequential (time-multiplexed) firing is required in firmware — one sensor fires at a time — to prevent one sensor's transmitted pulse from being falsely detected by an adjacent sensor's receiver.

### VL53L0X Time-of-Flight Sensors

| Sensor | Location | PCA9548A Channel | Purpose |
|--------|----------|-----------------|---------|
| Front ToF | Front of chassis, co-located with or below the Front HC-SR04 | CH2 | High-precision short-range frontal measurement; supplements HC-SR04 at distances below 30 cm |
| Pan ToF | Mounted on the pan/tilt camera bracket, co-axial with or adjacent to the webcam | CH3 | Measures distance along the camera's pan axis; provides depth context for vision detections |

The VL53L0X provides a narrow field of view (~25°) and high precision (±3%) compared to the HC-SR04 at close range. The Front ToF is particularly valuable for slow-speed approach manoeuvres where the HC-SR04 minimum range (2 cm) is too coarse.

The Pan ToF sensor is mounted on the camera pan arm so that it rotates with the camera. As the camera tracks a target, the Pan ToF measures actual distance along the camera's line of sight, enabling the Raspberry Pi to estimate real-world depth of detected objects.

### MPU6050 IMU

| Parameter | Value |
|-----------|-------|
| Location | Chassis centre, mounted flat and level with the chassis base plate |
| Orientation | X-axis aligned with the rover's forward direction |
| Purpose | Pitch/roll/yaw estimation, vibration monitoring, dead reckoning support |

Mount as close to the rover's centre of mass as possible to minimise lever-arm effects on accelerometer readings. Adhesive foam mounting tape is adequate for V1 vibration isolation.

### MQ-2 Gas Sensor

| Parameter | Value |
|-----------|-------|
| Location | Top of chassis, with open-air exposure |
| Interface | Analog — GPIO10 |
| Purpose | Smoke, LPG, and combustible gas detection |
| Warm-up Time | 20 – 30 seconds after power-on before readings are stable |

The MQ-2 requires open airflow and must not be enclosed in a sealed compartment. Its heater element draws approximately 150 mA continuously; ensure the 5V supply rail has adequate headroom.

---

## 8. Camera System

### USB Webcam

| Parameter | Value |
|-----------|-------|
| Interface | USB 2.0, connected to Raspberry Pi |
| Processing | Raspberry Pi — all frame capture and inference |
| Target Resolution | 640 x 480 or 1280 x 720 |
| Target Frame Rate | 15 – 30 fps |
| Typical Field of View | 60° – 90° horizontal (lens-dependent) |

The webcam is the rover's primary sensing organ for object detection, tracking, and visual navigation. The ESP32-S3 has no awareness of or connection to the webcam.

### Pan/Tilt Mechanism

The webcam is mounted on a two-axis pan/tilt bracket driven by two SG90 servos:

| Axis | Servo | GPIO | Range | Purpose |
|------|-------|------|-------|---------|
| Pan | SG90 | GPIO11 | 0° – 180° (software-limited) | Horizontal camera sweep |
| Tilt | SG90 | GPIO12 | 45° – 135° (software-limited) | Vertical camera elevation |

The Pan ToF sensor (VL53L0X, CH3) is mounted on the same bracket and rotates with the camera. The Raspberry Pi issues pan and tilt angle commands to the ESP32-S3 via the serial JSON bridge. Software angle limits must be enforced in firmware to prevent the servo from exceeding its mechanical range of motion and stalling against a stop.

### Camera–Sensor Spatial Relationship

```
Camera Line of Sight
        |
        v    (Pan axis rotates both together)
+-------+--------+
|  USB Webcam    |  --> Frame capture --> Raspberry Pi --> Object detection
+-------+--------+
|  VL53L0X (Pan) |  --> Distance reading --> ESP32-S3 --> Telemetry to Pi
+----------------+

The Pi fuses: detected object class + bounding box position + ToF distance
to estimate real-world depth and spatial position of detected targets.
```

---

## 9. OLED Eye System

### Overview

Recon Rover V1 features two SSD1306 OLED displays mounted at the front of the chassis, serving as the rover's eyes. These displays render animated expressions that reflect the current AI context, providing a human-readable emotional state indicator.

### Display Specifications

| Parameter | Value |
|-----------|-------|
| Model | SSD1306 |
| Resolution | 128 x 64 pixels |
| Interface | I2C |
| I2C Address | 0x3C (both panels, identical) |
| Supply Voltage | 3.3 V – 5.0 V |
| Display Size | 0.96" (typical) |

### Why Two Displays?

Two physically separated displays create a genuinely binocular eye system. Each eye is rendered independently, enabling:

- Asymmetric expressions (one eye wider, one narrowed).
- Independent blinking of left and right eyes.
- Gaze direction animation — pupils shift in opposite directions on each panel to simulate looking sideways.
- Per-eye error states (e.g., one eye shows an "X" to indicate a subsystem fault).

A single wide display spanning both eyes at adequate resolution would require a larger, more expensive panel and would lose the physical separation that makes the eyes look authentic on the chassis.

### Why PCA9548A Is Required

Both SSD1306 panels share the identical default I2C address (0x3C). On a standard I2C bus, both panels would respond simultaneously to every transaction, making independent control impossible.

The PCA9548A resolves this by routing each OLED to a separate, electrically isolated channel:

- Writing to PCA9548A CH0 communicates only with the Left Eye.
- Writing to PCA9548A CH1 communicates only with the Right Eye.
- Only one channel is ever active at a time.

### Eye Rendering Philosophy

Eye expressions are pre-defined animation bitmaps stored in the ESP32-S3 flash memory. The Raspberry Pi does not transmit pixel data over the serial bridge — this would be too slow and bandwidth-intensive.

Instead, the Raspberry Pi sends a lightweight expression identifier string, and the ESP32-S3 retrieves the corresponding bitmaps and animation sequences from local flash storage.

This keeps the serial bus lightweight and gives the ESP32-S3 full local control over animation timing, blinking cadence, and transition effects — without any real-time frame dependency on the Pi.

| Expression ID | Description | Example Trigger |
|---------------|-------------|-----------------|
| `idle` | Slow blinking, neutral gaze | Default state |
| `happy` | Wide open, curved top | Person detected |
| `curious` | One eye slightly narrowed, gaze offset | Object tracking |
| `alert` | Wide open, static, no blink | Close obstacle |
| `sleepy` | Half-closed, slow blink | Low activity |
| `error` | X symbols on both eyes | Critical fault |
| `hazard` | Narrow eyes, rapid blink | Gas threshold exceeded |

---

## 10. Motion System

### 4WD Chassis Overview

Recon Rover V1 uses a four-wheel drive (4WD) differential steering chassis. All four wheels are driven by independent DC gear motors, grouped into left-side and right-side pairs for differential steering.

| Motor ID | Position | Side Group |
|----------|----------|-----------|
| FL | Front Left | Left |
| RL | Rear Left | Left |
| FR | Front Right | Right |
| RR | Rear Right | Right |

### L298N Motor Driver

| Parameter | Value |
|-----------|-------|
| Model | L298N |
| Type | Dual H-bridge |
| Motor channels | 2 |
| Logic voltage | 5V |
| Motor supply | VBAT (raw battery) |
| Maximum continuous current | 2 A per channel |
| Peak current | 3 A per channel |
| Speed control | PWM on ENA / ENB |
| Direction control | IN1/IN2 (Ch A), IN3/IN4 (Ch B) |

**Motor Grouping:**

| L298N Channel | Motors Driven | Direction Pins | Speed Pin (PWM) |
|--------------|--------------|---------------|----------------|
| Channel A | FL + RL (Left side) | IN1, IN2 | ENA |
| Channel B | FR + RR (Right side) | IN3, IN4 | ENB |

Both motors on the same side share one H-bridge channel, wired in parallel. The L298N provides up to 2A continuous per channel; DC gear motors draw approximately 200 mA each under normal operating load.

### Motor Direction Logic

| IN1 | IN2 | Left Side Result |
|-----|-----|-----------------|
| HIGH | LOW | Forward |
| LOW | HIGH | Reverse |
| HIGH | HIGH | Brake |
| LOW | LOW | Coast (free wheel) |

The same logic applies to IN3/IN4 for the right side.

### Differential Steering Modes

| Mode | Left Side | Right Side |
|------|-----------|-----------|
| Forward | Forward, speed N | Forward, speed N |
| Reverse | Reverse, speed N | Reverse, speed N |
| Turn Left (gradual) | Forward, speed N-x | Forward, speed N |
| Turn Right (gradual) | Forward, speed N | Forward, speed N-x |
| Pivot Left (in place) | Reverse, speed N | Forward, speed N |
| Pivot Right (in place) | Forward, speed N | Reverse, speed N |
| Stop (brake) | Brake | Brake |
| Stop (coast) | Coast | Coast |

### Pan/Tilt Mechanism

| Servo | Axis | GPIO | Mechanical Range | Software Limit |
|-------|------|------|-----------------|----------------|
| Pan servo | Horizontal | GPIO11 | 0° – 180° | To be defined during calibration |
| Tilt servo | Vertical | GPIO12 | 0° – 180° | 45° – 135° recommended |

Software angle limits must be enforced in ESP32-S3 firmware to prevent stall against mechanical stops.

---

## 11. Lighting System

### WS2812B ARGB LED Strips

| Parameter | Value |
|-----------|-------|
| Model | WS2812B |
| LEDs per strip | 5 |
| Total LEDs | 10 |
| Protocol | Single-wire NZR (800 kHz) |
| Supply voltage | 5.0 V |
| Current per LED at full white | 60 mA |
| Maximum total current (all 10, full white) | 600 mA |

### Placement

| Strip | Physical Position | Orientation |
|-------|-----------------|-------------|
| Left strip | Left lateral face of chassis | LEDs facing outward-left |
| Right strip | Right lateral face of chassis | LEDs facing outward-right |

Lateral placement maximises visibility from all approach angles and provides effective scene illumination for the webcam in low-light environments.

### Status Indication Modes

| Mode | Colour | Pattern | Condition |
|------|--------|---------|-----------|
| Idle | Blue | Slow pulse | Active, stationary |
| Patrolling | Cyan | Steady | Autonomous navigation active |
| Object Detected | Green | Solid | Known object in camera view |
| Tracking | Yellow | Chasing fill | Following a target |
| Obstacle Alert | Orange | Rapid flash | Close obstacle detected |
| Gas Hazard | Red | Fast strobe | MQ-2 threshold exceeded |
| Low Battery | Red | Slow pulse | Battery below warning threshold |
| Error | Magenta | Alternating | System fault |
| Startup | White | Sweep animation | Initialisation sequence |
| Shutdown | Off | — | Graceful power-down |

LED modes and colours are defined in ESP32-S3 firmware and triggered by mode command packets received from the Raspberry Pi.

### Future Animation Capability

The WS2812B protocol supports full per-LED RGBW control. Future firmware can implement:

- Directional indicators (animate LEDs toward direction of travel).
- Reactive audio visualisation (pulse amplitude from microphone input, relayed by Pi).
- Night mode (dim amber fill for low-light operation).
- Custom mission profiles (user-defined colour schemes per operational mode).

---

## 12. Expansion Capability

### Available I2C Channels (PCA9548A)

| Channel | Status | Candidate Future Devices |
|---------|--------|-------------------------|
| CH4 | Available | BMP280 (barometric pressure + temperature) |
| CH5 | Available | Additional VL53L0X (side or rear precision ranging) |
| CH6 | Available | Additional SSD1306 (auxiliary status display) |
| CH7 | Available | INA219 (if I2C address conflicts with direct bus use) |

### Available GPIO (ESP32-S3 N16R8)

The ESP32-S3 N16R8 provides up to 45 GPIOs. Current allocation uses approximately 15–21 pins depending on final motor driver wiring, leaving 24–30 GPIOs available. Planned uses include:

| Peripheral | GPIO Required |
|-----------|--------------|
| Motor encoders (4 motors, quadrature) | 2 per encoder = 8 pins |
| Additional HC-SR04 | 2 per sensor |
| Additional servo axis | 1 PWM pin per axis |
| Buzzer / speaker | 1 pin |
| Status push button | 1 pin |

### Available USB Port (Raspberry Pi)

The Raspberry Pi 3B+ has 4 USB 2.0 ports. Three are currently used, leaving one port available for:

- USB GPS module.
- USB LTE/4G modem for remote telemetry.
- USB-to-serial adapter for additional peripherals.
- USB hub to expand further.

### Serial Protocol Expansion

The JSON serial protocol is forward-compatible. New packet `type` values can be added without modifying existing firmware parsers — unrecognised types are silently ignored. This enables incremental addition of new sensor categories, command types, and status reports as hardware is integrated.

---

## 13. Hardware Failure Strategy

Hardware failures are expected events. The system must degrade gracefully rather than fail catastrophically.

### Sensor Failures

| Failed Sensor | Detection Method | System Response |
|--------------|-----------------|-----------------|
| HC-SR04 (any one) | Reading returns 0 or polling timeout | Flag that direction zone as unknown; treat as obstructed; prohibit navigation into flagged zone |
| HC-SR04 (multiple) | Multiple zones flagged | Escalate to navigation halt; await operator intervention |
| VL53L0X (Front, CH2) | I2C error on CH2 | Fall back to Front HC-SR04 for proximity; log sensor fault warning |
| VL53L0X (Pan, CH3) | I2C error on CH3 | Camera tracking continues without range data; disable depth-based tracking features |
| MPU6050 | I2C no response | Disable IMU-dependent navigation features; continue with remaining sensor array |
| MQ-2 | ADC reads implausible value (< 0 or > reference) | Log sensor fault; disable gas hazard detection; do not raise false alarms |
| INA219 (planned) | I2C no response | Disable power monitoring; log warning; continue operating |

### I2C Bus / PCA9548A Failure

If the PCA9548A fails or loses power, all devices on channels CH0–CH3 (both OLEDs, both VL53L0Xs) become unreachable simultaneously. The ESP32-S3 firmware must:

1. Detect the failure via I2C transaction timeout.
2. Log a critical I2C bus fault event in the telemetry stream.
3. Disable all features dependent on PCA-connected devices.
4. Continue operating with the remaining sensors (HC-SR04 array, MPU6050, MQ-2).

### Camera Disconnect (USB Webcam)

1. The Raspberry Pi vision pipeline raises an exception and logs the event.
2. Navigation switches to sensor-only mode (HC-SR04 + VL53L0X obstacle avoidance; no object detection or tracking).
3. A camera fault event is pushed to the dashboard.
4. The rover continues operating safely using only its proximity sensor suite.

### Microphone Disconnect (USB Microphone)

1. The Raspberry Pi audio pipeline raises an exception and logs the event.
2. Voice command processing is disabled.
3. All other systems continue operating normally.
4. A hardware fault event is pushed to the dashboard.

### Motor Driver Failure (L298N)

1. Motors cease responding to commands.
2. The rover must halt all movement immediately.
3. A critical motor fault alert is transmitted to the Raspberry Pi and to the dashboard.
4. If motor encoders are available (V1.x feature), expected vs. actual wheel speed can be used for early detection before full failure.

### Battery Voltage Drop

| Voltage Level (2S Li-Po) | Threshold | Action |
|--------------------------|-----------|--------|
| 7.0 V | Warning | Event pushed to dashboard; LEDs switch to slow red pulse |
| 6.5 V | Critical | Alert issued; reduce motor speed; navigate to home position if known |
| 6.0 V | Hardware cutoff | BMS disconnects all loads; all systems lose power |

The INA219 sensor (planned) will monitor voltage with the precision necessary for these thresholds. Until installed, battery voltage monitoring relies on a resistor divider on an available ADC pin or manual periodic checks.

---

## 14. Hardware Design Decisions

This section explains the rationale behind each major hardware choice, and why alternatives were not selected.

### ESP32-S3 N16R8

**Chosen because:**
- Dual-core Xtensa LX7 at 240 MHz provides ample headroom for simultaneous sensor polling, PWM generation, I2C management, and serial communication.
- Native USB CDC (no external USB-to-serial chip required) simplifies the Pi–ESP32 serial bridge.
- 16 MB Flash and 8 MB PSRAM provide generous storage for OLED animation assets and future firmware expansion.
- 45 available GPIOs accommodate the full sensor and actuator complement with substantial room to grow.
- Low cost and broad community/library support.

**Alternatives considered and rejected:**
- *Arduino Mega:* Insufficient processing speed, no native USB CDC, 5V logic creates additional level-shifting requirements throughout.
- *STM32 series:* More complex toolchain, higher cost, smaller hobbyist ecosystem for rapid prototyping.
- *RP2040 (Raspberry Pi Pico):* Excellent real-time performance, but limited PSRAM and Flash on standard variants vs. the N16R8 configuration.

### Raspberry Pi 3B+

**Chosen because:**
- Linux OS enables the full Python ecosystem: OpenCV, TensorFlow Lite, SpeechRecognition, asyncio, WebSocket.
- Quad-core ARM Cortex-A53 at 1.4 GHz provides adequate throughput for concurrent lightweight inference, audio processing, and network I/O.
- 1 GB RAM is sufficient for simultaneous vision, audio, and networking workloads.
- 4 USB ports and built-in WiFi cover all Pi-side connectivity without expansion.
- Mature, extensively documented platform.

**Alternatives considered and rejected:**
- *Raspberry Pi 4:* More capable, but higher cost, higher power consumption, and more demanding thermal management in an enclosed chassis.
- *Jetson Nano:* Superior AI inference throughput, but significantly higher cost, power, and supply complexity, not justified for V1 scope.
- *Offboard PC (WiFi link):* Eliminates onboard processing limitations, but creates a hard WiFi dependency for all real-time decisions — unacceptable for autonomous operation.

### USB Webcam

**Chosen because:**
- Universal USB interface is plug-and-play on Linux (V4L2 subsystem).
- No proprietary drivers required.
- Wide selection of resolutions and field-of-view options.
- Mechanically replaceable without hardware modification.

**Alternatives considered and rejected:**
- *Raspberry Pi Camera Module (CSI):* Lower latency via CSI interface, but the ribbon cable is inflexible and difficult to route through a rotating pan/tilt bracket without damage risk.
- *Intel RealSense D-series:* Provides a built-in depth map, but high cost and high power draw are not justified at V1 scope.

### USB Microphone

**Chosen because:**
- Universal USB interface; no audio HAT, sound card, or additional GPIO required.
- Replaceable and upgradeable without hardware modification.

**Alternatives considered and rejected:**
- *I2S MEMS microphone:* Lower cost, but requires I2S interface configuration and additional firmware complexity.
- *ReSpeaker audio HAT:* Adds far-field pickup and DSP processing, but increases cost, weight, and occupies Pi GPIO header real estate.

### PCA9548A I2C Multiplexer

**Chosen because:**
- Directly and elegantly resolves I2C address conflicts between two SSD1306 OLEDs (0x3C) and two VL53L0X sensors (0x29).
- Provides 8 isolated I2C channels, allowing significant future expansion at zero additional hardware cost.
- Well supported by ESP-IDF and Arduino I2C libraries.
- Low cost; minimal board space.

**Alternatives considered and rejected:**
- *XSHUT-based VL53L0X address reassignment + SA0-based SSD1306 address change:* Adds extra GPIO pins, firmware sequencing complexity, and only partially solves the problem (SSD1306 has only one alternative address, 0x3D). The multiplexer is simpler, cleaner, and more scalable.
- *Multiple independent I2C buses on ESP32-S3:* Consumes additional GPIO pins without solving the scalability problem.

### Dual SSD1306 OLEDs

**Chosen because:**
- Two physically separated displays create authentic binocular eye geometry on the chassis face.
- SSD1306 is the most widely supported OLED controller in the embedded ecosystem.
- Very low current draw (< 20 mA each at typical brightness).
- Extensive library support for bitmap rendering and animation.

**Alternatives considered and rejected:**
- *Single wide display:* Loses the physical separation that creates the expressive appearance. Software cannot compensate for physical form factor.
- *RGB OLEDs (SSD1351):* Colour eyes are visually compelling, but higher cost, higher current, and more complex driver. Deferred to future version.

### VL53L0X Time-of-Flight Sensors

**Chosen because:**
- High-precision distance measurement (±3%) in a narrow FOV (~25°), immune to target surface colour or reflectivity.
- Short minimum range (< 5 cm) and maximum range up to 2 m — ideal for close-approach and camera-depth estimation.
- I2C interface integrates naturally with the existing bus infrastructure.

**Alternatives considered and rejected:**
- *Additional HC-SR04 units:* Coarser precision at short range, wider acoustic cone, acoustic crosstalk risk between units. Cannot provide the narrow-angle precision needed for camera depth estimation.
- *Sharp GP2Y IR sensors:* Analogue output affected by surface colour and ambient IR; non-linear response requires per-unit calibration.

### HC-SR04 Ultrasonic Sensors

**Chosen because:**
- Low cost allows full 360° chassis coverage with four units.
- 2 cm – 400 cm range covers all operationally relevant obstacle distances.
- Simple TRIG/ECHO GPIO interface requires no I2C address management.
- Wide 15° cone provides better coverage of angled and off-centre obstacles than narrow-beam alternatives.

**Alternatives considered and rejected:**
- *VL53L0X on all four sides:* More accurate at short range, but four times the cost and the narrow FOV would miss angled obstacles that the broader HC-SR04 cone captures.
- *Single rotating ultrasonic scanner:* Eliminates the multi-unit cost, but introduces mechanical complexity, dead zones during scan sweeps, and reduced update rate on any given direction.

### MQ-2 Gas Sensor

**Chosen because:**
- Detects LPG, smoke, methane, hydrogen — relevant for indoor reconnaissance in diverse or unknown environments.
- Analogue output connects directly to the ESP32 ADC.
- Low cost; widely used in research and hobbyist platforms.
- Adds genuine safety capability (gas hazard detection) that expands the rover's reconnaissance utility.

**Alternatives considered and rejected:**
- *MQ-135 (air quality):* Detects a broader pollutant range but is less sensitive to combustible gases central to fire/gas leak detection.
- *BME688 (Bosch multi-gas):* More accurate, temperature-compensated, digital I2C output — significantly superior, but substantially higher cost and more complex calibration. A strong candidate for V2.

### L298N Motor Driver

**Chosen because:**
- Dual H-bridge design controls two independent motor channels; sufficient for 4WD left/right grouping.
- Handles motor supply up to 46V and 2A continuous per channel — adequate for the DC gear motors.
- Built-in back-EMF protection diodes.
- Widely available, extensively documented, very low cost.
- Straightforward PWM speed control via ENA/ENB.

**Alternatives considered and rejected:**
- *DRV8833:* Lower voltage tolerance, lower current rating; suitable for lighter motors only.
- *MX1508:* Lower quality, limited current rating, no heatsink provision.
- *TB6612FNG (per motor, x4):* More efficient, lower heat dissipation, but higher cost and board space per motor.
- *Sabertooth 2x12:* High quality and compact, but significant capability and cost overkill for 6V gear motors at V1 scope.

---

## 15. Conclusion

Recon Rover V1 is built on a hardware philosophy of deliberate simplicity at the component level and deliberate complexity at the system level.

Individually, each component — the HC-SR04, the SSD1306, the L298N — is a well-understood, low-cost, widely supported device. Together, unified by the ESP32-S3 as the reactive hardware hub and the Raspberry Pi 3B+ as the cognitive brain, they form a cohesive, scalable, and professionally structured platform.

The key characteristics of this hardware architecture are:

- **Physical separation of cognition and reaction.** The USB serial bridge is the only connection between the two processors. This is a hardware constraint, not merely a software convention, and it enforces the system's most important design principle.

- **Systematic I2C management.** The PCA9548A multiplexer resolves address collisions that would otherwise make the chosen sensor and display configuration impossible, while simultaneously reserving four expansion channels for future hardware.

- **Layered power isolation.** Separate 5V rails for the Raspberry Pi and the ESP32-S3 subsystem prevent switching noise from the motor and LED loads from coupling into the Pi's sensitive computation and USB subsystems.

- **Omnidirectional sensing.** The combination of four HC-SR04 units covering all cardinal directions, two VL53L0X units providing precision depth on the critical front and pan axes, and the MPU6050 providing inertial state gives the navigation layer a rich, multi-modal model of the rover's physical environment.

- **Designed to grow.** Four spare PCA9548A channels, approximately 24–30 spare GPIO pins, one spare USB port, and a forward-compatible serial protocol mean that the hardware foundation of V1 can support substantially expanded capability without any architectural rework.

This document is the official hardware reference for Recon Rover V1. All wiring decisions, pin assignments, component substitutions, and future hardware additions must remain consistent with the architecture documented here and must not contradict the system-level principles established in `SYSTEM_ARCHITECTURE.md`.

---

*End of Document*

---

> **Document Control**
>
> | Version | Date | Author | Notes |
> |---------|------|--------|-------|
> | 1.0 | 2026-06-28 | Lead Hardware Architect | Initial foundation draft |
