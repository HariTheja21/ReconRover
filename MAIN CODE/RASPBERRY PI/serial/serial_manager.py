"""
serial_manager.py
Recon Rover V1 - Serial Communication Manager

Core orchestrator module bridging the EventBus with raw hardware tasks.
"""

from lifecycle_manager import BaseModule
from event_bus import EventBus
from .serial_connection import SerialConnection
from .serial_statistics import SerialStatistics
from .serial_health import SerialHealth
from .serial_reader import SerialReader
from .serial_writer import SerialWriter
from .serial_monitor import SerialMonitor

class SerialManager(BaseModule):
    def __init__(self, event_bus: EventBus, loop):
        super().__init__()
        self.event_bus = event_bus
        self.loop = loop
        
        # Instantiate subcomponents
        self.connection = SerialConnection(port="/dev/ttyUSB0", baudrate=115200)
        self.stats = SerialStatistics()
        self.health_monitor = SerialHealth()
        
        self.reader = SerialReader(self.connection, self.event_bus, self.stats, self.health_monitor)
        self.writer = SerialWriter(self.connection, self.event_bus, self.stats)
        self.monitor = SerialMonitor(self.connection, self.event_bus, self.health_monitor)

    async def initialize(self):
        self.log.info("SerialManager initialized.")

    async def start(self):
        self.log.info("Starting SerialManager tasks...")
        self.reader.start()
        self.writer.start()
        self.monitor.start()
        self.log.info("SerialManager started.")

    async def stop(self):
        self.log.info("Stopping SerialManager tasks...")
        self.monitor.stop()
        self.writer.stop()
        self.reader.stop()
        self.connection.close()
        self.log.info("SerialManager stopped.")

    def health(self) -> str:
        return self.health_monitor.get_status_string()

    def get_statistics(self):
        return self.stats.get_snapshot()
