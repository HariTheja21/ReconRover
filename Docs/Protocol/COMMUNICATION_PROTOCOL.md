# Recon Rover V1 — Communication Protocol Specification

**Document Version:** 1.0  
**Status:** Foundation Specification  
**Last Updated:** 2026-06-28  
**Author:** Lead Embedded Systems Architect  
**Classification:** Internal Engineering Specification  
**References:**
- `SYSTEM_ARCHITECTURE.md` — System design principles and communication philosophy
- `HARDWARE_ARCHITECTURE.md` — Physical layer: USB serial, GPIO, I2C topology
- `SOFTWARE_ARCHITECTURE.md` — Module design, packet structures, thread architecture

> **This document is the single authoritative specification for all communication between the Raspberry Pi 3B+ and the ESP32-S3 N16R8 on Recon Rover V1. Every packet, every field, every timing constraint, and every error condition is defined here. Implementation on both processors must comply exactly with this specification.**

---

## Table of Contents

1. [Communication Philosophy](#1-communication-philosophy)
2. [Design Goals](#2-design-goals)
3. [Protocol Overview](#3-protocol-overview)
4. [Physical Communication Layer](#4-physical-communication-layer)
5. [Serial Configuration](#5-serial-configuration)
6. [Packet Framing Rules](#6-packet-framing-rules)
7. [JSON Packet Standard](#7-json-packet-standard)
8. [Packet Lifecycle](#8-packet-lifecycle)
9. [Packet Timing](#9-packet-timing)
10. [Sequence Numbers](#10-sequence-numbers)
11. [Timestamp Strategy](#11-timestamp-strategy)
12. [Protocol Versioning](#12-protocol-versioning)
13. [Telemetry Packet Specification](#13-telemetry-packet-specification)
14. [Command Packet Specification](#14-command-packet-specification)
15. [ACK Packet Specification](#15-ack-packet-specification)
16. [Heartbeat Packet](#16-heartbeat-packet)
17. [READY Packet](#17-ready-packet)
18. [FAULT Packet](#18-fault-packet)
19. [SHUTDOWN Packet](#19-shutdown-packet)
20. [Error Packet](#20-error-packet)
21. [Packet Validation Rules](#21-packet-validation-rules)
22. [Required Fields](#22-required-fields)
23. [Optional Fields](#23-optional-fields)
24. [Field Naming Convention](#24-field-naming-convention)
25. [Units of Measurement](#25-units-of-measurement)
26. [Numeric Precision Rules](#26-numeric-precision-rules)
27. [Boolean Rules](#27-boolean-rules)
28. [Enum Definitions](#28-enum-definitions)
29. [Expression Registry](#29-expression-registry)
30. [LED Mode Registry](#30-led-mode-registry)
31. [Command Registry](#31-command-registry)
32. [Error Code Registry](#32-error-code-registry)
33. [Communication State Machine](#33-communication-state-machine)
34. [Packet Sequence Diagrams](#34-packet-sequence-diagrams)
35. [Communication Timing Diagrams](#35-communication-timing-diagrams)
36. [Retry Strategy](#36-retry-strategy)
37. [Timeout Handling](#37-timeout-handling)
38. [Link Recovery Procedure](#38-link-recovery-procedure)
39. [Packet Size Limits](#39-packet-size-limits)
40. [Serialization Rules](#40-serialization-rules)
41. [Deserialization Rules](#41-deserialization-rules)
42. [Protocol Examples](#42-protocol-examples)
43. [Good Packet Examples](#43-good-packet-examples)
44. [Invalid Packet Examples](#44-invalid-packet-examples)
45. [Debugging Guidelines](#45-debugging-guidelines)
46. [Logging Requirements](#46-logging-requirements)
47. [Future Expansion Strategy](#47-future-expansion-strategy)
48. [Security Considerations](#48-security-considerations)
49. [Compatibility Rules](#49-compatibility-rules)
50. [Complete Reference Tables](#50-complete-reference-tables)

---

## 1. Communication Philosophy

### The Inviolable Boundary

Recon Rover V1 is built on a strict dual-processor architecture. The Raspberry Pi 3B+ is the cognitive brain: it perceives, reasons, and decides. The ESP32-S3 N16R8 is the reactive body: it reads sensors, drives actuators, and executes commands. These two processors never share memory, never share a bus, and never reach into each other's domain.

The communication protocol defined in this document is the **only** interface between these two systems. Every byte of information that crosses the processor boundary passes through this protocol. Every decision made on the Raspberry Pi that affects hardware is expressed as a packet. Every sensor reading collected by the ESP32-S3 that informs a decision is expressed as a packet.

> **This protocol is not a detail of implementation. It is the contract that makes the architecture possible.**

### The Direction of Authority

The protocol enforces a strict chain of authority:

```
Raspberry Pi (DECIDES)
      |
      |  Commands (Pi -> ESP32)
      v
  Serial Bridge  (USB Serial / JSON)
      |
      |  Telemetry (ESP32 -> Pi)
      v
ESP32-S3 (EXECUTES)
      |
      v
  Physical Hardware
```

The Raspberry Pi is always the authority. The ESP32-S3 is always the executor. The protocol makes this chain explicit:

- **Commands flow downward:** Pi to ESP32.
- **Telemetry flows upward:** ESP32 to Pi.
- **Acknowledgements flow upward:** ESP32 to Pi (confirming receipt of commands).
- **Fault notifications flow upward:** ESP32 to Pi (reporting hardware anomalies).

### Why This Protocol Is Designed the Way It Is

Every design decision in this protocol is traceable to one of three priorities:

1. **Safety** — The system must fail safely. A lost packet must never cause runaway motors or stalled processes.
2. **Debuggability** — Every packet must be human-readable. A developer with a serial monitor must be able to understand every byte.
3. **Scalability** — Adding a new sensor, command, or subsystem must require no changes to the framing or parsing infrastructure.

---

## 2. Design Goals

| ID | Goal | Priority | Implementation |
|----|------|----------|----------------|
| DG-01 | All packets must be human-readable without tools | Critical | UTF-8 JSON encoding |
| DG-02 | All packets must be machine-parseable without a schema file | Critical | Self-describing JSON key names |
| DG-03 | A single corrupt packet must not corrupt subsequent packets | Critical | Newline framing; each packet is independent |
| DG-04 | Unknown packet types must be silently ignored | Critical | Unknown `type` field -> discard |
| DG-05 | Link loss must trigger a safe hardware state automatically | Critical | Watchdog timeout -> motors stop |
| DG-06 | Adding a new sensor requires no framing changes | High | New JSON fields added to telemetry object |
| DG-07 | Adding a new command requires no framing changes | High | New JSON fields added to command object |
| DG-08 | Every packet must carry a timestamp | High | `ts` field mandatory on all packets |
| DG-09 | Protocol version must be detectable in every packet | High | `proto` field mandatory |
| DG-10 | All field names must be consistent and lowercase | High | Snake_case naming convention |
| DG-11 | All units must be unambiguous and documented | High | This document defines all units |
| DG-12 | Telemetry rate must be configurable without protocol changes | Medium | Rate configured in firmware; protocol is rate-agnostic |
| DG-13 | ACK packets must be optional, not mandatory | Medium | ACK only sent when explicitly requested |
| DG-14 | The protocol must support offline debugging via log replay | Medium | All packets logged verbatim |

---

## 3. Protocol Overview

### Summary

| Property | Value |
|----------|-------|
| Protocol name | RoverSerial v1 |
| Transport | USB Serial (CDC-ACM) |
| Encoding | UTF-8 JSON |
| Framing | Newline-delimited (`\n` terminated) |
| Direction | Bidirectional, half-duplex logical streams |
| Packet types | 8 defined types (extensible) |
| Baud rate | 921600 bps (recommended); 115200 bps (minimum) |
| Max packet size | 512 bytes |
| Telemetry rate | 20 Hz (ESP32 -> Pi) |
| Command rate | Event-driven (Pi -> ESP32, up to 20 Hz) |
| Heartbeat rate | 1 Hz (bidirectional) |

### Packet Type Registry

| Type String | Direction | Purpose | Rate |
|-------------|-----------|---------|------|
| `"telemetry"` | ESP32 -> Pi | Full sensor suite snapshot | 20 Hz |
| `"cmd"` | Pi -> ESP32 | Actuator and display commands | Event-driven |
| `"ack"` | ESP32 -> Pi | Command receipt acknowledgement | On request |
| `"heartbeat"` | Bidirectional | Link liveness proof | 1 Hz |
| `"ready"` | ESP32 -> Pi | Boot complete notification | Once on boot |
| `"fault"` | ESP32 -> Pi | Critical hardware fault alert | On fault event |
| `"shutdown"` | Pi -> ESP32 | Graceful power-down instruction | Once on shutdown |
| `"error"` | Bidirectional | Protocol-level error notification | On protocol error |

### Directional Packet Map

```
+========================+           +========================+
|   Raspberry Pi 3B+     |           |    ESP32-S3 N16R8      |
|                        |           |                        |
|  serial_manager.py     |           |  serial_handler.cpp    |
|  command_builder.py    |           |  telemetry_builder.cpp |
|                        |           |  command_parser.cpp    |
+========================+           +========================+
          |                                     |
          |   "cmd"       ------------------>   |
          |   "heartbeat" ------------------>   |
          |   "shutdown"  ------------------>   |
          |                                     |
          |   "telemetry" <------------------   |
          |   "ack"       <------------------   |
          |   "heartbeat" <------------------   |
          |   "ready"     <------------------   |
          |   "fault"     <------------------   |
          |   "error"     <------------------   |
          |   "error"     ------------------>   |
          |                                     |
          +------------ USB Serial -------------+
                    (physical cable)
```

---

## 4. Physical Communication Layer

### Interface

| Parameter | Value |
|-----------|-------|
| Physical interface | USB 2.0 Full Speed |
| USB class | CDC-ACM (Communications Device Class - Abstract Control Model) |
| USB device role | ESP32-S3 acts as USB Device (CDC peripheral) |
| USB host role | Raspberry Pi acts as USB Host |
| Kernel driver (Pi) | `cdc_acm` — automatic; no installation required |
| Device path (Pi) | `/dev/ttyUSB0` or `/dev/ttyACM0` (configuration-defined) |
| Cable | USB-A to USB-C (or USB-A to micro-USB depending on ESP32-S3 board) |

### Physical Layer Diagram

```
Raspberry Pi 3B+                        ESP32-S3 N16R8
+------------------+                  +------------------+
|                  |                  |                  |
|  USB Host Port   |                  |  USB Device Port |
|  (USB-A)         |<-- USB Cable --> |  (USB-C / uUSB)  |
|                  |                  |                  |
|  /dev/ttyACM0    |                  |  CDC-ACM UART    |
|  (or ttyUSB0)    |                  |  (native USB)    |
|                  |                  |                  |
+------------------+                  +------------------+
       |                                      |
  serial_manager.py                   serial_handler.cpp
  (Python pyserial)                   (ESP-IDF USB CDC)
```

### Power Over USB

During development and bench testing, the ESP32-S3 may draw its 5V power supply from the USB cable (via the Raspberry Pi's USB port). In production deployment, the ESP32-S3 must be powered by its dedicated 5V rail (Buck Converter #2, as defined in `HARDWARE_ARCHITECTURE.md`). The USB cable in production carries data only.

> **Critical:** The Raspberry Pi USB port cannot safely sustain the combined current draw of the ESP32-S3 plus all attached peripherals (servos, LEDs, OLEDs). Always use the dedicated power rails in production.

### Cable Specification

| Parameter | Requirement |
|-----------|-------------|
| Length | 30 cm maximum (shorter is better for signal integrity) |
| Type | Shielded USB 2.0 |
| Connector (Pi end) | USB-A |
| Connector (ESP32 end) | Per ESP32-S3 development board specification |
| Ferrite bead | Recommended if motor EMI causes USB instability |

---

## 5. Serial Configuration

### UART Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Baud rate | 921600 bps | Recommended; provides low latency at 20 Hz |
| Baud rate (fallback) | 115200 bps | Use only if 921600 is unsupported |
| Data bits | 8 | Standard |
| Parity | None | No hardware parity |
| Stop bits | 1 | Standard |
| Flow control | None | No hardware or software flow control |
| Byte order | N/A (byte stream) | |
| Line ending | `\n` (LF, 0x0A) | Newline only; no CR |

### Why 921600 bps?

At 20 Hz telemetry rate with a maximum packet size of 512 bytes:

```
Data rate = 512 bytes * 20 Hz = 10,240 bytes/s = 81,920 bps

At 115200 bps: utilisation = 81920 / 115200 = 71%   (marginal headroom)
At 921600 bps: utilisation = 81920 / 921600 =  9%   (ample headroom for commands + ACKs)
```

921600 bps provides an 11x margin over the required data rate, ensuring that command packets injected concurrently with telemetry transmission do not cause queuing delays.

### Buffer Configuration

| Buffer | Recommended Size | Location |
|--------|-----------------|---------|
| ESP32 USB CDC TX buffer | 2048 bytes | ESP-IDF USB CDC configuration |
| ESP32 USB CDC RX buffer | 1024 bytes | ESP-IDF USB CDC configuration |
| Pi serial read buffer | 4096 bytes | pyserial configuration |
| Pi serial write buffer | 1024 bytes | pyserial configuration |

### Serial Port Initialisation Sequence

```
ESP32-S3 side:
    1. USB CDC driver initialised during boot
    2. TX and RX buffers allocated
    3. Line-end detection mode: LF (0x0A)
    4. Serial handler task started
    5. "ready" packet transmitted when all subsystems are initialised

Raspberry Pi side:
    1. Open serial port at configured path and baud rate
    2. Set timeout to 2 seconds per read operation
    3. Flush any stale bytes in the receive buffer
    4. Wait up to 10 seconds for "ready" packet from ESP32
    5. If "ready" received: proceed to OPERATIONAL state
    6. If timeout: log CRITICAL, retry or abort
```

---

## 6. Packet Framing Rules

### The Framing Contract

Every packet is a single JSON object on a single line, terminated by a Line Feed character (LF, 0x0A). No other framing is used. There is no start-of-frame byte, no length prefix, no checksum byte, and no end-of-frame marker other than the newline.

```
PACKET FORMAT:
+-----------------------------------------------------------+------+
| JSON object (UTF-8, arbitrary length up to 512 bytes)     | 0x0A |
+-----------------------------------------------------------+------+
  <--- complete, valid JSON object ----------------------->  <LF>
```

### Framing Rules

| Rule | ID | Detail |
|------|----|--------|
| One packet per line | FR-01 | Each packet occupies exactly one line |
| LF termination only | FR-02 | Line is terminated by LF (0x0A). CR+LF (0x0D 0x0A) is also accepted but LF is canonical |
| No line continuations | FR-03 | A packet must not span multiple lines |
| No embedded newlines | FR-04 | JSON string values must not contain unescaped newline characters |
| Maximum line length | FR-05 | A line must not exceed 512 bytes including the terminating LF |
| Empty lines ignored | FR-06 | An empty line (just LF) must be silently ignored by the receiver |
| One JSON object per packet | FR-07 | Arrays, primitives, and null at the top level are invalid |
| UTF-8 encoding only | FR-08 | No other encoding is permitted |

### Why Newline Framing?

| Alternative | Why Rejected |
|-------------|-------------|
| Length-prefix framing | Requires the receiver to maintain state across reads; a single corrupt length byte desynchronises the entire stream |
| Start/end byte framing | Requires byte stuffing if the delimiter byte appears in data; adds complexity |
| Fixed-size packets | Wastes bandwidth for short packets; insufficient for full telemetry |
| Newline-delimited JSON | Self-recovering — a corrupt packet only loses that one line; next `\n` resynchronises the stream |

### Stream Recovery

Because each packet is independently terminated by `\n`, the receiver can always resynchronise:

```
Corrupt stream scenario:

Received bytes: ...{"type":"tel   [corrupt/truncated]
                                                     \n   <- LF resynchronises
                {"type":"telemetry","ts":12345,...}\n      <- Next packet: fully intact
```

The corrupt packet is discarded. The next packet is received and processed normally. No state machine reset is required.

---

## 7. JSON Packet Standard

### Top-Level Structure

Every packet, regardless of type, must conform to the following top-level structure:

```json
{
  "proto":  <integer  — protocol version, always 1 for V1>,
  "type":   <string   — packet type identifier>,
  "ts":     <integer  — timestamp in milliseconds>,
  "seq":    <integer  — sequence number>,
  <type-specific fields>
}
```

### Mandatory Top-Level Fields

| Field | Type | Required In | Description |
|-------|------|------------|-------------|
| `proto` | integer | All packets | Protocol version. Must be `1` for Recon Rover V1. |
| `type` | string | All packets | Packet type identifier. See Packet Type Registry. |
| `ts` | integer | All packets | Sender's timestamp in milliseconds since sender boot. |
| `seq` | integer | All packets | Monotonically increasing sequence number. Resets to 0 on reboot. |

### JSON Type Rules

| JSON Type | Permitted For |
|-----------|--------------|
| String | `type`, enumerations, expression IDs, mode IDs, error messages |
| Integer | `ts`, `seq`, `proto`, distance values (cm, mm), raw ADC, motor values, servo angles, RGB colour components |
| Float | IMU values (m/s², deg/s), voltage (V), current (A) |
| Boolean | Health flags, hazard flags |
| Object | Nested data groups (e.g., `"ultrasonic"`, `"imu"`, `"motors"`) |
| Array | RGB colour values `[R, G, B]` only |
| Null | Not permitted in any field |

### JSON Formatting Rules

| Rule | Detail |
|------|--------|
| Compact serialisation | No whitespace between tokens (minimises packet size) |
| Key order | Type-specific keys should follow the order defined in this specification. Receivers must not depend on key order. |
| Key uniqueness | Duplicate keys within a single object are forbidden |
| String escaping | All special characters in string values must be JSON-escaped |
| Number format | No leading zeros; no trailing decimal points; no NaN or Infinity |
| Boolean literals | Lowercase `true` and `false` only |

### Canonical Example: Compact vs. Readable

**Wire format (compact — as transmitted):**
```
{"proto":1,"type":"telemetry","ts":45231,"seq":904,"ultrasonic":{"front":42,"left":80,"right":75,"rear":200},"tof":{"front":415,"pan":800},"imu":{"ax":0.02,"ay":-0.01,"az":9.81,"gx":0.10,"gy":0.00,"gz":-0.05},"gas":{"raw":218,"hazard":false},"power":{"voltage":7.38,"current":1.12},"health":{"imu_ok":true,"tof_f_ok":true,"tof_p_ok":true,"gas_ok":true,"pwr_ok":false}}
```

**Readable format (for documentation only — not transmitted):**
```json
{
  "proto": 1,
  "type": "telemetry",
  "ts": 45231,
  "seq": 904,
  "ultrasonic": {
    "front": 42,
    "left": 80,
    "right": 75,
    "rear": 200
  },
  "tof": {
    "front": 415,
    "pan": 800
  },
  "imu": {
    "ax": 0.02,
    "ay": -0.01,
    "az": 9.81,
    "gx": 0.10,
    "gy": 0.00,
    "gz": -0.05
  },
  "gas": {
    "raw": 218,
    "hazard": false
  },
  "power": {
    "voltage": 7.38,
    "current": 1.12
  },
  "health": {
    "imu_ok": true,
    "tof_f_ok": true,
    "tof_p_ok": true,
    "gas_ok": true,
    "pwr_ok": false
  }
}
```

---

## 8. Packet Lifecycle

### Complete Packet Lifecycle

```
SENDER                                            RECEIVER
  |                                                  |
  | [1] Data event occurs                            |
  |     (sensor read complete / decision made)       |
  |                                                  |
  | [2] Build payload dict / struct                  |
  |                                                  |
  | [3] Populate mandatory fields                    |
  |     proto, type, ts, seq                         |
  |                                                  |
  | [4] Populate type-specific fields                |
  |                                                  |
  | [5] Validate all values within range             |
  |     (clamp or flag out-of-range values)          |
  |                                                  |
  | [6] Serialise to compact JSON string             |
  |                                                  |
  | [7] Append LF (0x0A)                             |
  |                                                  |
  | [8] Write to serial TX buffer                    |
  |     -------------- USB Serial --------------->   |
  |                                                  |
  |                                     [9] Read until LF
  |                                                  |
  |                                    [10] Check line length <= 512
  |                                         If exceeded: discard, log
  |                                                  |
  |                                    [11] Parse JSON
  |                                         If parse fails: discard, log
  |                                                  |
  |                                    [12] Check "proto" field == 1
  |                                         If mismatch: discard, log
  |                                                  |
  |                                    [13] Check "type" field
  |                                         If unknown: discard (silently)
  |                                         If known: route to handler
  |                                                  |
  |                                    [14] Validate type-specific fields
  |                                         Missing required: discard, log
  |                                         Out of range: clamp, log WARNING
  |                                                  |
  |                                    [15] Process packet
  |                                                  |
  |  [16] If ACK requested and type == "cmd":        |
  |  <--- ACK packet sent back -----                 |
  |                                                  |
  | [17] Log packet (at DEBUG level)                 |
  |                                                  |
```

---

## 9. Packet Timing

### Nominal Timing Budget

```
Telemetry cycle (ESP32 side):
+--------+----------+----------+----------+----------+----------+-----------+
| t=0ms  | t=10ms   | t=20ms   | t=30ms   | t=40ms   | t=42ms   | t=50ms    |
| Fire   | Fire     | Fire     | Fire     | All HC-  | Build    | Next      |
| FRONT  | LEFT     | RIGHT    | REAR     | SR04     | + send   | cycle     |
| HC-SR04| HC-SR04  | HC-SR04  | HC-SR04  | done     | packet   | begins    |
+--------+----------+----------+----------+----------+----------+-----------+
VL53L0X and MPU6050 polled concurrently in background via I2C.
MQ-2 polled at 1 Hz (not every telemetry cycle).

Effective telemetry rate: 20 Hz (50 ms per cycle)
```

### End-to-End Latency

```
Sensor event -> Pi action latency budget:

ESP32 sensor read:           ~40 ms  (4 ultrasonic + I2C sensors)
ESP32 serialise + transmit:   ~2 ms  (at 921600 bps, 512-byte packet)
USB transfer latency:         ~1 ms
Pi serial read:               ~1 ms
Pi sensor fusion:             ~2 ms
Pi AI evaluation:             ~5 ms  (event-driven, not per-frame)
Pi navigation decision:       ~2 ms
Pi command build + transmit:  ~1 ms
USB transfer (return):        ~1 ms
ESP32 parse + dispatch:       ~1 ms
Actuator response:            ~1 ms  (PWM next cycle)
-----------------------------------------------
Total end-to-end (nominal):  ~57 ms
```

### Timing Constraints

| Constraint | Value | Consequence if violated |
|------------|-------|------------------------|
| Maximum telemetry interval | 100 ms | Pi watchdog raises link_stale event |
| Maximum command-to-ACK time | 50 ms | Pi logs WARNING, retries if ACK was requested |
| Maximum heartbeat interval | 2000 ms | Receiver treats link as lost |
| Maximum boot-to-READY time | 10000 ms | Pi times out, logs CRITICAL, retries or exits |
| Maximum packet transmission time | 5 ms | At 921600 bps, 512-byte packet takes ~4.4 ms |

---

## 10. Sequence Numbers

### Purpose

Every packet carries a monotonically increasing `seq` field. Sequence numbers allow the receiver to:

1. Detect dropped packets (gap in sequence).
2. Detect duplicate packets (repeated sequence number).
3. Correlate command packets with their ACK responses via the `ref_seq` field.
4. Verify temporal order of packets in logged data.

### Sequence Number Rules

| Rule | ID | Detail |
|------|----|--------|
| Monotonically increasing | SN-01 | Each packet's `seq` must be exactly 1 greater than the previous packet's `seq` sent by the same sender |
| Per-sender, not per-type | SN-02 | The sequence number is shared across all packet types sent by the same processor |
| Reset on reboot | SN-03 | Sequence number resets to 0 after each reboot |
| Wraparound at 2^32 | SN-04 | `seq` is an unsigned 32-bit integer; wraps from 4,294,967,295 to 0 |
| Receiver must handle wraparound | SN-05 | Receivers must not treat wraparound as a fault |
| Gaps are warnings, not errors | SN-06 | A gap in sequence numbers is logged as WARNING; the receiver continues processing |
| Duplicate sequence rejected | SN-07 | A packet with the same `seq` as a recently received packet is discarded and logged |

### Sequence Number Implementation

```
ESP32-S3 sends:
  seq=0    (READY packet on boot)
  seq=1    (first telemetry)
  seq=2    (second telemetry)
  seq=3    (heartbeat)
  seq=4    (third telemetry)
  ...

Raspberry Pi sends:
  seq=0    (first heartbeat after READY)
  seq=1    (first cmd)
  seq=2    (second cmd)
  seq=3    (heartbeat)
  ...

Each side maintains its own independent sequence counter.
```

---

## 11. Timestamp Strategy

### Clock Sources

| Processor | Clock Source | Resolution | Rollover |
|-----------|-------------|-----------|---------|
| ESP32-S3 | `esp_timer_get_time()` / `millis()` | 1 ms | ~49.7 days |
| Raspberry Pi | `time.monotonic_ns()` converted to ms | 1 ms | Effectively never |

### Timestamp Rules

| Rule | ID | Detail |
|------|----|--------|
| Milliseconds since boot | TS-01 | `ts` is milliseconds elapsed since the sender's last boot. It is NOT wall-clock time. |
| Monotonically increasing | TS-02 | `ts` must never decrease within a single session |
| Independent per sender | TS-03 | Pi timestamps and ESP32 timestamps are independent clocks; do not compare them as absolute times |
| No synchronisation required | TS-04 | The protocol does not require clock synchronisation between the two processors |
| Used for ordering, not timing | TS-05 | The receiver uses `ts` to order packets and compute intervals, not to compare against wall time |
| ACK echoes command timestamp | TS-06 | The `ref_ts` field in an ACK packet echoes the `ts` value from the command being acknowledged |
| Rollover at 2^32 ms | TS-07 | Timestamps roll over after approximately 49.7 days of continuous operation |

### Why Not Wall-Clock Time?

Using milliseconds since boot avoids requiring:
- NTP synchronisation between processors.
- RTC hardware on the ESP32-S3.
- Clock drift compensation logic.

Absolute event times are reconstructed in the logging layer on the Raspberry Pi, which tags log entries with the Pi's wall-clock time and the packet's `ts` value as a delta offset.

---

## 12. Protocol Versioning

### Version Field

Every packet carries a `proto` field containing the integer protocol version. For all Recon Rover V1 packets, this value is `1`.

```json
{ "proto": 1, "type": "telemetry", ... }
```

### Versioning Rules

| Rule | ID | Detail |
|------|----|--------|
| Version is mandatory | PV-01 | Any packet missing the `proto` field is discarded |
| Mismatch is non-fatal | PV-02 | A `proto` value that does not match the receiver's expected version causes the packet to be discarded and a WARNING logged, but does not terminate the connection |
| Minor changes do not increment version | PV-03 | Adding optional fields to existing packet types does not increment the protocol version |
| New mandatory fields increment version | PV-04 | Any change that breaks backward compatibility requires a version increment |
| Version 1 is the only version for V1 | PV-05 | All V1 firmware and software must produce and accept only `proto: 1` |

### Future Version Negotiation (V2+)

When protocol V2 is introduced:

1. The ESP32 READY packet will include: `"proto_max": 2, "proto_min": 1`.
2. The Pi will select the highest mutually supported version.
3. All subsequent packets use the negotiated version.
4. This negotiation mechanism is reserved for V2 and is not implemented in V1.

---

## 13. Telemetry Packet Specification

### Overview

The telemetry packet is the primary data stream from the ESP32-S3 to the Raspberry Pi. It is transmitted at 20 Hz (every 50 ms) and contains a complete snapshot of all sensor readings and system health flags.

### Direction
`ESP32-S3 → Raspberry Pi`

### Transmission Rate
`20 Hz (every 50 ms)`

### Complete Field Specification

```
{
  "proto":      <int>     Protocol version. Must be 1.
  "type":       "telemetry"
  "ts":         <int>     Milliseconds since ESP32 boot.
  "seq":        <int>     ESP32 transmit sequence number.

  "ultrasonic": {
    "front":    <int>     HC-SR04 front distance. Units: cm. Range: 2-400. -1 = sensor fault.
    "left":     <int>     HC-SR04 left distance.  Units: cm. Range: 2-400. -1 = sensor fault.
    "right":    <int>     HC-SR04 right distance. Units: cm. Range: 2-400. -1 = sensor fault.
    "rear":     <int>     HC-SR04 rear distance.  Units: cm. Range: 2-400. -1 = sensor fault.
  }

  "tof": {
    "front":    <int>     VL53L0X front distance. Units: mm. Range: 0-2000. -1 = sensor fault.
    "pan":      <int>     VL53L0X pan-axis distance. Units: mm. Range: 0-2000. -1 = sensor fault.
  }

  "imu": {
    "ax":       <float>   Accelerometer X. Units: m/s². Range: -20.0 to +20.0.
    "ay":       <float>   Accelerometer Y. Units: m/s². Range: -20.0 to +20.0.
    "az":       <float>   Accelerometer Z. Units: m/s². Range: -20.0 to +20.0.
    "gx":       <float>   Gyroscope X. Units: deg/s. Range: -500.0 to +500.0.
    "gy":       <float>   Gyroscope Y. Units: deg/s. Range: -500.0 to +500.0.
    "gz":       <float>   Gyroscope Z. Units: deg/s. Range: -500.0 to +500.0.
    "temp":     <float>   IMU die temperature. Units: degC. Range: -40.0 to +85.0.
  }

  "gas": {
    "raw":      <int>     MQ-2 raw ADC count. Units: ADC counts (0-4095).
    "hazard":   <bool>    True if raw >= gas_hazard_threshold (configured in firmware).
  }

  "power": {
    "voltage":  <float>   Battery voltage. Units: V. -1.0 = sensor not installed.
    "current":  <float>   System current draw. Units: A. -1.0 = sensor not installed.
  }

  "health": {
    "imu_ok":   <bool>    True if MPU6050 is responding and returning valid data.
    "tof_f_ok": <bool>    True if Front VL53L0X is responding and returning valid data.
    "tof_p_ok": <bool>    True if Pan VL53L0X is responding and returning valid data.
    "gas_ok":   <bool>    True if MQ-2 ADC is returning values in plausible range.
    "pwr_ok":   <bool>    True if INA219 is installed and responding. False if not installed.
    "i2c_ok":   <bool>    True if PCA9548A is responding to channel select commands.
  }
}
```

### Telemetry Field Table

| Field | Type | Unit | Valid Range | Fault Value | Notes |
|-------|------|------|------------|-------------|-------|
| `ultrasonic.front` | int | cm | 2 – 400 | -1 | HC-SR04, GPIO4/5 |
| `ultrasonic.left` | int | cm | 2 – 400 | -1 | HC-SR04, GPIO6/7 |
| `ultrasonic.right` | int | cm | 2 – 400 | -1 | HC-SR04, GPIO15/16 |
| `ultrasonic.rear` | int | cm | 2 – 400 | -1 | HC-SR04, GPIO17/18 |
| `tof.front` | int | mm | 0 – 2000 | -1 | VL53L0X, PCA9548A CH2 |
| `tof.pan` | int | mm | 0 – 2000 | -1 | VL53L0X, PCA9548A CH3 |
| `imu.ax` | float | m/s² | -20.0 – +20.0 | 0.0 + imu_ok=false | MPU6050 accel X |
| `imu.ay` | float | m/s² | -20.0 – +20.0 | 0.0 + imu_ok=false | MPU6050 accel Y |
| `imu.az` | float | m/s² | -20.0 – +20.0 | 0.0 + imu_ok=false | MPU6050 accel Z |
| `imu.gx` | float | deg/s | -500.0 – +500.0 | 0.0 + imu_ok=false | MPU6050 gyro X |
| `imu.gy` | float | deg/s | -500.0 – +500.0 | 0.0 + imu_ok=false | MPU6050 gyro Y |
| `imu.gz` | float | deg/s | -500.0 – +500.0 | 0.0 + imu_ok=false | MPU6050 gyro Z |
| `imu.temp` | float | °C | -40.0 – +85.0 | 0.0 + imu_ok=false | IMU die temperature |
| `gas.raw` | int | ADC | 0 – 4095 | 0 + gas_ok=false | MQ-2 raw value |
| `gas.hazard` | bool | — | true / false | false + gas_ok=false | Threshold-based flag |
| `power.voltage` | float | V | 0.0 – 15.0 | -1.0 | INA219; -1.0 = not installed |
| `power.current` | float | A | 0.0 – 10.0 | -1.0 | INA219; -1.0 = not installed |
| `health.imu_ok` | bool | — | true / false | false | MPU6050 I2C responsive |
| `health.tof_f_ok` | bool | — | true / false | false | Front VL53L0X responsive |
| `health.tof_p_ok` | bool | — | true / false | false | Pan VL53L0X responsive |
| `health.gas_ok` | bool | — | true / false | false | MQ-2 ADC in range |
| `health.pwr_ok` | bool | — | true / false | false | INA219 responsive |
| `health.i2c_ok` | bool | — | true / false | false | PCA9548A responsive |

---

## 14. Command Packet Specification

### Overview

The command packet is the primary control stream from the Raspberry Pi to the ESP32-S3. It contains motor commands, servo angle commands, OLED eye expression commands, and LED mode commands. All subsystem commands are packed into a single unified packet.

### Direction
`Raspberry Pi → ESP32-S3`

### Transmission Rate
`Event-driven. Maximum rate: 20 Hz. Minimum rate: as needed.`

### Design Principle: Unified Command Packet

All actuator commands are sent as a single packet. This avoids partial-state problems where the motor command has been applied but the LED command has not yet been received. The ESP32 receives the complete intended state in one atomic operation.

Fields within the command packet are **optional at the field level** — the command packet must contain at least one subsystem block, but not all blocks are required in every packet.

### Complete Field Specification

```
{
  "proto":    <int>       Protocol version. Must be 1.
  "type":     "cmd"
  "ts":       <int>       Milliseconds since Pi boot.
  "seq":      <int>       Pi transmit sequence number.
  "ack":      <bool>      Optional. If true, ESP32 must send an ACK packet. Default: false.

  "motors": {             Optional block. Omit to leave motor state unchanged.
    "fl":     <int>       Front-Left motor. Range: -100 (full reverse) to +100 (full forward). 0 = stop.
    "fr":     <int>       Front-Right motor. Range: -100 to +100.
    "rl":     <int>       Rear-Left motor. Range: -100 to +100.
    "rr":     <int>       Rear-Right motor. Range: -100 to +100.
  }

  "servos": {             Optional block. Omit to leave servo positions unchanged.
    "pan":    <int>       Pan servo angle. Units: degrees. Range: 0 – 180.
    "tilt":   <int>       Tilt servo angle. Units: degrees. Range: 0 – 180.
  }

  "eyes": {               Optional block. Omit to leave eye expression unchanged.
    "expr":   <string>    Expression identifier. Must be a registered expression ID.
                          See Section 29 — Expression Registry.
  }

  "leds": {               Optional block. Omit to leave LED mode unchanged.
    "mode":   <string>    LED mode identifier. See Section 30 — LED Mode Registry.
    "color":  [R, G, B]   Optional. Target colour as integer array [0-255, 0-255, 0-255].
                          Required for modes: "solid", "pulse", "blink", "chase", "strobe".
                          Ignored for modes: "off", "startup_sweep".
    "speed":  <int>       Optional. Animation speed. Range: 1 (slow) to 10 (fast). Default: 5.
  }
}
```

### Command Field Table

| Field | Type | Unit | Valid Range | Required | Default |
|-------|------|------|------------|---------|---------|
| `motors.fl` | int | % | -100 – +100 | If block present | — |
| `motors.fr` | int | % | -100 – +100 | If block present | — |
| `motors.rl` | int | % | -100 – +100 | If block present | — |
| `motors.rr` | int | % | -100 – +100 | If block present | — |
| `servos.pan` | int | degrees | 0 – 180 | If block present | — |
| `servos.tilt` | int | degrees | 0 – 180 | If block present | — |
| `eyes.expr` | string | — | See Expression Registry | If block present | — |
| `leds.mode` | string | — | See LED Mode Registry | If block present | — |
| `leds.color` | array [R,G,B] | 0-255 each | Mode-dependent | Conditional | — |
| `leds.speed` | int | 1-10 | 1 – 10 | No | 5 |
| `ack` | bool | — | true / false | No | false |

### Motor Command Semantics

| Value | Motor Behaviour |
|-------|----------------|
| +100 | Full forward speed |
| +50 | Half forward speed |
| 0 | Stop (brake) |
| -50 | Half reverse speed |
| -100 | Full reverse speed |

The motor value is mapped to L298N signals by the ESP32-S3 motor controller. The absolute maximum duty cycle is firmware-capped at `MOTOR_MAX_DUTY` to prevent full-voltage operation. The Pi may send any value in [-100, +100]; the firmware applies the safety cap internally.

### Servo Command Semantics

| Value | Servo Position |
|-------|---------------|
| 0 | Minimum position (leftmost / lowest) |
| 90 | Centre position |
| 180 | Maximum position (rightmost / highest) |

Firmware enforces the mechanical safe angle limits defined in `config.h`:
- Pan servo: firmware-limited to [0, 180] but may be further restricted per physical mount
- Tilt servo: firmware-limited to [45, 135] to avoid mechanical damage

The Pi sends the desired angle; the firmware clamps to safe range silently and logs a WARNING if clamping occurs.

---

## 15. ACK Packet Specification

### Overview

The ACK packet is sent by the ESP32-S3 to the Raspberry Pi to confirm receipt and processing of a command packet. ACK is optional — the Raspberry Pi must explicitly request it by including `"ack": true` in the command packet.

### Direction
`ESP32-S3 → Raspberry Pi`

### When to Use ACK

| Scenario | Use ACK? |
|---------|---------|
| High-speed autonomous navigation commands (20 Hz) | No — overhead too high |
| Critical one-time commands (emergency stop, shutdown) | Yes |
| Expression change commands | No |
| LED mode change commands | No |
| Diagnostic or calibration commands | Yes |

### Complete Field Specification

```json
{
  "proto":    1,
  "type":     "ack",
  "ts":       <int>,
  "seq":      <int>,
  "ref_seq":  <int>,
  "ref_ts":   <int>,
  "status":   <string>,
  "msg":      <string>
}
```

### ACK Field Table

| Field | Type | Required | Description |
|-------|------|---------|-------------|
| `proto` | int | Yes | Protocol version. Must be 1. |
| `type` | string | Yes | Always `"ack"`. |
| `ts` | int | Yes | ESP32 timestamp when ACK was generated. |
| `seq` | int | Yes | ESP32 sequence number for this ACK packet. |
| `ref_seq` | int | Yes | The `seq` value from the command packet being acknowledged. |
| `ref_ts` | int | Yes | The `ts` value from the command packet being acknowledged. |
| `status` | string | Yes | `"ok"` if command was accepted and dispatched. `"err"` if command was rejected. |
| `msg` | string | No | Optional human-readable description. Required when `status` is `"err"`. |

### ACK Status Values

| Status | Meaning |
|--------|---------|
| `"ok"` | Command received, validated, and dispatched to subsystem queues. |
| `"err"` | Command received but rejected. See `msg` field for reason. |

### ACK Example

```json
{"proto":1,"type":"ack","ts":48210,"seq":312,"ref_seq":201,"ref_ts":48190,"status":"ok","msg":""}
```

Error ACK example:
```json
{"proto":1,"type":"ack","ts":48300,"seq":313,"ref_seq":202,"ref_ts":48280,"status":"err","msg":"servo.pan out of range: received 250, max allowed 180"}
```

---

## 16. Heartbeat Packet

### Overview

The heartbeat packet is sent by both processors at 1 Hz. Its sole purpose is to prove that the sending processor is alive and the serial link is operational. Heartbeats contain no sensor data and no commands.

### Direction
`Bidirectional (each processor sends its own heartbeat)`

### Transmission Rate
`1 Hz (every 1000 ms)`

### Complete Field Specification

```json
{
  "proto":   1,
  "type":    "heartbeat",
  "ts":      <int>,
  "seq":     <int>,
  "uptime":  <int>,
  "mode":    <string>
}
```

### Heartbeat Field Table

| Field | Type | Required | Description |
|-------|------|---------|-------------|
| `proto` | int | Yes | Protocol version. Must be 1. |
| `type` | string | Yes | Always `"heartbeat"`. |
| `ts` | int | Yes | Sender's milliseconds since boot. |
| `seq` | int | Yes | Sender's sequence number. |
| `uptime` | int | Yes | Sender's uptime in whole seconds. |
| `mode` | string | Yes | Sender's current operational mode. See Mode Registry (Section 28). |

### Heartbeat Examples

ESP32-S3 heartbeat:
```json
{"proto":1,"type":"heartbeat","ts":60000,"seq":60,"uptime":60,"mode":"operational"}
```

Raspberry Pi heartbeat:
```json
{"proto":1,"type":"heartbeat","ts":60000,"seq":18,"uptime":60,"mode":"patrolling"}
```

### Heartbeat Timeout Behaviour

If either processor does not receive a heartbeat from the other within 2000 ms:

| Processor | Action |
|-----------|--------|
| Raspberry Pi | Log WARNING; publish `link_stale` event; navigation switches to STOP |
| ESP32-S3 | Watchdog triggers; all motors commanded to STOP; eyes switch to `"error"` |

---

## 17. READY Packet

### Overview

The READY packet is transmitted once by the ESP32-S3 after completing its full boot sequence. It signals to the Raspberry Pi that all hardware has been initialised and the ESP32 is prepared to receive commands and transmit telemetry.

### Direction
`ESP32-S3 → Raspberry Pi (once per boot)`

### Complete Field Specification

```json
{
  "proto":      1,
  "type":       "ready",
  "ts":         <int>,
  "seq":        0,
  "fw_version": <string>,
  "hw_rev":     <string>,
  "sensors": {
    "imu":      <bool>,
    "tof_f":    <bool>,
    "tof_p":    <bool>,
    "gas":      <bool>,
    "power":    <bool>
  }
}
```

### READY Field Table

| Field | Type | Required | Description |
|-------|------|---------|-------------|
| `proto` | int | Yes | Protocol version. Must be 1. |
| `type` | string | Yes | Always `"ready"`. |
| `ts` | int | Yes | Milliseconds since ESP32 boot. |
| `seq` | int | Yes | Always 0 (first packet after boot). |
| `fw_version` | string | Yes | ESP32 firmware version string (e.g., `"v1.0.0"`). |
| `hw_rev` | string | Yes | Hardware revision identifier (e.g., `"rev_a"`). |
| `sensors.imu` | bool | Yes | True if MPU6050 responded successfully during boot. |
| `sensors.tof_f` | bool | Yes | True if Front VL53L0X responded successfully during boot. |
| `sensors.tof_p` | bool | Yes | True if Pan VL53L0X responded successfully during boot. |
| `sensors.gas` | bool | Yes | True if MQ-2 ADC returned a plausible value during boot. |
| `sensors.power` | bool | Yes | True if INA219 responded during boot. False if not installed. |

### READY Example

```json
{"proto":1,"type":"ready","ts":3842,"seq":0,"fw_version":"v1.0.0","hw_rev":"rev_a","sensors":{"imu":true,"tof_f":true,"tof_p":true,"gas":true,"power":false}}
```

### Pi Response to READY

Upon receiving a valid READY packet, the Raspberry Pi must:

1. Log the firmware version and sensor availability at INFO level.
2. Store sensor availability flags for use in sensor fusion (e.g., skip power fields if `sensors.power` is false).
3. Advance the link state machine to OPERATIONAL.
4. Begin sending heartbeat packets.
5. Begin accepting command dispatch from the AI engine and navigation modules.

---

## 18. FAULT Packet

### Overview

The FAULT packet is sent by the ESP32-S3 immediately when a critical hardware fault occurs that requires the Raspberry Pi's immediate attention. FAULT packets are event-driven and not rate-limited — they are transmitted as fast as the condition is detected.

### Direction
`ESP32-S3 → Raspberry Pi (event-driven)`

### Complete Field Specification

```json
{
  "proto":    1,
  "type":     "fault",
  "ts":       <int>,
  "seq":      <int>,
  "code":     <int>,
  "severity": <string>,
  "source":   <string>,
  "msg":      <string>,
  "data":     <object>
}
```

### FAULT Field Table

| Field | Type | Required | Description |
|-------|------|---------|-------------|
| `proto` | int | Yes | Protocol version. Must be 1. |
| `type` | string | Yes | Always `"fault"`. |
| `ts` | int | Yes | ESP32 timestamp when fault was detected. |
| `seq` | int | Yes | ESP32 sequence number. |
| `code` | int | Yes | Error code from Error Code Registry (Section 32). |
| `severity` | string | Yes | `"warning"`, `"error"`, or `"critical"`. |
| `source` | string | Yes | Module or sensor that detected the fault (e.g., `"sensor_manager"`, `"i2c_bus"`). |
| `msg` | string | Yes | Human-readable description of the fault. |
| `data` | object | No | Optional structured data relevant to the fault. |

### FAULT Severity Levels

| Severity | Meaning | Pi Action Required |
|----------|---------|-------------------|
| `"warning"` | Sensor degraded but system operational | Log; flag in world model; continue |
| `"error"` | Subsystem disabled; partial function loss | Log; disable affected module; notify dashboard |
| `"critical"` | System cannot operate safely | Log; stop movement; notify dashboard; attempt recovery |

### FAULT Example

```json
{"proto":1,"type":"fault","ts":91450,"seq":1830,"code":2001,"severity":"error","source":"sensor_manager","msg":"Front VL53L0X not responding after 5 retries","data":{"channel":2,"i2c_addr":"0x29","retries":5}}
```

---

## 19. SHUTDOWN Packet

### Overview

The SHUTDOWN packet is sent by the Raspberry Pi to command the ESP32-S3 to perform a graceful shutdown of all actuators and enter a safe idle state.

### Direction
`Raspberry Pi → ESP32-S3 (once on Pi shutdown)`

### Complete Field Specification

```json
{
  "proto":   1,
  "type":    "shutdown",
  "ts":      <int>,
  "seq":     <int>,
  "reason":  <string>
}
```

### SHUTDOWN Field Table

| Field | Type | Required | Description |
|-------|------|---------|-------------|
| `proto` | int | Yes | Protocol version. Must be 1. |
| `type` | string | Yes | Always `"shutdown"`. |
| `ts` | int | Yes | Pi timestamp. |
| `seq` | int | Yes | Pi sequence number. |
| `reason` | string | Yes | Human-readable reason. E.g., `"operator_stop"`, `"low_battery"`, `"watchdog"`. |

### ESP32 Response to SHUTDOWN

Upon receiving a valid SHUTDOWN packet, the ESP32-S3 must:

1. Immediately stop all motor outputs (brake state).
2. Command all servos to their neutral/safe positions.
3. Set LED mode to `"off"`.
4. Set OLED eyes to `"idle"` or display shutdown animation.
5. Send an ACK packet (`status: "ok"`).
6. Continue transmitting telemetry (the ESP32 does not power off; only the Pi application may terminate).

### SHUTDOWN Example

```json
{"proto":1,"type":"shutdown","ts":184320,"seq":512,"reason":"operator_stop"}
```

---

## 20. Error Packet

### Overview

The error packet is sent by either processor to notify the other of a protocol-level error — specifically, a situation where an incoming packet was malformed, had an unknown type, or violated a protocol rule. It is distinct from the FAULT packet, which reports hardware faults.

### Direction
`Bidirectional`

### Complete Field Specification

```json
{
  "proto":    1,
  "type":     "error",
  "ts":       <int>,
  "seq":      <int>,
  "ref_seq":  <int>,
  "code":     <int>,
  "msg":      <string>
}
```

### Error Field Table

| Field | Type | Required | Description |
|-------|------|---------|-------------|
| `proto` | int | Yes | Protocol version. Must be 1. |
| `type` | string | Yes | Always `"error"`. |
| `ts` | int | Yes | Sender's timestamp. |
| `seq` | int | Yes | Sender's sequence number. |
| `ref_seq` | int | No | Sequence number of the packet that caused the error (if known). |
| `code` | int | Yes | Error code from Error Code Registry. |
| `msg` | string | Yes | Human-readable description. |

### Error Example

```json
{"proto":1,"type":"error","ts":22891,"seq":47,"ref_seq":21,"code":1002,"msg":"JSON parse failed: unexpected character at position 83"}
```

---

## 21. Packet Validation Rules

### Validation Layers

Every received packet is processed through four sequential validation layers. A packet that fails any layer is discarded; processing does not proceed to subsequent layers.

```
Received line (bytes)
        |
        v
[LAYER 1: Frame Validation]
  - Check line is not empty
  - Check line length <= 512 bytes
  - Check line ends with LF (0x0A)
  - FAIL: discard, log "frame_error"

        |
        v
[LAYER 2: JSON Parse Validation]
  - Attempt JSON deserialisation
  - Verify top-level structure is a JSON object {}
  - Verify no duplicate keys
  - FAIL: discard, log "json_parse_error", send error packet

        |
        v
[LAYER 3: Mandatory Field Validation]
  - Verify "proto" exists and == 1
  - Verify "type" exists and is a non-empty string
  - Verify "ts" exists and is a non-negative integer
  - Verify "seq" exists and is a non-negative integer
  - FAIL: discard, log "field_missing_error", send error packet

        |
        v
[LAYER 4: Type-Specific Validation]
  - Route to type-specific validator based on "type" field
  - Verify all required type-specific fields are present
  - Check all numeric values are within defined ranges
  - Check all enum values are registered
  - Out-of-range: clamp to valid range, log WARNING (do NOT discard)
  - Missing required field: discard, log "field_missing_error"
  - Unknown type: discard silently (not an error)

        |
        v
[Process packet normally]
```

### Validation Response Matrix

| Validation Failure | Response | Log Level | Send Error Packet? |
|-------------------|---------|-----------|-------------------|
| Frame too long | Discard | WARNING | No |
| Empty line | Discard | DEBUG | No |
| JSON parse failure | Discard | WARNING | Yes |
| Missing `proto` | Discard | WARNING | Yes |
| Wrong `proto` version | Discard | WARNING | Yes |
| Missing `type` | Discard | WARNING | Yes |
| Unknown `type` | Discard | DEBUG | No |
| Missing mandatory field | Discard | WARNING | Yes |
| Out-of-range numeric | Clamp + continue | WARNING | No |
| Unknown enum value | Discard | WARNING | Yes |
| Duplicate sequence number | Discard | WARNING | No |

---

## 22. Required Fields

### Required Fields by Packet Type

| Packet Type | Required Top-Level Fields | Required Sub-Fields |
|------------|--------------------------|-------------------|
| `telemetry` | proto, type, ts, seq, ultrasonic, tof, imu, gas, health | ultrasonic.{front,left,right,rear}, tof.{front,pan}, imu.{ax,ay,az,gx,gy,gz,temp}, gas.{raw,hazard}, health.{imu_ok,tof_f_ok,tof_p_ok,gas_ok,pwr_ok,i2c_ok} |
| `cmd` | proto, type, ts, seq + at least one subsystem block | Per block: see Section 14 |
| `ack` | proto, type, ts, seq, ref_seq, ref_ts, status | — |
| `heartbeat` | proto, type, ts, seq, uptime, mode | — |
| `ready` | proto, type, ts, seq, fw_version, hw_rev, sensors | sensors.{imu,tof_f,tof_p,gas,power} |
| `fault` | proto, type, ts, seq, code, severity, source, msg | — |
| `shutdown` | proto, type, ts, seq, reason | — |
| `error` | proto, type, ts, seq, code, msg | — |

---

## 23. Optional Fields

| Packet Type | Optional Field | Condition | Description |
|------------|---------------|----------|-------------|
| `cmd` | `ack` | Always | Request ACK. Default false if omitted. |
| `cmd` | `motors` block | — | Omit to leave motors unchanged |
| `cmd` | `servos` block | — | Omit to leave servos unchanged |
| `cmd` | `eyes` block | — | Omit to leave eye expression unchanged |
| `cmd` | `leds` block | — | Omit to leave LED mode unchanged |
| `cmd` | `leds.color` | Mode requires colour | Required for solid/pulse/blink/chase/strobe |
| `cmd` | `leds.speed` | Always | Animation speed hint. Default 5 if omitted. |
| `ack` | `msg` | Always | Required when status is "err". Optional when "ok". |
| `fault` | `data` | Always | Structured fault context. Optional. |
| `error` | `ref_seq` | When known | Sequence of erroneous packet. Optional. |
| `power` | Entire block | Always | Included in telemetry. Values are -1.0 when INA219 not installed. |

---

## 24. Field Naming Convention

### Rules

| Rule | ID | Detail |
|------|----|--------|
| All lowercase | FN-01 | All field names use lowercase ASCII characters only |
| Snake_case | FN-02 | Multi-word field names use underscores. No camelCase, no hyphens. |
| Abbreviations | FN-03 | Abbreviations are permitted for sensor names (ax, ay, az, gx, gy, gz) and established names (tof, imu) |
| Consistent across packet types | FN-04 | The same concept always uses the same field name. E.g., timestamp is always `ts`, never `timestamp` or `time`. |
| No reserved JSON keywords | FN-05 | Field names must not shadow JSON keywords or common programming language keywords |
| Maximum 16 characters | FN-06 | Field names should be kept short to minimise packet size |

### Canonical Field Name Reference

| Field Name | Meaning |
|-----------|---------|
| `proto` | Protocol version |
| `type` | Packet type identifier |
| `ts` | Timestamp (ms since sender boot) |
| `seq` | Sequence number |
| `ref_seq` | Referenced sequence number (for ACK/error) |
| `ref_ts` | Referenced timestamp (for ACK) |
| `uptime` | Uptime in seconds |
| `mode` | Operational mode string |
| `code` | Error or fault code integer |
| `severity` | Fault severity string |
| `source` | Originating module or subsystem name |
| `msg` | Human-readable message string |
| `status` | Outcome status string ("ok" or "err") |
| `fw_version` | Firmware version string |
| `hw_rev` | Hardware revision string |
| `ack` | ACK request flag (boolean) |
| `reason` | Reason string for shutdown or fault |

---

## 25. Units of Measurement

All physical quantities transmitted in protocol packets use the units defined in this table. Units may not be changed without a protocol version increment.

| Field | Unit | Symbol | Notes |
|-------|------|--------|-------|
| `ultrasonic.*` | Centimetres | cm | Integer. HC-SR04 resolution is ~0.3 cm. |
| `tof.*` | Millimetres | mm | Integer. VL53L0X precision ±3 mm. |
| `imu.ax`, `imu.ay`, `imu.az` | Metres per second squared | m/s² | Float, 2 decimal places. |
| `imu.gx`, `imu.gy`, `imu.gz` | Degrees per second | deg/s | Float, 2 decimal places. |
| `imu.temp` | Degrees Celsius | °C | Float, 1 decimal place. |
| `gas.raw` | ADC counts | — | Integer, 0-4095 (12-bit ADC). |
| `power.voltage` | Volts | V | Float, 2 decimal places. |
| `power.current` | Amperes | A | Float, 2 decimal places. |
| `motors.*` | Percentage of max speed | % | Integer, -100 to +100. Signed. |
| `servos.*` | Degrees | deg | Integer, 0 to 180. |
| `leds.color` | RGB component | — | Integer, 0 to 255 per channel. |
| `ts` | Milliseconds | ms | Integer. Since sender boot. |
| `uptime` | Seconds | s | Integer. |

---

## 26. Numeric Precision Rules

| Data Category | Precision Rule | Rationale |
|--------------|---------------|-----------|
| IMU accelerometer | 2 decimal places (e.g., `9.81`) | Sensor resolution ~0.001 m/s²; 2dp is sufficient |
| IMU gyroscope | 2 decimal places (e.g., `-0.05`) | Sensor resolution ~0.01 deg/s; 2dp is sufficient |
| IMU temperature | 1 decimal place (e.g., `32.4`) | Sufficient for thermal monitoring |
| Battery voltage | 2 decimal places (e.g., `7.38`) | INA219 voltage resolution ~0.004 V; 2dp is practical |
| Battery current | 2 decimal places (e.g., `1.12`) | INA219 current resolution depends on shunt; 2dp is practical |
| All distance values | Integer only | No sub-integer precision available from HC-SR04 or VL53L0X in this configuration |
| All control values (motors, servos) | Integer only | PWM resolution does not warrant fractional commands |
| All boolean fields | Literal `true` / `false` | No numeric representation of booleans permitted |

### Precision Violation Handling

- A float value transmitted with more than the specified decimal places must be accepted by the receiver (extra precision is not an error).
- A float value transmitted as `NaN` or `Infinity` is a protocol violation. The receiving parser must discard the packet.

---

## 27. Boolean Rules

| Rule | ID | Detail |
|------|----|--------|
| JSON literals only | BR-01 | Booleans must be JSON `true` or `false`. Not `1`/`0`, not `"true"`/`"false"`. |
| No null substitution | BR-02 | A boolean field must never be `null`. Use the defined fault convention instead. |
| Health flags default false | BR-03 | If a health flag cannot be determined (e.g., sensor not queried yet), it defaults to `false`. |
| Hazard flag latching | BR-04 | `gas.hazard` remains `true` until the raw ADC value falls below threshold AND a configurable hysteresis time has elapsed. |
| ACK flag default false | BR-05 | If `"ack"` is omitted from a command packet, the receiver treats it as `false`. |

---

## 28. Enum Definitions

### Packet Type Enum

| Value | Direction | Description |
|-------|-----------|-------------|
| `"telemetry"` | ESP32 -> Pi | Sensor snapshot |
| `"cmd"` | Pi -> ESP32 | Actuator commands |
| `"ack"` | ESP32 -> Pi | Command acknowledgement |
| `"heartbeat"` | Both | Liveness probe |
| `"ready"` | ESP32 -> Pi | Boot completion |
| `"fault"` | ESP32 -> Pi | Hardware fault |
| `"shutdown"` | Pi -> ESP32 | Graceful shutdown |
| `"error"` | Both | Protocol error |

### ACK Status Enum

| Value | Meaning |
|-------|---------|
| `"ok"` | Command accepted and dispatched |
| `"err"` | Command rejected; see msg field |

### Fault Severity Enum

| Value | Meaning |
|-------|---------|
| `"warning"` | Degraded operation; no immediate safety concern |
| `"error"` | Subsystem disabled; system partially functional |
| `"critical"` | Unsafe to operate; immediate response required |

### Operational Mode Enum (used in heartbeat `mode` field)

| Value | Applicable To | Description |
|-------|--------------|-------------|
| `"booting"` | Both | System is initialising |
| `"operational"` | ESP32 | ESP32 is fully initialised and processing |
| `"idle"` | Pi | Rover is active but stationary |
| `"patrolling"` | Pi | Rover is navigating autonomously |
| `"tracking"` | Pi | Rover is following a detected target |
| `"avoiding"` | Pi | Rover is executing obstacle avoidance |
| `"searching"` | Pi | Rover is searching for a lost target |
| `"hazard"` | Pi | Rover has detected a gas hazard |
| `"error"` | Pi | Pi software is in error state |
| `"shutdown"` | Both | Shutdown in progress |

---

## 29. Expression Registry

The expression registry is the canonical list of valid OLED eye expression identifiers. The Raspberry Pi's expression selector module may only use identifiers from this list. The ESP32-S3 firmware must implement all identifiers in this list.

Any identifier not in this list must be rejected by the ESP32-S3 command parser with an error response.

| Expression ID | Description | Trigger Context | Animation |
|--------------|-------------|----------------|-----------|
| `"idle"` | Neutral open eyes | Default/waiting | Slow blink every 4-6 s |
| `"happy"` | Wide open, curved top eyelid | Person detected | Occasional bright blink |
| `"curious"` | One eye slightly wider, gaze offset | Object in view, tracking | Slow asymmetric blink |
| `"alert"` | Wide open, static, no blink | Obstacle very close | Static, no blink |
| `"sleepy"` | Half-closed, drooping | Low activity, idle long period | Very slow blink |
| `"excited"` | Very wide, pupils enlarged | High-confidence target detection | Fast alternating blink |
| `"confused"` | One eye narrowed, one wide | Low-confidence detection | Head-tilt blink |
| `"hazard"` | Narrow slits, rapid blink | Gas threshold exceeded | Rapid blink 3 Hz |
| `"error"` | X symbols on both eyes | Critical system fault | Static |
| `"sleep"` | Fully closed | Deep idle mode | Static closed |
| `"startup"` | Expanding pupils from closed | Boot animation | Progressive open |
| `"shutdown"` | Slowly closing | Shutdown sequence | Progressive close |
| `"tracking_left"` | Both pupils shifted left | Target left of centre | Hold + slow blink |
| `"tracking_right"` | Both pupils shifted right | Target right of centre | Hold + slow blink |
| `"looking_up"` | Pupils shifted upward | Target elevated | Hold + slow blink |

### Adding New Expressions

1. Add the new ID to this registry with description and trigger context.
2. Implement the bitmap and animation in `oled_renderer.cpp`.
3. Update `expression_registry.md` in `SHARED/`.
4. No protocol version increment required (new enum values are backward compatible).

---

## 30. LED Mode Registry

The LED mode registry is the canonical list of valid WS2812B LED mode identifiers.

| Mode ID | Description | `color` Required | `speed` Effect |
|---------|-------------|-----------------|----------------|
| `"off"` | All LEDs off | No | N/A |
| `"solid"` | All LEDs constant colour | Yes | N/A |
| `"pulse"` | Sine-wave brightness on target colour | Yes | Period of pulse |
| `"blink"` | Toggle on/off at fixed interval | Yes | Toggle frequency |
| `"chase"` | Single LED travels across strip | Yes | Travel speed |
| `"strobe"` | Rapid high-frequency on/off | Yes | Strobe rate |
| `"sweep"` | Progressive fill left-to-right | Yes | Fill speed |
| `"rainbow"` | Full hue rotation across all LEDs | No | Rotation speed |
| `"breathe"` | Slow fade in and out | Yes | Breath rate |
| `"patrol"` | Cyan steady | No | N/A |
| `"tracking"` | Yellow chase | No | N/A |
| `"alert"` | Orange rapid blink | No | N/A |
| `"hazard"` | Red strobe | No | N/A |
| `"low_battery"` | Red slow pulse | No | N/A |
| `"error_mode"` | Magenta alternating | No | N/A |
| `"startup"` | White sweep animation | No | N/A |

> **Note:** Named semantic modes (patrol, tracking, alert, etc.) are convenience aliases. They map to a specific colour + animation combination defined in firmware. The Pi may use either the semantic alias or an explicit `"mode": "pulse", "color": [255, 200, 0]` combination.

---

## 31. Command Registry

The command registry documents all valid command packets and the subsystem blocks they may contain. This is a cross-reference for developers implementing the command parser.

| Command Context | Required Block | Key Fields |
|----------------|---------------|-----------|
| Move forward | `motors` | fl=+N, fr=+N, rl=+N, rr=+N |
| Move reverse | `motors` | fl=-N, fr=-N, rl=-N, rr=-N |
| Turn left (curve) | `motors` | fl=+Ns, fr=+Nf, rl=+Ns, rr=+Nf (slow left, fast right) |
| Turn right (curve) | `motors` | fl=+Nf, fr=+Ns, rl=+Nf, rr=+Ns |
| Pivot left | `motors` | fl=-N, fr=+N, rl=-N, rr=+N |
| Pivot right | `motors` | fl=+N, fr=-N, rl=+N, rr=-N |
| Stop (brake) | `motors` | fl=0, fr=0, rl=0, rr=0 |
| Pan camera | `servos` | pan=angle |
| Tilt camera | `servos` | tilt=angle |
| Pan + Tilt | `servos` | pan=angle, tilt=angle |
| Change eye expression | `eyes` | expr=expression_id |
| Change LED mode | `leds` | mode=mode_id, color=[R,G,B] |
| Full state update | `motors` + `servos` + `eyes` + `leds` | All blocks present |
| Emergency stop | `motors` | fl=0, fr=0, rl=0, rr=0, ack=true |
| Shutdown actuators | `shutdown` packet | reason="operator_stop" |

---

## 32. Error Code Registry

Error codes are integer identifiers used in FAULT packets and ERROR packets. They provide a machine-readable classification of error conditions.

### Code Ranges

| Range | Category |
|-------|---------|
| 1000 – 1099 | Protocol errors (framing, JSON, field validation) |
| 2000 – 2099 | Sensor faults |
| 3000 – 3099 | Actuator faults |
| 4000 – 4099 | Communication link faults |
| 5000 – 5099 | System-level faults |
| 9000 – 9099 | Reserved for future use |

### Protocol Error Codes (1000–1099)

| Code | Name | Description |
|------|------|-------------|
| 1001 | `FRAME_TOO_LONG` | Received line exceeds 512 bytes |
| 1002 | `JSON_PARSE_FAIL` | Line is not valid JSON |
| 1003 | `MISSING_PROTO` | `proto` field absent or wrong type |
| 1004 | `PROTO_MISMATCH` | `proto` value does not equal 1 |
| 1005 | `MISSING_TYPE` | `type` field absent |
| 1006 | `MISSING_TS` | `ts` field absent or wrong type |
| 1007 | `MISSING_SEQ` | `seq` field absent or wrong type |
| 1008 | `MISSING_REQUIRED_FIELD` | Required type-specific field absent |
| 1009 | `UNKNOWN_ENUM_VALUE` | Enum field contains unregistered value |
| 1010 | `EMPTY_CMD_PACKET` | Command packet has no subsystem blocks |
| 1011 | `DUPLICATE_SEQ` | Received duplicate sequence number |
| 1012 | `NULL_FIELD_VALUE` | A field contains JSON null |

### Sensor Fault Codes (2000–2099)

| Code | Name | Description |
|------|------|-------------|
| 2001 | `SENSOR_TOF_FRONT_FAIL` | Front VL53L0X not responding |
| 2002 | `SENSOR_TOF_PAN_FAIL` | Pan VL53L0X not responding |
| 2003 | `SENSOR_IMU_FAIL` | MPU6050 not responding |
| 2004 | `SENSOR_GAS_OUT_OF_RANGE` | MQ-2 ADC returned implausible value |
| 2005 | `SENSOR_POWER_FAIL` | INA219 not responding |
| 2006 | `SENSOR_I2C_BUS_FAIL` | PCA9548A not responding |
| 2007 | `SENSOR_HCSR04_TIMEOUT` | One or more HC-SR04 ECHO timed out |

### Actuator Fault Codes (3000–3099)

| Code | Name | Description |
|------|------|-------------|
| 3001 | `MOTOR_OVERCURRENT` | Motor draw exceeds safe threshold (requires INA219) |
| 3002 | `SERVO_ANGLE_CLAMPED` | Commanded servo angle was clamped to safe range |
| 3003 | `OLED_WRITE_FAIL` | I2C write to SSD1306 failed |
| 3004 | `LED_WRITE_FAIL` | WS2812B write failure |

### Communication Fault Codes (4000–4099)

| Code | Name | Description |
|------|------|-------------|
| 4001 | `LINK_IDLE_TIMEOUT` | No packet received from Pi within watchdog timeout |
| 4002 | `HEARTBEAT_MISSED` | Heartbeat not received within expected window |
| 4003 | `TX_BUFFER_OVERFLOW` | Serial TX buffer full; packet dropped |
| 4004 | `RX_BUFFER_OVERFLOW` | Serial RX buffer full; packet dropped |

### System Fault Codes (5000–5099)

| Code | Name | Description |
|------|------|-------------|
| 5001 | `WATCHDOG_TASK_TIMEOUT` | A FreeRTOS task missed its heartbeat |
| 5002 | `BOOT_SENSOR_FAILURE` | Critical sensor failed during boot initialisation |
| 5003 | `MEMORY_ALLOCATION_FAIL` | Firmware memory allocation failed |
| 5004 | `CONFIG_INVALID` | Configuration value out of valid range |

---

## 33. Communication State Machine

The communication link between the Raspberry Pi and ESP32-S3 is managed by a formal state machine on both processors. The states define what actions are permitted and what events trigger transitions.

### Link State Machine

```
+===============================================================+
|              LINK STATE MACHINE  (both processors)            |
+===============================================================+

                     [POWER ON]
                          |
                          v
                  +---------------+
                  |    OFFLINE    |
                  | Serial port   |
                  | not open      |
                  +-------+-------+
                          |
                   Serial port opened
                          |
                          v
                  +---------------+
                  |  CONNECTING   |
                  | Waiting for   |
                  | READY packet  |<-- timeout (10s) --> OFFLINE
                  | (Pi side)     |
                  +-------+-------+
                          |
              READY received (Pi) / first packet received (ESP32)
                          |
                          v
                  +---------------+
                  | OPERATIONAL   | <--- Heartbeats exchanged
                  | Normal running|      Telemetry flowing
                  | state         |      Commands processed
                  +-------+-------+
                    |           |
         Heartbeat           SHUTDOWN received
         timeout             OR Pi exits
         (>2000ms)                |
              |                   v
              v           +---------------+
       +-------------+    |  SHUTTING     |
       |   STALE     |    |  DOWN         |
       | No recent   |    | Actuators     |
       | packets     |    | stopping      |
       +------+------+    +-------+-------+
              |                   |
         Heartbeat         Shutdown complete
         received                 |
              |                   v
              |           +---------------+
              |           |   OFFLINE     |
              |           | (final state) |
              |           +---------------+
              |
        Recovery timeout (>5000ms total)
              |
              v
       +-------------+
       |  LINK LOST  |
       | Motors stop |
       | Eyes: error |
       | Attempting  |
       | reconnect   |
       +------+------+
              |
         Valid packet received
              |
              v
       [OPERATIONAL]
```

### State Descriptions

| State | Description | Permitted Actions |
|-------|------------|-------------------|
| `OFFLINE` | Serial port not open | Open serial port |
| `CONNECTING` | Awaiting READY or first valid packet | Receive only |
| `OPERATIONAL` | Full bidirectional communication active | All packet types |
| `STALE` | Recent heartbeat missed | All operations at reduced confidence |
| `LINK_LOST` | Extended silence; unsafe to operate | Stop actuators; await recovery |
| `SHUTTING_DOWN` | Shutdown sequence in progress | Stop actuators; send final ACK |

### State Transition Table

| Current State | Event | Next State |
|--------------|-------|-----------|
| OFFLINE | Serial port opened | CONNECTING |
| CONNECTING | READY packet received | OPERATIONAL |
| CONNECTING | Any valid packet received | OPERATIONAL |
| CONNECTING | 10 s timeout | OFFLINE |
| OPERATIONAL | Valid packet received | OPERATIONAL (reset timer) |
| OPERATIONAL | Heartbeat missed >2000 ms | STALE |
| OPERATIONAL | SHUTDOWN packet received | SHUTTING_DOWN |
| STALE | Valid packet received | OPERATIONAL |
| STALE | Silence >5000 ms total | LINK_LOST |
| LINK_LOST | Valid packet received | OPERATIONAL |
| SHUTTING_DOWN | Actuators stopped + ACK sent | OFFLINE |

---

## 34. Packet Sequence Diagrams

### 1. Normal Boot Sequence

```
Raspberry Pi                              ESP32-S3
     |                                        |
     |  [Power applied]                       |  [Power applied]
     |  Pi opens serial port                  |  ESP32 boots FreeRTOS
     |  Pi waits for READY                    |  Initialises all sensors
     |                                        |  Spawns all tasks
     |  <-- {"type":"ready","seq":0,...} ---- |  READY transmitted
     |                                        |
     |  Pi logs firmware + sensor status      |
     |  Pi transitions to OPERATIONAL         |
     |  --> {"type":"heartbeat",...} -------> |
     |  <-- {"type":"telemetry",...} -------- |  seq=1
     |  <-- {"type":"heartbeat",...} -------- |
     |  [Normal OPERATIONAL state]            |
```

### 2. Normal Telemetry + Command Exchange

```
Raspberry Pi                              ESP32-S3
     |  <-- telemetry (seq=100) ------------- |
     |  sensor_fusion processes               |
     |  navigation computes                   |
     |  --> cmd (seq=50, motors) -----------> |
     |  [no ACK]                              |  motor_controller updates
     |  <-- telemetry (seq=101) ------------- |
     |  <-- telemetry (seq=102) ------------- |
     |  --> cmd (seq=51, eyes+leds) ------->  |
     |  <-- telemetry (seq=103) ------------- |
```

### 3. Command with ACK and Error

```
Raspberry Pi                              ESP32-S3
     |  --> cmd (seq=202, servos.pan=250,     |
     |           ack:true) ----------------> |
     |                                        |  Validate servo.pan
     |                                        |  250 > max (180); clamp to 180
     |  <-- ack (ref_seq=202, status:"err",   |
     |       msg:"servo.pan clamped") ------- |
     |  Pi logs WARNING                       |
```

### 4. Fault Detection and Response

```
Raspberry Pi                              ESP32-S3
     |  <-- telemetry (health.tof_f_ok=false) |  Fault flagged in telemetry
     |  Pi: sensor_fusion flags tof_f_fault   |
     |  <-- fault (code:2001, severity:error) |  Separate fault packet
     |  Pi: log ERROR                         |
     |  Pi: disable tof_front dependent logic |
     |  Pi: notify dashboard                  |
```

### 5. Link Loss and Recovery

```
Raspberry Pi                              ESP32-S3
     |  <-- telemetry (seq=500) ------------- |
     |  [USB cable disconnected]              |
     |  ...2000 ms silence...                |  ...2000 ms silence...
     |  Pi: STALE state, nav -> STOP          |  watchdog: motors -> STOP
     |  ...3000 ms more silence...           |  eyes -> "error"
     |  Pi: LINK_LOST                         |
     |  [USB cable reconnected]               |
     |  <-- ready (seq=0) ------------------- |  ESP32 rebooted
     |  Pi: OPERATIONAL restored              |
     |  Pi: log INFO "link recovered"         |
```

### 6. Graceful Shutdown

```
Raspberry Pi                              ESP32-S3
     |  --> cmd (motors all=0, ack:true) ---> |
     |  <-- ack (status:"ok") --------------- |
     |  --> shutdown (reason:"operator_stop") |
     |                                        |  Motors stop, servos neutral
     |                                        |  LEDs off
     |  <-- ack (ref to shutdown, "ok") ----- |
     |  Pi: close serial port                 |
```

---

## 35. Communication Timing Diagrams

### Nominal Steady-State Timing (50 ms window)

```
Time (ms):  0    10   20   30   40   42  50
            |    |    |    |    |    |   |

ESP32:   Fire  Fire  Fire  Fire  All   Tx  Next
         FRONT LEFT  RIGHT REAR  done  pkt cycle

Pi:                               42ms: Rx telemetry
                                  43ms: Sensor fusion
                                  44ms: World model
                                  44ms: AI evaluate
                                  46ms: Navigation
                                  47ms: Tx command

ESP32:                                       48ms: Rx + dispatch
                                             48ms: Actuators respond
```

### Heartbeat Timing

```
Time (s):  0    1    2    3    4    5
           |    |    |    |    |    |

Pi HB:     H         H         H         H
ESP32 HB:       H         H         H

Watchdog window (ESP32): |<-- 2000ms -->|
If no Pi packet in window -> LINK LOST
```

### ACK Round-Trip

```
Time (ms): 0    1    2    3    4    5
           |    |    |    |    |    |

Pi:        Tx cmd
ESP32:          Rx, parse, validate, dispatch
                                    Tx ACK
Pi:                                      Rx ACK, cancel timer
Round-trip: ~5ms    ACK timeout: 50ms (10x margin)
```

---

## 36. Retry Strategy

### Retry Policy Table

| Scenario | Retry? | Max Retries | Interval |
|---------|--------|------------|---------|
| ACK not received | Yes | 3 | 50 ms |
| Serial port open failure | Yes | 5 | 2000 ms |
| READY packet timeout | Yes | 3 | 10000 ms |
| JSON parse error | No | — | N/A |
| Sensor read failure (ESP32) | Yes | 5 | Next poll |

### Retry Rules

| Rule | ID | Detail |
|------|----|--------|
| Retried commands carry new seq | RT-01 | Each retry increments the sequence number |
| Retried commands carry new ts | RT-02 | Each retry carries current timestamp |
| Retry limit is hard | RT-03 | After exhausting retries: log ERROR, abandon |
| Emergency stop never retried | RT-05 | Emergency stop is sent 3 times consecutively regardless of ACK |

### Emergency Stop Transmission Protocol

```
Pi sends: stop_cmd (seq=N+1, motors all=0, ack:true)
Pi sends: stop_cmd (seq=N+2, motors all=0, ack:false)  <- immediate
Pi sends: stop_cmd (seq=N+3, motors all=0, ack:false)  <- immediate

Triple transmission ensures delivery across any momentary serial hiccup.
```

---

## 37. Timeout Handling

### Timeout Registry

| Timeout | Value | Monitored By | Action on Expiry |
|---------|-------|-------------|-----------------|
| READY wait | 10000 ms | Pi serial_manager | Retry or exit |
| ACK wait | 50 ms | Pi command_builder | Retry up to 3x |
| Heartbeat stale | 2000 ms | Both | STALE state |
| Link lost | 5000 ms | Both | LINK_LOST; stop actuators |
| Sensor read (I2C) | 10 ms | ESP32 sensor_manager | Fault value |
| HC-SR04 ECHO | 30 ms | ESP32 driver | Report -1 |
| Telemetry age | 200 ms | Pi sensor_fusion | Stale warning |

### Timeout Implementation

- Pi uses `asyncio` timeout contexts for all async waits.
- ESP32 uses FreeRTOS `xQueueReceive` with tick-count timeout.
- Any valid packet received resets the heartbeat watchdog — not only heartbeat packets.

---

## 38. Link Recovery Procedure

### Scenario A: Reconnect Without Reboot

```
1. ESP32: serial read fails for >2s
   -> Watchdog: motors STOP, eyes="error", leds="error_mode"
   -> ESP32 continues attempting serial read (no reboot)

2. Pi: no packets for >2s
   -> STALE -> LINK_LOST
   -> navigation: STOP published
   -> dashboard: link_lost notification

3. [USB cable reconnected]

4. Pi: flush serial buffer
   -> send heartbeat
   -> wait up to 10s for any ESP32 packet

5. ESP32: receives Pi heartbeat
   -> OPERATIONAL state restored
   -> eyes -> "idle"

6. Pi: receives any ESP32 packet
   -> OPERATIONAL state restored
   -> log INFO "link recovered after N ms"
```

### Scenario B: ESP32 Reboots

```
1. Pi: LINK_LOST (no packets >5s)

2. ESP32 reboots
   -> seq resets to 0
   -> transmits READY packet (seq=0)

3. Pi: receives READY packet
   -> seq tracking reset to expect seq=1
   -> new sensor availability stored
   -> OPERATIONAL state restored
   -> log INFO "ESP32 rebooted, session restarted"
```

---

## 39. Packet Size Limits

| Packet Type | Typical | Maximum |
|------------|---------|--------|
| `telemetry` | 280–320 bytes | 512 bytes |
| `cmd` | 80–200 bytes | 256 bytes |
| `ack` | 90–140 bytes | 256 bytes |
| `heartbeat` | 70–90 bytes | 128 bytes |
| `ready` | 120–160 bytes | 256 bytes |
| `fault` | 100–300 bytes | 512 bytes |
| `shutdown` | 70–90 bytes | 128 bytes |
| `error` | 80–200 bytes | 256 bytes |

The 512-byte hard limit fits within a single USB full-speed transfer frame, the ESP32 CDC TX buffer without fragmentation, and the Pi serial read buffer with margin.

---

## 40. Serialization Rules

### Raspberry Pi (Python)

| Rule | Detail |
|------|--------|
| Use `json.dumps(separators=(',', ':'))` | Compact JSON, no whitespace |
| Float precision via `round(value, N)` | Prevents floating-point noise |
| Append `\n` manually | One byte LF, not CRLF |
| Encode to UTF-8: `line.encode('utf-8')` | Before writing to serial |

### ESP32-S3 (C++)

| Rule | Detail |
|------|--------|
| Use ArduinoJson or cJSON | ArduinoJson recommended |
| Use `StaticJsonDocument` | Avoids heap fragmentation |
| Use `serializeJson(doc, buffer, size)` | Stack-allocated buffer |
| Append `0x0A` after serialisation | LF byte appended manually |

---

## 41. Deserialization Rules

### Raspberry Pi (Python)

| Rule | Detail |
|------|--------|
| `json.loads(line.decode('utf-8'))` | Decode bytes first |
| Catch `json.JSONDecodeError` | Discard + log + send error packet |
| Catch `UnicodeDecodeError` | Discard + log at WARNING |
| Use `.get(key, default)` | Never use bare `[]` indexing |
| Validate types and ranges after parsing | `json.loads` does not validate ranges |

### ESP32-S3 (C++)

| Rule | Detail |
|------|--------|
| `StaticJsonDocument<512>` | Matches max packet size |
| Check `deserializeJson()` return value | Non-zero = parse error |
| Check `isNull()` on each required key | Absent required key = discard |
| `constrain()` all numeric values | Clamp after parse |
| Never deserialise in interrupt context | command_parser task only |

---

## 42. Protocol Examples

This section provides complete, wire-ready packet examples. All are shown as transmitted on the serial line.

---

## 43. Good Packet Examples

### Telemetry — All Sensors Healthy

```
{"proto":1,"type":"telemetry","ts":45231,"seq":904,"ultrasonic":{"front":42,"left":80,"right":75,"rear":200},"tof":{"front":415,"pan":800},"imu":{"ax":0.02,"ay":-0.01,"az":9.81,"gx":0.10,"gy":0.00,"gz":-0.05,"temp":32.4},"gas":{"raw":218,"hazard":false},"power":{"voltage":7.38,"current":1.12},"health":{"imu_ok":true,"tof_f_ok":true,"tof_p_ok":true,"gas_ok":true,"pwr_ok":true,"i2c_ok":true}}
```

### Telemetry — Front ToF Faulted, Power Not Installed

```
{"proto":1,"type":"telemetry","ts":46120,"seq":905,"ultrasonic":{"front":38,"left":82,"right":78,"rear":205},"tof":{"front":-1,"pan":810},"imu":{"ax":0.01,"ay":0.00,"az":9.80,"gx":0.00,"gy":0.00,"gz":0.01,"temp":32.5},"gas":{"raw":215,"hazard":false},"power":{"voltage":-1.0,"current":-1.0},"health":{"imu_ok":true,"tof_f_ok":false,"tof_p_ok":true,"gas_ok":true,"pwr_ok":false,"i2c_ok":true}}
```

### Command — Forward Movement Only

```
{"proto":1,"type":"cmd","ts":18450,"seq":91,"ack":false,"motors":{"fl":65,"fr":65,"rl":65,"rr":65}}
```

### Command — Pivot Right + Pan Camera

```
{"proto":1,"type":"cmd","ts":18520,"seq":92,"ack":false,"motors":{"fl":60,"fr":-60,"rl":60,"rr":-60},"servos":{"pan":120,"tilt":90}}
```

### Command — Full State Update with ACK

```
{"proto":1,"type":"cmd","ts":18590,"seq":93,"ack":true,"motors":{"fl":0,"fr":0,"rl":0,"rr":0},"servos":{"pan":90,"tilt":90},"eyes":{"expr":"idle"},"leds":{"mode":"solid","color":[0,80,200],"speed":5}}
```

### Command — Eyes and LEDs Only

```
{"proto":1,"type":"cmd","ts":18650,"seq":94,"ack":false,"eyes":{"expr":"happy"},"leds":{"mode":"patrol"}}
```

### ACK — Success

```
{"proto":1,"type":"ack","ts":18595,"seq":315,"ref_seq":93,"ref_ts":18590,"status":"ok","msg":""}
```

### ACK — Error (servo clamped)

```
{"proto":1,"type":"ack","ts":48300,"seq":313,"ref_seq":202,"ref_ts":48280,"status":"err","msg":"servo.pan out of range: received 250, max allowed 180"}
```

### Heartbeat — Pi

```
{"proto":1,"type":"heartbeat","ts":60000,"seq":18,"uptime":60,"mode":"patrolling"}
```

### Heartbeat — ESP32

```
{"proto":1,"type":"heartbeat","ts":60050,"seq":62,"uptime":60,"mode":"operational"}
```

### READY — All Sensors Online

```
{"proto":1,"type":"ready","ts":3842,"seq":0,"fw_version":"v1.0.0","hw_rev":"rev_a","sensors":{"imu":true,"tof_f":true,"tof_p":true,"gas":true,"power":false}}
```

### FAULT — I2C Bus Critical

```
{"proto":1,"type":"fault","ts":91450,"seq":1830,"code":2006,"severity":"critical","source":"sensor_manager","msg":"PCA9548A not responding. All multiplexed devices unreachable.","data":{"i2c_addr":"0x70","last_error":"NACK"}}
```

### FAULT — IMU Warning

```
{"proto":1,"type":"fault","ts":95000,"seq":1910,"code":2003,"severity":"warning","source":"driver_mpu6050","msg":"MPU6050 returned out-of-range accelerometer value on axis Z","data":{"axis":"az","raw_value":45.2,"max_valid":20.0}}
```

### SHUTDOWN

```
{"proto":1,"type":"shutdown","ts":184320,"seq":512,"reason":"low_battery"}
```

### ERROR — JSON Parse Failure

```
{"proto":1,"type":"error","ts":22891,"seq":47,"ref_seq":21,"code":1002,"msg":"JSON parse failed: unexpected token at position 83"}
```

### ERROR — Unknown Expression ID

```
{"proto":1,"type":"error","ts":23100,"seq":48,"ref_seq":22,"code":1009,"msg":"eyes.expr value winking is not a registered expression ID"}
```

---

## 44. Invalid Packet Examples

| Example | Fault | Response |
|---------|-------|---------|
| `{"type":"telemetry","ts":1000,"seq":1}` | Missing `proto` | Discard, log WARNING, send error code 1003 |
| `{"proto":2,"type":"telemetry","ts":1000,"seq":1}` | Proto mismatch | Discard, log WARNING, send error code 1004 |
| `{"proto":1,"type":"telemetry","ts":1000,"seq":1,"ultrasonic":{"front":42` | Truncated JSON | Discard, log WARNING, send error code 1002 |
| `[{"proto":1,"type":"telemetry"}]` | Array root | Discard, log WARNING, send error code 1002 |
| `{"proto":1,"type":"telemetry","ts":null,"seq":1}` | Null field | Discard, log WARNING, send error code 1012 |
| `{"proto":1,"type":"cmd","ts":1000,"seq":5,"motors":{"fl":150,"fr":65,"rl":65,"rr":65}}` | fl out of range | Clamp fl to 100, log WARNING, continue |
| `{"proto":1,"type":"cmd","ts":1000,"seq":6,"eyes":{"expr":"winking"}}` | Unknown expression | Discard eyes block, log WARNING, send error code 1009 |
| `{"proto":1,"type":"cmd","ts":1000,"seq":7,"ack":false}` | Empty cmd, no blocks | Discard, log WARNING, send error code 1010 |
| `[600-byte packet]` | Frame too long | Discard, log WARNING, send error code 1001 |

---

## 45. Debugging Guidelines

### Live Serial Monitoring

Every packet is newline-delimited UTF-8 JSON — readable directly in any serial terminal:

```
PuTTY:     Set baud 921600, connection type: Serial, LF line endings
minicom:   minicom -b 921600 -D /dev/ttyACM0
Python:    python -m serial.tools.miniterm /dev/ttyACM0 921600
```

### Pretty-Print Stream

```
python -c "
import sys, json
for line in sys.stdin:
    try: print(json.dumps(json.loads(line), indent=2))
    except: print('[RAW]', line.strip())
" < /dev/ttyACM0
```

### Diagnostic Checklist

| Symptom | Likely Cause | Diagnostic Step |
|---------|-------------|----------------|
| No packets received | Wrong port path | Check `/dev/ttyACM0` vs `/dev/ttyUSB0` |
| Garbled packets | Baud mismatch | Confirm both sides use 921600 |
| Frequent parse errors | Buffer overflow or noise | Reduce rate; check cable; add ferrite bead |
| Motors unresponsive | cmd not reaching ESP32 | Enable ACK; check serial TX path |
| Telemetry stops after reconnect | Seq tracking bug | Verify seq=0 handled on READY detection |
| High end-to-end latency | Pi CPU overloaded | Profile OpenCV inference; reduce frame rate |
| Heartbeat timeouts | asyncio loop blocked | Check for blocking calls in threads |

### Packet Rate Monitoring (Target Values)

| Metric | Target |
|--------|--------|
| Telemetry packets/s | 20 |
| Heartbeats/s (each direction) | 1 |
| Parse errors/s | 0 |
| ACK timeouts/session | 0 |
| Sequence gaps/session | 0 |

---

## 46. Logging Requirements

### Log Entry Format (JSON)

```json
{
  "ts": "2026-06-28T10:30:00.123Z",
  "level": "WARNING",
  "module": "serial_manager",
  "event": "json_parse_error",
  "data": {
    "raw_bytes_prefix": "{\"proto\":1,\"type\":\"telem",
    "error": "Unexpected end of JSON"
  }
}
```

### Required Log Events

| Event | Level | Fields |
|-------|-------|--------|
| Serial port opened | INFO | port, baud |
| READY received | INFO | fw_version, hw_rev, sensors |
| Parse failure | WARNING | raw_bytes (first 64), error |
| Proto mismatch | WARNING | received, expected |
| Missing required field | WARNING | packet_type, field_name |
| Out-of-range clamped | WARNING | field, received, clamped_to |
| Unknown enum | WARNING | field, value |
| FAULT received | ERROR | code, severity, source, msg |
| CRITICAL fault | CRITICAL | code, source, msg, data |
| Heartbeat missed | WARNING | elapsed_ms |
| Link STALE | WARNING | elapsed_ms |
| Link LOST | ERROR | elapsed_ms |
| Link recovered | INFO | downtime_ms |
| Seq gap | WARNING | expected, received, gap |
| Duplicate seq | WARNING | seq, packet_type |
| ACK timeout | WARNING | cmd_seq, elapsed, retries |
| Emergency stop | ERROR | reason, seq |
| Shutdown sent | INFO | reason, seq |

---

## 47. Future Expansion Strategy

### Adding a New Sensor

1. Add sensor driver on ESP32-S3.
2. Add new field(s) to the `telemetry` packet in an appropriate sub-object.
3. Add `"new_sensor_ok": <bool>` to the `health` object.
4. Document in Section 13. Add units to Section 25.
5. Update fault code registry if new fault conditions exist.
6. Update `SHARED/protocol_spec.md`.
7. **No framing changes. No version increment if fields are initially optional.**

### Adding a New Actuator

1. Implement subsystem on ESP32-S3.
2. Add new optional block to the `cmd` packet.
3. Document in Section 14.
4. Add new enum values to relevant registries.
5. Old firmware ignores unknown blocks — forward compatible.

### Adding a New Packet Type

1. Choose a unique `type` string.
2. Define all required and optional fields.
3. Document in a new section. Add to Section 3 Packet Type Registry.
4. Implement handlers on both processors.
5. Old implementations silently ignore unknown types — forward compatible.

### Protocol Version Increment Triggers

Increment `proto` when:
- An existing required field is **renamed**
- An existing field's **type changes**
- An existing field's **unit changes**
- A previously optional field becomes **mandatory**
- **Framing rules change**

Do NOT increment `proto` for:
- Adding new optional fields
- Adding new packet types
- Adding new enum values
- Adding new error codes

---

## 48. Security Considerations

### Threat Model

| Threat | Likelihood | Mitigation |
|--------|-----------|-----------|
| Cable interception | Negligible | None required (physical proximity) |
| Malicious process on Pi | Low | OS serial port permissions |
| Malformed injection via serial monitor | Low | All values clamped on ESP32 |
| Replay attacks | Very low | Sequence numbers detect replays |
| Dashboard WiFi interception | Medium | TLS planned for V1.x |

### Security Rules

| Rule | ID | Detail |
|------|----|--------|
| OS serial permissions | SEC-01 | `/dev/ttyACM0` owned by dedicated rover user |
| No credentials in protocol | SEC-02 | No tokens, passwords, or keys over serial |
| Value clamping as safety floor | SEC-03 | ESP32 clamps all actuator values regardless of Pi commands |
| Watchdog as safety layer | SEC-04 | ESP32 watchdog cannot be bypassed by protocol |
| Dashboard token auth | SEC-05 | WebSocket tokens required in production (V1.x) |

---

## 49. Compatibility Rules

### Backward Compatibility

| Rule | ID | Detail |
|------|----|--------|
| Ignore unknown fields | BC-01 | V1 receivers silently ignore fields they do not recognise |
| Accept V1-compliant packets | BC-02 | Future versions must accept all V1 packets |
| Optional fields may be absent | BC-03 | Receivers must work correctly if optional fields are missing |
| Proto field governs | BC-04 | Matching proto version requires best-effort processing |

### Forward Compatibility

| Rule | ID | Detail |
|------|----|--------|
| New fields are additive | FC-01 | Protocol evolution adds; never modifies existing fields |
| New packet types are transparent | FC-02 | Unknown type string -> silent discard, no error |
| New enum values are handled | FC-03 | Unknown enum value -> reject block, log WARNING |

### Hardware Revision Compatibility

| hw_rev | Meaning |
|--------|---------|
| `"rev_a"` | V1 baseline; INA219 not installed |
| `"rev_b"` | (Future) INA219 installed |
| `"rev_c"` | (Future) Encoder motors |

The Pi uses `hw_rev` to enable or disable feature sets without code changes.

---

## 50. Complete Reference Tables

### Table 1: All Packet Types

| Type | Direction | Rate | ACK? |
|------|-----------|------|------|
| `telemetry` | ESP32 -> Pi | 20 Hz | Never |
| `cmd` | Pi -> ESP32 | Event | Optional |
| `ack` | ESP32 -> Pi | On request | N/A |
| `heartbeat` | Both | 1 Hz | Never |
| `ready` | ESP32 -> Pi | Once | No |
| `fault` | ESP32 -> Pi | Event | Never |
| `shutdown` | Pi -> ESP32 | Once | Recommended |
| `error` | Both | Event | Never |

### Table 2: Mandatory Top-Level Fields

| Field | Type | Constraint |
|-------|------|-----------|
| `proto` | int | Must equal 1 |
| `type` | string | Must be registered |
| `ts` | int | Non-negative; ms since boot |
| `seq` | int | Non-negative; monotonic |

### Table 3: Telemetry Fields Summary

| Field | Type | Unit | Fault |
|-------|------|------|-------|
| `ultrasonic.{front,left,right,rear}` | int | cm | -1 |
| `tof.{front,pan}` | int | mm | -1 |
| `imu.{ax,ay,az}` | float | m/s² | 0.0 |
| `imu.{gx,gy,gz}` | float | deg/s | 0.0 |
| `imu.temp` | float | °C | 0.0 |
| `gas.raw` | int | ADC | 0 |
| `gas.hazard` | bool | — | false |
| `power.voltage` | float | V | -1.0 |
| `power.current` | float | A | -1.0 |
| `health.*_ok` | bool | — | false |

### Table 4: Command Fields Summary

| Field | Type | Unit | Range |
|-------|------|------|-------|
| `motors.{fl,fr,rl,rr}` | int | % | -100–+100 |
| `servos.pan` | int | deg | 0–180 |
| `servos.tilt` | int | deg | 0–180 |
| `eyes.expr` | string | — | See registry |
| `leds.mode` | string | — | See registry |
| `leds.color` | [int,int,int] | 0-255 | 0–255 each |
| `leds.speed` | int | — | 1–10 |

### Table 5: All Timeouts

| Timeout | Value | Action |
|---------|-------|--------|
| READY wait | 10000 ms | Retry or abort |
| ACK wait | 50 ms | Retry (max 3) |
| Heartbeat stale | 2000 ms | STALE state |
| Link lost | 5000 ms | Stop actuators |
| I2C read | 10 ms | Fault value |
| HC-SR04 ECHO | 30 ms | -1 distance |
| Telemetry age | 200 ms | Stale warning |

### Table 6: Error Code Registry

| Code | Name | Category |
|------|------|---------|
| 1001 | FRAME_TOO_LONG | Protocol |
| 1002 | JSON_PARSE_FAIL | Protocol |
| 1003 | MISSING_PROTO | Protocol |
| 1004 | PROTO_MISMATCH | Protocol |
| 1005 | MISSING_TYPE | Protocol |
| 1006 | MISSING_TS | Protocol |
| 1007 | MISSING_SEQ | Protocol |
| 1008 | MISSING_REQUIRED_FIELD | Protocol |
| 1009 | UNKNOWN_ENUM_VALUE | Protocol |
| 1010 | EMPTY_CMD_PACKET | Protocol |
| 1011 | DUPLICATE_SEQ | Protocol |
| 1012 | NULL_FIELD_VALUE | Protocol |
| 2001 | SENSOR_TOF_FRONT_FAIL | Sensor |
| 2002 | SENSOR_TOF_PAN_FAIL | Sensor |
| 2003 | SENSOR_IMU_FAIL | Sensor |
| 2004 | SENSOR_GAS_OUT_OF_RANGE | Sensor |
| 2005 | SENSOR_POWER_FAIL | Sensor |
| 2006 | SENSOR_I2C_BUS_FAIL | Sensor |
| 2007 | SENSOR_HCSR04_TIMEOUT | Sensor |
| 3001 | MOTOR_OVERCURRENT | Actuator |
| 3002 | SERVO_ANGLE_CLAMPED | Actuator |
| 3003 | OLED_WRITE_FAIL | Actuator |
| 3004 | LED_WRITE_FAIL | Actuator |
| 4001 | LINK_IDLE_TIMEOUT | Communication |
| 4002 | HEARTBEAT_MISSED | Communication |
| 4003 | TX_BUFFER_OVERFLOW | Communication |
| 4004 | RX_BUFFER_OVERFLOW | Communication |
| 5001 | WATCHDOG_TASK_TIMEOUT | System |
| 5002 | BOOT_SENSOR_FAILURE | System |
| 5003 | MEMORY_ALLOCATION_FAIL | System |
| 5004 | CONFIG_INVALID | System |

### Table 7: Expression Registry

| ID | Trigger | Animation |
|----|---------|-----------|
| `idle` | Default | Slow blink |
| `happy` | Person detected | Bright blink |
| `curious` | Tracking | Asymmetric blink |
| `alert` | Close obstacle | Static, no blink |
| `sleepy` | Long idle | Very slow blink |
| `excited` | High-confidence target | Fast blink |
| `confused` | Low-confidence | Asymmetric |
| `hazard` | Gas threshold | 3 Hz rapid blink |
| `error` | System fault | Static X |
| `sleep` | Deep idle | Static closed |
| `startup` | Boot | Progressive open |
| `shutdown` | Shutdown | Progressive close |
| `tracking_left` | Target left | Hold shifted |
| `tracking_right` | Target right | Hold shifted |
| `looking_up` | Target elevated | Hold shifted |

### Table 8: LED Mode Registry

| Mode | Colour Required | Semantic |
|------|----------------|---------|
| `off` | No | All LEDs off |
| `solid` | Yes | Constant colour |
| `pulse` | Yes | Sine brightness |
| `blink` | Yes | Toggle |
| `chase` | Yes | Moving LED |
| `strobe` | Yes | Rapid flash |
| `sweep` | Yes | Progressive fill |
| `rainbow` | No | Hue rotation |
| `breathe` | Yes | Slow fade |
| `patrol` | No | Cyan steady |
| `tracking` | No | Yellow chase |
| `alert` | No | Orange blink |
| `hazard` | No | Red strobe |
| `low_battery` | No | Red slow pulse |
| `error_mode` | No | Magenta alternate |
| `startup` | No | White sweep |

### Table 9: Serial Configuration Reference

| Parameter | Value |
|-----------|-------|
| Baud rate | 921600 (preferred), 115200 (min) |
| Data bits | 8 |
| Parity | None |
| Stop bits | 1 |
| Flow control | None |
| Line ending | LF (0x0A) |
| Encoding | UTF-8 |
| Frame delimiter | `\n` |
| Max frame size | 512 bytes |

### Table 10: Link State Summary

| State | Actuators | Commands | Telemetry |
|-------|-----------|---------|-----------|
| OFFLINE | N/A | Blocked | None |
| CONNECTING | STOP | Blocked | None |
| OPERATIONAL | Normal | Allowed | 20 Hz |
| STALE | Normal | Allowed | Degraded |
| LINK_LOST | STOP | Blocked | None |
| SHUTTING_DOWN | Stopping | Final only | Continues |

---

*End of Document*

---

> **Document Control**
>
> | Version | Date | Author | Notes |
> |---------|------|--------|-------|
> | 1.0 | 2026-06-28 | Lead Embedded Systems Architect | Initial foundation specification |
