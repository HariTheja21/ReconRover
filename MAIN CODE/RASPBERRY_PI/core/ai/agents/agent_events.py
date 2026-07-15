from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AgentTaskCreated:
    task_id: str
    agent_id: str
    priority: int
    timestamp: float

@dataclass
class AgentTaskCompleted:
    task_id: str
    agent_id: str
    result: str
    timestamp: float

@dataclass
class AgentStateUpdated:
    agent_id: str
    state: str
    timestamp: float

@dataclass
class AgentConflictDetected:
    agent_a: str
    agent_b: str
    reason: str
    timestamp: float

@dataclass
class SharedContextUpdated:
    key: str
    value: str
    timestamp: float
