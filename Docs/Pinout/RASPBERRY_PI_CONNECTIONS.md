# Recon Rover V1 — Raspberry Pi 3B+ Connections

**Document Version:** 1.0  
**Status:** Frozen Specification  
**Last Updated:** 2026-06-28  

This document details the physical connections and peripheral assignments for the Raspberry Pi 3B+ on Recon Rover V1.

> **Note:** The Raspberry Pi acts as the high-level cognitive layer. It does **not** connect directly to any GPIO-level sensors, actuators, or I2C buses. All low-level hardware is managed by the ESP32-S3.

## USB Port Allocation

The Raspberry Pi 3B+ provides four USB 2.0 host ports.

| Port | Device | Purpose | Notes |
|------|--------|---------|-------|
| **USB 1** | USB Webcam | Primary vision sensor | Captures frames for OpenCV/AI inference |
| **USB 2** | USB Microphone | Audio input | Voice command processing |
| **USB 3** | ESP32-S3 N16R8 | Serial JSON Bridge | The exclusive command/telemetry link |
| **USB 4** | *Available* | Expansion | Reserved for future use (e.g., GPS, LTE) |

## Power Connections

| Interface | Source | Voltage | Purpose |
|-----------|--------|---------|---------|
| **Micro-USB / GPIO 5V** | 5V Buck Converter #1 | 5.0 V | Main board power |
| **Ground** | Common Ground | 0 V | Return path |

> **Warning:** Do not power the Raspberry Pi directly from the battery without the Buck Converter, and do not share the Pi's 5V rail with the ESP32-S3 or servos, as this can cause voltage sag and SD card corruption.

## Network Interfaces

| Interface | Connection | Purpose |
|-----------|------------|---------|
| **WiFi (WLAN0)** | Local Network / Hotspot | Dashboard telemetry, remote control, and SSH access |
| **Ethernet (ETH0)** | *Unused* | Bench debugging (optional) |

## GPIO Usage

**None.**
The 40-pin GPIO header on the Raspberry Pi is intentionally unused in the V1 architecture to enforce strict separation of concerns. All real-time hardware IO is delegated to the ESP32-S3.
