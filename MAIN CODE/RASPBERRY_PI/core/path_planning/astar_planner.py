"""
A* Path Planner Module
Recon Rover V2 - Phase 3.7
"""
import math
import heapq
import threading
from typing import List, Tuple
from .path_planner import BasePathPlanner

class AStarPlanner(BasePathPlanner):
    """Implementation of A* Pathfinding."""
    
    def __init__(self, resolution=10.0):
        self._lock = threading.RLock()
        self.resolution = resolution # cm per grid cell
        
    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        # Euclidean distance
        return math.hypot(a[0] - b[0], a[1] - b[1])
        
    def _get_neighbors(self, current: Tuple[int, int], occupied_set: set) -> List[Tuple[int, int]]:
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if (nx, ny) not in occupied_set:
                neighbors.append((nx, ny))
        return neighbors

    def plan(self, start: Tuple[float, float], goal: Tuple[float, float], map_grid: tuple) -> List[Tuple[float, float]]:
        with self._lock:
            occupied_cells, _ = map_grid
            
            # Grid conversion (assuming cells in map_grid are already grid coords if scaled, else we scale them)
            # For this Phase, assume the occupancy grid operates on the same resolution integers
            occupied_set = set(occupied_cells)
            
            start_grid = (int(start[0] // self.resolution), int(start[1] // self.resolution))
            goal_grid = (int(goal[0] // self.resolution), int(goal[1] // self.resolution))
            
            if start_grid == goal_grid:
                return [goal]
                
            open_set = []
            heapq.heappush(open_set, (0.0, start_grid))
            
            came_from = {}
            g_score = {start_grid: 0.0}
            
            # F_score = G_score + Heuristic
            f_score = {start_grid: self._heuristic(start_grid, goal_grid)}
            
            while open_set:
                _, current = heapq.heappop(open_set)
                
                if current == goal_grid:
                    # Reconstruct path
                    path = []
                    while current in came_from:
                        # Convert back to world coordinates
                        world_x = current[0] * self.resolution + (self.resolution / 2.0)
                        world_y = current[1] * self.resolution + (self.resolution / 2.0)
                        path.append((world_x, world_y))
                        current = came_from[current]
                        
                    # Add exact start and goal for perfection
                    path.append(start)
                    path.reverse()
                    path[-1] = goal
                    return path
                    
                for neighbor in self._get_neighbors(current, occupied_set):
                    tentative_g = g_score[current] + self._heuristic(current, neighbor)
                    
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f = tentative_g + self._heuristic(neighbor, goal_grid)
                        f_score[neighbor] = f
                        
                        # Add to open set if not present (Python heapq allows duplicates, we tolerate them for speed)
                        heapq.heappush(open_set, (f, neighbor))
                        
            # No path found
            return []
