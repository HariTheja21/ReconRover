"""
dashboard_api.py
Recon Rover V1 - Dashboard Subsystem

Provides the API interface for the dashboard to retrieve state.
"""

import json
from .dashboard_state import DashboardState

class DashboardAPI:
    def __init__(self, state: DashboardState):
        self.state = state

    def get_full_state(self) -> str:
        """Returns the full dashboard state as a JSON string."""
        return json.dumps(self.state.to_dict())

    def get_module_health(self) -> str:
        return json.dumps(self.state.modules)

    def get_sensor_status(self) -> str:
        return json.dumps(self.state.sensors)

    def get_system_stats(self) -> str:
        return json.dumps({
            "cpu_usage": self.state.cpu_usage,
            "memory_usage": self.state.memory_usage,
            "queues": self.state.queues
        })

    def get_fault_history(self) -> str:
        return json.dumps(self.state.fault_history)
