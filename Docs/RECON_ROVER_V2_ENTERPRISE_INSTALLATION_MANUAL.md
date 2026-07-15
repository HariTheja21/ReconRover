# RECON ROVER V2 - ENTERPRISE INSTALLATION & OPERATION MANUAL

**Version:** 1.0.0
**Architecture Version:** 8.9
**Document Version:** 1.0
**Project Repository:** Recon Rover V2

## Revision History
| Date | Version | Description | Author |
|---|---|---|---|
| 2026-07-16 | 1.0 | Initial Release of Enterprise Installation Manual | AI Engineering Team |

---

## 1. Executive Summary
This document is the definitive build and operation manual for the Recon Rover V2. Derived exclusively from the Phase 8.9 repository implementation, it details the precise physical construction, wiring, software provisioning, and AI dependency installation required to replicate the autonomous platform.

---

## 2. Table of Contents
1. Executive Summary
2. Hardware Requirements
3. Software Requirements
4. Complete Bill of Materials (BOM)
5. Wiring Guide
6. GPIO Tables
7. Power Architecture
8. Raspberry Pi Setup
9. ESP32 Setup
10. AI Dependency Installation
11. Repository Setup
12. Firmware Upload
13. Calibration
14. Testing
15. Operation
16. Troubleshooting
17. Maintenance
18. Safety
19. Appendix

---

## 3. Hardware Requirements
- Microcomputer: Raspberry Pi 5 (8GB)
- Microcontroller: ESP32 DevKit V1
- Motor Controller: L298N Dual H-Bridge
- Sensors: HC-SR04 (Ultrasonic), MPU6050 (IMU), Pi Camera Module 3
- Power: 3x 18650 Li-Ion (3S BMS), 2x LM2596 Buck Converters

## 4. Software Requirements
- OS: Raspberry Pi OS (64-bit, Bookworm)
- Python: 3.12+
- AI: Ollama, PyTorch, ONNX Runtime
- ESP32: PlatformIO Core

---

## 5. GPIO Tables

### Raspberry Pi 5
| Pin | Direction | Voltage | Connected Device | Purpose |
|---|---|---|---|---|
| GPIO 14 (TX) | OUT | 3.3V | ESP32 RX (16) | UART Comms |
| GPIO 15 (RX) | IN | 3.3V | ESP32 TX (17) | UART Comms |
| GPIO 2 (SDA) | I/O | 3.3V | MPU6050 | I2C Data |
| GPIO 3 (SCL) | OUT | 3.3V | MPU6050 | I2C Clock |

### ESP32 DevKit V1
| Pin | Direction | Voltage | Connected Device | Purpose |
|---|---|---|---|---|
| GPIO 16 (RX2) | IN | 3.3V | Pi TX | UART Comms |
| GPIO 17 (TX2) | OUT | 3.3V | Pi RX | UART Comms |
| GPIO 25 | OUT | 3.3V | L298N ENA | Left Motor PWM |
| GPIO 26 | OUT | 3.3V | L298N ENB | Right Motor PWM |
| GPIO 27 | OUT | 3.3V | L298N IN1 | Left Motor FWD |
| GPIO 14 | OUT | 3.3V | L298N IN2 | Left Motor REV |
| GPIO 12 | OUT | 3.3V | L298N IN3 | Right Motor FWD |
| GPIO 13 | OUT | 3.3V | L298N IN4 | Right Motor REV |
| GPIO 32 | OUT | 3.3V | HC-SR04 Trig | Ultrasonic Ping |
| GPIO 33 | IN | 3.3V | HC-SR04 Echo | Ultrasonic Recv |

*(Note: ESP32 requires a logic level converter or voltage divider on the Echo pin if powered by 5V).*

---

## 6. Wiring Guide & Power Architecture
1. **Battery Pack:** 3S (11.1V - 12.6V) connects to Dual LM2596 inputs.
2. **Buck 1 (5V):** Powers Raspberry Pi 5 (via USB-C or GPIO 5V) and HC-SR04 VCC.
3. **Buck 2 (5V):** Powers ESP32 (via VIN) and MPU6050 VCC.
4. **Direct (12V):** Powers L298N 12V input terminal (with onboard 5V jumper removed if >12V, but 3S is safe).
5. **Grounding:** ALL grounds (Pi, ESP32, L298N, Sensors, Bucks, Battery) MUST be tied together.

---

## 7. Raspberry Pi Setup
**Commands:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git i2c-tools
```
**Verification:** Run `i2cdetect -y 1`. Expected output shows `0x68` (MPU6050).

## 8. Repository Setup
```bash
git clone <repository_url> ReconRoverV2
cd ReconRoverV2
python3 -m venv rover_env
source rover_env/bin/activate
pip install -r requirements.txt
```

## 9. AI Dependency Installation
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull llama3:8b
```
*(Verification: `ollama run llama3:8b "test"` responds successfully).*

## 10. Firmware Upload (ESP32)
**Commands:**
```bash
cd "MAIN CODE/ESP32"
pio run --target upload
pio device monitor -b 115200
```
*(Verification: Terminal displays "Rover Firmware Booted. Awaiting Serial.").*

---

## 11. Calibration
1. **IMU Calibration:** Run `python TOOLS/calibration_launcher.py --module imu`. Keep the rover perfectly still.
2. **Motor Tuning:** Elevate the chassis. Run `python TOOLS/calibration_launcher.py --module motors`. Verify both treads spin forward at 50% PWM.

## 12. Testing
Execute the overarching demo verification test:
```bash
cd "MAIN CODE/RASPBERRY_PI"
python main.py --demo
```
*(Verification: EventBus outputs "SystemReady" followed by simulated mission steps).*

## 13. Operation
**Startup:** Power on 5V bucks. Wait for Pi to boot. Run `main.py`.
**Shutdown:** Send `SIGINT` (Ctrl+C). The `DemoRuntime` gracefully halts motors and closes UART.

## 14. Troubleshooting
- **No Serial Comms:** Verify RX/TX are crossed (Pi TX -> ESP32 RX). Ensure grounds are tied.
- **LLM Timeout:** Verify `ollama serve` is running. Check thermal throttling via `vcgencmd measure_temp`.
- **Vision Crashes:** Ensure camera ribbon cable is seated. Run `libcamera-hello` to test underlying driver.

## 15. Safety & Maintenance
- **Safety:** Do not place fingers near motor gears during `DemoRuntime` operation.
- **Maintenance:** Periodically check 3S battery cell balance. Do not discharge below 9.6V.

*(End of Installation Manual)*
