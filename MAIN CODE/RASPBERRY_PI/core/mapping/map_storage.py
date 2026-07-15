"""
Map Storage Module
Recon Rover V2 - Phase 3.4
"""
import threading
import json
import os

class MapStorage:
    """Handles serialization of the grid for cold storage."""
    def __init__(self, filepath="map_storage.json"):
        self._lock = threading.RLock()
        self.filepath = filepath
        
    def save(self, grid_dict: dict):
        with self._lock:
            # Convert tuple keys to strings for JSON
            serializable = {f"{k[0]},{k[1]}": v for k, v in grid_dict.items()}
            with open(self.filepath, 'w') as f:
                json.dump(serializable, f)
                
    def load(self) -> dict:
        with self._lock:
            if not os.path.exists(self.filepath):
                return {}
            with open(self.filepath, 'r') as f:
                data = json.load(f)
            return {tuple(map(int, k.split(','))): v for k, v in data.items()}
