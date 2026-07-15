from typing import Dict, Any, List

class SceneGraph:
    def __init__(self):
        self.nodes: Dict[str, Any] = {}
        self.edges: List[Dict[str, Any]] = []
        
    def update(self, entities: List[Dict[str, Any]], relationships: List[Dict[str, Any]]):
        self.nodes.clear()
        self.edges.clear()
        
        for e in entities:
            tid = str(e.get("tracking_id"))
            self.nodes[tid] = e
            
        self.edges = relationships
        
    def get_snapshot(self) -> Dict[str, Any]:
        return {
            "entities": list(self.nodes.keys()),
            "relationships": self.edges
        }
