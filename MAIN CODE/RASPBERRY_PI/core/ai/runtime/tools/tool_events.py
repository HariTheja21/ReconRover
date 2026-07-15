from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ToolExecutionStarted:
    tool_name: str
    execution_id: str
    timestamp: float

@dataclass
class ToolExecutionCompleted:
    tool_name: str
    execution_id: str
    latency_ms: float
    timestamp: float

@dataclass
class ToolExecutionFailed:
    tool_name: str
    execution_id: str
    error_message: str
    timestamp: float

@dataclass
class ToolResultGenerated:
    tool_name: str
    execution_id: str
    result: Dict[str, Any]
    timestamp: float

@dataclass
class ToolStatisticsUpdated:
    total_executions: int
    success_rate: float
    avg_latency_ms: float
    timestamp: float

@dataclass
class ToolHealthUpdated:
    is_healthy: bool
    active_errors: int
    timestamp: float
