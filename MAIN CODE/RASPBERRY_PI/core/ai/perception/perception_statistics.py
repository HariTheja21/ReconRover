from dataclasses import dataclass

@dataclass
class PerceptionStatistics:
    scenes_analyzed: int = 0
    entities_tracked: int = 0
    events_published: int = 0
    avg_processing_latency_ms: float = 0.0
