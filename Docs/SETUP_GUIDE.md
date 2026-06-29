# Recon Rover V1 — Environment Setup Guide

**Document Version:** 1.0  
**Status:** Frozen Specification  
**Last Updated:** 2026-06-28  

This guide provides instructions for configuring development environments for both the ESP32-S3 firmware and the Raspberry Pi software.

## 1. ESP32-S3 Firmware Environment (C++ / FreeRTOS)

The ESP32-S3 uses the official Espressif IoT Development Framework (ESP-IDF). We do not use the Arduino IDE to ensure full access to FreeRTOS internals and hardware features.

### Prerequisites
* Windows, macOS, or Linux Host PC
* **ESP-IDF v5.x** installed

### Installation Steps
1. Download and install the ESP-IDF tools from the [official Espressif documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/).
2. Set up the target: `idf.py set-target esp32s3`
3. Configure project options via `idf.py menuconfig`.
4. Build the firmware: `idf.py build`
5. Flash to the ESP32-S3 via USB: `idf.py -p (PORT) flash monitor`

## 2. Raspberry Pi Software Environment (Python)

The Raspberry Pi software stack is written in Python 3.

### Prerequisites
* Raspberry Pi OS (64-bit recommended)
* Python 3.10+
* Virtual Environment (`venv`)

### Installation Steps
1. SSH into the Raspberry Pi.
2. Clone the repository: `git clone https://github.com/HariTheja21/ReconRover.git`
3. Navigate to the Raspberry Pi runtime directory:
   ```bash
   cd ReconRover
   cd "MAIN CODE"
   cd "RASPBERRY PI"
   ```
4. Create a virtual environment:
   ```bash
   python -m venv rover_env
   source rover_env/bin/activate
   ```
5. Install dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   *(Typical dependencies include: `pyserial`, `opencv-python-headless`, `asyncio`, `websockets`)*
6. Ensure the user has dialout group permissions to access the USB serial port:
   ```bash
   sudo usermod -a -G dialout $USER
   ```
7. Run the main entry point: `python main.py`
