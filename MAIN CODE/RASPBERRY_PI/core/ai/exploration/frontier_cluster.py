from typing import List, Tuple, Dict, Any

class FrontierCluster:
    def __init__(self):
        pass
        
    def cluster(self, frontiers: List[Tuple[int, int]], distance_threshold: float = 2.0) -> List[Dict[str, Any]]:
        # Stub: group adjacent frontier points into clusters
        # Returns list of clusters, each with a centroid
        return [
            {"centroid": (10, 10.5), "size": 2, "points": [(10, 10), (10, 11)]},
            {"centroid": (20, 20), "size": 1, "points": [(20, 20)]}
        ]
