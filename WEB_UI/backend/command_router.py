import time
from typing import Callable

from .control_events import OperatorCommandEvent, EmergencyStopEvent
from .input_validator import InputValidator
from .rate_limiter import RateLimiter
from .control_statistics import ControlStatistics

class CommandRouter:
    def __init__(self, publish_callback: Callable, stats: ControlStatistics):
        self.publish = publish_callback
        self.stats = stats
        self.validator = InputValidator()
        self.rate_limiter = RateLimiter(max_commands_per_second=20)
        self.active_controller_id = None

    def handle_incoming_command(self, client_id: str, command: str, payload: dict) -> bool:
        self.stats.total_commands_received += 1
        
        # 1. Validation
        if not self.validator.validate(command, payload):
            self.stats.commands_rejected += 1
            return False

        # 2. Emergency Stop Bypass (Always allow E-STOP from ANY client immediately)
        if command == "EMERGENCY_STOP":
            self.publish("EmergencyStopEvent", EmergencyStopEvent(source=client_id, reason="Operator E-Stop", timestamp=time.time()))
            self.stats.emergency_stops_triggered += 1
            return True

        # 3. Ownership Check (Only one client drives at a time)
        if self.active_controller_id is None:
            self.active_controller_id = client_id
        elif self.active_controller_id != client_id:
            self.stats.commands_rejected += 1
            return False

        # 4. Rate Limiting
        if not self.rate_limiter.allow_command(client_id):
            self.stats.commands_rate_limited += 1
            return False

        # 5. Route to EventBus
        event = OperatorCommandEvent(client_id, command, payload, time.time())
        self.publish("OperatorCommandEvent", event)
        self.stats.commands_routed += 1
        return True

    def handle_client_disconnect(self, client_id: str):
        # If the active driver disconnects, stop the rover immediately
        if self.active_controller_id == client_id:
            self.publish("EmergencyStopEvent", EmergencyStopEvent(source="System", reason="Driver Disconnected", timestamp=time.time()))
            self.stats.emergency_stops_triggered += 1
            self.active_controller_id = None
