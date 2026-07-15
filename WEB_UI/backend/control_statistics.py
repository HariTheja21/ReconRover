from dataclasses import dataclass

@dataclass
class ControlStatistics:
    total_commands_received: int = 0
    commands_routed: int = 0
    commands_rejected: int = 0
    commands_rate_limited: int = 0
    emergency_stops_triggered: int = 0
