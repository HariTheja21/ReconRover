import time
import asyncio
from typing import Callable, Dict, Any

from .test_scenarios import TestScenarios

class TestRunner:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback
        self.scenarios = {
            "Command Round-Trip": TestScenarios.run_command_round_trip,
            "Emergency Stop": TestScenarios.run_emergency_stop,
            "Sensor Feedback": TestScenarios.run_sensor_feedback,
            "Telemetry Consistency": TestScenarios.run_telemetry_consistency,
            "Packet Loss Simulation": TestScenarios.run_packet_loss_simulation
        }

    async def execute_all_tests(self) -> Dict[str, dict]:
        results = {}
        for name, scenario_func in self.scenarios.items():
            try:
                res = await scenario_func()
                results[name] = res
            except Exception as e:
                results[name] = {"passed": False, "error": str(e), "latency_ms": 0}
        return results
