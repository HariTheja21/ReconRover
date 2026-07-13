"""
dashboard_server.py
Recon Rover V1 - Cognitive Layer

WebSocket/HTTP server; streams telemetry to the dashboard.
"""

import asyncio
import json
from event_bus import EventBus
from logger import Logger
from dashboard.dashboard_state import DashboardState
from dashboard.dashboard_api import DashboardAPI
from system.system_statistics import SystemStatistics

class DashboardServer:
    """
    WebSocket/HTTP server; streams telemetry to the dashboard.
    """
    def __init__(self, event_bus: EventBus, stats: SystemStatistics):
        self.event_bus = event_bus
        self.stats = stats
        self.state = DashboardState()
        self.api = DashboardAPI(self.state)
        self.log = Logger.get("DashboardServer")
        self._running = False
        self._task = None

    async def initialize(self):
        self.log.info("DashboardServer initialized.")
        # Subscribe to EventBus to keep state updated
        self.event_bus.subscribe("SystemHealthy", self._on_health_update)
        self.event_bus.subscribe("SystemDegraded", self._on_health_update)
        self.event_bus.subscribe("SystemCritical", self._on_health_update)
        self.event_bus.subscribe("ModuleFailed", self._on_fault)
        self.event_bus.subscribe("SensorUpdated", self._on_sensor_update)

    def _on_health_update(self, event):
        self.state.system_health = event.__class__.__name__.replace("System", "")

    def _on_fault(self, event):
        if hasattr(event, "module_name"):
            self.state.add_fault(f"ModuleFailed: {event.module_name}")

    def _on_sensor_update(self, event):
        if hasattr(event, "sensor_id") and hasattr(event, "value"):
            self.state.update_sensor_status(event.sensor_id, event.value)

    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self._server_loop())
        self.log.info("DashboardServer started.")

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        self.log.info("DashboardServer stopped.")

    async def _server_loop(self):
        while self._running:
            try:
                # Mock updating generic stats
                snapshot = self.stats.get_snapshot()
                self.state.cpu_usage = 0.0 # would be updated by psutil or similar
                self.state.memory_usage = 0.0
                
                # A real server would broadcast self.api.get_full_state() to WS clients here.
                await asyncio.sleep(1.0)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"DashboardServer loop error: {e}")
                await asyncio.sleep(1.0)
