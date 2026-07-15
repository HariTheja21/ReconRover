from dataclasses import dataclass

@dataclass
class AgentStatistics:
    tasks_dispatched: int = 0
    tasks_completed: int = 0
    conflicts_detected: int = 0
    conflicts_resolved: int = 0
    messages_routed: int = 0
    context_updates: int = 0
