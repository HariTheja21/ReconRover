from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class AgentExecutionStarted:
    agent_id: str
    task_id: str
    timestamp: float

@dataclass
class AgentExecutionCompleted:
    agent_id: str
    task_id: str
    result: Dict[str, Any]
    latency_ms: float
    timestamp: float

@dataclass
class AgentConflictDetected:
    agent_id_1: str
    agent_id_2: str
    conflict_type: str
    timestamp: float

@dataclass
class ConsensusReached:
    topic: str
    participants: List[str]
    agreement: Dict[str, Any]
    timestamp: float

@dataclass
class BlackboardUpdated:
    key: str
    writer_id: str
    timestamp: float

@dataclass
class AgentStatisticsUpdated:
    active_agents: int
    tasks_completed: int
    avg_latency_ms: float
    timestamp: float

@dataclass
class AgentHealthUpdated:
    is_healthy: bool
    stalled_agents: int
    timestamp: float
