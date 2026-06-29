"""
config.py
Recon Rover V1 - Cognitive Layer

Loads, validates, and exposes all configuration values.
"""

import os

class Config:
    """
    Centralized configuration management for the Raspberry Pi layer.
    """
    # Serial Configuration
    SERIAL_PORT = os.getenv("ROVER_SERIAL_PORT", "/dev/ttyACM0")
    SERIAL_BAUDRATE = int(os.getenv("ROVER_SERIAL_BAUD", "115200"))
    SERIAL_TIMEOUT = 0.1
    PROTOCOL_VERSION_MAJOR = 1

    # System configuration
    TELEMETRY_HZ = 20
    HEALTH_HZ = 1
    DIAGNOSTICS_HZ = 1

    # Logging
    LOG_LEVEL = os.getenv("ROVER_LOG_LEVEL", "INFO")
    LOG_DIR = os.getenv("ROVER_LOG_DIR", "logs/")

    @classmethod
    def load(cls):
        """
        Future expansion to load from JSON/YAML.
        For now, relies on defaults and ENV vars.
        """
        if not os.path.exists(cls.LOG_DIR):
            os.makedirs(cls.LOG_DIR, exist_ok=True)
