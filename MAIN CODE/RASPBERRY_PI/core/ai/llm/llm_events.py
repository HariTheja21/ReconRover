from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ReasoningStarted:
    session_id: str
    timestamp: float

@dataclass
class ReasoningCompleted:
    session_id: str
    result: str
    timestamp: float

@dataclass
class AgentInstructionGenerated:
    agent_id: str
    instruction: dict
    timestamp: float

@dataclass
class ToolExecutionRequested:
    tool_name: str
    args: dict
    timestamp: float

@dataclass
class ConversationUpdated:
    session_id: str
    messages_count: int
    timestamp: float
