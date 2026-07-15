# RECON ROVER V2
## OFFICIAL INSTALLATION, WIRING & OPERATION MANUAL

**Version:** 1.0.0
**Project Repository:** Recon Rover V2

### Revision History
| Date | Version | Description | Author |
|---|---|---|---|
| 2026-07-16 | 1.0 | Initial Release of Installation Manual | AI Engineering Team |

---

## 2. Executive Summary
Welcome to the Recon Rover V2 Official Installation, Wiring & Operation Manual. This document provides an exhaustive, step-by-step guide to building, configuring, testing, and deploying the Recon Rover V2. Assuming zero prior knowledge of the platform, this manual covers the physical assembly, precise GPIO mappings, electrical safety, software dependencies, firmware flashing, and AI model provisioning. By the end of this guide, you will have a fully functional, autonomous robotic system running the complete Phase 8.9 AI Architecture.

---

## 3. Table of Contents
1. Cover Page
2. Executive Summary
3. Table of Contents
4. Hardware Requirements
5. Software Requirements
6. Complete Bill of Materials
7. Complete Wiring Guide
8. Complete GPIO Mapping
9. Power System
10. Raspberry Pi Installation
11. ESP32 Setup
12. AI Installation
13. Repository Setup
14. Firmware Upload
15. Calibration
16. Testing Procedures
17. Operating Instructions
18. Maintenance
19. Troubleshooting
20. Appendix

---

## 4. Hardware Requirements
To build Recon Rover V2, you will need:
- A stable workbench with anti-static mat.
- Soldering iron, lead-free solder, and flux.
- Multimeter (for voltage testing before connecting logical boards).
- Wire strippers, crimping tool (for JST connectors), and heat shrink tubing.
- Micro-SD card reader (for Raspberry Pi OS flashing).
- High-quality USB-C cables.

---

## 5. Software Requirements
You will need a host computer (Windows, macOS, or Linux) with:
- **VS Code** with **PlatformIO** extension installed.
- **Raspberry Pi Imager**.
- SSH Client (e.g., PuTTY or native terminal).
- Git installed.

---

## 6. Complete Bill of Materials
| Component | Purpose | Specs | Qty |
|---|---|---|---|
| Raspberry Pi 5 | High-Level AI Brain | 8GB RAM minimum | 1 |
| ESP32 DevKit V1 | Low-Level Motor Control | 240MHz dual-core | 1 |
| L298N Motor Driver | DC Motor actuation | Dual H-Bridge, 2A | 1 |
| TT Gear Motors | Drive mechanism | 6V, 200 RPM | 4 |
| 18650 Batteries | Primary Power | 3.7V, 3000mAh | 3 |
| 3S BMS Board | Battery Protection | 11.1V, 20A limit | 1 |
| LM2596 Buck Converter | Stepping down voltage | 12V to 5V (3A) | 2 |
| HC-SR04 | Ultrasonic Collision Detection| 2cm-400cm range | 3 |
| MPU6050 | IMU (Orientation/Dead Recon)| 6-axis gyro/accel | 1 |
| Raspberry Pi Camera v3 | Computer Vision Input | 12MP, IMX708 | 1 |
| USB Microphone | Voice Command Input | Omni-directional | 1 |
| INA219 | Power Monitoring (I2C) | 0-26V, 3.2A | 1 |
| WS2812B NeoPixels | Visual Status Feedback | 5V Addressable LED | 1 (Strip) |

> **TIP:** Do not cheap out on the Buck Converters. The Raspberry Pi 5 will pull heavy transients during LLM inference. Ensure the converter is rated for a continuous 3A output.

---

## 7. Complete Wiring Guide
### Power Distribution
- **Batteries:** Wire 3x 18650 cells in series to the 3S BMS (B-, B1, B2, B+).
- **BMS Output (P+, P-):** Connects to the main power switch.
- **Main Power Switch:** Connects to a power distribution block (11.1V).
- **Buck Converter 1 (Pi):** Connect input to 11.1V block. Tune output to exactly 5.1V using a multimeter BEFORE plugging in the Pi. Connect output to Pi 5V/GND pins.
- **Buck Converter 2 (Sensors/Servos):** Connect input to 11.1V block. Tune output to 5.0V. Connect to servo logic and NeoPixels.
- **L298N Driver:** Connect 12V input directly to the 11.1V block. Connect GND to common ground.

### ESP32 Wiring
- **ESP32 VIN:** Connect to 5V output of Buck Converter 2.
- **ESP32 GND:** Connect to common ground.
- **UART to Pi:** ESP32 TX (GPIO 17) -> Pi RX (GPIO 15). ESP32 RX (GPIO 16) -> Pi TX (GPIO 14). *Note: Ensure grounds are tied.*

---

## 8. Complete GPIO Mapping
### ESP32 GPIO Table
| Pin | Function | Subsystem |
|---|---|---|
| GPIO 16 | UART2 RX | Comm to Pi |
| GPIO 17 | UART2 TX | Comm to Pi |
| GPIO 25 | PWM Channel 0 | Left Motor ENA |
| GPIO 26 | Digital Out | Left Motor IN1 |
| GPIO 27 | Digital Out | Left Motor IN2 |
| GPIO 14 | PWM Channel 1 | Right Motor ENB |
| GPIO 12 | Digital Out | Right Motor IN3 |
| GPIO 13 | Digital Out | Right Motor IN4 |
| GPIO 32 | Digital In/Out | HC-SR04 Front TRIG |
| GPIO 33 | Digital In | HC-SR04 Front ECHO |

