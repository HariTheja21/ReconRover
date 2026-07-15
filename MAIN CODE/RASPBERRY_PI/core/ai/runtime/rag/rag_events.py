from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class RetrievalCompleted:
    query: str
    num_results: int
    latency_ms: float
    timestamp: float

@dataclass
class ContextBuilt:
    session_id: str
    context_length: int
    timestamp: float

@dataclass
class KnowledgeRetrieved:
    topic: str
    results: List[Dict[str, Any]]
    timestamp: float

@dataclass
class MemoryRetrieved:
    memory_type: str
    results: List[Dict[str, Any]]
    timestamp: float

@dataclass
class RAGStatisticsUpdated:
    total_queries: int
    total_documents: int
    avg_latency_ms: float
    timestamp: float

@dataclass
class RAGHealthUpdated:
    is_healthy: bool
    error_message: str
    timestamp: float
