from dataclasses import dataclass

@dataclass
class SemanticStatistics:
    total_landmarks: int = 0
    total_objects: int = 0
    rooms_classified: int = 0
    graph_nodes: int = 0
    graph_edges: int = 0
    database_size_kb: float = 0.0
