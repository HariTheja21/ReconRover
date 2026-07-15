from typing import List, Dict, Any

class GoalSelector:
    def __init__(self):
        pass
        
    def select_best(self, ranked_clusters: List[Dict[str, Any]]) -> tuple[float, float, float]:
        # Returns (target_x, target_y, score)
        if not ranked_clusters:
            return 0.0, 0.0, 0.0
        best = ranked_clusters[0]
        return best["centroid"][0], best["centroid"][1], best["score"]
