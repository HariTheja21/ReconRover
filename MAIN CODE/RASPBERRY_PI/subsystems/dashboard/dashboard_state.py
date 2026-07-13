"""
dashboard_state.py
Recon Rover V1 - Dashboard Subsystem

Maintains the live aggregated state of the system for the dashboard.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class DashboardState:
    system_health: str = "UNKNOWN"
    modules: Dict[str, str] = field(default_factory=dict)
    sensors: Dict[str, Any] = field(default_factory=dict)
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    queues: Dict[str, int] = field(default_factory=dict)
    communications: str = "DISCONNECTED"
    fault_history: List[str] = field(default_factory=list)

    def update_module_health(self, module_name: str, status: str):
        self.modules[module_name] = status

    def update_sensor_status(self, sensor_name: str, value: Any):
        self.sensors[sensor_name] = value

    def add_fault(self, fault: str):
        self.fault_history.append(fault)
        if len(self.fault_history) > 50:
            self.fault_history.pop(0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "system_health": self.system_health,
            "modules": self.modules,
            "sensors": self.sensors,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "queues": self.queues,
            "communications": self.communications,
            "fault_history": self.fault_history
        }
