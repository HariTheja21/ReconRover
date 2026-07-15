"""
Serial Port Abstraction
Recon Rover V2 - Phase 4.3
"""
import asyncio
import serial

class SerialPort:
    """Async wrapper around pyserial."""
    def __init__(self, port: str = "/dev/serial0", baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self._serial = None
        
    def connect(self) -> bool:
        try:
            self._serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=0, # Non-blocking read
                write_timeout=0
            )
            return True
        except serial.SerialException:
            self._serial = None
            return False
            
    def disconnect(self):
        if self._serial and self._serial.is_open:
            self._serial.close()
        self._serial = None
        
    def is_connected(self) -> bool:
        return self._serial is not None and self._serial.is_open
        
    def write(self, data: bytes) -> bool:
        if not self.is_connected():
            return False
        try:
            self._serial.write(data)
            return True
        except serial.SerialException:
            self.disconnect()
            return False
            
    def read_all(self) -> bytes:
        if not self.is_connected():
            return b''
        try:
            # Requires timeout=0 in init for non-blocking
            data = self._serial.read(self._serial.in_waiting or 1)
            return data if data else b''
        except serial.SerialException:
            self.disconnect()
            return b''
