#!/usr/bin/env python3
"""
calibration_launcher.py
Recon Rover V1 - Deployment Tools

Connects to the ESP32 and streams raw IMU/Motor values to help tune offsets.
"""

import serial
import json
import argparse
import time
import sys

def run_calibration(port: str, baudrate: int):
    print(f"Connecting to ESP32 on {port} at {baudrate} baud...")
    
    try:
        ser = serial.Serial(port, baudrate, timeout=1.0)
    except serial.SerialException as e:
        print(f"Error opening port: {e}")
        sys.exit(1)
        
    print("Connection established. Waiting for raw telemetry data...")
    print("Press Ctrl+C to exit.")
    
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    try:
                        data = json.loads(line)
                        if data.get("type") == "sensor":
                            sensor = data.get("sensor")
                            val = data.get("value")
                            print(f"[CALIBRATION] {sensor}: {val:0.2f}")
                    except json.JSONDecodeError:
                        print(f"Raw: {line}")
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nCalibration session ended.")
    finally:
        ser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch calibration stream for Recon Rover.")
    parser.add_argument("-p", "--port", default="/dev/ttyUSB0", help="Serial port")
    parser.add_argument("-b", "--baud", default=115200, type=int, help="Baud rate")
    args = parser.parse_args()
    
    run_calibration(args.port, args.baud)
