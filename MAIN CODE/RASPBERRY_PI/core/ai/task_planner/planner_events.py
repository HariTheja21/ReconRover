from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class TaskCreated:
    task_id: str
    mission_id: str
    task_type: str
    timestamp: float

@dataclass
class TaskStarted:
    task_id: str
    timestamp: float

@dataclass
class TaskCompleted:
    task_id: str
    result: str
    timestamp: float

@dataclass
class TaskFailed:
    task_id: str
    reason: str
    timestamp: float

@dataclass
class MissionUpdated:
    mission_id: str
    status: str
    completion_pct: float
    timestamp: float

@dataclass
class BehaviorTreeUpdated:
    tree_id: str
    node_id: str
    status: str
    timestamp: float
