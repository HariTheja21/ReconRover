import numpy as np
from typing import List, Tuple

class FrontierDetector:
    def __init__(self):
        pass
        
    def detect(self, occupancy_grid: np.ndarray, threshold: int = 5) -> List[Tuple[int, int]]:
        # Stub: Identify edges between known free space and unknown space
        # Return list of (x, y) grid coordinates
        return [(10, 10), (10, 11), (20, 20)]
