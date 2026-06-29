# Recon Rover V1 — Firmware Architecture

**Document Version:** 1.0  
**Status:** Foundation Specification  
**Last Updated:** 2026-06-28  
**Author:** Lead Embedded Systems Engineer  
**Classification:** Internal Engineering Specification  
**Target Hardware:** ESP32-S3 N16R8 (dual-core Xtensa LX7, 240 MHz, 16 MB Flash, 8 MB PSRAM)  
**References:**
- `SYSTEM_ARCHITECTURE.md` — System design, processor responsibilities, design principles
- `HARDWARE_ARCHITECTURE.md` — GPIO allocation, I2C topology, power architecture
- `SOFTWARE_ARCHITECTURE.md` — FreeRTOS task layout, inter-task queues, module responsibilities
- `COMMUNICATION_PROTOCOL.md` — JSON packet specifications, serial framing, timing requirements

> **This document is the single authoritative firmware architecture reference for the ESP32-S3 N16R8 on Recon Rover V1. It defines every task, queue, driver, interrupt, and memory region. All firmware development must comply with this specification.**

---

## Table of Contents

1. [Firmware Philosophy](#1-firmware-philosophy)
2. [Firmware Layer Architecture](#2-firmware-layer-architecture)
3. [Boot Process](#3-boot-process)
4. [FreeRTOS Architecture](#4-freertos-architecture)
5. [Core Allocation](#5-core-allocation)
6. [Task Creation Order](#6-task-creation-order)
7. [Task Priority Table](#7-task-priority-table)
8. [Task Lifecycle](#8-task-lifecycle)
9. [Inter-Task Communication](#9-inter-task-communication)
10. [Queue Architecture](#10-queue-architecture)
11. [Event Groups](#11-event-groups)
12. [Mutex Strategy](#12-mutex-strategy)
13. [Timer Strategy](#13-timer-strategy)
14. [Watchdog Strategy](#14-watchdog-strategy)
15. [Memory Layout](#15-memory-layout)
16. [Flash Partition Usage](#16-flash-partition-usage)
17. [RAM Allocation Strategy](#17-ram-allocation-strategy)
18. [Heap Management](#18-heap-management)
19. [Stack Size Planning](#19-stack-size-planning)
20. [Sensor Manager Architecture](#20-sensor-manager-architecture)
21. [Motor Controller Architecture](#21-motor-controller-architecture)
22. [Servo Controller Architecture](#22-servo-controller-architecture)
23. [OLED Renderer](#23-oled-renderer)
24. [LED Controller](#24-led-controller)
25. [Command Parser](#25-command-parser)
26. [Telemetry Builder](#26-telemetry-builder)
27. [Health Monitor](#27-health-monitor)
28. [Fault Manager](#28-fault-manager)
29. [Safe Mode](#29-safe-mode)
30. [Startup Self-Test](#30-startup-self-test)
31. [Runtime Diagnostics](#31-runtime-diagnostics)
32. [Sensor Polling Strategy](#32-sensor-polling-strategy)
33. [Scheduling Timeline](#33-scheduling-timeline)
34. [Interrupt Usage](#34-interrupt-usage)
35. [Driver Layer Design](#35-driver-layer-design)
36. [Hardware Abstraction Layer](#36-hardware-abstraction-layer)
37. [Configuration Strategy](#37-configuration-strategy)
38. [Logging Strategy](#38-logging-strategy)
39. [Error Recovery](#39-error-recovery)
40. [Module Dependency Diagram](#40-module-dependency-diagram)
41. [Firmware Folder Structure](#41-firmware-folder-structure)
42. [File Responsibility Table](#42-file-responsibility-table)
43. [Coding Standards](#43-coding-standards)
44. [Scalability Strategy](#44-scalability-strategy)
45. [Future Firmware Modules](#45-future-firmware-modules)
46. [Performance Targets](#46-performance-targets)
47. [Resource Budget](#47-resource-budget)
48. [Failure Scenarios](#48-failure-scenarios)
49. [Design Constraints](#49-design-constraints)
50. [Conclusion](#50-conclusion)

---

## 1. Firmware Philosophy

### The Governing Principle

> **The ESP32-S3 firmware does one thing with absolute reliability: it makes the hardware respond to the physical world in real time, and it faithfully reports what it observes to the Raspberry Pi. It does not think. It does not decide. It executes and reports.**

This principle is not a software preference — it is a system-level architectural constraint imposed by `SYSTEM_ARCHITECTURE.md`. The ESP32-S3 is the reactive layer of the Recon Rover V1 dual-processor architecture. Its firmware must be deterministic, minimal, and failure-resistant.

### Core Firmware Tenets

| Tenet | Statement | Implication |
|-------|-----------|-------------|
| **Determinism over cleverness** | Every task runs in bounded time at a known rate | No dynamic memory allocation in tasks; no unbounded loops |
| **Hardware isolation** | The firmware is the only software that touches hardware registers | All Pi commands are mediated through the command parser; no direct Pi GPIO access exists |
| **Fail to safe** | When anything goes wrong, actuators stop | Watchdog, link loss, and fault manager all converge on the same safe state |
| **Report everything** | Every sensor fault, every clamped value, every timeout is reported to the Pi | Health flags and fault packets provide full observability |
| **Independence** | Firmware must operate correctly when the Raspberry Pi is absent | Boot sequence, sensor reading, and self-test complete regardless of Pi connection status |
| **No shared state** | FreeRTOS queues and semaphores are the only inter-task communication mechanism | Global variables accessible from multiple tasks are forbidden |
| **Allocation at startup** | All memory — queues, stacks, buffers — is allocated during boot | No runtime memory allocation in steady-state operation |

### What the Firmware Is Responsible For

```
OWNS:
  - All GPIO pins (digital I/O, PWM, ADC)
  - All I2C transactions (PCA9548A, MPU6050, VL53L0X, SSD1306, INA219)
  - All PWM outputs (LEDC peripheral for motors and servos)
  - All WS2812B LED data generation
  - All HC-SR04 pulse timing
  - USB CDC serial communication
  - FreeRTOS task scheduling
  - Hardware watchdog and software watchdog
  - JSON telemetry packet construction
  - JSON command packet parsing
  - OLED eye bitmap rendering
  - Self-test on boot

DOES NOT OWN:
  - USB Webcam
  - USB Microphone
  - WiFi
  - AI inference
  - Navigation decisions
  - Object detection
  - Voice processing
  - Dashboard communication (beyond serial bridge)
```

---

## 2. Firmware Layer Architecture

The firmware is organised into four distinct layers. Each layer communicates only with its immediate neighbours. No layer skips a level.

```
+==================================================================+
|  LAYER 4 — APPLICATION LAYER                                     |
|                                                                  |
|  main.cpp — Entry point, boot orchestration, task spawning       |
|                                                                  |
+==================================================================+
                               |
+==================================================================+
|  LAYER 3 — SUBSYSTEM LAYER                                       |
|                                                                  |
|  sensor_manager    motor_controller    servo_controller          |
|  oled_renderer     led_controller      health_monitor            |
|  telemetry_builder command_parser      serial_handler            |
|  fault_manager     watchdog                                      |
|                                                                  |
+==================================================================+
                               |
+==================================================================+
|  LAYER 2 — DRIVER LAYER                                          |
|                                                                  |
|  driver_hcsr04    driver_vl53l0x    driver_mpu6050               |
|  driver_mq2       driver_ina219     driver_pca9548a              |
|  driver_ssd1306   driver_ws2812b    driver_l298n                 |
|  driver_sg90                                                     |
|                                                                  |
+==================================================================+
                               |
+==================================================================+
|  LAYER 1 — HARDWARE ABSTRACTION LAYER                            |
|                                                                  |
|  hal_gpio     hal_i2c     hal_ledc     hal_adc                   |
|  hal_uart_cdc hal_rmt                                            |
|                                                                  |
+==================================================================+
                               |
+==================================================================+
|  LAYER 0 — HARDWARE (Physical)                                   |
|                                                                  |
|  HC-SR04 x4  VL53L0X x2  MPU6050  MQ-2   INA219                 |
|  SSD1306 x2  PCA9548A    L298N    SG90x2  WS2812B x2             |
|  USB CDC                                                         |
|                                                                  |
+==================================================================+
```

### Layer Responsibilities

| Layer | Name | Responsibility | Hardware Access |
|-------|------|---------------|-----------------|
| L4 | Application | Boot orchestration; task lifecycle management | None direct |
| L3 | Subsystem | FreeRTOS tasks; business logic; JSON parsing/building | Via Layer 2 only |
| L2 | Driver | Device-specific protocols (I2C sequences, PWM timings) | Via Layer 1 only |
| L1 | HAL | ESP-IDF peripheral APIs (gpio_set_level, i2c_master_transmit) | Direct register access |
| L0 | Hardware | Physical sensors and actuators | Physical signals |

---

## 3. Boot Process

### Complete Boot Sequence

```
+------------------------------------------------------------------+
|  ESP32-S3 POWER-ON RESET                                         |
+------------------------------------------------------------------+
                    |
                    v
[STAGE 0: ROM Boot]
  ESP32 ROM loads bootloader from flash partition 0x0000
  Bootloader verifies OTA partition table
  Bootloader jumps to application partition
                    |
                    v
[STAGE 1: ESP-IDF System Initialisation]
  FreeRTOS kernel initialised
  Memory regions configured (DRAM, IRAM, PSRAM)
  CPU0 and CPU1 clocked to 240 MHz
  Non-Volatile Storage (NVS) initialised
  Heap allocator initialised
                    |
                    v
[STAGE 2: HAL Initialisation] (main.cpp app_main, sequential)
  hal_gpio:     Configure all GPIO pins (direction, pull, mode)
  hal_i2c:      Configure I2C master (SDA=GPIO13, SCL=GPIO14, 400kHz)
  hal_ledc:     Configure LEDC timer and channels (motors + servos)
  hal_adc:      Configure ADC1 channel for GPIO10 (MQ-2)
  hal_uart_cdc: Initialise USB CDC driver; allocate TX/RX buffers
  hal_rmt:      Configure RMT peripheral for WS2812B NZR signal
                    |
                    v
[STAGE 3: Startup Self-Test] (see Section 30)
  I2C bus scan — verify PCA9548A responds at 0x70
  MPU6050 WHO_AM_I register check
  VL53L0X CH2 — ping and model ID check
  VL53L0X CH3 — ping and model ID check
  MQ-2 ADC — read and check range plausibility
  L298N — assert all direction pins LOW (safe state)
  Servo — initialise LEDC; set both servos to 90 degrees
  WS2812B — short startup colour flash (white) to verify data line
  SSD1306 CH0 — send init sequence; display boot screen
  SSD1306 CH1 — send init sequence; display boot screen
  Self-test result stored in boot_status struct
                    |
                    v
[STAGE 4: Subsystem Initialisation]
  sensor_manager:    Initialise sensor state, fault flags, reading buffers
  motor_controller:  Initialise motor state to BRAKE (all motors stopped)
  servo_controller:  Confirm servos at centre; store current angles
  oled_renderer:     Load idle expression; queue first render
  led_controller:    Set startup animation sequence
  telemetry_builder: Initialise telemetry struct with defaults
  command_parser:    Initialise dispatch table
  health_monitor:    Initialise health flag struct (all sensors assumed OK)
  fault_manager:     Initialise fault queue and fault log
  watchdog:          Register all task watchdog handles; set timeout
                    |
                    v
[STAGE 5: Queue and IPC Allocation]
  Allocate all FreeRTOS queues (see Section 10)
  Allocate all FreeRTOS event groups (see Section 11)
  Allocate all FreeRTOS mutexes (see Section 12)
  Allocate all FreeRTOS timers (see Section 13)
  Verify all allocations succeeded (halt on failure)
                    |
                    v
[STAGE 6: Task Spawning] (see Section 6 for order)
  Spawn all FreeRTOS tasks with defined stack sizes and priorities
  All tasks start in suspended state
                    |
                    v
[STAGE 7: USB CDC Ready]
  USB CDC driver connected and TX buffer flushed
  Transmit READY packet over serial (proto=1, type="ready", seq=0)
                    |
                    v
[STAGE 8: Resume All Tasks]
  vTaskResume all spawned tasks
  FreeRTOS scheduler takes control
  System transitions to OPERATIONAL state
+------------------------------------------------------------------+
```

### Boot Timing Budget

| Stage | Maximum Time | Failure Action |
|-------|-------------|---------------|
| ROM Boot | ~100 ms | Hardware reset |
| ESP-IDF Init | ~200 ms | Hardware reset |
| HAL Init | ~50 ms | Halt + error LED |
| Self-Test | ~500 ms | Log failures; continue (non-critical sensors) |
| Subsystem Init | ~100 ms | Halt on critical failure |
| Queue Allocation | ~20 ms | Halt + error LED |
| Task Spawning | ~50 ms | Halt on failure |
| READY Packet | ~5 ms | Retry once |
| **Total boot time** | **~1.0 s** | |

---

## 4. FreeRTOS Architecture

### FreeRTOS Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Kernel | FreeRTOS (ESP-IDF bundled) | Fully integrated with ESP32 SDK |
| Scheduler type | Preemptive, priority-based | Required for deterministic task execution |
| Tick rate | 1000 Hz (1 ms tick) | Fine-grained timing for sensor scheduling |
| SMP mode | Symmetric Multiprocessing (both cores) | Maximises throughput |
| Idle task | One per core | Standard FreeRTOS SMP behaviour |
| Timer task | Core 0 | FreeRTOS software timer daemon |
| Stack overflow detection | Stack Canary (configCHECK_FOR_STACK_OVERFLOW = 2) | Detects stack corruption |
| Heap model | heap_4 (merged, coalescing) | Best for systems with mixed alloc/free patterns |
| Max task priority | 25 (ESP-IDF default) | Rover firmware uses 2–5 only |
| Total FreeRTOS tasks | 10 (rover) + 2 (idle) + 1 (timer) = 13 | Within ESP32 capacity |

### FreeRTOS Kernel Objects Summary

| Object Type | Count | Purpose |
|------------|-------|---------|
| Tasks | 10 (rover-defined) | Concurrent subsystem execution |
| Queues | 7 | Inter-task data transfer |
| Event Groups | 2 | Multi-task synchronisation |
| Mutexes | 3 | Shared resource protection |
| Timers | 4 | Periodic callbacks, watchdog |
| Semaphores | 0 | Replaced by queues and event groups |

---

## 5. Core Allocation

### Core Assignment Strategy

The ESP32-S3 N16R8 has two Xtensa LX7 cores (Core 0 and Core 1). Rover firmware assigns tasks to cores based on two principles:

1. **Isolation principle:** Real-time sensor I/O (Core 0) is physically separated from serial and actuator tasks (Core 1). This prevents serial processing jitter from affecting sensor timing.
2. **Throughput principle:** High-frequency tasks are distributed evenly to prevent one core from becoming a bottleneck.

```
+=================================================================+
|  Core 0 — SENSING CORE                                          |
|                                                                  |
|  Responsible for:                                               |
|    - All sensor polling (HC-SR04, VL53L0X, MPU6050, MQ-2)      |
|    - Telemetry packet construction                              |
|    - Health monitoring                                          |
|    - Software watchdog                                          |
|                                                                  |
|  Tasks:                                                         |
|    watchdog         (Priority 5 — 100 ms)                       |
|    sensor_manager   (Priority 4 — 50 ms)                        |
|    telemetry_builder(Priority 3 — triggered)                    |
|    health_monitor   (Priority 2 — 1000 ms)                      |
|                                                                  |
+=================================================================+

+=================================================================+
|  Core 1 — ACTUATION CORE                                        |
|                                                                  |
|  Responsible for:                                               |
|    - USB CDC serial RX and TX                                   |
|    - Command parsing and dispatch                               |
|    - Motor and servo control                                    |
|    - OLED rendering and LED animation                           |
|                                                                  |
|  Tasks:                                                         |
|    serial_handler   (Priority 4 — event-driven)                 |
|    motor_controller (Priority 4 — event-driven)                 |
|    command_parser   (Priority 3 — event-driven)                 |
|    servo_controller (Priority 3 — event-driven)                 |
|    oled_renderer    (Priority 2 — event-driven)                 |
|    led_controller   (Priority 2 — event-driven)                 |
|                                                                  |
+=================================================================+
```

### Core Assignment Rationale

| Decision | Rationale |
|----------|-----------|
| Watchdog on Core 0 | Must never be preempted by serial or actuator traffic |
| sensor_manager on Core 0 | HC-SR04 timing is sensitive; serial I/O on Core 1 adds no jitter |
| serial_handler on Core 1 | USB CDC interrupt fires on Core 1 by default in ESP-IDF |
| motor_controller on Core 1 | Command dispatch and motor response on the same core reduces queue latency |
| oled_renderer on Core 1 | I2C transactions for OLED are lengthy (~5 ms per frame); Core 1 absorbs this without disturbing sensor timing |

---

## 6. Task Creation Order

Tasks are spawned in a specific order to ensure that consumers are created before producers attempt to enqueue data. All tasks start in a suspended state and are resumed only after all queues and IPC objects are confirmed allocated.

```
Creation order in main.cpp:

Step 1:  watchdog          Core 0, Priority 5
         (Must exist first; it registers handles for all subsequent tasks)

Step 2:  sensor_manager    Core 0, Priority 4
         (Must exist before telemetry_builder; writes to Sensor Queue)

Step 3:  telemetry_builder Core 0, Priority 3
         (Must exist before sensor_manager runs; reads from Sensor Queue)

Step 4:  health_monitor    Core 0, Priority 2
         (Reads from Health Queue; depends on sensor_manager)

Step 5:  serial_handler    Core 1, Priority 4
         (Must exist before command_parser; writes to Command Queue)
         (Must exist before telemetry_builder; reads from TX Queue)

Step 6:  command_parser    Core 1, Priority 3
         (Must exist before subsystem controllers; writes to their queues)

Step 7:  motor_controller  Core 1, Priority 4
         (Reads from Motor Queue; must exist before command_parser runs)

Step 8:  servo_controller  Core 1, Priority 3
         (Reads from Servo Queue; must exist before command_parser runs)

Step 9:  oled_renderer     Core 1, Priority 2
         (Reads from Eye Queue; must exist before command_parser runs)

Step 10: led_controller    Core 1, Priority 2
         (Reads from LED Queue; must exist before command_parser runs)

All tasks suspended.
All IPC objects verified.
READY packet transmitted.
All tasks resumed.
FreeRTOS scheduler takes control.
```

---

## 7. Task Priority Table

### Priority Assignment

FreeRTOS priorities are unsigned integers where higher numbers run first when multiple tasks are ready. Rover firmware uses 5 priority levels mapped to the standard ESP-IDF range.

| FreeRTOS Priority | Rover Level | Tasks | Preempts |
|------------------|-------------|-------|---------|
| 5 | CRITICAL | `watchdog` | All other tasks |
| 4 | HIGH | `sensor_manager`, `serial_handler`, `motor_controller` | NORMAL and below |
| 3 | NORMAL | `telemetry_builder`, `command_parser`, `servo_controller` | LOW and below |
| 2 | LOW | `oled_renderer`, `led_controller`, `health_monitor` | IDLE only |
| 1 | IDLE | FreeRTOS idle task (x2) | Nothing |

### Full Task Reference Table

| Task Name | Core | Priority | Period / Mode | Stack (bytes) | Wake Condition |
|-----------|------|----------|--------------|--------------|----------------|
| `watchdog` | 0 | 5 (CRITICAL) | 100 ms periodic | 2048 | `vTaskDelay(100ms)` |
| `sensor_manager` | 0 | 4 (HIGH) | 50 ms periodic | 4096 | `vTaskDelay(50ms)` |
| `serial_handler` | 1 | 4 (HIGH) | Event-driven | 4096 | CDC RX data available |
| `motor_controller` | 1 | 4 (HIGH) | Event-driven | 2048 | Motor Queue item received |
| `telemetry_builder` | 0 | 3 (NORMAL) | Event-driven | 4096 | Sensor Queue item received |
| `command_parser` | 1 | 3 (NORMAL) | Event-driven | 4096 | Command Queue item received |
| `servo_controller` | 1 | 3 (NORMAL) | Event-driven | 2048 | Servo Queue item received |
| `oled_renderer` | 1 | 2 (LOW) | Event-driven | 4096 | Eye Queue item received |
| `led_controller` | 1 | 2 (LOW) | Event-driven | 2048 | LED Queue item received |
| `health_monitor` | 0 | 2 (LOW) | 1000 ms periodic | 2048 | `vTaskDelay(1000ms)` |

### Priority Rationale

**Why watchdog is Priority 5 (CRITICAL):**
The watchdog must run every 100 ms to verify task liveness. If any higher-priority task were to spin-block (a firmware bug), the watchdog must still be able to preempt it. Placing the watchdog at the highest application priority ensures it always gets CPU time.

**Why motor_controller is Priority 4 (HIGH):**
Motor commands must be applied without queuing delay. A received stop command must reach the motor driver within one scheduler tick of being dispatched. Placing it at HIGH priority with the serial handler ensures the command pipeline has minimum latency.

**Why oled_renderer and led_controller are Priority 2 (LOW):**
OLED rendering and LED animation are non-safety-critical and introduce lengthy I2C transactions. Running them at LOW priority ensures they never delay sensor reading, serial communication, or motor control.

---

## 8. Task Lifecycle

### General Task Lifecycle

Every rover firmware task follows the same lifecycle pattern:

```
[Task Created (suspended)]
         |
         v
[Global IPC objects verified]
         |
         v
[Task Resumed by main.cpp]
         |
         v
[Task Initialisation Block]
  - Register watchdog handle
  - Initialise local state variables
  - Set initial output state (safe defaults)
         |
         v
+----> [Wait for trigger]
|      - Periodic: vTaskDelay(N)
|      - Event: xQueueReceive(queue, &item, portMAX_DELAY)
|
|       |
|       v
|     [Process]
|      - Execute subsystem logic
|      - Read sensors / parse commands / render frames
|      - Produce output (write to queue / update hardware)
|
|       |
|       v
|     [Watchdog Pet]
|      - Report heartbeat to watchdog task
|
|       |
|       v
+------ [Return to wait]

[On system shutdown or fault]
         |
         v
[Task safe state]
  - Zero outputs
  - Flush queues
  - Enter indefinite vTaskDelay
```

### Task State Transitions

```
                    CREATED
                       |
                    SUSPENDED  <--(all tasks after creation)
                       |
                   main.cpp: vTaskResume
                       |
                    RUNNING / READY
                       |
           +-----------+-----------+
           |                       |
        BLOCKED                 RUNNING
        (waiting)              (on CPU)
           |                       |
           |   Trigger received    |
           +---------> <-----------+
                       |
                    Processing
                       |
                    BLOCKED again
                       (wait for next trigger)
```

---

## 9. Inter-Task Communication

### Communication Architecture Overview

```
+------------------------------------------------------------------+
|  CORE 0 (Sensing)              CORE 1 (Actuation)               |
|                                                                  |
|  sensor_manager                serial_handler                   |
|      |                              |                           |
|      | [Sensor Queue]               | [Command Queue]           |
|      v                              v                           |
|  telemetry_builder           command_parser                     |
|      |                         |    |    |    |                 |
|      | [TX Queue]         [Motor][Servo][Eye][LED]              |
|      v                         |    |    |    |                 |
|  serial_handler           motor  servo  oled   led             |
|  (TX path)                _ctrl  _ctrl  _rend  _ctrl           |
|                                                                  |
|  sensor_manager                                                  |
|      |                                                          |
|      | [Health Queue]                                           |
|      v                                                          |
|  health_monitor                                                  |
|      |                                                          |
|      | [Fault Queue]                                            |
|      v                                                          |
|  fault_manager -> [TX Queue] -> serial_handler (fault TX)       |
|                                                                  |
|  watchdog: monitors all task heartbeats via [Watchdog Queue]     |
+------------------------------------------------------------------+
```

### IPC Object Inventory

| Object | Type | Producer | Consumer | Depth | Item Size |
|--------|------|---------|---------|-------|-----------|
| Sensor Queue | Queue | sensor_manager | telemetry_builder | 2 | sizeof(sensor_data_t) |
| Health Queue | Queue | sensor_manager | health_monitor | 4 | sizeof(health_event_t) |
| TX Queue | Queue | telemetry_builder, fault_manager | serial_handler | 4 | sizeof(tx_packet_t) |
| Command Queue | Queue | serial_handler | command_parser | 4 | sizeof(raw_packet_t) |
| Motor Queue | Queue | command_parser | motor_controller | 2 | sizeof(motor_cmd_t) |
| Servo Queue | Queue | command_parser | servo_controller | 2 | sizeof(servo_cmd_t) |
| Eye Queue | Queue | command_parser | oled_renderer | 2 | sizeof(eye_cmd_t) |
| LED Queue | Queue | command_parser | led_controller | 2 | sizeof(led_cmd_t) |
| Fault Queue | Queue | health_monitor, any task | fault_manager | 8 | sizeof(fault_event_t) |
| Watchdog Queue | Queue | all tasks | watchdog | 16 | sizeof(watchdog_token_t) |
| System Event Group | Event Group | main.cpp, watchdog | multiple | — | 32 bits |
| Link Event Group | Event Group | serial_handler | motor_controller, watchdog | — | 32 bits |
| I2C Mutex | Mutex | — | sensor_manager, oled_renderer | — | — |
| Serial TX Mutex | Mutex | — | serial_handler | — | — |
| Config Mutex | Mutex | — | all read config | — | — |

---

## 10. Queue Architecture

### Queue Design Rules

| Rule | ID | Detail |
|------|----|--------|
| Queues are statically allocated | Q-01 | All queues allocated in `main.cpp` before task creation; heap not used at runtime |
| Queues are typed | Q-02 | Each queue carries a specific struct type; no void* passing |
| Non-blocking sends from ISR context | Q-03 | Any queue write from an interrupt uses `xQueueSendFromISR` |
| Blocking receives in task context | Q-04 | All queue reads use `xQueueReceive` with `portMAX_DELAY` unless timing requires otherwise |
| Queue overflow is a fault | Q-05 | A full queue causes the producing task to log a fault and drop the item, never block indefinitely |
| Queue depth is minimal | Q-06 | Depth is sized for burst absorption, not as a substitute for processing speed |

### Queue Specifications

#### Sensor Queue

```
Producer:   sensor_manager (Core 0, 20 Hz)
Consumer:   telemetry_builder (Core 0, triggered)
Type:       sensor_data_t

struct sensor_data_t {
  uint32_t  ts;               // ESP32 ms timestamp
  int16_t   us_front_cm;      // HC-SR04 front, cm (-1=fault)
  int16_t   us_left_cm;       // HC-SR04 left, cm
  int16_t   us_right_cm;      // HC-SR04 right, cm
  int16_t   us_rear_cm;       // HC-SR04 rear, cm
  int16_t   tof_front_mm;     // VL53L0X front, mm (-1=fault)
  int16_t   tof_pan_mm;       // VL53L0X pan, mm (-1=fault)
  float     imu_ax;           // m/s2
  float     imu_ay;
  float     imu_az;
  float     imu_gx;           // deg/s
  float     imu_gy;
  float     imu_gz;
  float     imu_temp_c;       // degC
  uint16_t  gas_raw_adc;      // ADC counts
  bool      gas_hazard;
  float     pwr_voltage_v;    // V (-1.0 = not installed)
  float     pwr_current_a;    // A (-1.0 = not installed)
  health_flags_t health;      // per-sensor bool flags
}

Depth: 2 (latest-reading pattern; older reading discarded if telemetry_builder is slow)
Item size: ~60 bytes
```

#### Command Queue

```
Producer:   serial_handler (Core 1, event-driven)
Consumer:   command_parser (Core 1, event-driven)
Type:       raw_packet_t

struct raw_packet_t {
  char  json[256];   // NULL-terminated JSON string
  uint16_t length;   // Byte count excluding NULL
}

Depth: 4
Item size: 258 bytes
```

#### Motor Queue

```
Producer:   command_parser (Core 1)
Consumer:   motor_controller (Core 1, event-driven)
Type:       motor_cmd_t

struct motor_cmd_t {
  int8_t fl;    // -100 to +100
  int8_t fr;
  int8_t rl;
  int8_t rr;
}

Depth: 2 (latest command wins; discard older if controller is behind)
Item size: 4 bytes
```

#### Servo Queue

```
Producer:   command_parser (Core 1)
Consumer:   servo_controller (Core 1, event-driven)
Type:       servo_cmd_t

struct servo_cmd_t {
  uint8_t pan_deg;    // 0-180
  uint8_t tilt_deg;   // 0-180
  bool    pan_valid;  // command contains pan?
  bool    tilt_valid; // command contains tilt?
}

Depth: 2
Item size: 4 bytes
```

#### Eye Queue

```
Producer:   command_parser (Core 1)
Consumer:   oled_renderer (Core 1, event-driven)
Type:       eye_cmd_t

struct eye_cmd_t {
  char  expr_id[24];   // NULL-terminated expression ID string
}

Depth: 2 (latest expression wins)
Item size: 24 bytes
```

#### LED Queue

```
Producer:   command_parser (Core 1)
Consumer:   led_controller (Core 1, event-driven)
Type:       led_cmd_t

struct led_cmd_t {
  char    mode_id[24];  // NULL-terminated mode ID string
  uint8_t r, g, b;     // Target colour (0-255 each)
  uint8_t speed;        // 1-10
  bool    color_valid;  // false = use mode default
}

Depth: 2
Item size: 28 bytes
```

#### TX Queue

```
Producer:   telemetry_builder (Core 0), fault_manager (any core)
Consumer:   serial_handler TX path (Core 1)
Type:       tx_packet_t

struct tx_packet_t {
  char     json[512];   // NULL-terminated JSON string
  uint16_t length;
  uint8_t  priority;    // 0=normal (telemetry), 1=high (fault/ack)
}

Depth: 4
Item size: 514 bytes
Note: High-priority items (faults, ACKs) are enqueued at front.
```

#### Health Queue

```
Producer:   sensor_manager (Core 0, per-cycle)
Consumer:   health_monitor (Core 0, 1 Hz aggregation)
Type:       health_event_t

struct health_event_t {
  uint32_t       ts;
  health_flags_t flags;      // current per-sensor bool flags
  uint8_t        fault_code; // 0 = no new fault this cycle
}

Depth: 4
Item size: ~16 bytes
```

#### Fault Queue

```
Producer:   health_monitor, sensor_manager, command_parser, watchdog
Consumer:   fault_manager
Type:       fault_event_t

struct fault_event_t {
  uint32_t ts;
  uint16_t code;            // Error code (see COMMUNICATION_PROTOCOL.md)
  uint8_t  severity;        // 0=warning, 1=error, 2=critical
  char     source[24];      // Module name string
  char     msg[80];         // Human-readable description
}

Depth: 8
Item size: ~112 bytes
```

---

## 11. Event Groups

### System Event Group

```
Bit positions:
  Bit 0  (0x01) — SYSTEM_READY:   Set when boot completes and all tasks are running
  Bit 1  (0x02) — SAFE_MODE:      Set when system enters safe mode
  Bit 2  (0x04) — SHUTDOWN:       Set when shutdown command received
  Bit 3  (0x08) — WATCHDOG_FAULT: Set when watchdog detects a missed heartbeat
  Bit 4  (0x10) — I2C_BUS_FAULT:  Set when PCA9548A stops responding
  Bit 5  (0x20) — GAS_HAZARD:     Set when MQ-2 threshold exceeded
  Bit 6  (0x40) — LOW_BATTERY:    Set when INA219 reports below threshold
  Bit 7  (0x80) — BOOT_ERROR:     Set if any self-test critical failure
```

Task interactions:
- `main.cpp` sets Bit 0 on boot completion
- `watchdog` monitors Bit 3; sets it on timeout; waits for it to send fault
- `health_monitor` sets Bits 4, 5, 6 based on ongoing assessment
- `motor_controller` waits for Bit 1 (SAFE_MODE): if set, ignores motor commands
- `command_parser` checks Bit 2 (SHUTDOWN): if set, dispatches zero-speed motor command

### Link Event Group

```
Bit positions:
  Bit 0  (0x01) — LINK_CONNECTED:   Set when first valid packet received from Pi
  Bit 1  (0x02) — LINK_STALE:       Set when heartbeat timeout exceeded (>2s)
  Bit 2  (0x04) — LINK_LOST:        Set when extended silence (>5s)
  Bit 3  (0x08) — LINK_RECOVERING:  Set when link is being re-established
```

Task interactions:
- `serial_handler` sets Bit 0 on first packet; clears Bits 1/2; sets Bit 3 during recovery
- `watchdog` reads Bit 2 (LINK_LOST); triggers safe mode on motor_controller
- `motor_controller` reads Bit 2: on LINK_LOST, applies brake immediately

---

## 12. Mutex Strategy

### Mutex Definitions

| Mutex | Protects | Held By | Max Hold Time |
|-------|---------|---------|--------------|
| `i2c_mutex` | I2C bus (shared between sensor_manager and oled_renderer) | sensor_manager or oled_renderer | ~10 ms (longest I2C transaction) |
| `serial_tx_mutex` | USB CDC TX write path | serial_handler | ~5 ms (longest packet transmission) |
| `config_mutex` | Runtime configuration struct | Any task reading config | <1 ms |

### Mutex Rules

| Rule | ID | Detail |
|------|----|--------|
| No nested mutexes | MX-01 | A task must never hold two mutexes simultaneously |
| Priority inheritance enabled | MX-02 | FreeRTOS mutex type (not binary semaphore) ensures priority inheritance |
| Bounded hold time | MX-03 | Every mutex holder releases within a documented maximum time |
| No mutex in interrupt | MX-04 | ISRs must never acquire a mutex |
| Timeout on acquire | MX-05 | All mutex acquires use a finite timeout (100 ms); failure logged as fault |

### I2C Mutex Contention Analysis

```
I2C bus users:
  sensor_manager:  Reads MPU6050, VL53L0X x2 via PCA9548A (~40 ms per cycle)
  oled_renderer:   Writes both SSD1306 via PCA9548A (~5 ms per frame)

Contention window:
  sensor_manager holds I2C for ~40 ms out of every 50 ms cycle.
  oled_renderer frame rate is limited to ~10 fps (100 ms per frame minimum).
  oled_renderer must acquire i2c_mutex and wait if sensor_manager holds it.
  Maximum oled_renderer wait: 40 ms (bounded by sensor cycle time).
  This is acceptable for the LOW-priority OLED task.
```

---

## 13. Timer Strategy

### Software Timer Definitions

FreeRTOS software timers run in the Timer Task daemon (Core 0). Rover firmware uses four timers.

| Timer | Period | Mode | Callback Action |
|-------|--------|------|----------------|
| `link_watchdog_timer` | 2000 ms | Auto-reload | Sets LINK_STALE bit in Link Event Group if no packet received |
| `heartbeat_tx_timer` | 1000 ms | Auto-reload | Enqueues an ESP32 heartbeat packet to TX Queue |
| `gas_hazard_latch_timer` | 5000 ms | One-shot | Clears GAS_HAZARD bit after threshold falls below level for 5 s |
| `oled_blink_timer` | Random 3000–6000 ms | One-shot | Triggers autonomous eye blink; resets to new random interval |

### Timer Rules

| Rule | ID | Detail |
|------|----|--------|
| No blocking in timer callback | TM-01 | Callbacks must not call vTaskDelay or block on a queue |
| Timers enqueue, not execute | TM-02 | Timer callbacks enqueue an event to a queue; the actual work is done by a task |
| All timers created before tasks | TM-03 | Timers are created and started in the same boot phase as queues |
| One-shot timers are restarted explicitly | TM-04 | One-shot timers (blink, gas latch) are restarted by the consuming task after handling |

### Hardware Timer Usage

| Timer | Peripheral | Purpose |
|-------|-----------|---------|
| HC-SR04 echo timing | ESP32 GPTimer (64-bit) | Measures ECHO pulse width in microseconds for distance calculation |
| LEDC (motor PWM) | LEDC Timer 0 | 1 kHz PWM for ENA/ENB motor speed control |
| LEDC (servo PWM) | LEDC Timer 1 | 50 Hz PWM for SG90 servo position |
| RMT (WS2812B) | RMT Peripheral | 800 kHz NZR timing for LED data |

---

## 14. Watchdog Strategy

### Two-Level Watchdog Architecture

Recon Rover V1 implements two independent watchdog layers:

```
+------------------------------------------------------------------+
|  LEVEL 1: ESP32 Hardware Watchdog (TWDT)                         |
|                                                                  |
|  Provided by: ESP-IDF Task Watchdog Timer                        |
|  Timeout:     5000 ms                                            |
|  Scope:       Monitors the FreeRTOS idle task                    |
|  Action:      If idle task never runs (CPU is 100% busy),        |
|               TWDT triggers an abort and reboot                  |
|  Purpose:     Last-resort protection against infinite loops      |
|               in any task                                        |
+------------------------------------------------------------------+

+------------------------------------------------------------------+
|  LEVEL 2: Firmware Software Watchdog (watchdog task)            |
|                                                                  |
|  Implemented by: watchdog.cpp FreeRTOS task (Priority 5)         |
|  Timeout:     2000 ms per task (configurable in config.h)        |
|  Scope:       Monitors all 9 other firmware tasks individually   |
|  Action:      On timeout, enters safe state and sends fault       |
|  Purpose:     Catches individual task stalls before the          |
|               hardware watchdog is needed                        |
+------------------------------------------------------------------+
```

### Software Watchdog Operation

```
Monitored Tasks (9):
  sensor_manager, telemetry_builder, serial_handler, command_parser,
  motor_controller, servo_controller, oled_renderer, led_controller,
  health_monitor

Each monitored task:
  - Pets the watchdog by sending a watchdog token to Watchdog Queue
    after every successful processing cycle
  - Token contains: task_id, current_ts

watchdog task (100 ms period):
  - Reads all pending tokens from Watchdog Queue
  - Updates last_seen_ts for each task_id
  - For each task: if (current_ts - last_seen_ts) > WATCHDOG_TIMEOUT_MS:
      -> Set WATCHDOG_FAULT bit in System Event Group
      -> Enqueue fault event (code 5001) to Fault Queue
      -> Call safe_mode_enter()
      -> log fault to serial TX

Watchdog timeout values:
  sensor_manager:   200 ms  (runs at 50 ms; 4x margin)
  serial_handler:   500 ms  (event-driven; allow for quiet periods)
  motor_controller: 500 ms  (event-driven; allow for quiet periods)
  others:          1000 ms  (lower-frequency tasks)
```

### Safe State Definition

When the watchdog triggers, the following hardware state is enforced:

```
Motors:     All PWM duty = 0; all direction pins LOW (coast)
Servos:     Hold current position (no command issued to prevent jitter)
OLEDs:      Queue "error" expression (oled_renderer picks it up)
LEDs:       Queue "error_mode" LED mode
Serial TX:  Send fault packet with code 5001 and task_id
```

### Link Watchdog

A separate `link_watchdog_timer` fires every 2000 ms. `serial_handler` resets the timer on every valid packet received. If the timer expires (no packet in 2000 ms):

```
link_watchdog_timer fires:
  -> Set LINK_STALE bit in Link Event Group
  -> motor_controller reads LINK_STALE: continue (reduced confidence)
  -> If LINK_STALE persists for 3 additional intervals (5000 ms total):
       -> Set LINK_LOST bit
       -> motor_controller: STOP all motors (brake state)
       -> oled_renderer: queue "error" expression
       -> led_controller: queue "error_mode"
```

---

## 15. Memory Layout

### ESP32-S3 N16R8 Memory Map

```
+------------------------------------------------------------------+
|  FLASH (16 MB — SPI NOR Flash)                                   |
|                                                                  |
|  0x000000  Bootloader         (64 KB)                            |
|  0x010000  Application        (3 MB — main firmware binary)      |
|  0x310000  OTA partition 0    (3 MB — over-the-air update slot)  |
|  0x610000  OTA partition 1    (3 MB — second OTA slot, planned)  |
|  0x910000  NVS                (512 KB — runtime config)          |
|  0x990000  OLED assets        (1 MB — eye bitmaps + animations)  |
|  0xA90000  Reserved           (remaining)                        |
+------------------------------------------------------------------+

+------------------------------------------------------------------+
|  INTERNAL SRAM (512 KB)                                          |
|                                                                  |
|  DRAM (Data RAM):                                                |
|    .data section (initialised globals):  ~20 KB                  |
|    .bss section (zero-init globals):     ~10 KB                  |
|    FreeRTOS kernel structures:           ~16 KB                  |
|    Task stacks (10 tasks):               ~32 KB (see Section 19) |
|    Queue storage (7 queues + 3 others):  ~8 KB                   |
|    I2C driver buffers:                   ~4 KB                   |
|    USB CDC buffers:                      ~8 KB                   |
|    Heap (remaining):                     ~414 KB                 |
|                                                                  |
|  IRAM (Instruction RAM):                                         |
|    Time-critical code (.iram section):   ~32 KB                  |
|    FreeRTOS kernel code:                 ~48 KB                  |
|    ISR handlers:                         ~8 KB                   |
|                                                                  |
+------------------------------------------------------------------+

+------------------------------------------------------------------+
|  PSRAM (8 MB — external SPI PSRAM)                               |
|                                                                  |
|  OLED frame buffer (double-buffered):    ~4 KB                   |
|  JSON serialisation work buffer:         ~8 KB                   |
|  ArduinoJson document pool:              ~8 KB                   |
|  Sensor data ring buffers (logging):     ~64 KB                  |
|  Firmware diagnostic log ring buffer:    ~32 KB                  |
|  Available for future expansion:         ~7.87 MB                |
|                                                                  |
+------------------------------------------------------------------+
```

---

## 16. Flash Partition Usage

### Partition Table

| Partition | Offset | Size | Type | Purpose |
|-----------|--------|------|------|---------|
| bootloader | 0x000000 | 64 KB | Boot | ESP-IDF second-stage bootloader |
| app_main | 0x010000 | 3 MB | app | Primary firmware application |
| ota_0 | 0x310000 | 3 MB | app | OTA update slot A |
| ota_1 | 0x610000 | 3 MB | app | OTA update slot B (planned V2) |
| nvs | 0x910000 | 512 KB | data/nvs | Non-volatile runtime config |
| oled_assets | 0x990000 | 1 MB | data | Eye bitmaps and animation tables |
| reserved | 0xA90000 | ~5.4 MB | — | Future expansion |

### OTA Partition Design

The OTA design allows the Raspberry Pi to push new firmware to the ESP32-S3 over the USB serial link without physical access to the flash. In V1 the OTA infrastructure is reserved but inactive. Active use is planned for V1.x.

### NVS Usage

The NVS partition stores runtime configuration values that may need adjustment without reflashing. NVS keys and their defaults:

| NVS Key | Type | Default | Description |
|---------|------|---------|-------------|
| `baud_rate` | uint32 | 921600 | Serial baud rate |
| `telem_hz` | uint8 | 20 | Telemetry rate |
| `gas_thresh` | uint16 | 800 | MQ-2 hazard threshold ADC count |
| `wdog_timeout` | uint16 | 2000 | Watchdog timeout ms |
| `servo_pan_min` | uint8 | 0 | Pan servo minimum safe angle |
| `servo_pan_max` | uint8 | 180 | Pan servo maximum safe angle |
| `servo_tilt_min` | uint8 | 45 | Tilt servo minimum safe angle |
| `servo_tilt_max` | uint8 | 135 | Tilt servo maximum safe angle |
| `motor_max_duty` | uint8 | 200 | Maximum PWM duty out of 255 |
| `log_level` | uint8 | 2 | 0=none, 1=error, 2=warn, 3=info, 4=debug |

### OLED Asset Partition Layout

```
oled_assets partition (1 MB):
  +-- asset_header         (256 bytes)  Version + expression count + table offset
  +-- expression_table     (4 KB)       Lookup: expr_id string -> frame array offset
  +-- bitmap_data          (remaining)  128x64 monochrome bitmaps, 1024 bytes each
      +-- idle_open.bmp      (1 KB)
      +-- idle_closed.bmp    (1 KB)    <- blink frame
      +-- happy_open.bmp     (1 KB)
      +-- curious_open.bmp   (1 KB)
      +-- alert_open.bmp     (1 KB)
      +-- ... (all expressions, 2-4 frames each)
```

---

## 17. RAM Allocation Strategy

### Static vs Dynamic Allocation

| Allocation Type | Used For | Rationale |
|----------------|---------|-----------|
| Static (compile-time) | Task stacks, queue storage arrays | Predictable; no runtime failure; no fragmentation |
| FreeRTOS heap (heap_4) | FreeRTOS internal structures only | FreeRTOS requires heap for some internal objects |
| PSRAM heap | JSON work buffers, diagnostic ring buffers | Large allocations that don't fit in SRAM |
| Stack-allocated | Temporary buffers within tasks (char arrays) | Lifetime bounded by function scope |

### Allocation Rules

| Rule | ID | Detail |
|------|----|--------|
| No malloc in task loop | RA-01 | All runtime allocations happen during boot; task loops are allocation-free |
| Stack buffers for JSON | RA-02 | JSON serialisation uses stack-allocated char[512] arrays in task context |
| PSRAM for large buffers | RA-03 | Buffers larger than 4 KB are allocated in PSRAM using `heap_caps_malloc(MALLOC_CAP_SPIRAM)` |
| Verify all allocations | RA-04 | Every allocation result is checked; NULL return halts boot with error |
| No fragmentation risk | RA-05 | Because all allocations happen once at boot, heap fragmentation cannot occur in steady state |

---

## 18. Heap Management

### Heap Configuration

| Parameter | Value |
|-----------|-------|
| Heap algorithm | heap_4 (first-fit with coalescing) |
| Total SRAM heap at boot | ~414 KB (after static allocation) |
| Total PSRAM heap at boot | ~8 MB (after PSRAM allocations) |
| Minimum free SRAM heap target | 32 KB (headroom for driver allocation) |
| Heap monitoring frequency | Every 1000 ms (health_monitor task) |

### Heap Monitoring

The `health_monitor` task checks free heap size every 1000 ms:

```
if free_heap < LOW_HEAP_WARNING_BYTES (32 KB):
  Enqueue fault_event: code=5003, severity=warning
  Log WARNING: "Low SRAM heap: N bytes remaining"

if free_heap < CRITICAL_HEAP_BYTES (8 KB):
  Enqueue fault_event: code=5003, severity=critical
  Trigger safe_mode_enter()
```

---

## 19. Stack Size Planning

### Stack Size Allocation

Stack size is calculated from the maximum call depth within each task, multiplied by a 2x safety factor, then rounded up to the nearest 512-byte boundary.

| Task | Base Requirement | Safety Margin | Allocated Stack | Rationale |
|------|-----------------|--------------|----------------|-----------|
| `watchdog` | 512 B | 4x | 2048 B | Minimal logic; just queue reads |
| `sensor_manager` | 1536 B | ~3x | 4096 B | HC-SR04 ISR context + I2C calls |
| `telemetry_builder` | 1024 B | ~4x | 4096 B | JSON serialisation buffer on stack |
| `serial_handler` | 1024 B | 4x | 4096 B | CDC read buffer + JSON fragment assembly |
| `command_parser` | 1536 B | ~3x | 4096 B | ArduinoJson document on stack |
| `motor_controller` | 512 B | 4x | 2048 B | Minimal: map value, write GPIO/PWM |
| `servo_controller` | 512 B | 4x | 2048 B | Minimal: angle-to-duty, write LEDC |
| `oled_renderer` | 1536 B | ~3x | 4096 B | SSD1306 frame buffer on stack |
| `led_controller` | 512 B | 4x | 2048 B | RMT buffer + animation state |
| `health_monitor` | 512 B | 4x | 2048 B | Health struct + fault queue write |
| **Total** | | | **32768 B (32 KB)** | |

### Stack Overflow Protection

FreeRTOS configCHECK_FOR_STACK_OVERFLOW is set to 2 (full pattern check). If a stack overflow is detected, the `vApplicationStackOverflowHook` callback fires and:

1. Immediately stops all motors (direct register write — no queue).
2. Transmits a fault packet via serial (if TX path is alive).
3. Triggers an ESP32 abort → hardware watchdog reboot.

---

## 20. Sensor Manager Architecture

### Responsibilities

The `sensor_manager` task is the single point of contact for all hardware sensors on the ESP32-S3. It owns the read schedule, manages fault detection, and produces a complete `sensor_data_t` snapshot for every cycle.

### Processing Loop (50 ms cycle — 20 Hz)

```
[sensor_manager wakes — every 50 ms]
     |
     v
[PHASE 1: HC-SR04 Ultrasonic Array — Time-Multiplexed]
  t=0ms:  Assert TRIG GPIO4 HIGH for 10 µs -> LOW
          Wait for ECHO GPIO5 HIGH (timeout: 30 ms)
          Measure ECHO pulse width (µs) via GPTimer
          distance_cm = pulse_width_us / 58
          If no ECHO within 30 ms: us_front_cm = -1, flag fault
  
  t=10ms: Repeat for LEFT  (GPIO6/7)
  t=20ms: Repeat for RIGHT (GPIO15/16)
  t=30ms: Repeat for REAR  (GPIO17/18)
     |
     v
[PHASE 2: VL53L0X ToF Sensors — I2C via PCA9548A]
  Acquire i2c_mutex (timeout: 100 ms)
    Select CH2 on PCA9548A (0x70 <- 0x04)
    Read VL53L0X range result register (0x1E) — I2C transaction
    Store result in tof_front_mm (or -1 on fault)
    Deselect PCA9548A (0x70 <- 0x00)
    Select CH3 on PCA9548A (0x70 <- 0x08)
    Read VL53L0X range result register
    Store result in tof_pan_mm (or -1 on fault)
    Deselect PCA9548A (0x70 <- 0x00)
  Release i2c_mutex
     |
     v
[PHASE 3: MPU6050 IMU — I2C (direct, no mux)]
  Acquire i2c_mutex (timeout: 100 ms)
    Write I2C: device addr 0x68, reg 0x3B, read 14 bytes
    Parse: raw_ax, raw_ay, raw_az, raw_temp, raw_gx, raw_gy, raw_gz
    Apply scale factors: accel /= 16384.0 (for ±2g); gyro /= 131.0 (for ±250 deg/s)
    Convert temp: temp_c = (raw_temp / 340.0) + 36.53
    Store converted values
  Release i2c_mutex
     |
     v
[PHASE 4: MQ-2 Gas Sensor — ADC]
  Read ADC1 channel (GPIO10) — single conversion
  Store raw_adc_count
  If raw_adc_count >= gas_hazard_threshold:
    gas_hazard = true
    Set GAS_HAZARD bit in System Event Group
  Else:
    gas_hazard = false (hysteresis timer governs latch clear — see Section 13)
     |
     v
[PHASE 5: INA219 Power Monitor — I2C (if installed)]
  If sensors.power == true (from boot self-test):
    Acquire i2c_mutex (timeout: 100 ms)
      Read INA219 bus voltage register (0x02)
      Read INA219 current register (0x04)
      Convert to V and A
    Release i2c_mutex
  Else:
    pwr_voltage_v = -1.0;  pwr_current_a = -1.0
     |
     v
[PHASE 6: Health Flag Update]
  Update health_flags_t based on current readings:
    imu_ok   = (MPU6050 I2C succeeded this cycle)
    tof_f_ok = (VL53L0X CH2 read succeeded this cycle)
    tof_p_ok = (VL53L0X CH3 read succeeded this cycle)
    gas_ok   = (ADC value in plausible range 0-4095)
    pwr_ok   = (INA219 read succeeded, or false if not installed)
    i2c_ok   = (PCA9548A responded to channel select)
     |
     v
[PHASE 7: Enqueue Results]
  Build sensor_data_t struct from all readings
  xQueueOverwrite(sensor_queue, &sensor_data)    <- latest reading always available
  xQueueSend(health_queue, &health_event, 0)     <- health update to health_monitor
     |
     v
[PHASE 8: Pet Watchdog]
  Send watchdog_token{task_id=TASK_SENSOR_MGR, ts=now} to Watchdog Queue
     |
     v
[vTaskDelay until next 50 ms boundary]
```

### Sensor Fault Handling

| Sensor | Fault Condition | Fault Value | Health Flag | Action |
|--------|----------------|------------|-------------|--------|
| HC-SR04 (any) | ECHO timeout | -1 cm | (no dedicated flag) | Count consecutive faults; after 5: send FAULT packet |
| VL53L0X (front) | I2C NACK | -1 mm | `tof_f_ok = false` | Send health event; fault after 3 consecutive |
| VL53L0X (pan) | I2C NACK | -1 mm | `tof_p_ok = false` | Send health event; fault after 3 consecutive |
| MPU6050 | I2C NACK | 0.0 | `imu_ok = false` | Send health event; disable IMU reads for 1 s; retry |
| MQ-2 | ADC < 0 or > 4095 | 0 | `gas_ok = false` | Send health event; do not raise hazard |
| INA219 | I2C NACK | -1.0 | `pwr_ok = false` | Send health event; disable INA219 reads |
| PCA9548A | No ACK on channel select | — | `i2c_ok = false` | CRITICAL fault; disable all mux-dependent devices |

---

## 21. Motor Controller Architecture

### Responsibilities

The `motor_controller` task translates abstract speed values (integer, -100 to +100) into L298N H-bridge GPIO direction signals and LEDC PWM duty cycles.

### L298N Wiring Model

```
L298N Channel A (Left side: FL + RL motors in parallel):
  IN1 GPIO -> HIGH = forward direction pin A
  IN2 GPIO -> HIGH = reverse direction pin A
  ENA LEDC  -> duty cycle = speed percentage

L298N Channel B (Right side: FR + RR motors in parallel):
  IN3 GPIO -> HIGH = forward direction pin B
  IN4 GPIO -> HIGH = reverse direction pin B
  ENB LEDC  -> duty cycle = speed percentage
```

### Processing Loop

```
[motor_controller wakes on Motor Queue item]
     |
     v
[STEP 1: Check System State]
  Read System Event Group
  If SAFE_MODE bit set:
    Discard command; apply BRAKE state; return to wait
  Read Link Event Group
  If LINK_LOST bit set:
    Apply BRAKE state; return to wait
     |
     v
[STEP 2: Validate Command Values]
  For each motor (fl, fr, rl, rr):
    Clamp to [-100, +100]
    If clamping occurred: enqueue fault event (code 3002, severity=warning)
     |
     v
[STEP 3: Apply Safety Speed Cap]
  max_duty = config.motor_max_duty  (from NVS, default 200/255)
  For each motor:
    duty = (abs(value) / 100.0) * max_duty
     |
     v
[STEP 4: Decode Direction for Channel A (Left side)]
  fl_value = (fl + rl) / 2  (average, since both wired together)
  if left_avg > 0:  IN1=HIGH, IN2=LOW   (forward)
  if left_avg < 0:  IN1=LOW,  IN2=HIGH  (reverse)
  if left_avg == 0: IN1=HIGH, IN2=HIGH  (brake)
  
  Repeat for Channel B (Right side: fr, rr)
     |
     v
[STEP 5: Write GPIO Direction Pins]
  gpio_set_level(PIN_IN1, in1_state)
  gpio_set_level(PIN_IN2, in2_state)
  gpio_set_level(PIN_IN3, in3_state)
  gpio_set_level(PIN_IN4, in4_state)
     |
     v
[STEP 6: Write LEDC PWM Duty]
  ledc_set_duty(LEDC_LOW_SPEED_MODE, MOTOR_CH_A, left_duty)
  ledc_update_duty(LEDC_LOW_SPEED_MODE, MOTOR_CH_A)
  ledc_set_duty(LEDC_LOW_SPEED_MODE, MOTOR_CH_B, right_duty)
  ledc_update_duty(LEDC_LOW_SPEED_MODE, MOTOR_CH_B)
     |
     v
[STEP 7: Pet Watchdog]
[Return to wait — xQueueReceive(motor_queue, ...)]
```

### Motor Safety State Table

| Condition | IN1 | IN2 | ENA Duty | Description |
|-----------|-----|-----|---------|-------------|
| value > 0 | HIGH | LOW | proportional | Forward |
| value < 0 | LOW | HIGH | proportional | Reverse |
| value == 0 | HIGH | HIGH | 0 | Brake (active stop) |
| SAFE_MODE | HIGH | HIGH | 0 | Forced brake |
| LINK_LOST | HIGH | HIGH | 0 | Forced brake |

---

## 22. Servo Controller Architecture

### Responsibilities

The `servo_controller` task translates angle commands (integer degrees, 0–180) into SG90 servo PWM pulse widths via the ESP32 LEDC peripheral.

### SG90 PWM Specification

```
PWM frequency: 50 Hz (20 ms period)
Pulse width range:
  0 degrees:   ~500 µs  pulse (duty cycle = 500/20000 = 2.5%)
  90 degrees:  ~1500 µs pulse (duty cycle = 1500/20000 = 7.5%)
  180 degrees: ~2500 µs pulse (duty cycle = 2500/20000 = 12.5%)

LEDC timer resolution: 14-bit (0-16383)
Duty for 0 deg:   = 500/20000 * 16383 = 410
Duty for 90 deg:  = 1500/20000 * 16383 = 1229
Duty for 180 deg: = 2500/20000 * 16383 = 2048
```

### Processing Loop

```
[servo_controller wakes on Servo Queue item]
     |
     v
[STEP 1: Read command (pan_deg, tilt_deg, pan_valid, tilt_valid)]
     |
     v
[STEP 2: Angle Safety Clamping]
  Pan angle:
    clamped_pan = constrain(pan_deg, config.servo_pan_min, config.servo_pan_max)
    If pan_deg != clamped_pan: log WARNING; set fault code 3002

  Tilt angle:
    clamped_tilt = constrain(tilt_deg, config.servo_tilt_min, config.servo_tilt_max)
    If tilt_deg != clamped_tilt: log WARNING; set fault code 3002
     |
     v
[STEP 3: Angle to Duty Conversion]
  pan_duty  = map(clamped_pan,  0, 180, DUTY_0_DEG, DUTY_180_DEG)
  tilt_duty = map(clamped_tilt, 0, 180, DUTY_0_DEG, DUTY_180_DEG)
     |
     v
[STEP 4: Apply if Valid]
  If pan_valid:
    ledc_set_duty(LEDC_LOW_SPEED_MODE, SERVO_PAN_CH, pan_duty)
    ledc_update_duty(LEDC_LOW_SPEED_MODE, SERVO_PAN_CH)
    current_pan_angle = clamped_pan  // store for heartbeat/diagnostics

  If tilt_valid:
    ledc_set_duty(LEDC_LOW_SPEED_MODE, SERVO_TILT_CH, tilt_duty)
    ledc_update_duty(LEDC_LOW_SPEED_MODE, SERVO_TILT_CH)
    current_tilt_angle = clamped_tilt
     |
     v
[STEP 5: Pet Watchdog]
[Return to wait]
```

---

## 23. OLED Renderer

### Responsibilities

The `oled_renderer` task manages both SSD1306 OLED displays. It renders eye expression bitmaps independently per eye, handles autonomous blinking, and manages PCA9548A channel switching.

### Display Architecture

```
+------------------+         +------------------+
|  SSD1306 Left    |         |  SSD1306 Right   |
|  (Left Eye)      |         |  (Right Eye)     |
|  128 x 64 px     |         |  128 x 64 px     |
|  I2C addr 0x3C   |         |  I2C addr 0x3C   |
|  PCA9548A CH0    |         |  PCA9548A CH1    |
+------------------+         +------------------+
         \                          /
          \     PCA9548A            /
           +--------+--------+
           |  I2C Multiplexer |
           |  addr 0x70       |
           +------------------+
                    |
               I2C Bus
               GPIO13 (SDA)
               GPIO14 (SCL)
```

### Processing Loop

```
[oled_renderer wakes on Eye Queue item (xQueueReceive portMAX_DELAY)]
     |
     v
[STEP 1: Expression Lookup]
  Look up expr_id string in expression_table (from OLED asset flash partition)
  Retrieve asset_entry_t:
    - left_frame_offsets[]   (array of flash offsets for left-eye bitmaps)
    - right_frame_offsets[]  (array of flash offsets for right-eye bitmaps)
    - frame_count            (number of animation frames)
    - frame_delay_ms         (inter-frame delay)
    - flags                  (LOOPS | BLINK_ENABLED)
  If expr_id not found: use "idle" fallback; log WARNING
     |
     v
[STEP 2: Animation Loop begins]
  for frame_index = 0; frame_index < frame_count or LOOPS:
    |
    v
  [STEP 3: Load Left Eye Bitmap from Flash]
    spi_flash_read(left_frame_offsets[frame_index], left_buf, 1024)
    |
    v
  [STEP 4: Load Right Eye Bitmap from Flash]
    spi_flash_read(right_frame_offsets[frame_index], right_buf, 1024)
    |
    v
  [STEP 5: Render Left Eye]
    Acquire i2c_mutex (timeout: 200 ms)
      driver_pca9548a_select(CH0)          // Select Left Eye
      driver_ssd1306_write_framebuffer(left_buf, 1024)
      driver_pca9548a_deselect()
    Release i2c_mutex
    |
    v
  [STEP 6: Render Right Eye]
    Acquire i2c_mutex (timeout: 200 ms)
      driver_pca9548a_select(CH1)          // Select Right Eye
      driver_ssd1306_write_framebuffer(right_buf, 1024)
      driver_pca9548a_deselect()
    Release i2c_mutex
    |
    v
  [STEP 7: Autonomous Blink Check]
    If BLINK_ENABLED flag set and oled_blink_timer expired:
      Load closed-eye bitmaps for both panels
      Render both eyes closed (same procedure as STEP 5-6)
      vTaskDelay(150 ms)     // Eye closed duration
      Restore open-eye bitmaps
      Re-render both eyes open
      Restart oled_blink_timer with new random interval (3000-6000 ms)
    |
    v
  [STEP 8: Frame delay]
    vTaskDelay(frame_delay_ms)
    |
    v
  [STEP 9: Check Eye Queue for new command (non-blocking)]
    xQueueReceive(eye_queue, &new_cmd, 0)
    If new item received: break animation loop; start new expression
    |
    v
  [STEP 10: Pet Watchdog]
    Send watchdog token
    |
    v
  [Continue animation loop]
```

### OLED Fault Handling

```
If driver_ssd1306_write_framebuffer fails:
  Increment oled_fail_count
  If oled_fail_count >= 3:
    Enqueue fault_event (code 3003, severity=error)
    Disable OLED rendering for 5 s (do not attempt further I2C writes)
    Set health flag: oled_ok = false (added to telemetry health extension)
    After 5 s: retry init sequence on both OLEDs
```

---

## 24. LED Controller

### Responsibilities

The `led_controller` task manages both WS2812B ARGB LED strips. It receives mode+colour commands from the LED Queue and drives the RMT peripheral to generate the WS2812B NZR bit stream.

### WS2812B Timing (RMT Encoding)

```
WS2812B NZR Protocol:
  Bit 1: T_H = 800 ns HIGH, T_L = 450 ns LOW
  Bit 0: T_H = 400 ns HIGH, T_L = 850 ns LOW
  Reset: > 50 µs LOW

ESP32 RMT peripheral generates this timing without CPU involvement.
Each LED requires 24 bits (GRB order).
Strip of 5 LEDs = 5 * 24 = 120 bits per update.
Total TX time per strip update = ~150 µs (negligible CPU time).
```

### Processing Loop

```
[led_controller wakes on LED Queue item]
     |
     v
[STEP 1: Parse command (mode_id, r, g, b, speed, color_valid)]
     |
     v
[STEP 2: Mode Lookup]
  Look up mode_id in mode_table
  Retrieve: animation_function pointer, default_color (if !color_valid)
  If color_valid: use provided r, g, b
  Else: use mode default colour
     |
     v
[STEP 3: Animation Execution Loop]
  While no new item in LED Queue (non-blocking check):
    |
    v
    Execute animation_function(r, g, b, speed, frame_counter++)
    Results in pixel_buffer[10] — one RGB entry per LED (5 left + 5 right)
    |
    v
  [STEP 4: WS2812B Write — Left Strip]
    rmt_transmit(LEFT_STRIP_RMT_CH, pixel_buffer[0..4])
    |
    v
  [STEP 5: WS2812B Write — Right Strip]
    rmt_transmit(RIGHT_STRIP_RMT_CH, pixel_buffer[5..9])
    |
    v
  [STEP 6: Pet Watchdog]
    Send watchdog token
    |
    v
  [vTaskDelay(animation_frame_period)]
  [Continue loop]
```

### Animation Functions

| Mode ID | Function Logic | Frame Period |
|---------|---------------|-------------|
| `off` | Set all pixels to (0,0,0) | 1000 ms (static) |
| `solid` | Set all pixels to (r,g,b) | 1000 ms (static) |
| `pulse` | brightness = sin(frame/rate) * 255; scale r,g,b | 20 ms |
| `blink` | Toggle all pixels between (r,g,b) and (0,0,0) | speed-mapped ms |
| `chase` | One pixel lit at a time, position = frame % 5 | speed-mapped ms |
| `strobe` | Rapid toggle (r,g,b) on/off | 5 ms |
| `sweep` | Progressive fill: n = frame % 6 pixels lit | 50 ms |
| `rainbow` | HSV hue = (frame * 2) % 360; convert to RGB | 20 ms |
| `breathe` | Slow sine wave on brightness | 30 ms |
| Semantic aliases | Map to above with preset colour | Per above |

---

## 25. Command Parser

### Responsibilities

The `command_parser` task receives raw JSON strings from the Command Queue and dispatches typed command structs to the appropriate subsystem queues.

### Processing Loop

```
[command_parser wakes on Command Queue item]
     |
     v
[STEP 1: JSON Deserialise]
  StaticJsonDocument<256> doc
  DeserializationError err = deserializeJson(doc, raw_packet.json)
  If err != OK:
    Enqueue error packet (code 1002) to TX Queue
    Log WARNING; discard packet; return to wait
     |
     v
[STEP 2: Mandatory Field Validation]
  Check proto == 1         -> else: discard + error packet (1004)
  Check type exists        -> else: discard + error packet (1005)
  Check ts exists          -> else: discard + error packet (1006)
  Check seq exists         -> else: discard + error packet (1007)
     |
     v
[STEP 3: Type Dispatch]
  Switch on doc["type"].as<string>():
    "cmd"       -> handle_cmd(doc)
    "heartbeat" -> handle_heartbeat(doc)
    "shutdown"  -> handle_shutdown(doc)
    default     -> silently discard (unknown types are benign)
     |
     v
[handle_cmd(doc)]:
  If no motors block AND no servos block AND no eyes block AND no leds block:
    Discard + error packet (1010)
    Return
  
  If motors block present:
    Validate fl, fr, rl, rr are integers in [-100, 100]
    Clamp out-of-range values; log WARNING if clamped
    Build motor_cmd_t; xQueueOverwrite(motor_queue, &motor_cmd)
  
  If servos block present:
    Validate pan, tilt are integers in [0, 180]
    Build servo_cmd_t; xQueueOverwrite(servo_queue, &servo_cmd)
  
  If eyes block present:
    Validate expr string is in known expression registry
    If unknown: send error packet (1009); skip eyes dispatch
    Else: build eye_cmd_t; xQueueOverwrite(eye_queue, &eye_cmd)
  
  If leds block present:
    Validate mode string is in known LED mode registry
    If color present: validate [R,G,B] are integers [0,255]
    Build led_cmd_t; xQueueOverwrite(led_queue, &led_cmd)
  
  If doc["ack"] == true:
    Build ACK packet (status="ok", ref_seq, ref_ts)
    Enqueue to TX Queue (high priority)
     |
     v
[handle_heartbeat(doc)]:
  Reset link_watchdog_timer
  Set LINK_CONNECTED bit in Link Event Group
  Clear LINK_STALE, LINK_LOST bits
  Store last_pi_heartbeat_ts = doc["ts"]
     |
     v
[handle_shutdown(doc)]:
  Set SHUTDOWN bit in System Event Group
  Enqueue motor_cmd_t (all zeros) to motor_queue
  Send ACK packet (ref_seq, status="ok")
  Log INFO "Shutdown command received"
     |
     v
[STEP 4: Sequence Number Tracking]
  If doc["seq"] <= last_received_seq AND NOT first packet:
    Discard; enqueue error packet (1011 — duplicate seq)
    Return
  last_received_seq = doc["seq"]
     |
     v
[STEP 5: Pet Watchdog]
[Return to wait]
```

---

## 26. Telemetry Builder

### Responsibilities

The `telemetry_builder` task receives a complete `sensor_data_t` struct from the Sensor Queue and serialises it into a JSON telemetry packet conforming to the `COMMUNICATION_PROTOCOL.md` specification.

### Processing Loop

```
[telemetry_builder wakes on Sensor Queue item]
     |
     v
[STEP 1: Receive sensor_data_t from Sensor Queue]
     |
     v
[STEP 2: Construct JSON document]
  StaticJsonDocument<512> doc
  doc["proto"] = 1
  doc["type"]  = "telemetry"
  doc["ts"]    = sensor_data.ts
  doc["seq"]   = tx_seq_counter++

  JsonObject us = doc.createNestedObject("ultrasonic")
  us["front"] = sensor_data.us_front_cm
  us["left"]  = sensor_data.us_left_cm
  us["right"] = sensor_data.us_right_cm
  us["rear"]  = sensor_data.us_rear_cm

  JsonObject tof = doc.createNestedObject("tof")
  tof["front"] = sensor_data.tof_front_mm
  tof["pan"]   = sensor_data.tof_pan_mm

  JsonObject imu = doc.createNestedObject("imu")
  imu["ax"]   = round2(sensor_data.imu_ax)     // 2 decimal places
  imu["ay"]   = round2(sensor_data.imu_ay)
  imu["az"]   = round2(sensor_data.imu_az)
  imu["gx"]   = round2(sensor_data.imu_gx)
  imu["gy"]   = round2(sensor_data.imu_gy)
  imu["gz"]   = round2(sensor_data.imu_gz)
  imu["temp"] = round1(sensor_data.imu_temp_c)  // 1 decimal place

  JsonObject gas = doc.createNestedObject("gas")
  gas["raw"]    = sensor_data.gas_raw_adc
  gas["hazard"] = sensor_data.gas_hazard

  JsonObject pwr = doc.createNestedObject("power")
  pwr["voltage"] = round2(sensor_data.pwr_voltage_v)
  pwr["current"] = round2(sensor_data.pwr_current_a)

  JsonObject health = doc.createNestedObject("health")
  health["imu_ok"]   = sensor_data.health.imu_ok
  health["tof_f_ok"] = sensor_data.health.tof_f_ok
  health["tof_p_ok"] = sensor_data.health.tof_p_ok
  health["gas_ok"]   = sensor_data.health.gas_ok
  health["pwr_ok"]   = sensor_data.health.pwr_ok
  health["i2c_ok"]   = sensor_data.health.i2c_ok
     |
     v
[STEP 3: Serialise to char buffer]
  char json_buf[512]
  size_t len = serializeJson(doc, json_buf, sizeof(json_buf))
  json_buf[len] = '\n'
  len++
     |
     v
[STEP 4: Enqueue to TX Queue]
  Build tx_packet_t: {json_buf, len, priority=0}
  xQueueSend(tx_queue, &tx_packet, 0)
  If queue full: log WARNING; discard (never block)
     |
     v
[STEP 5: Pet Watchdog]
[Return to wait]
```

---

## 27. Health Monitor

### Responsibilities

The `health_monitor` task aggregates health events from the Health Queue and generates trend analysis, fault suppression (to prevent duplicate fault packets), and battery monitoring decisions.

### Processing Loop (1000 ms period)

```
[health_monitor wakes — every 1000 ms]
     |
     v
[STEP 1: Drain Health Queue]
  Drain all pending health_event_t items from health_queue
  Merge into aggregated_health_flags (boolean OR per flag)
     |
     v
[STEP 2: Fault Trend Analysis]
  For each sensor:
    Count consecutive cycles with fault flag set
    If count >= FAULT_THRESHOLD (default 3):
      If not already fault_active for this sensor:
        Enqueue fault_event to Fault Queue
        Set fault_active flag for this sensor
    If count == 0:
      Clear fault_active flag for this sensor
     |
     v
[STEP 3: Battery Voltage Threshold Check]
  Read pwr_voltage_v from last sensor_data snapshot
  If voltage < LOW_BATTERY_V (7.0 V):
    Set LOW_BATTERY bit in System Event Group
    Enqueue fault_event (code=LOW_BATTERY, severity=warning) if not already raised
  If voltage < CRITICAL_BATTERY_V (6.5 V):
    Enqueue fault_event (severity=critical)
  If voltage == -1.0:
    INA219 not installed; skip
     |
     v
[STEP 4: Free Heap Check]
  free_heap = xPortGetFreeHeapSize()
  If free_heap < LOW_HEAP_THRESHOLD:
    Enqueue fault_event (code 5003, severity=warning)
     |
     v
[STEP 5: Pet Watchdog]
[vTaskDelay(1000 ms)]
```

---

## 28. Fault Manager

### Responsibilities

The `fault_manager` is a logical module (not a separate FreeRTOS task) that runs within the `serial_handler` TX path and the `health_monitor` task. Its role is to:

1. Rate-limit fault packet transmission (no more than 1 fault packet per second per error code).
2. Build the JSON FAULT packet conforming to `COMMUNICATION_PROTOCOL.md` Section 18.
3. Enqueue the FAULT packet to the TX Queue with `priority=1` (high priority).

### Fault Packet Construction

```
Triggered by: fault_event_t item received from Fault Queue

[Build fault packet]
  StaticJsonDocument<512> fdoc
  fdoc["proto"]    = 1
  fdoc["type"]     = "fault"
  fdoc["ts"]       = esp_timer_get_time() / 1000
  fdoc["seq"]      = tx_seq_counter++
  fdoc["code"]     = fault_event.code
  fdoc["severity"] = severity_string(fault_event.severity)
  fdoc["source"]   = fault_event.source
  fdoc["msg"]      = fault_event.msg

  char fault_json[512]
  serializeJson(fdoc, fault_json, sizeof(fault_json))
  Append '\n'

  Build tx_packet_t: {fault_json, len, priority=1}
  xQueueSendToFront(tx_queue, &tx_packet, 0)  <- HIGH PRIORITY: enqueue at front
```

### Rate Limiting

A fault_suppression_table tracks the last transmission time for each error code. If the same code fires again within 1000 ms, the event is logged internally but not transmitted to the Pi. This prevents fault storms from flooding the serial link.

---

## 29. Safe Mode

### Safe Mode Definition

Safe mode is a system-level state where all physical actuators are placed in a known, harmless state. Safe mode does not stop the firmware — telemetry continues, serial communication continues, and the system can be commanded out of safe mode by the Raspberry Pi.

### Safe Mode Trigger Conditions

| Trigger | Condition | Severity |
|---------|-----------|---------|
| Watchdog timeout | A task missed its heartbeat for > watchdog timeout | CRITICAL |
| I2C bus fault | PCA9548A not responding | CRITICAL |
| Stack overflow | FreeRTOS stack canary triggered | CRITICAL |
| Link lost | No Pi packet in > 5000 ms | ERROR |
| Gas hazard | MQ-2 raw > hazard threshold | WARNING (motors not stopped) |
| Low battery | Voltage < critical threshold | CRITICAL |
| SHUTDOWN packet | Graceful command from Pi | — |

### Safe Mode Actions

```
safe_mode_enter() procedure:

  1. Write motor safe state directly (register write, no queue):
       IN1=HIGH, IN2=HIGH, IN3=HIGH, IN4=HIGH (brake state)
       ENA duty = 0, ENB duty = 0

  2. Set SAFE_MODE bit in System Event Group

  3. Servo: do nothing (hold position to avoid jitter)

  4. LED: enqueue led_cmd_t("error_mode") to LED Queue

  5. OLED: enqueue eye_cmd_t("error") to Eye Queue

  6. Enqueue fault_event describing the trigger cause

  7. Continue all read tasks (sensor_manager, telemetry_builder):
       Telemetry must continue so the Pi can observe the system state

  8. Await either:
       a. SHUTDOWN bit in System Event Group -> power down
       b. Recovery signal from Raspberry Pi (future: explicit clear command)
```

---

## 30. Startup Self-Test

### Self-Test Sequence

The startup self-test executes during boot Stage 3 before any tasks are spawned. Failures are graded as CRITICAL (halt boot) or NON-CRITICAL (continue, mark sensor as unavailable).

```
TEST 1: I2C Bus Continuity
  Write to PCA9548A address 0x70: deselect all channels (0x00)
  Verify ACK received
  PASS: i2c_bus_ok = true
  FAIL (CRITICAL): Halt. Turn on error LED. Log "I2C bus fault at boot."

TEST 2: PCA9548A Channel 0 — Left OLED
  Select CH0; attempt SSD1306 init command; verify ACK
  PASS: oled_left_ok = true
  FAIL (NON-CRITICAL): oled_left_ok = false; log WARNING

TEST 3: PCA9548A Channel 1 — Right OLED
  Select CH1; attempt SSD1306 init command; verify ACK
  PASS: oled_right_ok = true
  FAIL (NON-CRITICAL): log WARNING

TEST 4: PCA9548A Channel 2 — Front VL53L0X
  Select CH2; read VL53L0X WHO_AM_I register (should return 0xEE)
  PASS: tof_front_ok = true
  FAIL (NON-CRITICAL): tof_front_ok = false; log WARNING

TEST 5: PCA9548A Channel 3 — Pan VL53L0X
  Select CH3; read VL53L0X WHO_AM_I register
  PASS: tof_pan_ok = true
  FAIL (NON-CRITICAL): log WARNING

TEST 6: MPU6050 WHO_AM_I
  Read register 0x75 from I2C address 0x68 (expected 0x70 for MPU6050)
  PASS: imu_ok = true
  FAIL (NON-CRITICAL): imu_ok = false; log WARNING

TEST 7: MQ-2 ADC Plausibility
  Read GPIO10 ADC; check result is in [0, 4095]
  PASS: gas_ok = true
  FAIL (NON-CRITICAL): log WARNING

TEST 8: L298N Direction Pin Self-Test
  Assert IN1, IN2, IN3, IN4 all LOW (safe state)
  No verification possible without motor feedback; log INFO "Motor pins set LOW"

TEST 9: Servo Centre Position
  Set pan=90 deg, tilt=90 deg via LEDC
  Verify LEDC duty written without error
  PASS: servo_ok = true

TEST 10: WS2812B LED Data Line
  Send 10 pixels of white (255,255,255) via RMT
  Send 10 pixels of off (0,0,0) via RMT
  No electrical verification; log INFO "LED data line exercised"

TEST 11: INA219 (if present)
  Attempt I2C read from 0x40
  PASS: pwr_ok = true
  FAIL: pwr_ok = false (not a fault; INA219 is optional in V1)

TEST 12: Memory Integrity
  Check xPortGetFreeHeapSize() > MINIMUM_FREE_HEAP_AT_BOOT
  PASS: memory_ok = true
  FAIL (CRITICAL): log "Insufficient heap at boot"; halt
```

### Self-Test Result in READY Packet

The self-test results are stored in `boot_status_t` and serialised into the READY packet (`sensors.imu`, `sensors.tof_f`, etc.) transmitted to the Raspberry Pi after boot.

---

## 31. Runtime Diagnostics

### Diagnostic Data Collected

The firmware collects the following runtime metrics, logged at 1 Hz by `health_monitor` to the PSRAM diagnostic ring buffer and optionally transmitted in extended telemetry (V1.x):

| Metric | Source | Format |
|--------|--------|--------|
| Free SRAM heap | `xPortGetFreeHeapSize()` | bytes |
| Task high-water marks | `uxTaskGetStackHighWaterMark()` per task | bytes remaining |
| Sensor error rate | Consecutive fault count per sensor | counter |
| TX queue depth | `uxQueueMessagesWaiting(tx_queue)` | items |
| Telemetry packets sent | Monotonic counter | count |
| Commands received | Monotonic counter | count |
| Fault packets sent | Monotonic counter | count |
| Serial RX errors | CDC driver error count | count |
| I2C NACK count | Per device | count |
| Watchdog pings missed | Per task | count |
| Uptime | `esp_timer_get_time() / 1e6` | seconds |

### Diagnostic Ring Buffer

The PSRAM diagnostic ring buffer stores the last 1000 diagnostic snapshots (1000 s of data at 1 Hz) without allocation:

```
PSRAM ring_buf[1000]:
  Each entry: diagnostic_snapshot_t
    uint32_t  ts;
    uint32_t  free_heap_bytes;
    uint16_t  tx_queue_depth;
    uint16_t  telemetry_count;
    uint16_t  command_count;
    uint16_t  fault_count;
    uint8_t   task_hwm[10];      // per task in KB
    uint8_t   sensor_err_rate[6]; // per sensor
    uint8_t   uptime_hrs;
```

---

## 32. Sensor Polling Strategy

### Polling Model

The ESP32-S3 firmware uses a **time-scheduled, task-driven polling model** for all sensors. No sensor uses hardware interrupts for data readiness notification (the MPU6050 interrupt pin is not used in V1). All sensor reads are initiated by the `sensor_manager` task on its 50 ms cycle.

### Rationale for Polling vs. Interrupt-Driven

| Approach | Pros | Cons | Decision |
|---------|------|------|---------|
| Interrupt-driven (INT pin) | Lower latency per reading | Complex synchronisation; ESP32 INT pins consumed | Rejected for V1 |
| Polling (timer-based) | Simple; deterministic timing | Fixed rate regardless of data readiness | **Adopted** |
| DMA transfers | Zero CPU overhead during read | Requires careful memory alignment; complex | Reserved for V1.x |

### Sensor Rate Table

| Sensor | Poll Rate | Poll Latency | Notes |
|--------|-----------|-------------|-------|
| HC-SR04 x4 | 20 Hz | ~40 ms total (10 ms per sensor, sequential) | Sequential fire to avoid ultrasonic crosstalk |
| VL53L0X x2 | 20 Hz | ~4 ms (2 ms per device via I2C) | Polled after HC-SR04 sequence completes |
| MPU6050 | 20 Hz | ~2 ms (14-byte I2C read) | Single transaction per cycle |
| MQ-2 | 20 Hz | ~0.1 ms (ADC single conversion) | Lightweight; polled every cycle |
| INA219 | 1 Hz | ~1 ms (I2C read) | Not needed at 20 Hz; sampled in health_monitor |

### HC-SR04 Sequential Fire Strategy

```
Why sequential and not simultaneous?

HC-SR04 sensors emit 40 kHz ultrasonic pulses. If two sensors fire simultaneously,
each sensor can receive the OTHER sensor's echo, producing grossly incorrect readings.

Solution: Fire each sensor in sequence with 10 ms separation.
  t=0ms:  FRONT fires. ECHO timed.  (~8.5 ms for 1.5m range)
  t=10ms: LEFT fires. ECHO timed.
  t=20ms: RIGHT fires. ECHO timed.
  t=30ms: REAR fires. ECHO timed.
  t=40ms: All readings complete.

The 10 ms gap is sufficient for all echoes to decay before the next TRIG pulse.
```

---

## 33. Scheduling Timeline

### Steady-State 1000 ms Window

```
Time (ms):  0    50   100  150  200  250 ... 950  1000
            |    |    |    |    |    |         |    |

Core 0:
sensor_mgr  [==] [==] [==] [==] [==] [==] ... [==] [==]   (50ms periodic)
telem_build  [=]  [=]  [=]  [=]  [=]  [=] ...  [=]  [=]   (triggered by sensor)
health_mon                                   [====]          (1000ms periodic)
watchdog    [][][][][][]...                                   (100ms periodic)

Core 1:
serial_hndlr (event-driven — wakes on USB CDC RX data)
cmd_parser   (event-driven — wakes on Command Queue item)
motor_ctrl   (event-driven — wakes on Motor Queue item)
servo_ctrl   (event-driven — wakes on Servo Queue item)
oled_render  (event-driven — wakes on Eye Queue item, then animates at 10 fps)
led_ctrl     (event-driven — wakes on LED Queue item, then animates at 50 fps)

Heartbeat TX timer fires at:
  1000ms, 2000ms, 3000ms ... (1 Hz)
  Adds heartbeat packet to TX Queue
  serial_handler transmits on next wakeup
```

### Critical Path — Sensor to Actuator (Nominal)

```
t=0ms     sensor_manager wakes
t=40ms    All sensors read, sensor_data_t assembled
t=40ms    xQueueOverwrite(sensor_queue, &data)
t=41ms    telemetry_builder wakes (preempted sensor_manager)
t=42ms    JSON serialised; enqueued to TX Queue
t=42ms    serial_handler wakes; transmits over USB CDC
t=43ms    Pi receives telemetry
t=44ms    Pi sensor_fusion.process()
t=46ms    Pi navigation decision; command built
t=47ms    Pi transmits cmd packet
t=47ms    serial_handler (ESP32) wakes; reads CDC data
t=47ms    Enqueues to Command Queue
t=47ms    command_parser wakes; dispatches to Motor Queue
t=48ms    motor_controller wakes; applies PWM
t=48ms    L298N responds; motor state changes
---
Sensor to actuator: ~48ms (within 50ms telemetry cycle)
```

---

## 34. Interrupt Usage

### Interrupt Source Table

| Interrupt Source | ISR Location | Action in ISR |
|-----------------|-------------|--------------|
| USB CDC RX (USB interrupt) | ESP-IDF USB driver | Copies RX bytes to RX ring buffer; sets event flag; wakes serial_handler |
| HC-SR04 ECHO GPIO falling edge | `driver_hcsr04.cpp` (GPIO ISR) | Records GPTimer capture value; stores pulse width |
| FreeRTOS tick (systick) | FreeRTOS kernel | Tick counter increment; scheduler invocation |
| Hardware Watchdog (TWDT) | ESP-IDF TWDT | Abort + reboot (last resort) |
| RMT TX complete | ESP-IDF RMT driver | Signals TX complete; led_controller reads via event |

### Interrupt Rules

| Rule | ID | Detail |
|------|----|--------|
| Minimal ISR code | IR-01 | ISRs capture timestamps and set flags only; no processing in ISR |
| No FreeRTOS blocking calls in ISR | IR-02 | ISRs use `xQueueSendFromISR`, `xEventGroupSetBitsFromISR` only |
| ISR stacks are IRAM-resident | IR-03 | ISR functions decorated with `IRAM_ATTR` to prevent cache miss during ISR |
| HC-SR04 ISR is time-critical | IR-04 | HC-SR04 ECHO ISR must capture GPTimer value within 1 µs of edge event |
| GPIO ISRs use edge detection | IR-05 | HC-SR04 ECHO ISR fires on both rising (start timer) and falling (stop timer) edges |

### HC-SR04 Echo Timing Detail

```
TRIG pulse:   10 µs HIGH on TRIG GPIO
              (generated by gpio_set_level + esp_rom_delay_us)

ECHO timing:
  Rising edge ISR:  capture GPTimer64 value -> echo_start_us
  Falling edge ISR: capture GPTimer64 value -> echo_end_us
  In driver:        pulse_width_us = echo_end_us - echo_start_us
                    distance_cm    = pulse_width_us / 58.0

Timeout detection:
  A FreeRTOS timer set to 30 ms after TRIG.
  If falling edge ISR does not fire before timer: distance = -1 (no echo)
```

---

## 35. Driver Layer Design

### Driver Design Principles

| Principle | Detail |
|-----------|--------|
| Single responsibility | Each driver file manages exactly one physical device |
| No FreeRTOS calls | Drivers do not call vTaskDelay, xQueueSend, or any FreeRTOS API |
| HAL-only hardware access | Drivers access hardware exclusively through HAL functions |
| Synchronous API | All driver functions are synchronous (blocking); async wrapper provided in subsystem layer if needed |
| Error return codes | All driver functions return a driver_status_t enum (DRIVER_OK, DRIVER_NACK, DRIVER_TIMEOUT, DRIVER_INVALID) |

### Driver Inventory

| Driver File | Device | Interface | Key Functions |
|------------|--------|-----------|--------------|
| `driver_hcsr04.cpp` | HC-SR04 x4 | GPIO + GPTimer | `hcsr04_trigger(channel)`, `hcsr04_read_cm(channel, *result)` |
| `driver_vl53l0x.cpp` | VL53L0X x2 | I2C (via PCA9548A) | `vl53l0x_init(channel)`, `vl53l0x_read_mm(channel, *result)` |
| `driver_mpu6050.cpp` | MPU6050 | I2C direct | `mpu6050_init()`, `mpu6050_read(imu_data_t*)` |
| `driver_mq2.cpp` | MQ-2 | ADC (GPIO10) | `mq2_read_raw(*adc_val)` |
| `driver_ina219.cpp` | INA219 | I2C direct | `ina219_init()`, `ina219_read(float* v, float* i)` |
| `driver_pca9548a.cpp` | PCA9548A | I2C direct | `pca9548a_select(channel)`, `pca9548a_deselect()` |
| `driver_ssd1306.cpp` | SSD1306 x2 | I2C (via PCA9548A) | `ssd1306_init(channel)`, `ssd1306_write_framebuffer(buf, len)` |
| `driver_ws2812b.cpp` | WS2812B x2 | RMT | `ws2812b_write(strip_id, pixels, count)` |
| `driver_l298n.cpp` | L298N | GPIO + LEDC | `l298n_set_channel(ch, dir, duty)`, `l298n_brake()` |
| `driver_sg90.cpp` | SG90 x2 | LEDC | `sg90_set_angle(channel, angle_deg)` |

### Driver Status Return Codes

| Code | Value | Meaning |
|------|-------|---------|
| `DRIVER_OK` | 0 | Operation completed successfully |
| `DRIVER_NACK` | 1 | I2C NACK received from device |
| `DRIVER_TIMEOUT` | 2 | Operation did not complete within timeout |
| `DRIVER_INVALID` | 3 | Invalid parameter supplied |
| `DRIVER_NOT_INIT` | 4 | Driver not initialised before use |
| `DRIVER_BUSY` | 5 | Device busy; retry later |

---

## 36. Hardware Abstraction Layer

### HAL Design Philosophy

The Hardware Abstraction Layer (HAL) wraps ESP-IDF peripheral APIs into a simplified, testable interface. The driver layer calls HAL functions only; it never calls ESP-IDF APIs directly. This means all drivers can be unit-tested by substituting a mock HAL.

### HAL Modules

| Module | Wraps | Key Functions |
|--------|-------|--------------|
| `hal_gpio.cpp` | esp_idf/gpio.h | `hal_gpio_set(pin, level)`, `hal_gpio_get(pin)`, `hal_gpio_config(pin, mode, pull)` |
| `hal_i2c.cpp` | esp_idf/i2c.h | `hal_i2c_write(addr, reg, buf, len)`, `hal_i2c_read(addr, reg, buf, len)` |
| `hal_ledc.cpp` | esp_idf/ledc.h | `hal_ledc_set_duty(channel, duty)`, `hal_ledc_set_freq(timer, freq)` |
| `hal_adc.cpp` | esp_idf/adc.h | `hal_adc_read(channel, *value)` |
| `hal_uart_cdc.cpp` | esp_idf/usb_cdc.h | `hal_cdc_write(buf, len)`, `hal_cdc_read(buf, maxlen, *actual)`, `hal_cdc_flush()` |
| `hal_rmt.cpp` | esp_idf/rmt.h | `hal_rmt_transmit(channel, symbols, count)` |

### HAL I2C Implementation Notes

```
hal_i2c_write and hal_i2c_read:
  Both wrap i2c_master_transmit_receive (ESP-IDF unified i2c driver).
  Timeout per transaction: 10 ms (configurable in config.h)
  Error mapping:
    ESP_OK         -> DRIVER_OK
    ESP_ERR_TIMEOUT -> DRIVER_TIMEOUT
    all others     -> DRIVER_NACK
```

---

## 37. Configuration Strategy

### Configuration Hierarchy

```
Level 1: Compile-time constants (config.h)
   Cannot be changed without recompiling.
   Used for: pin assignments, memory sizes, array dimensions.
   Examples:
     PIN_HC_FRONT_TRIG = 4
     SENSOR_QUEUE_DEPTH = 2
     STACK_SENSOR_MANAGER = 4096

Level 2: NVS runtime config (nvs_config.cpp)
   Can be changed by writing to NVS via a future config command or serial tool.
   Used for: threshold values, timing parameters, operational tuning.
   Examples:
     gas_hazard_threshold = 800
     motor_max_duty = 200
     telemetry_hz = 20

Level 3: Packet-level dynamic config (future V1.x)
   The Raspberry Pi sends a "config" packet type to update NVS values at runtime.
   Not implemented in V1; infrastructure reserved.
```

### config.h Structure

```
config.h sections:
  Section A: GPIO Pin Assignments (matches HARDWARE_ARCHITECTURE.md exactly)
  Section B: I2C Configuration (SDA, SCL, frequency)
  Section C: FreeRTOS Configuration (stack sizes, queue depths, priorities)
  Section D: Protocol Configuration (baud rate, max packet size, timing)
  Section E: Safety Limits (motor max duty, servo angle limits)
  Section F: Fault Thresholds (sensor fault counts, heap minimums)
  Section G: Boot Configuration (watchdog timeout, self-test enable/disable)
  Section H: Asset Configuration (flash partition offsets, asset table size)
```

### NVS Read Procedure

All NVS reads occur during boot Stage 2 before HAL initialisation. If an NVS key is absent (first boot), the compiled default is used and the key is written to NVS for future access.

---

## 38. Logging Strategy

### Log Levels

| Level | Value | When Used |
|-------|-------|---------|
| NONE | 0 | Logging disabled |
| ERROR | 1 | Hardware fault; communication failure; safe mode entry |
| WARN | 2 | Clamped value; missed heartbeat; queue full |
| INFO | 3 | Boot stage transitions; READY packet; shutdown |
| DEBUG | 4 | Per-packet events; driver calls; task scheduling |

### Log Destinations

| Destination | When Active | Format |
|------------|------------|--------|
| USB CDC Serial (raw text) | Always (development) | `[LEVEL] [MODULE] message` |
| PSRAM ring buffer | Always | Structured log_entry_t |
| Pi dashboard (future) | V1.x | JSON log event packet |

### Log Format

```
Serial log line format:
[LEVEL][TASK][ts_ms] message_string

Examples:
[INFO ][main      ][00003842] Boot complete. Transmitting READY packet.
[WARN ][sensor_mgr][00045231] VL53L0X CH2 NACK (fault count: 2)
[ERROR][health_mon][00091450] PCA9548A not responding. Raising fault code 2006.
[DEBUG][telem_bld ][00045243] Telemetry packet serialised: 312 bytes, seq=904
```

### Log Overhead

At DEBUG level, one log line per telemetry cycle (50 ms) is approximately 80 bytes. At 921600 bps, one log line takes ~0.7 ms to transmit. Combined with the telemetry packet (~4 ms), total serial TX time at DEBUG level is ~5 ms per cycle, within the TX queue capacity.

In production (log_level=WARN), serial output drops to near zero during normal operation.

---

## 39. Error Recovery

### Recovery Strategy by Error Type

| Error Type | Immediate Action | Recovery Procedure | Max Retries |
|-----------|-----------------|-------------------|------------|
| Single sensor NACK (I2C) | Use fault value (-1); log WARNING | Retry on next cycle automatically | Unlimited (per cycle) |
| Persistent sensor fault (3+ cycles) | Send FAULT packet; disable sensor | Attempt re-init every 5 s | 5 re-inits, then leave disabled |
| PCA9548A bus fault | Disable all mux-dependent devices; set i2c_ok=false | Attempt full I2C re-scan every 10 s | 3 re-scans |
| Motor driver fault (overcurrent) | Set motor to BRAKE state | Await explicit motor command with non-zero value | N/A |
| Serial link timeout | Set LINK_STALE; watchdog tracks | Await next received packet (auto-recovery) | N/A |
| Serial link lost | Set LINK_LOST; safe_mode_enter() | Await valid packet (auto-recovery on reception) | N/A |
| Stack overflow | Stop motors (direct register); abort | Hardware reboot | 1 (reboot) |
| Watchdog timeout | safe_mode_enter(); send fault packet | Await Pi restart command | N/A |
| NVS read failure | Use compiled defaults; log WARNING | Re-initialise NVS partition on next boot | 1 |
| Heap exhaustion | safe_mode_enter(); log CRITICAL | Hardware reboot | 1 |

### Sensor Re-Initialisation Procedure

```
When a sensor is marked as persistently faulted:
  1. Record fault time (ts_fault)
  2. On every health_monitor cycle:
     if (current_ts - ts_fault) > SENSOR_REINIT_INTERVAL (5000 ms):
        Attempt driver re-init (send init command sequence over I2C)
        If success: clear fault flag; log INFO "Sensor recovered"
        If failure: increment reinit_count
          if reinit_count >= MAX_REINIT_ATTEMPTS:
            Permanently disable sensor (no further reinit attempts)
            Send FAULT packet (severity=error)
```

---

## 40. Module Dependency Diagram

```
+------------------------------------------------------------------+
|  DEPENDENCY GRAPH (arrows point to dependency)                   |
+------------------------------------------------------------------+

main.cpp
  |-> hal_gpio, hal_i2c, hal_ledc, hal_adc, hal_uart_cdc, hal_rmt
  |-> All subsystem modules (creates and resumes tasks)

sensor_manager
  |-> driver_hcsr04   -> hal_gpio, hal_gptimer
  |-> driver_vl53l0x  -> driver_pca9548a -> hal_i2c
  |-> driver_mpu6050  -> hal_i2c
  |-> driver_mq2      -> hal_adc
  |-> driver_ina219   -> hal_i2c
  |-> [Sensor Queue]  -> telemetry_builder
  |-> [Health Queue]  -> health_monitor
  |-> [Watchdog Queue]-> watchdog

telemetry_builder
  |-> [Sensor Queue]  (reads from sensor_manager)
  |-> [TX Queue]      -> serial_handler (write path)
  |-> [Watchdog Queue]-> watchdog

serial_handler
  |-> hal_uart_cdc
  |-> [TX Queue]      (reads from telemetry_builder, fault_manager)
  |-> [Command Queue] -> command_parser (write path)
  |-> [Watchdog Queue]-> watchdog

command_parser
  |-> ArduinoJson
  |-> [Command Queue] (reads from serial_handler)
  |-> [Motor Queue]   -> motor_controller
  |-> [Servo Queue]   -> servo_controller
  |-> [Eye Queue]     -> oled_renderer
  |-> [LED Queue]     -> led_controller
  |-> [TX Queue]      -> serial_handler (ACK + error packets)
  |-> [Watchdog Queue]-> watchdog

motor_controller
  |-> driver_l298n    -> hal_gpio, hal_ledc
  |-> [Motor Queue]   (reads from command_parser)
  |-> [Watchdog Queue]-> watchdog
  |-> System Event Group (reads SAFE_MODE)
  |-> Link Event Group (reads LINK_LOST)

servo_controller
  |-> driver_sg90     -> hal_ledc
  |-> [Servo Queue]   (reads from command_parser)
  |-> [Watchdog Queue]-> watchdog

oled_renderer
  |-> driver_ssd1306  -> driver_pca9548a -> hal_i2c
  |-> spi_flash (OLED asset partition)
  |-> i2c_mutex
  |-> [Eye Queue]     (reads from command_parser)
  |-> [Watchdog Queue]-> watchdog

led_controller
  |-> driver_ws2812b  -> hal_rmt
  |-> [LED Queue]     (reads from command_parser)
  |-> [Watchdog Queue]-> watchdog

health_monitor
  |-> [Health Queue]  (reads from sensor_manager)
  |-> [Fault Queue]   -> fault_manager
  |-> System Event Group (sets LOW_BATTERY, I2C_BUS_FAULT)
  |-> [Watchdog Queue]-> watchdog

fault_manager (inline in health_monitor + serial_handler TX path)
  |-> [Fault Queue]   (reads from health_monitor, others)
  |-> [TX Queue]      -> serial_handler

watchdog
  |-> [Watchdog Queue](reads from all tasks)
  |-> [TX Queue]      -> serial_handler (fault packets)
  |-> safe_mode_enter()
  |-> Link Event Group (reads LINK_LOST)
```

---

## 41. Firmware Folder Structure

```
ESP32/
|
|-- main.cpp                    Entry point; boot orchestration; task spawning
|
|-- config.h                    All compile-time constants
|
|-- types.h                     Shared struct definitions (sensor_data_t, etc.)
|
|-- HAL/
|   |-- hal_gpio.h / .cpp       GPIO abstraction
|   |-- hal_i2c.h / .cpp        I2C master abstraction
|   |-- hal_ledc.h / .cpp       LEDC (PWM) abstraction
|   |-- hal_adc.h / .cpp        ADC abstraction
|   |-- hal_uart_cdc.h / .cpp   USB CDC abstraction
|   |-- hal_rmt.h / .cpp        RMT peripheral abstraction
|
|-- Drivers/
|   |-- driver_hcsr04.h / .cpp  HC-SR04 ultrasonic driver
|   |-- driver_vl53l0x.h / .cpp VL53L0X Time-of-Flight driver
|   |-- driver_mpu6050.h / .cpp MPU6050 IMU driver
|   |-- driver_mq2.h / .cpp     MQ-2 gas sensor driver
|   |-- driver_ina219.h / .cpp  INA219 power monitor driver
|   |-- driver_pca9548a.h / .cpp PCA9548A I2C multiplexer driver
|   |-- driver_ssd1306.h / .cpp SSD1306 OLED display driver
|   |-- driver_ws2812b.h / .cpp WS2812B LED strip driver (RMT)
|   |-- driver_l298n.h / .cpp   L298N dual H-bridge driver
|   |-- driver_sg90.h / .cpp    SG90 servo driver
|
|-- Subsystems/
|   |-- sensor_manager.h / .cpp FreeRTOS task: all sensor polling
|   |-- motor_controller.h / .cpp FreeRTOS task: motor commands
|   |-- servo_controller.h / .cpp FreeRTOS task: servo commands
|   |-- oled_renderer.h / .cpp  FreeRTOS task: eye expression rendering
|   |-- led_controller.h / .cpp FreeRTOS task: LED animation
|   |-- serial_handler.h / .cpp FreeRTOS task: USB CDC TX and RX
|   |-- command_parser.h / .cpp FreeRTOS task: JSON command dispatch
|   |-- telemetry_builder.h / .cpp FreeRTOS task: telemetry JSON builder
|   |-- health_monitor.h / .cpp FreeRTOS task: health aggregation
|   |-- watchdog.h / .cpp       FreeRTOS task: software watchdog
|   |-- fault_manager.h / .cpp  Fault packet builder (called inline)
|   |-- safe_mode.h / .cpp      Safe state entry procedure (callable from any task)
|
|-- Protocol/
|   |-- expression_registry.h   Expression ID lookup table
|   |-- led_mode_registry.h     LED mode lookup table
|   |-- error_codes.h           Error code constants (matches COMMUNICATION_PROTOCOL.md)
|   |-- packet_builder.h / .cpp Shared helpers: ACK builder, error packet builder
|
|-- Utils/
|   |-- math_utils.h            round2(), round1(), map_constrain() helpers
|   |-- ring_buffer.h / .cpp    PSRAM ring buffer implementation
|   |-- nvs_config.h / .cpp     NVS read/write wrappers
|   |-- logger.h / .cpp         Log formatting and ring buffer writer
|
|-- Assets/                     (partition loaded from OLED asset flash partition)
|   |-- asset_loader.h / .cpp   Flash partition reader for OLED bitmaps
```

---

## 42. File Responsibility Table

This table maps the firmware files to their specific architectural responsibilities, providing a quick reference for developers.

| File | Primary Responsibility | Key Functions / Tasks |
|------|------------------------|-----------------------|
| `main.cpp` | System entry point | `app_main()`, boot orchestration, task spawning |
| `config.h` | Static system configuration | Hardware pinouts, stack sizes, default timeouts |
| `types.h` | Shared data structures | `sensor_data_t`, `motor_cmd_t`, `fault_event_t` |
| `hal_*.cpp` | Hardware Abstraction Layer | Peripheral initialization and access (GPIO, I2C, ADC, LEDC, USB, RMT) |
| `driver_*.cpp` | Device Drivers | Device-specific protocols (e.g., MPU6050 init, SSD1306 rendering) |
| `sensor_manager.cpp` | Sensor Polling Task | `sensor_manager_task()`, reading all sensors, health flag generation |
| `motor_controller.cpp` | Motor Actuation Task | `motor_controller_task()`, processing motor commands, safety capping |
| `servo_controller.cpp` | Servo Actuation Task | `servo_controller_task()`, processing servo angle commands |
| `oled_renderer.cpp` | OLED Display Task | `oled_renderer_task()`, eye bitmap rendering, autonomous blinking |
| `led_controller.cpp` | LED Animation Task | `led_controller_task()`, WS2812B pattern generation |
| `serial_handler.cpp` | USB CDC I/O Task | `serial_handler_task()`, serial read/write, TX queue processing |
| `command_parser.cpp` | JSON Dispatch Task | `command_parser_task()`, deserialization, command routing |
| `telemetry_builder.cpp`| JSON Assembly Task | `telemetry_builder_task()`, formatting sensor data into JSON |
| `health_monitor.cpp` | System Health Task | `health_monitor_task()`, fault aggregation, battery monitoring |
| `watchdog.cpp` | Software Watchdog Task | `watchdog_task()`, heartbeat tracking, safe mode triggering |
| `fault_manager.cpp` | Fault Packet Builder | `fault_manager_build_packet()`, rate-limiting fault transmission |
| `safe_mode.cpp` | Safe State Logic | `safe_mode_enter()`, forcing safe actuator states |
| `nvs_config.cpp` | Non-Volatile Storage | Reading and writing dynamic settings |
| `logger.cpp` | Diagnostic Logging | Formatting log strings, writing to PSRAM ring buffer |

---

## 43. Coding Standards

To ensure long-term maintainability, all ESP32-S3 firmware must adhere to the following coding standards.

### Naming Conventions

*   **Files:** snake_case (e.g., `sensor_manager.cpp`)
*   **Tasks:** snake_case with `_task` suffix (e.g., `telemetry_builder_task`)
*   **Functions:** snake_case (e.g., `calculate_distance()`)
*   **Variables:** snake_case (e.g., `current_speed`)
*   **Constants/Macros:** UPPER_SNAKE_CASE (e.g., `MAX_SPEED_DUTY`)
*   **Structs/Enums:** snake_case with `_t` suffix (e.g., `sensor_data_t`)

### Language and Style

*   **Language:** C++17 (using ESP-IDF standard compiler settings).
*   **Indentation:** 4 spaces (no tabs).
*   **Braces:** K&R style (opening brace on the same line).
*   **No Exceptions:** C++ exceptions (`throw`, `try`, `catch`) are **strictly prohibited** to save flash space and execution overhead. Use return codes.
*   **No RTTI:** Run-Time Type Information is disabled.
*   **Static Allocation:** Prefer static or stack allocation over `malloc`/`new`.

### FreeRTOS Specifics

*   Always check return values of FreeRTOS API calls (e.g., `xQueueSend`, `xEventGroupSetBits`).
*   Never call blocking APIs (`vTaskDelay`, `xQueueReceive` with timeout) from an ISR.
*   Use `FromISR` variants of APIs inside interrupt handlers.
*   Keep ISRs as short as possible; defer heavy processing to tasks using queues or event groups.

---

## 44. Scalability Strategy

The firmware architecture is designed to accommodate future expansion without requiring a complete rewrite.

1.  **Queue-Based Decoupling:** Adding a new actuator simply requires adding a new queue and a handler task. The `command_parser` is updated to route new JSON fields to the new queue.
2.  **I2C Multiplexing:** The PCA9548A 8-channel multiplexer currently uses only 4 channels. 4 channels remain available for future I2C sensors.
3.  **Extensible JSON:** The JSON telemetry format allows new sensor fields to be added seamlessly. The Raspberry Pi will ignore unrecognized fields until updated.
4.  **Generous RAM Reserves:** The firmware uses only ~98 KB of internal SRAM, leaving ~414 KB available for future tasks and drivers. The 8 MB PSRAM provides immense headroom for future logging or buffer needs.
5.  **Multi-Core Headroom:** Both Xtensa cores are currently underutilized. New computationally expensive tasks (like local sensor fusion or DSP) can be added without disrupting the core polling loops.

---

## 45. Future Firmware Modules

These modules are not implemented in V1 but the architecture is prepared for their inclusion in V1.x or V2:

| Module | Purpose | Impact on Architecture |
|--------|---------|------------------------|
| **OTA Manager** | Over-The-Air firmware updates | Requires WiFi stack; uses OTA flash partitions |
| **Encoder Driver** | Reading motor wheel encoders | Requires PCNT (Pulse Counter) peripheral interrupts |
| **PID Controller** | Closed-loop velocity control | Requires high-priority task reading encoders and adjusting PWM |
| **IMU Fusion** | Local AHRS (Attitude and Heading) | Requires DSP task; offloads Pi |
| **Config API** | Dynamic NVS updates via JSON | Requires new JSON packet type handling in `command_parser` |

---

## 46. Performance Targets

| Metric | Target Value | Hard Limit |
|--------|--------------|------------|
| Telemetry Loop Jitter | < 2 ms | < 5 ms |
| Command to PWM Latency | < 5 ms | < 10 ms |
| I2C Bus Utilization | < 50% | < 75% |
| Core 0 CPU Utilization | < 30% | < 80% |
| Core 1 CPU Utilization | < 20% | < 80% |
| Serial TX Buffer Full Events | 0 | 0 |

---

## 47. Resource Budget

### Hardware Resources

| Resource | Total Available | Used in V1 | Remaining |
|----------|-----------------|------------|-----------|
| ESP32 Cores | 2 | 2 | 0 |
| GPIO Pins | 45 (approx) | 22 | ~23 |
| I2C Buses | 2 | 1 | 1 |
| SPI Buses | 4 | 0 (Internal flash only) | 4 |
| UARTs | 3 | 0 (Using USB CDC) | 3 |
| LEDC Channels | 8 | 6 | 2 |
| ADC Channels | 20 | 1 | 19 |

### Memory Resources

| Resource | Total | Used | Remaining |
|----------|-------|------|-----------|
| SRAM | 512 KB | ~98 KB | ~414 KB |
| PSRAM | 8 MB | ~120 KB | ~7.8 MB |
| Flash (App) | 3 MB | ~1 MB | ~2 MB |
| Flash (NVS) | 512 KB | < 4 KB | ~508 KB |

---

## 48. Failure Scenarios

| Scenario | Detection | Immediate Action | Recovery |
|----------|-----------|------------------|----------|
| **I2C Bus Lockup** | Timeout in `hal_i2c` | Assert `I2C_BUS_FAULT` event; stop all I2C access | Attempt bus reset (toggle SCL line) every 10s |
| **Motor Stall** | Current surge > threshold (requires INA219) | Set motor to BRAKE; raise fault 3001 | Await new command from Pi |
| **JSON Parse Exception** | Error return from ArduinoJson | Discard packet; send ERROR packet to Pi | None required (stateless) |
| **Task Starvation** | Software Watchdog timeout | Trigger `safe_mode_enter()`; halt motors | Await manual reset or Pi intervention |
| **Stack Overflow** | FreeRTOS stack canary | Hardware reset (ESP-IDF behavior) | Reboot sequence |

---

## 49. Design Constraints

1.  **No WiFi/Bluetooth:** The ESP32-S3 radio is explicitly disabled in V1 to reduce power consumption and simplify the architecture. All communication is via USB serial.
2.  **No Dynamic Memory in Control Loop:** To guarantee deterministic latency, `malloc` and `free` are banned in all periodic tasks and interrupt handlers.
3.  **No Blocking I2C in Interrupts:** I2C transactions are slow (~ms). They must only occur in task context, never in an ISR.
4.  **Single Serial Interface:** The USB CDC serial interface handles commands, telemetry, and debugging output. The firmware must multiplex these carefully to avoid dropped packets.

---

## 50. Conclusion

The Recon Rover V1 ESP32-S3 firmware architecture establishes a robust, highly deterministic foundation for the robot's reactive layer. By strictly adhering to the dual-processor design philosophy, isolating tasks by core and priority, utilizing safe queue-based IPC, and implementing redundant watchdog systems, the firmware ensures that the rover responds to commands reliably and fails safely under all fault conditions.

This document serves as the final specification for the ESP32-S3 development phase. All subsequent firmware implementation, debugging, and testing must align with the structures and rules defined herein.

---
*End of Document*
