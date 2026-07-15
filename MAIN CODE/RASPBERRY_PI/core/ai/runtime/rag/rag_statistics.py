from dataclasses import dataclass

@dataclass
class RAGStatistics:
    total_queries: int = 0
    total_documents: int = 0
    total_chunks: int = 0
    avg_latency_ms: float = 0.0
