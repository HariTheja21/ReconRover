#!/usr/bin/env python3
"""
firmware_uploader.py
Recon Rover V1 - Deployment Tools

Automates flashing the ESP32 firmware using ESP-IDF tools.
"""

import os
import subprocess
import argparse
import sys

def flash_firmware(port: str):
    print(f"Starting firmware upload to ESP32 on {port}...")
    
    # Change directory to the ESP32 project root
    esp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ESP32S3'))
    
    if not os.path.exists(os.path.join(esp_dir, 'CMakeLists.txt')):
        print("Error: Could not find ESP32S3 project directory.")
        sys.exit(1)
        
    try:
        # Run idf.py build and flash
        subprocess.run(["idf.py", "-p", port, "flash", "monitor"], cwd=esp_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Firmware upload failed with code {e.returncode}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: idf.py not found. Please ensure the ESP-IDF environment is activated.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload firmware to the Recon Rover ESP32.")
    parser.add_argument("-p", "--port", default="/dev/ttyUSB0", help="Serial port (e.g., COM3 or /dev/ttyUSB0)")
    args = parser.parse_args()
    
    flash_firmware(args.port)