### Raspberry Pi GPIO Table
| Pin (BCM) | Function | Subsystem |
|---|---|---|
| GPIO 14 | UART0 TX | Comm to ESP32 |
| GPIO 15 | UART0 RX | Comm to ESP32 |
| GPIO 2 (SDA)| I2C1 | MPU6050 & INA219 |
| GPIO 3 (SCL)| I2C1 | MPU6050 & INA219 |
| GPIO 18 | SPI/PWM | NeoPixel Control |

---

## 9. Power System
### Protections
- **Over-voltage:** Handled by the 3S BMS.
- **Over-current:** BMS limits draw to 20A. INA219 monitors continuous draw.
- **Warning:** NEVER wire the Pi directly to the battery pack. Doing so will instantly destroy the board.

---

## 10. Raspberry Pi Installation
1. Use Raspberry Pi Imager. Select "Raspberry Pi OS (64-bit)".
2. Press `CTRL+SHIFT+X` to access advanced options:
   - Enable SSH.
   - Set username (`pi`) and password.
   - Configure WiFi.
3. Flash the Micro-SD card.
4. Insert into the Pi and power on.
5. SSH into the Pi: `ssh pi@<pi-ip-address>`.
6. Run `sudo raspi-config`:
   - Enable I2C, SPI, and Serial Port (disable serial console).
   - Reboot.

---

## 11. ESP32 Setup
1. Open VS Code on your host computer.
2. Install the PlatformIO extension.
3. Clone the Recon Rover repository to your host.
4. Open the `MAIN CODE/ESP32/` directory in PlatformIO.
5. Plug the ESP32 into your host computer via USB.
6. Click the PlatformIO "Upload" button (Right arrow on the bottom bar).

---

## 12. AI Installation
Execute these commands on the Raspberry Pi:
```bash
# Update System
sudo apt update && sudo apt upgrade -y

# Install Core Dependencies
sudo apt install -y python3-pip python3-venv libopenblas-dev libjpeg-dev

# Create Virtual Environment
python3 -m venv ~/rover_env
source ~/rover_env/bin/activate

# Install PyTorch (CPU optimized for Pi)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install Vector Database and LLM bindings
pip install chromadb langchain sentence-transformers pydantic

# Install Ollama (LLM Engine)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3:8b-instruct-q4_0
```

---

## 13. Repository Setup
```bash
# Clone the Codebase
git clone https://github.com/HariTheja21/ReconRover.git ~/ReconRover
cd ~/ReconRover

# Setup Environment Variables
cp .env.example .env
nano .env
# Enter any required API keys (e.g., OPENAI_API_KEY if not using local models)
```

---

## 14. Firmware Upload
- Ensure the ESP32 is flashed (Step 11).
- Verify connection by running `ls /dev/serial0` on the Pi.

---

## 15. Calibration
### IMU (MPU6050)
Place the rover on a perfectly flat surface. Run `python MAIN CODE/RASPBERRY_PI/calibrate_imu.py`. Do not move the rover for 60 seconds.

### Camera
Run `python MAIN CODE/RASPBERRY_PI/calibrate_vision.py`. Place a printed ArUco marker 1 meter exactly in front of the lens to tune focal length constants.

---

## 16. Testing Procedures
Before running the full AI stack, test components individually:
```bash
source ~/rover_env/bin/activate
cd ~/ReconRover

# 1. Test Hardware Comms
python scripts/test_serial.py

# 2. Test Camera
python scripts/test_vision.py

# 3. Test LLM
python scripts/test_llm.py
```
> **IMPORTANT:** Do not proceed to full operation if any of these scripts throw an error.

---

## 17. Operating Instructions
1. **Power On:** Turn on the main 11.1V switch.
2. **Startup:** Wait 45 seconds for the Pi to boot.
3. **Launch Runtime:**
```bash
source ~/rover_env/bin/activate
cd ~/ReconRover
python MAIN CODE/RASPBERRY_PI/core/main.py
```
4. **Autonomous Mode:** Triggered via the Web Dashboard or by speaking "Rover, begin autonomous exploration."
5. **Emergency Stop:** Speak "Rover, STOP IMMEDIATE" or hit the physical hardware kill switch on the chassis.

---

## 18. Maintenance
- **Battery:** Do not let 18650 cells drop below 3.0V per cell (9.0V total pack). The Pi will auto-shutdown at 9.5V, but long-term storage below 11.1V degrades cells.
- **Sensors:** Wipe the VL53L0X Time-of-Flight sensors with a microfiber cloth weekly to prevent dust scattering.

---

## 19. Troubleshooting
- **Pi Brownouts:** If the Pi crashes during heavy LLM generation, your Buck Converter cannot supply 3A. Replace the Buck Converter.
- **No Serial Comm:** Check that Pi RX goes to ESP32 TX, and Pi TX goes to ESP32 RX. Check common ground.
- **Ollama Timeout:** Ensure the Ollama service is running (`systemctl status ollama`).
- **Vision Lag:** The RPi 5 may thermal throttle under load. Attach an active cooling heatsink.

---

## 20. Appendix
### Useful Commands
- Tail system logs: `tail -f /var/log/syslog`
- Monitor Pi thermals: `watch -n 1 vcgencmd measure_temp`
- Monitor RAM usage: `htop`

*(End of Manual)*
