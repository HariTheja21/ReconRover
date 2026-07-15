import numpy as np

class CoverageMap:
    def __init__(self):
        # Keeps track of cells that have been explored
        self.explored_cells = set()
        
    def update(self, occupancy_grid: np.ndarray, resolution: float, origin: tuple):
        # Stub: Mark cells as explored if they are known (free or occupied)
        # Assuming grid values: -1 = unknown, 0 = free, 100 = occupied
        pass
        
    def get_explored_area(self, resolution: float) -> float:
        # Returns area in square meters
        return len(self.explored_cells) * (resolution ** 2)
