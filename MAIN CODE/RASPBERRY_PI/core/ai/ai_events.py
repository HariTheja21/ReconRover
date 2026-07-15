from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class ModelLoadEvent:
    model_id: str
    model_type: str
    status: str # LOADING, READY, FAILED, UNLOADED
    timestamp: float

@dataclass
class InferenceRequestEvent:
    request_id: str
    model_id: str
    priority: int
    timestamp: float

@dataclass
class InferenceResultEvent:
    request_id: str
    model_id: str
    status: str # SUCCESS, ERROR
    latency_ms: float
    timestamp: float

@dataclass
class ToolExecutionEvent:
    tool_name: str
    status: str # START, SUCCESS, FAILED
    latency_ms: float
    timestamp: float
