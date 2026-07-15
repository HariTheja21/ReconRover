class CoverageTracker:
    def __init__(self, coverage_map):
        self.coverage_map = coverage_map
        self.total_area = 0.0
        
    def calculate_coverage(self, resolution: float) -> tuple[float, float]:
        area = self.coverage_map.get_explored_area(resolution)
        self.total_area = area
        # Stub: hardcoded estimated max area for percentage
        percentage = min((area / 100.0) * 100, 100.0)
        return area, percentage
