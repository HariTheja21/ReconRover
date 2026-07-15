"""
Serial Port Manager Module
Recon Rover V2 - Phase 2.4

Handles dynamic scanning, auto-connection, and disconnection for the ESP32 Serial port.
"""

import os
import sys
import asyncio
from typing import Optional

# We will mock the physical serial layer if pyserial is not installed
try:
    import serial
    import serial.tools.list_ports
    HAS_PYSERIAL = True
except ImportError:
    HAS_PYSERIAL = False

class SerialPortManager:
    """
    Manages physical COM/TTY port lifecycle.
    """
    
    def __init__(self, target_baudrate: int = 115200):
        self.baudrate = target_baudrate
        self.active_port_name: Optional[str] = None
        self._connection = None
        
    def find_esp32_port(self) -> Optional[str]:
        """
        Scans available ports to find a likely ESP32 candidate.
        In a real scenario, we might check VID:PID (e.g. CP2102 or CH340).
        """
        if not HAS_PYSERIAL:
            return "MOCK_PORT"
            
        ports = serial.tools.list_ports.comports()
        for p in ports:
            # Common USB-UART bridge chips
            if "CP210" in p.description or "CH340" in p.description or "USB" in p.description:
                return p.device
        
        # Fallback to first available if none match specifically
        if ports:
            return ports[0].device
            
        return None

    def connect(self, port_name: str = None) -> bool:
        """
        Attempts to open the serial port.
        """
        target_port = port_name or self.find_esp32_port()
        if not target_port:
            return False
            
        if not HAS_PYSERIAL or target_port == "MOCK_PORT":
            self.active_port_name = "MOCK_PORT"
            self._connection = "MOCK_CONNECTION"
            return True
            
        try:
            # Note: For full asyncio we would use serial_asyncio.open_serial_connection.
            # But this manager encapsulates the connection instance.
            self._connection = serial.Serial(target_port, self.baudrate, timeout=0)
            self.active_port_name = target_port
            return True
        except serial.SerialException:
            self.active_port_name = None
            self._connection = None
            return False

    def disconnect(self) -> None:
        """
        Closes the active serial port.
        """
        if self._connection and self._connection != "MOCK_CONNECTION":
            try:
                self._connection.close()
            except Exception:
                pass
                
        self._connection = None
        self.active_port_name = None

    def get_connection(self):
        """Returns the active serial connection object."""
        return self._connection
        
    @property
    def is_connected(self) -> bool:
        """Returns True if a port is actively open."""
        return self._connection is not None
