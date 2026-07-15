from dataclasses import dataclass

@dataclass
class AgentStatistics:
    active_agents: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    messages_routed: int = 0
    conflicts_resolved: int = 0
    avg_latency_ms: float = 0.0
