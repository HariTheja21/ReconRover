"""
serial_connection.py
Recon Rover V1 - Serial Communication Manager

Non-blocking wrapper for pyserial connection.
"""

import asyncio
import serial
from logger import Logger
import time

class SerialConnection:
    """
    Manages the raw pyserial resource. 
    Reads and writes are done in thread-pool executors to prevent asyncio blocking.
    """
    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.serial_port = None
        self.log = Logger.get("SerialConnection")
        self.loop = asyncio.get_running_loop()

    def connect(self) -> bool:
        try:
            self.serial_port = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=0.1,  # short timeout to prevent deadlocks
                write_timeout=0.1
            )
            self.serial_port.reset_input_buffer()
            return True
        except serial.SerialException as e:
            self.log.error(f"Failed to connect to {self.port}: {e}")
            self.serial_port = None
            return False

    def close(self):
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.close()
            except Exception:
                pass
        self.serial_port = None

    def is_open(self) -> bool:
        return self.serial_port is not None and self.serial_port.is_open

    async def read_chunk(self, size: int = 1024) -> bytes:
        """Reads up to `size` bytes from the port in a thread-pool."""
        if not self.is_open():
            return b""
        
        def _read():
            try:
                return self.serial_port.read(size)
            except Exception:
                return b""
                
        return await self.loop.run_in_executor(None, _read)

    async def write(self, data: bytes) -> bool:
        """Writes data to the port in a thread-pool."""
        if not self.is_open():
            return False
            
        def _write():
            try:
                self.serial_port.write(data)
                self.serial_port.flush()
                return True
            except Exception:
                return False
                
        return await self.loop.run_in_executor(None, _write)
